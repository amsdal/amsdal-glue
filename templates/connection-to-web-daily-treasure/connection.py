import logging
import re
import xml.etree.ElementTree as ElementTree
from datetime import datetime
from functools import lru_cache
from typing import Any
from typing import ClassVar

import httpx
import polars as pl

from amsdal_glue import AggregationQuery
from amsdal_glue import AnnotationQuery
from amsdal_glue import Conditions
from amsdal_glue import Data
from amsdal_glue import Field
from amsdal_glue import FieldReference
from amsdal_glue import FieldReferenceAliased
from amsdal_glue import GroupByQuery
from amsdal_glue import JoinQuery
from amsdal_glue import LimitQuery
from amsdal_glue import OrderByQuery
from amsdal_glue import PropertySchema
from amsdal_glue import QueryStatement
from amsdal_glue import Schema
from amsdal_glue import SchemaCommand
from amsdal_glue import TransactionCommand
from amsdal_glue import Version
from amsdal_glue.interfaces import ConnectionBase
from amsdal_glue.queries.polars_operator_constructor import polars_operator_constructor
from amsdal_glue_core.commands.lock_command_node import ExecutionLockCommand
from amsdal_glue_core.common.helpers.singleton import Singleton
from amsdal_glue_core.common.operations.mutations.data import DataMutation
from amsdal_glue_core.queries.final_query_statement import QueryStatementNode

logger = logging.getLogger(__name__)


class DailyTreasureWebCache(metaclass=Singleton):
    def __init__(self):
        self.cache: dict[str, pl.DataFrame] = {}


