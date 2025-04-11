from datetime import datetime
from typing import Any

import sqloxide
from amsdal_glue_core.common.data_models.aggregation import AggregationQuery
from amsdal_glue_core.common.data_models.annotation import AnnotationQuery
from amsdal_glue_core.common.data_models.annotation import ExpressionAnnotation
from amsdal_glue_core.common.data_models.annotation import ValueAnnotation
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.constraints import BaseConstraint
from amsdal_glue_core.common.data_models.constraints import CheckConstraint
from amsdal_glue_core.common.data_models.constraints import ForeignKeyConstraint
from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.field_reference import FieldReferenceAliased
from amsdal_glue_core.common.data_models.group_by import GroupByQuery
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.join import JoinQuery
from amsdal_glue_core.common.data_models.limit import LimitQuery
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import FilterConnector
from amsdal_glue_core.common.enums import JoinType
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import TransactionAction
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.aggregation import Avg
from amsdal_glue_core.common.expressions.aggregation import Count
from amsdal_glue_core.common.expressions.aggregation import Max
from amsdal_glue_core.common.expressions.aggregation import Min
from amsdal_glue_core.common.expressions.aggregation import Sum
from amsdal_glue_core.common.expressions.common import Combinable
from amsdal_glue_core.common.expressions.common import CombinedExpression
from amsdal_glue_core.common.expressions.expression import Expression
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.func import Func
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.base import Operation
from amsdal_glue_core.common.operations.commands import DataCommand
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.commands import TransactionCommand
from amsdal_glue_core.common.operations.mutations.data import DeleteData
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.data import UpdateData
from amsdal_glue_core.common.operations.mutations.schema import AddConstraint
from amsdal_glue_core.common.operations.mutations.schema import AddIndex
from amsdal_glue_core.common.operations.mutations.schema import AddProperty
from amsdal_glue_core.common.operations.mutations.schema import DeleteConstraint
from amsdal_glue_core.common.operations.mutations.schema import DeleteProperty
from amsdal_glue_core.common.operations.mutations.schema import DeleteSchema
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.operations.mutations.schema import RenameProperty
from amsdal_glue_core.common.operations.mutations.schema import RenameSchema
from amsdal_glue_core.common.operations.queries import DataQueryOperation
from amsdal_glue_core.common.operations.queries import SchemaQueryOperation

from amsdal_glue_sql_parser.parsers.base import SqlParserBase

SCHEMA_REGISTRY_TABLE = 'amsdal_schema_registry'
AGGREGATION_FUNCTIONS = {
    'COUNT': Count,
    'SUM': Sum,
    'AVG': Avg,
    'MIN': Min,
    'MAX': Max,
}
POWER_FUNCTIONS = ('power', 'pow')


def _number_cast(value: str) -> int | float:
    try:
        return int(value)
    except ValueError:
        return float(value)


VALUE_TYPE_MAPPING = {
    'Number': _number_cast,
    'Boolean': bool,
    'SingleQuotedString': str,
    'DoubleQuotedString': str,
}


