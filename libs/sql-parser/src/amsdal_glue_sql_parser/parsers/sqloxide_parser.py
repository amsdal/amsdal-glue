from typing import Any

import sqloxide
from amsdal_glue_core.common.data_models.aggregation import AggregationQuery
from amsdal_glue_core.common.data_models.annotation import AnnotationQuery
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.field_reference import FieldReferenceAliased
from amsdal_glue_core.common.data_models.group_by import GroupByQuery
from amsdal_glue_core.common.data_models.join import JoinQuery
from amsdal_glue_core.common.data_models.limit import LimitQuery
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import FilterConnector
from amsdal_glue_core.common.enums import JoinType
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.aggregation import Avg
from amsdal_glue_core.common.expressions.aggregation import Count
from amsdal_glue_core.common.expressions.aggregation import Max
from amsdal_glue_core.common.expressions.aggregation import Min
from amsdal_glue_core.common.expressions.aggregation import Sum
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.base import Operation
from amsdal_glue_core.common.operations.queries import DataQueryOperation

from amsdal_glue_sql_parser.parsers.base import SqlParserBase


class SqlOxideParser(SqlParserBase):
    def parse_sql(self, sql: str, dialect: str | None = None) -> list[Operation]:
        dialect = dialect or 'ansi'
        parsed_sqls: list[dict[str, Any]] = sqloxide.parse_sql(sql, dialect=dialect)

        return [self._parsed_sql_to_operation(parsed_sql) for parsed_sql in parsed_sqls]

    def _parsed_sql_to_operation(self, parsed_sql: dict[str, Any]) -> Operation:
        if 'Query' in parsed_sql:
            return DataQueryOperation(query=self._parsed_sql_query_to_operation(parsed_sql['Query']))

        msg = 'Unsupported SQL operation'
        raise ValueError(msg)

    def _identifier_to_field(self, identifier: dict[str, Any], table_name: str) -> FieldReference | Value:
        if 'Identifier' in identifier:
            return FieldReference(
                field=Field(name=identifier['Identifier']['value']),
                table_name=table_name,
            )

        if 'CompoundIdentifier' in identifier:
            return FieldReference(
                field=Field(name=identifier['CompoundIdentifier'][1]['value']),
                table_name=identifier['CompoundIdentifier'][0]['value'],
            )

        if 'Value' in identifier:
            _value = identifier['Value']

            if 'SingleQuotedString' in _value:
                return Value(identifier['Value']['SingleQuotedString'])

            if 'Number' in _value:
                return Value(identifier['Value']['Number'][0])

            msg = 'Unsupported identifier'
            raise ValueError(msg)

        if 'Unnamed' in identifier:
            field_name = identifier['Unnamed']

            if field_name == 'Wildcard':
                field_name = '*'

            if isinstance(field_name, dict) and 'Expr' in field_name:
                field_name = field_name['Expr']['Identifier']['value']
            return FieldReference(
                field=Field(name=field_name),
                table_name=table_name,
            )

        msg = 'Unsupported identifier'
        raise ValueError(msg)

    def _process_projections(
        self,
        projections: list[dict[str, Any]],
        table_name: str,
    ) -> list[FieldReference | FieldReferenceAliased] | None:
        fields = []
        widlcard = True
        for projection in projections:
            if 'Wildcard' in projection:
                continue

            widlcard = False

            if 'UnnamedExpr' in projection:
                if 'Function' in projection['UnnamedExpr']:
                    continue
                fields.append(self._identifier_to_field(projection['UnnamedExpr'], table_name))

            elif 'QualifiedWildcard' in projection:
                fields.append(
                    FieldReference(
                        field=Field(name='*'),
                        table_name=projection['QualifiedWildcard'][0][0]['value'],
                    )
                )

            elif 'ExprWithAlias' in projection:
                continue

            else:
                msg = 'Unsupported projection'
                raise ValueError(msg)

        return (fields or None) if not widlcard else None

    def _process_selection(
        self,
        selection: dict[str, Any],
        table_name: str,
    ) -> Condition | Conditions | None:
        if not selection:
            return None

        if 'BinaryOp' in selection:
            value = selection['BinaryOp']
            if value['op'].lower() in ['and', 'or']:
                connector = FilterConnector.AND if value['op'].lower() == 'and' else FilterConnector.OR
                return Conditions(
                    self._process_selection(value['left'], table_name),
                    self._process_selection(value['right'], table_name),
                    connector=connector,
                )

            if value['op'].lower() in ['eq', 'neq', 'gt', 'gte', 'lt', 'lte', 'in']:
                return Condition(
                    field=self._identifier_to_field(value['left'], table_name),
                    lookup=FieldLookup(value['op'].upper()),
                    value=self._identifier_to_field(value['right'], table_name),
                )

        if 'Nested' in selection:
            return Conditions(self._process_selection(selection['Nested'], table_name))

        msg = 'Unsupported selection'
        raise ValueError(msg)

    def _process_joins(self, joins: list[dict[str, Any]], table_name: str) -> list[JoinQuery] | None:
        if not joins:
            return None

        join_queries = []
        for join in joins:
            join_table_description = join['relation']['Table']
            join_table_name = join_table_description['name'][0]['value']
            join_schema = SchemaReference(name=join_table_name, version=Version.LATEST)

            if join_table_description['alias']:
                join_schema.alias = join_table_description['alias']['name']['value']

            if 'Inner' in join['join_operator']:
                join_query = JoinQuery(
                    table=join_schema,
                    on=Conditions(self._process_selection(join['join_operator']['Inner']['On'], table_name)),
                    join_type=JoinType.INNER,
                )
            else:
                msg = 'Unsupported join type'
                raise ValueError(msg)
            join_queries.append(join_query)

        return join_queries

    def _process_group_by(self, group_by: list[dict[str, Any]], table_name: str) -> list[GroupByQuery] | None:
        if not group_by:
            return None

        group_by_queries = []
        for group in group_by:
            field = self._identifier_to_field(group, table_name)
            group_by_queries.append(GroupByQuery(field=field))

        return group_by_queries

    def _process_order_by(self, order_by: list[dict[str, Any]], table_name: str) -> list[OrderByQuery] | None:
        if not order_by:
            return None

        order_by_queries = []
        for order in order_by:
            field = self._identifier_to_field(order['expr'], table_name)
            direction = OrderDirection.ASC if order['asc'] else OrderDirection.DESC
            order_by_queries.append(OrderByQuery(field=field, direction=direction))

        return order_by_queries

    def _process_limit_offset(self, limit: dict[str, Any], offset: dict[str, Any]) -> LimitQuery | None:
        if not limit:
            return None

        return LimitQuery(
            limit=int(limit['Value']['Number'][0]),
            offset=int(offset['value']['Value']['Number'][0]) if offset else 0,
        )

    def _process_aggregations(
        self,
        projections: list[dict[str, Any]],
        table_name: str,
    ) -> list[AggregationQuery] | None:
        if not projections:
            return None

        aggregation_queries = []
        for projection in projections:
            alias = None
            if 'ExprWithAlias' in projection:
                aggregation = projection['ExprWithAlias']['expr']
                alias = projection['ExprWithAlias']['alias']['value']

            elif 'UnnamedExpr' in projection and 'Function' in projection['UnnamedExpr']:
                aggregation = projection['UnnamedExpr']
                alias = None
            else:
                continue

            if 'Function' in aggregation:
                function = aggregation['Function']
                if 'name' in function:
                    name = function['name'][0]['value']
                    aff_function = {
                        'COUNT': Count,
                        'SUM': Sum,
                        'AVG': Avg,
                        'MIN': Min,
                        'MAX': Max,
                    }.get(name)
                    if not aff_function:
                        msg = 'Unsupported aggregation function'
                        raise ValueError(msg)
                    expression = aff_function(
                        field=self._identifier_to_field(function['args']['List']['args'][0], table_name)
                    )
                    aggregation_queries.append(
                        AggregationQuery(
                            expression=expression,
                            alias=alias if alias else (f'{aff_function.name.lower()}({expression.field.field.name})'),
                        )
                    )
                else:
                    msg = 'Unsupported aggregation function'
                    raise ValueError(msg)
            elif 'Subquery' in aggregation:
                continue
            else:
                msg = 'Unsupported aggregation'
                raise ValueError(msg)

        if not aggregation_queries:
            return None

        return aggregation_queries

    def _process_annotations(
        self,
        projections: list[dict[str, Any]],
        table_name: str,  # noqa: ARG002
    ) -> list[AnnotationQuery] | None:
        if not projections:
            return None

        annotation_queries = []
        for projection in projections:
            if 'ExprWithAlias' in projection:
                annotation = projection['ExprWithAlias']
                alias = annotation['alias']['value']
                value = annotation['expr']
            else:
                continue

            if 'Subquery' in value:
                sub_query = value['Subquery']
                query = self._parsed_sql_query_to_operation(sub_query)
                annotation_queries.append(AnnotationQuery(value=SubQueryStatement(query=query, alias=alias)))
            else:
                continue

        if not annotation_queries:
            return None

        return annotation_queries

    def _parsed_sql_query_to_operation(self, parsed_sql: dict[str, Any]) -> QueryStatement:
        table_description = parsed_sql['body']['Select']['from'][0]['relation']['Table']
        table_name = table_description['name'][0]['value']
        schema = SchemaReference(name=table_name, version=Version.LATEST)

        if table_description['alias']:
            schema.alias = table_description['alias']['name']['value']
        query = QueryStatement(table=schema)

        query.only = self._process_projections(
            parsed_sql['body']['Select']['projection'],
            table_name,
        )
        where = self._process_selection(
            parsed_sql['body']['Select']['selection'],
            table_name,
        )
        if isinstance(where, Condition):
            where = Conditions(where)
        query.where = where

        query.joins = self._process_joins(
            parsed_sql['body']['Select']['from'][0]['joins'],
            table_name,
        )

        query.order_by = self._process_order_by(
            parsed_sql['order_by'],
            table_name,
        )

        query.limit = self._process_limit_offset(
            parsed_sql['limit'],
            parsed_sql['offset'],
        )

        query.group_by = self._process_group_by(
            parsed_sql['body']['Select']['group_by']['Expressions'],
            table_name,
        )

        query.aggregations = self._process_aggregations(
            parsed_sql['body']['Select']['projection'],
            table_name,
        )

        query.annotations = self._process_annotations(
            parsed_sql['body']['Select']['projection'],
            table_name,
        )

        return query