class DailyTreasureWebConnection(ConnectionBase):
    BASE_URL: ClassVar[str] = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/pages/xml'
    TABLES: ClassVar[list[str]] = [
        'daily_treasury_yield_curve',
        'daily_treasury_bill_rates',
        'daily_treasury_long_term_rate',
        'daily_treasury_real_yield_curve',
        'daily_treasury_real_long_term',
    ]
    TABLES_CONTEXT: ClassVar[pl.SQLContext] = pl.SQLContext(
        frames={
            'schemas': pl.DataFrame({'name': TABLES}),
        },
    )

    def __init__(self):
        self.cache_service: DailyTreasureWebCache = DailyTreasureWebCache()

    def query(self, query: QueryStatement) -> list[Data]:
        tables = query.get_related_tables()

        for table in tables:
            if table in self.cache_service.cache:
                continue

            self.cache_service.cache[table] = self._load_all(table)

        sql = self._build_sql(query)
        sql_context = pl.SQLContext(frames=self.cache_service.cache)
        return self.process_results(
            sql_context.execute(sql).collect().to_dicts(),  # type: ignore[attr-defined]
        )

    def query_schema(self, filters: Conditions | None = None) -> list[Schema]:
        _statement = 'SELECT name FROM schemas'

        if filters:
            _statement += f' WHERE {self._sql_build_conditions(filters)}'

        _schemas = self.TABLES_CONTEXT.execute(_statement).collect().to_dicts()  # type: ignore[attr-defined]

        return [
            self.extract_schema(name=_schema['name'], xml_content=self._request_xml(_schema['name'], 2024))
            for _schema in _schemas
        ]

    def run_mutations(self, mutations: list[DataMutation]) -> list[list[Data] | None]:
        msg = f"Mutations are not supported"
        raise NotImplementedError(msg)

    def acquire_lock(self, lock: ExecutionLockCommand) -> Any:
        logger.warning('This connection does not support locks')

    def release_lock(self, lock: ExecutionLockCommand) -> Any:
        logger.warning('This connection does not support locks')

    def commit_transaction(self, transaction: TransactionCommand | str | None) -> Any:
        logger.warning('This connection does not support transactions')

    def rollback_transaction(self, transaction: TransactionCommand | str | None) -> Any:
        logger.warning('This connection does not support transactions')

    def begin_transaction(self, transaction: TransactionCommand | str | None) -> Any:
        logger.warning('This connection does not support transactions')

    def revert_transaction(self, transaction: TransactionCommand | str | None) -> Any:
        logger.warning('This connection does not support transactions')

    def run_schema_command(self, command: SchemaCommand) -> list[Schema | None]:
        msg = f"Schema commands are not supported"
        raise NotImplementedError(msg)

    def connect(self, *args: Any, **kwargs: Any) -> None:
        self._client = httpx.Client(timeout=120)

    def disconnect(self) -> None:
        self._client.close()

    @property
    def is_connected(self) -> bool:
        return not self._client.is_closed

    def process_results(self, data: list[dict[str, Any]]) -> list[Data]:
        _first_item = data[0] if data else {}

        # check columns duplications

        for key in _first_item:
            if ':' in key:
                msg = f'Column name {key.split(":", 1)[1]} is duplicated'
                raise ValueError(msg)

        return [Data(data=_item) for _item in data] if data is not None else []

    def _sql_build_conditions(
        self,
        conditions: Conditions,
    ) -> str:
        _stmt = []

        for condition in conditions.children:
            if isinstance(condition, Conditions):
                _stmt.append(f'({self._sql_build_conditions(condition)})')
                continue

            _field = self._build_field_reference_stmt(condition.field)
            _stmt.append(
                polars_operator_constructor(
                    field=_field,
                    lookup=condition.lookup,
                    value=condition.value,
                )
            )

        return f' {conditions.connector.value} '.join(_stmt)

    def _build_field_reference_stmt(
        self,
        field: FieldReference | FieldReferenceAliased,
    ) -> str:
        _item_stmt = f'{field.table_name}.{self._build_field(field.field)}'

        if isinstance(field, FieldReferenceAliased):
            _item_stmt += f' AS {field.alias}'

        return _item_stmt

    def _build_field(self, field: Field) -> str:
        parts = []

        while field:
            parts.append(field.name)
            field = field.child  # type: ignore[assignment]

        return '__'.join(parts)

    def extract_schema(self, name: str, xml_content: str) -> Schema:
        root = ElementTree.fromstring(xml_content)
        namespaces = dict(re.findall(r'xmlns:?(\w*?)=["\'](.*?)["\']', xml_content))
        first_entry = root.find('.//{http://www.w3.org/2005/Atom}entry', namespaces)

        if first_entry is None:
            msg = 'No schema found'
            raise ValueError(msg)

        _properties_section = first_entry.find('.//m:properties', namespaces)
        _properties: list[PropertySchema] = []

        for _property in _properties_section:
            tag_name = _property.tag.split('}')[-1]  # Remove namespace
            _type = _property.attrib.get('{' + namespaces["m"] + '}type')
            _properties.append(
                PropertySchema(
                    name=tag_name,
                    type=self._xml_to_python_type(_type),
                    required=False,
                ),
            )

        return Schema(
            name=name,
            version=Version.LATEST,
            properties=_properties,
        )

    @staticmethod
    def _xml_to_python_type(xml_type: str | None) -> Any:
        match xml_type:
            case 'Edm.DateTime':
                return datetime
            case 'Edm.Double':
                return float
            case 'Edm.Int32':
                return int
            case 'Edm.String':
                return str
            case _:
                return str

    @lru_cache(maxsize=None)
    def _request_xml(
        self,
        name: str,
        period_year: int | str,
        period_month: int | None = None,
        page: int = 0,
    ) -> str:
        period_param = 'field_tdr_date_value_month' if period_month else 'field_tdr_date_value'
        period_value = f'{period_year}{period_month:02d}' if period_month else str(period_year)
        params = {
            'data': name,
            period_param: period_value,
        }

        if page:
            params['page'] = page

        response = self._client.get(
            url=self.BASE_URL,
            params=params,
        )
        response.raise_for_status()

        return response.text

    def _load_all(self, table_name: str) -> pl.DataFrame:
        page = 0
        all_pages = []

        while data := self._load_data(self._request_xml(table_name, 'all', page=page)):
            all_pages.extend(data)
            page += 1

        return pl.DataFrame(all_pages)

    def _load_data(self, xml_content: str) -> list[dict[str, Any]] | None:
        root = ElementTree.fromstring(xml_content)
        namespaces = dict(re.findall(r'xmlns:?(\w*?)=["\'](.*?)["\']', xml_content))
        entries = root.findall('.//{' + namespaces[''] + '}entry', namespaces)

        if not entries:
            return None

        data: list[dict[str, Any]] = []

        for entry in entries:
            _properties = entry.find('.//m:properties', namespaces)
            _item = {}

            for _property in _properties:
                tag_name = _property.tag.split('}')[-1]  # Remove namespace
                _type = _property.attrib.get('{' + namespaces["m"] + '}type')
                _value_raw = _property.text
                _python_type = self._xml_to_python_type(_type)

                if _python_type is datetime:
                    _value = datetime.fromisoformat(_value_raw)
                else:
                    _value = _python_type(_value_raw)

                _item[tag_name] = _value
            data.append(_item)

        return data

    def _build_sql(self, query: QueryStatement) -> str:
        _sql = [
            'SELECT',
        ]
        _selection_stmt = self._sql_build_selection_stmt(
            query.only,
            query.annotations,
            query.aggregations,
        )

        _sql.append(_selection_stmt or '*')
        _sql.append(f'FROM {query.table.alias or query.table.name}')
        _sql.append(self._sql_build_joins(query.joins))
        _sql.append(self._sql_build_where(query.where))
        _sql.append(self._sql_build_group_by(query.group_by))
        _sql.append(self._sql_build_order_by(query.order_by))
        _sql.append(self._sql_build_limit(query.limit))

        return ' '.join(filter(None, _sql))

    def _sql_build_selection_stmt(
        self,
        only: list[FieldReference | FieldReferenceAliased] | None,
        annotations: list[AnnotationQuery] | None,
        aggregations: list[AggregationQuery] | None,
    ) -> str:
        _stmt = [self._build_field_reference_stmt(_item) for _item in only or []]

        for annotation in annotations or []:
            if isinstance(annotation.value, QueryStatementNode):
                msg = 'PolarsFinalQueryExecutor does not support subquery annotations'
                raise TypeError(msg)

            _val = repr(annotation.value.value)
            _stmt.append(f'{_val} AS {annotation.value.alias}')

        for aggregation in aggregations or []:
            _aggr_field = self._build_field_reference_stmt(aggregation.field)
            _stmt.append(f'{aggregation.expression.name}({_aggr_field}) AS {aggregation.alias}')

        return ', '.join(filter(None, _stmt))

    def _sql_build_joins(
        self,
        joins: list[JoinQuery] | None,
    ) -> str:
        if not joins:
            return ''

        _stmt = []

        for join in joins:
            _conditions = self._sql_build_conditions(join.on)
            _stmt.append(f'{join.join_type.value} JOIN {join.table.alias} ON {_conditions}')

        return ' '.join(_stmt)

    def _sql_build_conditions(
        self,
        conditions: Conditions,
    ) -> str:
        _stmt = []

        for condition in conditions.children:
            if isinstance(condition, Conditions):
                _stmt.append(f'({self._sql_build_conditions(condition)})')
                continue

            _field = self._build_field_reference_stmt(condition.field)
            _stmt.append(
                polars_operator_constructor(
                    field=_field,
                    lookup=condition.lookup,
                    value=condition.value,
                )
            )

        return f' {conditions.connector.value} '.join(_stmt)

    def _sql_build_where(
        self,
        where: Conditions | None,
    ) -> str:
        if not where:
            return ''

        return f'WHERE {self._sql_build_conditions(where)}'

    def _sql_build_group_by(
        self,
        group_by: list[GroupByQuery] | None,
    ) -> str:
        if not group_by:
            return ''

        _stmt = [self._build_field_reference_stmt(_item.field) for _item in group_by]

        return f'GROUP BY {", ".join(_stmt)}'

    def _sql_build_order_by(
        self,
        order_by: list[OrderByQuery] | None,
    ) -> str:
        if not order_by:
            return ''

        _stmt = []

        for field in order_by:
            _item_stmt = self._build_field_reference_stmt(field.field)
            _stmt.append(f'{_item_stmt} {field.direction.value}')

        return f'ORDER BY {", ".join(_stmt)}'

    def _sql_build_limit(
        self,
        limit: LimitQuery | None,
    ) -> str:
        if not limit:
            return ''

        _stmt = f'LIMIT {limit.limit}'

        if limit.offset:
            _stmt += f' OFFSET {limit.offset}'

        return _stmt