class SqlOxideParser(SqlParserBase):
    def parse_sql(self, sql: str, dialect: str | None = None) -> list[Operation]:
        dialect = dialect or 'ansi'
        parsed_sqls: list[dict[str, Any]] = sqloxide.parse_sql(sql, dialect=dialect)

        return [self._parsed_sql_to_operation(parsed_sql) for parsed_sql in parsed_sqls]

    def _parsed_sql_to_operation(self, parsed_sql: dict[str, Any]) -> Operation:  # noqa: PLR0911, C901, PLR0912
        if 'Query' in parsed_sql:
            query = self._parsed_sql_query_to_operation(parsed_sql['Query'])

            if isinstance(query.table, SchemaReference) and query.table.name == SCHEMA_REGISTRY_TABLE:  # type: ignore[union-attr]
                return SchemaQueryOperation(filters=query.where)

            return DataQueryOperation(query=query)

        if 'Insert' in parsed_sql:
            return self._parse_insert_sql_operation(parsed_sql['Insert'])

        if 'Update' in parsed_sql:
            return self._parse_update_sql_operation(parsed_sql['Update'])

        if 'Delete' in parsed_sql:
            return self._parse_delete_sql_operation(parsed_sql['Delete'])

        if 'CreateTable' in parsed_sql:
            return self._create_table_sql_operation(parsed_sql['CreateTable'])

        if 'CreateIndex' in parsed_sql:
            return self._create_index(parsed_sql['CreateIndex'])

        if 'AlterTable' in parsed_sql:
            return self._alter_table(parsed_sql['AlterTable'])

        if 'Drop' in parsed_sql:
            return self._drop_operation(parsed_sql['Drop'])

        if 'StartTransaction' in parsed_sql:
            return TransactionCommand(
                transaction_id=None,
                schema=SchemaReference(name='', version=Version.LATEST),
                action=TransactionAction.BEGIN,
            )

        if 'Savepoint' in parsed_sql:
            return TransactionCommand(
                transaction_id=parsed_sql['Savepoint']['name']['value'],
                schema=SchemaReference(name='', version=Version.LATEST),
                action=TransactionAction.BEGIN,
            )

        if 'Rollback' in parsed_sql:
            transaction_id = None

            if parsed_sql['Rollback'].get('savepoint'):
                transaction_id = parsed_sql['Rollback']['savepoint']['value']

            return TransactionCommand(
                transaction_id=transaction_id,
                schema=SchemaReference(name='', version=Version.LATEST),
                action=TransactionAction.ROLLBACK,
            )

        if 'Commit' in parsed_sql:
            return TransactionCommand(
                transaction_id=None,
                schema=SchemaReference(name='', version=Version.LATEST),
                action=TransactionAction.COMMIT,
            )

        msg = 'Unsupported SQL operation'
        raise ValueError(msg)

    def _drop_operation(self, parsed_sql: dict[str, Any]) -> SchemaCommand:
        if parsed_sql['object_type'] == 'Table':
            return SchemaCommand(
                mutations=[
                    DeleteSchema(
                        schema_reference=SchemaReference(
                            name=parsed_sql['names'][0][0]['value'], version=Version.LATEST
                        )
                    )
                ]
            )

        msg = 'Unsupported drop operation'
        raise ValueError(msg)

    def _constraint_name(self, constraint: dict[str, Any]) -> str:
        if constraint.get('name'):
            return constraint['name']['value']
        return ''

    def _alter_table(self, parsed_sql: dict[str, Any]) -> SchemaCommand:
        table_name = parsed_sql['name'][0]['value']
        schema = SchemaReference(name=table_name, version=Version.LATEST)

        operations: list[SchemaCommand] = []
        for operation in parsed_sql['operations']:
            if 'AddColumn' in operation:
                column = operation['AddColumn']['column_def']
                column_name = column['name']['value']
                column_type = self._process_column_type(column['data_type'])
                _property = PropertySchema(
                    name=column_name, type=column_type, required=False, description=None, default=None
                )

                operations.append(SchemaCommand(mutations=[AddProperty(schema_reference=schema, property=_property)]))
            elif 'DropColumn' in operation:
                column_name = operation['DropColumn']['column_name']['value']
                operations.append(
                    SchemaCommand(mutations=[DeleteProperty(schema_reference=schema, property_name=column_name)])
                )
            elif 'RenameColumn' in operation:
                old_column_name = operation['RenameColumn']['old_column_name']['value']
                new_column_name = operation['RenameColumn']['new_column_name']['value']
                operations.append(
                    SchemaCommand(
                        mutations=[
                            RenameProperty(schema_reference=schema, old_name=old_column_name, new_name=new_column_name)
                        ]
                    )
                )
            elif 'RenameTable' in operation:
                new_table_name = operation['RenameTable']['table_name'][0]['value']
                operations.append(
                    SchemaCommand(mutations=[RenameSchema(schema_reference=schema, new_schema_name=new_table_name)])
                )

            elif 'AddConstraint' in operation:
                constraint = operation['AddConstraint']
                if 'PrimaryKey' in constraint:
                    fields = [column['value'] for column in constraint['PrimaryKey']['columns']]
                    operations.append(
                        SchemaCommand(
                            mutations=[
                                AddConstraint(
                                    schema_reference=schema,
                                    constraint=PrimaryKeyConstraint(
                                        name=self._constraint_name(constraint['PrimaryKey']), fields=fields
                                    ),
                                )
                            ]
                        )
                    )
                else:
                    msg = 'Unsupported alter table operation'
                    raise ValueError(msg)

            elif 'DropConstraint' in operation:
                constraint = operation['DropConstraint']
                operations.append(
                    SchemaCommand(
                        mutations=[
                            DeleteConstraint(schema_reference=schema, constraint_name=self._constraint_name(constraint))
                        ]
                    )
                )
            else:
                msg = 'Unsupported alter table operation'
                raise ValueError(msg)

        return operations[0]

    def _create_index(self, parsed_sql: dict[str, Any]) -> SchemaCommand:
        table_name = parsed_sql['table_name'][0]['value']
        schema = SchemaReference(name=table_name, version=Version.LATEST)

        fields = [column['expr']['Identifier']['value'] for column in parsed_sql['columns']]
        condition = None
        if parsed_sql['predicate']:
            condition = Conditions(self._process_selection(parsed_sql['predicate'], table_name))

        return SchemaCommand(
            mutations=[
                AddIndex(
                    schema_reference=schema,
                    index=IndexSchema(
                        name=parsed_sql['name'][0]['value'],
                        fields=fields,
                        condition=condition,
                    ),
                )
            ]
        )

    def _process_column_type(self, column_type: str | dict[str, Any]) -> type:
        if column_type == 'Text' or 'Varchar' in column_type:
            return str

        if 'Integer' in column_type or 'Int' in column_type:
            return int

        if 'Timestamp' in column_type:
            return datetime

        if 'JSON' in column_type or 'JSONB' in column_type:
            return dict

        if 'Boolean' in column_type:
            return bool

        if 'Real' in column_type or 'Float4' in column_type or 'Float8' in column_type:
            return float

        msg = 'Unsupported column type'
        raise ValueError(msg)

    def _create_table_sql_operation(self, parsed_sql: dict[str, Any]) -> SchemaCommand:
        table_name = parsed_sql['name'][0]['value']
        schema = Schema(name=table_name, version=Version.LATEST, properties=[])

        properties = []
        constraints = self._process_constraints_on_table(parsed_sql['constraints'], table_name)
        for column in parsed_sql['columns']:
            column_name = column['name']['value']
            column_type = self._process_column_type(column['data_type'])
            _property = PropertySchema(
                name=column_name, type=column_type, required=False, description=None, default=None
            )

            for option in column['options']:
                if 'Unique' in option['option']:
                    if option['option']['Unique']['is_primary']:
                        constraints.append(PrimaryKeyConstraint(name=column_name, fields=[column_name]))
                        _property.required = True
                    else:
                        constraints.append(UniqueConstraint(name=column_name, fields=[column_name]))

                elif option['option'] == 'NotNull':
                    _property.required = True

                else:
                    msg = 'Unsupported column option'
                    raise ValueError(msg)

            properties.append(_property)

        schema.properties = properties
        schema.constraints = constraints or None

        return SchemaCommand(mutations=[RegisterSchema(schema=schema)])

    def _process_constraints_on_table(self, constraints: list[dict[str, Any]], table_name: str) -> list[BaseConstraint]:
        if not constraints:
            return []

        constraints_list: list[BaseConstraint] = []
        for constraint in constraints:
            if 'PrimaryKey' in constraint:
                fields = [field['value'] for field in constraint['PrimaryKey']['columns']]

                constraints_list.append(
                    PrimaryKeyConstraint(name=self._constraint_name(constraint['PrimaryKey']), fields=fields)
                )

            elif 'Unique' in constraint:
                fields = [field['value'] for field in constraint['Unique']['columns']]

                constraints_list.append(
                    UniqueConstraint(name=self._constraint_name(constraint['Unique']), fields=fields)
                )

            elif 'Check' in constraint:
                condition = self._process_selection(constraint['Check']['expr'], table_name)

                constraints_list.append(
                    CheckConstraint(name=self._constraint_name(constraint['Check']), condition=Conditions(condition))
                )

            elif 'ForeignKey' in constraint:
                fields = [field['value'] for field in constraint['ForeignKey']['columns']]
                reference_schema = SchemaReference(
                    name=constraint['ForeignKey']['foreign_table'][0]['value'], version=Version.LATEST
                )
                reference_fields = [field['value'] for field in constraint['ForeignKey']['referred_columns']]

                constraints_list.append(
                    ForeignKeyConstraint(
                        name=self._constraint_name(constraint['ForeignKey']),
                        fields=fields,
                        reference_schema=reference_schema,
                        reference_fields=reference_fields,
                    )
                )

            else:
                msg = 'Unsupported constraint'
                raise ValueError(msg)

        return constraints_list

    def _parse_delete_sql_operation(self, parsed_sql: dict[str, Any]) -> DataCommand:
        table_name = parsed_sql['from']['WithFromKeyword'][0]['relation']['Table']['name'][0]['value']
        schema = SchemaReference(name=table_name, version=Version.LATEST)

        where = self._process_selection(parsed_sql['selection'], table_name)

        if isinstance(where, Condition):
            where = Conditions(where)

        return DataCommand(mutations=[DeleteData(schema=schema, query=where)])

    def _parse_update_sql_operation(self, parsed_sql: dict[str, Any]) -> DataCommand:
        table_name = parsed_sql['table']['relation']['Table']['name'][0]['value']
        schema = SchemaReference(name=table_name, version=Version.LATEST)

        assignments = {}
        for assignment in parsed_sql['assignments']:
            field = assignment['id'][0]['value']
            value = assignment['value']
            _value = self._identifier_to_field(value, table_name)
            assignments[field] = _value.value if isinstance(_value, Value) else _value.field.name

        where = self._process_selection(parsed_sql['selection'], table_name)

        if isinstance(where, Condition):
            where = Conditions(where)

        return DataCommand(
            mutations=[
                UpdateData(
                    schema=schema,
                    data=Data(data=assignments, metadata=None),
                    query=where,
                )
            ]
        )

    def _parse_insert_sql_operation(self, parsed_sql: dict[str, Any]) -> DataCommand:
        columns = [column['value'] for column in parsed_sql['columns']]
        table_name = parsed_sql['table_name'][0]['value']

        data_rows = []

        for row in parsed_sql['source']['body']['Values']['rows']:
            data_row = {}

            for column, value in zip(columns, row, strict=False):
                _value = self._identifier_to_field(value, table_name)
                data_row[column] = _value.value if isinstance(_value, Value) else _value.field.name

            data_rows.append(data_row)

        return DataCommand(
            mutations=[
                InsertData(
                    schema=SchemaReference(name=table_name, version=Version.LATEST),
                    data=[Data(data=row, metadata=None) for row in data_rows],
                )
            ]
        )

    def _identifier_to_field(self, identifier: dict[str, Any], table_name: str) -> FieldReference | Value:  # noqa: C901, PLR0911
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

            if 'Boolean' in _value:
                return Value(identifier['Value']['Boolean'])

            msg = f'Unsupported identifier: {identifier}'
            raise ValueError(msg)

        if 'Unnamed' in identifier:
            field_name = identifier['Unnamed']

            if field_name == 'Wildcard':
                field_name = '*'

            if isinstance(field_name, dict) and 'Expr' in field_name:
                _expression = field_name['Expr']

                if 'Identifier' in _expression:
                    field_name = _expression['Identifier']['value']
                elif 'CompoundIdentifier' in _expression:
                    return FieldReference(
                        field=Field(name=_expression['CompoundIdentifier'][1]['value']),
                        table_name=_expression['CompoundIdentifier'][0]['value'],
                    )
                else:
                    msg = f'Unsupported expression: {_expression}'
                    raise ValueError(msg)

            return FieldReference(
                field=Field(name=field_name),
                table_name=table_name,
            )

        msg = f'Unsupported identifier: {identifier}'
        raise ValueError(msg)

    def _identifier_to_field_reference(self, identifier: dict[str, Any], table_name: str) -> FieldReference:
        field_reference = self._identifier_to_field(identifier, table_name)

        if not isinstance(field_reference, FieldReference):
            msg = 'Unsupported identifier'
            raise TypeError(msg)

        return field_reference

    def _process_only(
        self,
        projections: list[dict[str, Any]],
        table_name: str,
    ) -> list[FieldReference | FieldReferenceAliased] | None:
        if not projections:
            return None

        fields = []

        for projection in projections:
            if 'Wildcard' in projection:
                continue

            if 'UnnamedExpr' in projection:
                if 'Function' in projection['UnnamedExpr']:
                    continue

                fields.append(self._identifier_to_field_reference(projection['UnnamedExpr'], table_name))
            elif 'QualifiedWildcard' in projection:
                fields.append(
                    FieldReference(
                        field=Field(name='*'),
                        table_name=projection['QualifiedWildcard'][0][0]['value'],
                    )
                )
            elif 'ExprWithAlias' in projection:
                _expression = projection['ExprWithAlias']
                _alias = _expression['alias']['value']
                _expression = _expression['expr']

                if 'CompoundIdentifier' in _expression:
                    _identifier = _expression['CompoundIdentifier']

                    fields.append(
                        FieldReferenceAliased(
                            field=Field(name=_identifier[1]['value']),
                            table_name=_identifier[0]['value'],
                            alias=_alias,
                        )
                    )

                continue
            else:
                msg = f'Unsupported projection: {projection}'
                raise ValueError(msg)

        return fields if fields else None

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
                _field = self._identifier_to_field(value['right'], table_name)

                _right = (
                    FieldReferenceExpression(field_reference=_field) if isinstance(_field, FieldReference) else _field
                )

                return Condition(
                    left=FieldReferenceExpression(
                        field_reference=self._identifier_to_field_reference(value['left'], table_name)
                    ),
                    lookup=FieldLookup(value['op'].upper()),
                    right=_right,
                )

        if 'Nested' in selection:
            return Conditions(self._process_selection(self._unwrap_nested_expression(selection), table_name))

        msg = 'Unsupported selection'
        raise ValueError(msg)

    def _process_joins(self, joins: list[dict[str, Any]], table_name: str) -> list[JoinQuery] | None:
        if not joins:
            return None

        join_queries = []
        for join in joins:
            _relation = join['relation']
            join_schema: SchemaReference | SubQueryStatement
            if 'Derived' in _relation:
                join_table_description = _relation['Derived']
                join_table_name = join_table_description['alias']['name']['value']
                join_schema = SubQueryStatement(
                    query=self._parsed_sql_query_to_operation(join_table_description['subquery']),
                    alias=join_table_name,
                )
            elif 'Table' in _relation:
                join_table_description = _relation['Table']
                join_table_name = join_table_description['name'][0]['value']
                join_schema = SchemaReference(name=join_table_name, version=Version.LATEST)

                if join_table_description['alias']:
                    join_schema.alias = join_table_description['alias']['name']['value']
            else:
                msg = f'Unsupported join relation: {join["relation"]}'
                raise ValueError(msg)

            if 'Inner' in join['join_operator']:
                join_query = JoinQuery(
                    table=join_schema,
                    on=Conditions(self._process_selection(join['join_operator']['Inner']['On'], table_name)),
                    join_type=JoinType.INNER,
                )
            elif 'LeftOuter' in join['join_operator']:
                join_query = JoinQuery(
                    table=join_schema,
                    on=Conditions(self._process_selection(join['join_operator']['LeftOuter']['On'], table_name)),
                    join_type=JoinType.LEFT,
                )
            elif 'RightOuter' in join['join_operator']:
                join_query = JoinQuery(
                    table=join_schema,
                    on=Conditions(self._process_selection(join['join_operator']['RightOuter']['On'], table_name)),
                    join_type=JoinType.RIGHT,
                )
            elif 'FullOuter' in join['join_operator']:
                join_query = JoinQuery(
                    table=join_schema,
                    on=Conditions(self._process_selection(join['join_operator']['FullOuter']['On'], table_name)),
                    join_type=JoinType.FULL,
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
            field = self._identifier_to_field_reference(group, table_name)
            group_by_queries.append(GroupByQuery(field=field))

        return group_by_queries

    def _process_order_by(self, order_by: list[dict[str, Any]], table_name: str) -> list[OrderByQuery] | None:
        if not order_by:
            return None

        order_by_queries = []
        for order in order_by:
            field = self._identifier_to_field_reference(order['expr'], table_name)
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

    def _unwrap_nested_expression(
        self,
        expression: dict[str, Any],
    ) -> dict[str, Any]:
        if 'Nested' in expression:
            return self._unwrap_nested_expression(expression['Nested'])
        return expression

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
                aggregation = self._unwrap_nested_expression(projection['ExprWithAlias']['expr'])

                alias = projection['ExprWithAlias']['alias']['value']

            elif 'UnnamedExpr' in projection and 'Function' in projection['UnnamedExpr']:
                aggregation = projection['UnnamedExpr']
                alias = None
            else:
                continue

            if 'Function' in aggregation:
                function_expression = aggregation['Function']
                if 'name' in function_expression:
                    name = function_expression['name'][0]['value']
                    agg_function = AGGREGATION_FUNCTIONS.get(name)

                    if not agg_function:
                        continue

                    expression = agg_function(
                        field=self._identifier_to_field_reference(
                            function_expression['args']['List']['args'][0], table_name
                        )
                    )
                    field_alias_name = expression.field.field.name if expression.field.field.name != '*' else 'total'
                    aggregation_queries.append(
                        AggregationQuery(
                            expression=expression,
                            alias=alias if alias else f'{agg_function.name.lower()}_{field_alias_name}',
                        )
                    )
                else:
                    msg = f'Unsupported aggregation function: {aggregation}'
                    raise ValueError(msg)
            elif (
                'Subquery' in aggregation
                or 'CompoundIdentifier' in aggregation
                or 'BinaryOp' in aggregation
                or 'Value' in aggregation
            ):
                continue
            else:
                msg = f'Unsupported aggregation: {projection}'
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
            if 'ExprWithAlias' not in projection:
                continue

            _annotation = self._process_annotation_expression(projection)

            if _annotation:
                annotation_queries.append(AnnotationQuery(value=_annotation))

        if not annotation_queries:
            return None

        return annotation_queries

    def _process_annotation_expression(  # noqa: PLR0911
        self,
        annotation: dict[str, Any],
    ) -> SubQueryStatement | ValueAnnotation | ExpressionAnnotation | None:
        _expression = annotation
        alias = None

        if 'ExprWithAlias' in _expression:
            _annotation = _expression['ExprWithAlias']
            _expression = self._unwrap_nested_expression(_annotation['expr'])
            alias = _annotation['alias']['value']

        if 'Value' in _expression:
            _value_expr = _expression['Value']
            _expr_type = next(iter(_value_expr))
            _expr_value = _value_expr[_expr_type]
            _value_type = VALUE_TYPE_MAPPING[_expr_type]

            _value = _expr_value if _value_type in (bool, str) else _value_type(_expr_value[0])  # type: ignore[operator]

            return ValueAnnotation(
                value=Value(_value),
                alias=alias,  # type: ignore[arg-type]
            )
        if 'Subquery' in _expression:
            sub_query = _expression['Subquery']
            query = self._parsed_sql_query_to_operation(sub_query)
            return SubQueryStatement(query=query, alias=alias)  # type: ignore[arg-type]
        if 'BinaryOp' in _expression:
            return ExpressionAnnotation(
                expression=self._process_binary_op_expression(_expression),
                alias=alias,  # type: ignore[arg-type]
            )
        if 'Function' in _expression:
            function_expression = _expression['Function']

            if 'name' not in function_expression:
                return None

            name = function_expression['name'][0]['value']

            if name in AGGREGATION_FUNCTIONS:
                return None

            _args = function_expression['args']['List']['args']

            if name.lower() in POWER_FUNCTIONS:
                _left = self._process_binary_op_expression(_args[0])
                _right = self._process_binary_op_expression(_args[1])

                return ExpressionAnnotation(
                    expression=CombinedExpression(
                        left=_left,
                        operator=Combinable.POW,
                        right=_right,
                    ),
                    alias=alias,  # type: ignore[arg-type]
                )
            return ExpressionAnnotation(
                expression=Func(
                    name=name,
                    args=[self._process_binary_op_expression(arg) for arg in _args],
                ),
                alias=alias,  # type: ignore[arg-type]
            )
        return None

    def _process_binary_op_expression(self, binary_operation: dict[str, Any]) -> Expression:
        if 'Unnamed' in binary_operation:
            binary_operation = binary_operation['Unnamed']

        if 'Expr' in binary_operation:
            binary_operation = binary_operation['Expr']

        if 'Nested' in binary_operation:
            binary_operation = binary_operation['Nested']

        if 'CompoundIdentifier' in binary_operation:
            _identifier = binary_operation['CompoundIdentifier']

            return FieldReferenceExpression(
                field_reference=FieldReference(
                    field=Field(name=_identifier[1]['value']),
                    table_name=_identifier[0]['value'],
                ),
            )

        if 'BinaryOp' in binary_operation:
            _binary_op = binary_operation['BinaryOp']
            left = self._process_binary_op_expression(_binary_op['left'])
            right = self._process_binary_op_expression(_binary_op['right'])
            operator = _binary_op['op'].lower()
            operator_mapping = {
                'minus': Combinable.SUB,
                'plus': Combinable.ADD,
                'divide': Combinable.DIV,
                'multiply': Combinable.MUL,
                'modulo': Combinable.MOD,
                'bitwisexor': Combinable.XOR,
                'bitwiseand': Combinable.AND,
                'bitwiseor': Combinable.OR,
            }

            return CombinedExpression(
                left=left,
                operator=operator_mapping[operator],
                right=right,
            )

        if 'Value' in binary_operation:
            _value_expr = binary_operation['Value']
            _expr_type = next(iter(_value_expr))
            _expr_value = _value_expr[_expr_type]
            _value_type = VALUE_TYPE_MAPPING[_expr_type]

            _value = _expr_value if _value_type in (bool, str) else _value_type(_expr_value[0])  # type: ignore[operator]

            return Value(_value)

        msg = f'Unsupported binary operation: {binary_operation}'
        raise ValueError(msg)

    def _parsed_sql_query_to_operation(self, parsed_sql: dict[str, Any]) -> QueryStatement:
        _relation = parsed_sql['body']['Select']['from'][0]['relation']

        table_obj: SchemaReference | SubQueryStatement
        if 'Derived' in _relation:
            _derived = _relation['Derived']
            _subquery = _derived['subquery']
            _alias = _derived['alias']['name']['value']
            table_name = _alias
            subquery = self._parsed_sql_query_to_operation(_subquery)
            table_obj = SubQueryStatement(query=subquery, alias=_alias)
        elif 'Table' in _relation:
            table_description = parsed_sql['body']['Select']['from'][0]['relation']['Table']
            table_name = table_description['name'][0]['value']
            table_obj = SchemaReference(name=table_name, version=Version.LATEST)

            if table_description['alias']:
                table_obj.alias = table_description['alias']['name']['value']
        else:
            msg = f'Unsupported relation type. Cannot parse FROM statement: {_relation}'
            raise ValueError(msg)

        query = QueryStatement(table=table_obj)

        _distinct = parsed_sql['body']['Select']['distinct']
        if isinstance(_distinct, str) and _distinct == 'Distinct':
            query.distinct = True
        elif isinstance(_distinct, dict) and 'On' in _distinct:
            query.distinct = [self._identifier_to_field_reference(field, table_name) for field in _distinct['On']]

        query.only = self._process_only(
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
