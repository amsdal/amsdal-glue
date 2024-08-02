# mypy: disable-error-code="type-abstract"
from amsdal_glue_core.common.data_models.aggregation import AggregationQuery
from amsdal_glue_core.common.data_models.annotation import AnnotationQuery
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
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
from amsdal_glue_core.containers import Container
from amsdal_glue_sql_parser.parsers.base import SqlParserBase


def test_simple_query_command(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('SELECT * FROM "users"')

    result = benchmark(parse_sql)

    assert result == [
        DataQueryOperation(query=QueryStatement(table=SchemaReference(name='users', version=Version.LATEST)))
    ]


def test_only_select_query_command(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('SELECT first_name, users.last_name FROM users;')

    result = benchmark(parse_sql)

    assert result == [
        DataQueryOperation(
            query=QueryStatement(
                table=SchemaReference(name='users', version=Version.LATEST),
                only=[
                    FieldReference(field=Field(name='first_name'), table_name='users'),
                    FieldReference(field=Field(name='last_name'), table_name='users'),
                ],
            ),
        )
    ]


def test_conditions(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql(
            'SELECT first_name, last_name '
            'FROM users '
            'WHERE first_name = \'John\' AND ("users"."last_name" = \'Doe\' OR "first_name" = "last_name");'
        )

    result = benchmark(parse_sql)

    assert result == [
        DataQueryOperation(
            query=QueryStatement(
                table=SchemaReference(name='users', version=Version.LATEST),
                only=[
                    FieldReference(field=Field(name='first_name'), table_name='users'),
                    FieldReference(field=Field(name='last_name'), table_name='users'),
                ],
                where=Conditions(
                    Condition(
                        field=FieldReference(field=Field(name='first_name'), table_name='users'),
                        lookup=FieldLookup.EQ,
                        value=Value('John'),
                    ),
                    Conditions(
                        Condition(
                            field=FieldReference(field=Field(name='last_name'), table_name='users'),
                            lookup=FieldLookup.EQ,
                            value=Value('Doe'),
                        ),
                        Condition(
                            field=FieldReference(field=Field(name='first_name'), table_name='users'),
                            lookup=FieldLookup.EQ,
                            value=FieldReference(field=Field(name='last_name'), table_name='users'),
                        ),
                        connector=FilterConnector.OR,
                    ),
                    connector=FilterConnector.AND,
                ),
            ),
        ),
    ]


def test_simple_alias(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('SELECT "u".first_name, u.last_name ' 'FROM users u WHERE u."last_name" = \'Doe\';')

    result = benchmark(parse_sql)

    assert result == [
        DataQueryOperation(
            query=QueryStatement(
                table=SchemaReference(name='users', version=Version.LATEST, alias='u'),
                only=[
                    FieldReference(field=Field(name='first_name'), table_name='u'),
                    FieldReference(field=Field(name='last_name'), table_name='u'),
                ],
                where=Conditions(
                    Condition(
                        field=FieldReference(field=Field(name='last_name'), table_name='u'),
                        lookup=FieldLookup.EQ,
                        value=Value('Doe'),
                    ),
                    connector=FilterConnector.AND,
                ),
            ),
        ),
    ]


def test_simple_join(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql(
            'SELECT u.first_name, u.last_name, s.* '
            'FROM users u '
            'JOIN shippings s ON u.id = s.customer_id '
            "WHERE u.last_name = 'Doe';"
        )

    result = benchmark(parse_sql)

    assert result == [
        DataQueryOperation(
            query=QueryStatement(
                table=SchemaReference(name='users', version=Version.LATEST, alias='u'),
                only=[
                    FieldReference(field=Field(name='first_name'), table_name='u'),
                    FieldReference(field=Field(name='last_name'), table_name='u'),
                    FieldReference(field=Field(name='*'), table_name='s'),
                ],
                joins=[
                    JoinQuery(
                        table=SchemaReference(name='shippings', version=Version.LATEST, alias='s'),
                        on=Conditions(
                            Condition(
                                field=FieldReference(field=Field(name='id'), table_name='u'),
                                lookup=FieldLookup.EQ,
                                value=FieldReference(field=Field(name='customer_id'), table_name='s'),
                            ),
                            connector=FilterConnector.AND,
                        ),
                        join_type=JoinType.INNER,
                    ),
                ],
                where=Conditions(
                    Condition(
                        field=FieldReference(field=Field(name='last_name'), table_name='u'),
                        lookup=FieldLookup.EQ,
                        value=Value('Doe'),
                    ),
                    connector=FilterConnector.AND,
                ),
            ),
        ),
    ]


def test_multiple_joins(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql(
            'SELECT u.first_name, u.last_name, s.status, a.address '
            'FROM users u '
            'JOIN shippings s ON u.id = s.customer_id '
            'JOIN addresses a ON u.id = a.customer_id '
            "WHERE u.last_name = 'Doe';"
        )

    result = benchmark(parse_sql)

    assert result == [
        DataQueryOperation(
            query=QueryStatement(
                table=SchemaReference(name='users', version=Version.LATEST, alias='u'),
                only=[
                    FieldReference(field=Field(name='first_name'), table_name='u'),
                    FieldReference(field=Field(name='last_name'), table_name='u'),
                    FieldReference(field=Field(name='status'), table_name='s'),
                    FieldReference(field=Field(name='address'), table_name='a'),
                ],
                joins=[
                    JoinQuery(
                        table=SchemaReference(name='shippings', version=Version.LATEST, alias='s'),
                        on=Conditions(
                            Condition(
                                field=FieldReference(field=Field(name='id'), table_name='u'),
                                lookup=FieldLookup.EQ,
                                value=FieldReference(field=Field(name='customer_id'), table_name='s'),
                            ),
                            connector=FilterConnector.AND,
                        ),
                        join_type=JoinType.INNER,
                    ),
                    JoinQuery(
                        table=SchemaReference(name='addresses', version=Version.LATEST, alias='a'),
                        on=Conditions(
                            Condition(
                                field=FieldReference(field=Field(name='id'), table_name='u'),
                                lookup=FieldLookup.EQ,
                                value=FieldReference(field=Field(name='customer_id'), table_name='a'),
                            ),
                            connector=FilterConnector.AND,
                        ),
                        join_type=JoinType.INNER,
                    ),
                ],
                where=Conditions(
                    Condition(
                        field=FieldReference(field=Field(name='last_name'), table_name='u'),
                        lookup=FieldLookup.EQ,
                        value=Value('Doe'),
                    ),
                    connector=FilterConnector.AND,
                ),
            ),
        ),
    ]


def test_query_ordering(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql(
            'SELECT u.first_name, u.last_name, s.status, a.address '
            'FROM users u '
            'JOIN shippings s ON u.id = s.customer_id '
            'JOIN addresses a ON u.id = a.customer_id '
            "WHERE u.last_name = 'Doe' "
            'ORDER BY u.first_name ASC, u.last_name DESC, s.status ASC, a.address DESC;'
        )

    result = benchmark(parse_sql)

    assert result == [
        DataQueryOperation(
            query=QueryStatement(
                table=SchemaReference(name='users', version=Version.LATEST, alias='u'),
                only=[
                    FieldReference(field=Field(name='first_name'), table_name='u'),
                    FieldReference(field=Field(name='last_name'), table_name='u'),
                    FieldReference(field=Field(name='status'), table_name='s'),
                    FieldReference(field=Field(name='address'), table_name='a'),
                ],
                joins=[
                    JoinQuery(
                        table=SchemaReference(name='shippings', version=Version.LATEST, alias='s'),
                        on=Conditions(
                            Condition(
                                field=FieldReference(field=Field(name='id'), table_name='u'),
                                lookup=FieldLookup.EQ,
                                value=FieldReference(field=Field(name='customer_id'), table_name='s'),
                            ),
                            connector=FilterConnector.AND,
                        ),
                        join_type=JoinType.INNER,
                    ),
                    JoinQuery(
                        table=SchemaReference(name='addresses', version=Version.LATEST, alias='a'),
                        on=Conditions(
                            Condition(
                                field=FieldReference(field=Field(name='id'), table_name='u'),
                                lookup=FieldLookup.EQ,
                                value=FieldReference(field=Field(name='customer_id'), table_name='a'),
                            ),
                            connector=FilterConnector.AND,
                        ),
                        join_type=JoinType.INNER,
                    ),
                ],
                where=Conditions(
                    Condition(
                        field=FieldReference(field=Field(name='last_name'), table_name='u'),
                        lookup=FieldLookup.EQ,
                        value=Value('Doe'),
                    ),
                    connector=FilterConnector.AND,
                ),
                order_by=[
                    OrderByQuery(
                        field=FieldReference(field=Field(name='first_name'), table_name='u'),
                        direction=OrderDirection.ASC,
                    ),
                    OrderByQuery(
                        field=FieldReference(field=Field(name='last_name'), table_name='u'),
                        direction=OrderDirection.DESC,
                    ),
                    OrderByQuery(
                        field=FieldReference(field=Field(name='status'), table_name='s'),
                        direction=OrderDirection.ASC,
                    ),
                    OrderByQuery(
                        field=FieldReference(field=Field(name='address'), table_name='a'),
                        direction=OrderDirection.DESC,
                    ),
                ],
            ),
        ),
    ]


def test_simple_query_limit(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('SELECT * FROM "users" LIMIT 10;')

    result = benchmark(parse_sql)

    assert result == [
        DataQueryOperation(
            query=QueryStatement(
                table=SchemaReference(name='users', version=Version.LATEST),
                limit=LimitQuery(limit=10),
            ),
        )
    ]


def test_simple_query_limit_offset(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('SELECT * FROM "users" LIMIT 10 OFFSET 10;')

    result = benchmark(parse_sql)

    assert result == [
        DataQueryOperation(
            query=QueryStatement(
                table=SchemaReference(name='users', version=Version.LATEST),
                limit=LimitQuery(limit=10, offset=10),
            ),
        )
    ]


def test_simple_group_by(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql(
            'SELECT first_name, last_name, age FROM users WHERE age > 18 GROUP BY first_name, last_name;'
        )

    result = benchmark(parse_sql)

    assert result == [
        DataQueryOperation(
            query=QueryStatement(
                table=SchemaReference(name='users', version=Version.LATEST),
                only=[
                    FieldReference(field=Field(name='first_name'), table_name='users'),
                    FieldReference(field=Field(name='last_name'), table_name='users'),
                    FieldReference(field=Field(name='age'), table_name='users'),
                ],
                group_by=[
                    GroupByQuery(field=FieldReference(field=Field(name='first_name'), table_name='users')),
                    GroupByQuery(field=FieldReference(field=Field(name='last_name'), table_name='users')),
                ],
                where=Conditions(
                    Condition(
                        field=FieldReference(field=Field(name='age'), table_name='users'),
                        lookup=FieldLookup.GT,
                        value=Value('18'),
                    ),
                    connector=FilterConnector.AND,
                ),
            ),
        )
    ]


def test_simple_aggregate(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql(
            'SELECT COUNT(*) as total, AVG(age) as average, MAX(age) as max_age, MIN(age) as age_min, SUM(age) '
            'FROM users '
            'WHERE age > 18 '
            'GROUP BY first_name, last_name;'
        )

    result = benchmark(parse_sql)

    assert result == [
        DataQueryOperation(
            query=QueryStatement(
                table=SchemaReference(name='users', version=Version.LATEST),
                aggregations=[
                    AggregationQuery(
                        expression=Count(field=FieldReference(field=Field(name='*'), table_name='users')),
                        alias='total',
                    ),
                    AggregationQuery(
                        expression=Avg(field=FieldReference(field=Field(name='age'), table_name='users')),
                        alias='average',
                    ),
                    AggregationQuery(
                        expression=Max(field=FieldReference(field=Field(name='age'), table_name='users')),
                        alias='max_age',
                    ),
                    AggregationQuery(
                        expression=Min(field=FieldReference(field=Field(name='age'), table_name='users')),
                        alias='age_min',
                    ),
                    AggregationQuery(
                        expression=Sum(field=FieldReference(field=Field(name='age'), table_name='users')),
                        alias='sum_age',
                    ),
                ],
                group_by=[
                    GroupByQuery(field=FieldReference(field=Field(name='first_name'), table_name='users')),
                    GroupByQuery(field=FieldReference(field=Field(name='last_name'), table_name='users')),
                ],
                where=Conditions(
                    Condition(
                        field=FieldReference(field=Field(name='age'), table_name='users'),
                        lookup=FieldLookup.GT,
                        value=Value('18'),
                    ),
                    connector=FilterConnector.AND,
                ),
            ),
        )
    ]


def test_aggregation_with_joins(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql(
            'SELECT customers.first_name, customers.last_name, SUM(price) '
            'FROM orders JOIN customers ON customers.id = orders.customer_id '
            'GROUP BY customers.first_name, customers.last_name '
            'ORDER BY customers.id ASC '
        )

    result = benchmark(parse_sql)

    assert result == [
        DataQueryOperation(
            query=QueryStatement(
                table=SchemaReference(name='orders', version=Version.LATEST),
                only=[
                    FieldReference(field=Field(name='first_name'), table_name='customers'),
                    FieldReference(field=Field(name='last_name'), table_name='customers'),
                ],
                joins=[
                    JoinQuery(
                        table=SchemaReference(name='customers', version=Version.LATEST),
                        on=Conditions(
                            Condition(
                                field=FieldReference(field=Field(name='id'), table_name='customers'),
                                lookup=FieldLookup.EQ,
                                value=FieldReference(field=Field(name='customer_id'), table_name='orders'),
                            ),
                        ),
                        join_type=JoinType.INNER,
                    ),
                ],
                aggregations=[
                    AggregationQuery(
                        expression=Sum(field=FieldReference(field=Field(name='price'), table_name='orders')),
                        alias='sum_price',
                    ),
                ],
                group_by=[
                    GroupByQuery(field=FieldReference(field=Field(name='first_name'), table_name='customers')),
                    GroupByQuery(field=FieldReference(field=Field(name='last_name'), table_name='customers')),
                ],
                order_by=[
                    OrderByQuery(
                        field=FieldReference(field=Field(name='id'), table_name='customers'),
                        direction=OrderDirection.ASC,
                    ),
                ],
            ),
        ),
    ]


def test_simple_annotation(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql(
            'SELECT first_name, last_name, '
            '(SELECT COUNT(*) FROM orders WHERE orders.user_id = users.id) as orders_count '
            'FROM users;'
        )

    result = benchmark(parse_sql)

    assert result == [
        DataQueryOperation(
            query=QueryStatement(
                table=SchemaReference(name='users', version=Version.LATEST),
                only=[
                    FieldReference(field=Field(name='first_name'), table_name='users'),
                    FieldReference(field=Field(name='last_name'), table_name='users'),
                ],
                annotations=[
                    AnnotationQuery(
                        value=SubQueryStatement(
                            query=QueryStatement(
                                table=SchemaReference(name='orders', version=Version.LATEST),
                                aggregations=[
                                    AggregationQuery(
                                        expression=Count(
                                            field=FieldReference(field=Field(name='*'), table_name='orders')
                                        ),
                                        alias='count_total',
                                    ),
                                ],
                                where=Conditions(
                                    Condition(
                                        field=FieldReference(field=Field(name='user_id'), table_name='orders'),
                                        lookup=FieldLookup.EQ,
                                        value=FieldReference(field=Field(name='id'), table_name='users'),
                                    ),
                                    connector=FilterConnector.AND,
                                ),
                            ),
                            alias='orders_count',
                        ),
                    )
                ],
            ),
        )
    ]


def test_select_distinct(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('SELECT DISTINCT first_name, last_name FROM users;')

    result = benchmark(parse_sql)

    assert result == [
        DataQueryOperation(
            query=QueryStatement(
                table=SchemaReference(name='users', version=Version.LATEST),
                only=[
                    FieldReference(field=Field(name='first_name'), table_name='users'),
                    FieldReference(field=Field(name='last_name'), table_name='users'),
                ],
                distinct=True,
            ),
        )
    ]
