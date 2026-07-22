from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.distinct import DistinctClause
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.group_by import GroupByQuery
from amsdal_glue_core.common.data_models.join import JoinQuery
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.select_expression import SelectExpression
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import JoinType
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.aggregation import Sum
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.sql.connections.csv_connection import CsvConnection


def query_customers(database_connection: CsvConnection, namespace: str | None = None) -> list[Data]:
    return database_connection.query(
        QueryStatement(
            table=SchemaReference(name='customers', alias='c', namespace=namespace, version=Version.LATEST),
            order_by=[
                OrderByQuery(
                    expression=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='id'), table_name='c')
                    ),
                    direction=OrderDirection.ASC,
                ),
            ],
        )
    )


def query_orders_with_customers(database_connection: CsvConnection, join_type: JoinType = JoinType.INNER) -> list[Data]:
    return database_connection.query(
        QueryStatement(
            table=SchemaReference(name='orders', alias='o', version=Version.LATEST),
            order_by=[
                OrderByQuery(
                    expression=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='id'), table_name='o')
                    ),
                    direction=OrderDirection.ASC,
                ),
            ],
            only=[
                FieldReference(field=Field(name='id'), table_name='o'),
                FieldReference(field=Field(name='amount'), table_name='o'),
                FieldReference(field=Field(name='customer_id'), table_name='o'),
                FieldReference(field=Field(name='name'), table_name='c'),
                FieldReference(field=Field(name='age'), table_name='c'),
            ],
            joins=[
                JoinQuery(
                    table=SchemaReference(name='customers', alias='c', version=Version.LATEST),
                    on=Conditions(
                        Condition(
                            left=FieldReferenceExpression(
                                field_reference=FieldReference(field=Field(name='customer_id'), table_name='o')
                            ),
                            lookup=FieldLookup.EQ,
                            right=FieldReferenceExpression(
                                field_reference=FieldReference(field=Field(name='id'), table_name='c')
                            ),
                        ),
                    ),
                    join_type=join_type,
                ),
            ],
        )
    )


def query_customers_age(database_connection: CsvConnection, *, distinct: bool = False) -> list[Data]:
    query = QueryStatement(
        table=SchemaReference(name='customers', alias='c', version=Version.LATEST),
        only=[
            FieldReference(field=Field(name='age'), table_name='c'),
        ],
        order_by=[
            OrderByQuery(
                expression=FieldReferenceExpression(
                    field_reference=FieldReference(field=Field(name='age'), table_name='c')
                ),
                direction=OrderDirection.ASC,
            ),
        ],
    )

    if distinct:
        query.distinct = DistinctClause()

    return database_connection.query(query)


def query_big_orders(database_connection: CsvConnection) -> list[Data]:
    return database_connection.query(
        QueryStatement(
            table=SchemaReference(name='orders', alias='o', version=Version.LATEST),
            order_by=[
                OrderByQuery(
                    expression=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='id'), table_name='o')
                    ),
                    direction=OrderDirection.ASC,
                ),
            ],
            only=[
                FieldReference(field=Field(name='id'), table_name='o'),
                FieldReference(field=Field(name='amount'), table_name='o'),
                FieldReference(field=Field(name='customer_id'), table_name='o'),
            ],
            where=Conditions(
                Condition(
                    left=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='amount'), table_name='o')
                    ),
                    lookup=FieldLookup.GT,
                    right=Value(100),
                ),
            ),
        )
    )


def query_orders_for_customer(database_connection: CsvConnection) -> list[Data]:
    return database_connection.query(
        QueryStatement(
            table=SchemaReference(name='orders', alias='o', version=Version.LATEST),
            order_by=[
                OrderByQuery(
                    expression=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='id'), table_name='o')
                    ),
                    direction=OrderDirection.ASC,
                ),
            ],
            only=[
                FieldReference(field=Field(name='id'), table_name='o'),
                FieldReference(field=Field(name='amount'), table_name='o'),
                FieldReference(field=Field(name='customer_id'), table_name='o'),
                FieldReference(field=Field(name='age'), table_name='c'),
            ],
            joins=[
                JoinQuery(
                    table=SchemaReference(name='customers', alias='c', version=Version.LATEST),
                    on=Conditions(
                        Condition(
                            left=FieldReferenceExpression(
                                field_reference=FieldReference(field=Field(name='customer_id'), table_name='o')
                            ),
                            lookup=FieldLookup.EQ,
                            right=FieldReferenceExpression(
                                field_reference=FieldReference(field=Field(name='id'), table_name='c')
                            ),
                        ),
                    ),
                    join_type=JoinType.INNER,
                ),
            ],
            where=Conditions(
                Condition(
                    left=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='name'), table_name='c')
                    ),
                    lookup=FieldLookup.EQ,
                    right=Value('Alice'),
                ),
            ),
        )
    )


def query_customers_expenses(database_connection: CsvConnection) -> list[Data]:
    return database_connection.query(
        QueryStatement(
            only=[
                FieldReference(field=Field(name='id'), table_name='c'),
            ],
            expressions=[
                SelectExpression(
                    expression=SubQueryStatement(
                        alias='total_amount',
                        query=QueryStatement(
                            expressions=[
                                SelectExpression(
                                    expression=Sum(
                                        expression=FieldReferenceExpression(
                                            field_reference=FieldReference(field=Field(name='amount'), table_name='o')
                                        ),
                                    ),
                                    alias='total_amount',
                                ),
                            ],
                            table=SchemaReference(name='orders', alias='o', version=Version.LATEST),
                            where=Conditions(
                                Condition(
                                    left=FieldReferenceExpression(
                                        field_reference=FieldReference(field=Field(name='customer_id'), table_name='o')
                                    ),
                                    lookup=FieldLookup.EQ,
                                    right=FieldReferenceExpression(
                                        field_reference=FieldReference(field=Field(name='id'), table_name='c')
                                    ),
                                ),
                            ),
                        ),
                    ),
                    alias='total_amount',
                ),
            ],
            table=SchemaReference(name='customers', alias='c', version=Version.LATEST),
            order_by=[
                OrderByQuery(
                    expression=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='id'), table_name='c')
                    ),
                    direction=OrderDirection.ASC,
                ),
            ],
        )
    )


def query_expenses_by_customer(database_connection: CsvConnection) -> list[Data]:
    return database_connection.query(
        query=QueryStatement(
            table=SchemaReference(name='orders', alias='o', version=Version.LATEST),
            only=[
                FieldReference(field=Field(name='customer_id'), table_name='o'),
            ],
            expressions=[
                SelectExpression(
                    expression=Sum(
                        expression=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='amount'), table_name='o')
                        ),
                    ),
                    alias='total_amount',
                ),
            ],
            group_by=[
                GroupByQuery(
                    expression=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='customer_id'), table_name='o')
                    )
                ),
            ],
            order_by=[
                OrderByQuery(
                    expression=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='customer_id'), table_name='o')
                    ),
                    direction=OrderDirection.ASC,
                ),
            ],
        ),
    )


def query_expenses_by_customer_with_name(database_connection: CsvConnection) -> list[Data]:
    return database_connection.query(
        query=QueryStatement(
            table=SchemaReference(name='orders', version=Version.LATEST),
            only=[
                FieldReference(field=Field(name='id'), table_name='customers'),
                FieldReference(field=Field(name='name'), table_name='customers'),
            ],
            joins=[
                JoinQuery(
                    table=SchemaReference(name='customers', version=Version.LATEST),
                    on=Conditions(
                        Condition(
                            left=FieldReferenceExpression(
                                field_reference=FieldReference(field=Field(name='customer_id'), table_name='orders')
                            ),
                            lookup=FieldLookup.EQ,
                            right=FieldReferenceExpression(
                                field_reference=FieldReference(field=Field(name='id'), table_name='customers')
                            ),
                        ),
                    ),
                    join_type=JoinType.INNER,
                ),
            ],
            expressions=[
                SelectExpression(
                    expression=Sum(
                        expression=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='amount'), table_name='orders')
                        ),
                    ),
                    alias='sum_amount',
                ),
            ],
            group_by=[
                GroupByQuery(
                    expression=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='id'), table_name='customers')
                    )
                ),
                GroupByQuery(
                    expression=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='name'), table_name='customers')
                    )
                ),
            ],
            order_by=[
                OrderByQuery(
                    expression=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='id'), table_name='customers')
                    ),
                    direction=OrderDirection.ASC,
                ),
            ],
        ),
    )
