# mypy: disable-error-code="type-abstract"
import pytest
from amsdal_glue_core.common.data_models.aggregation import AggregationQuery
from amsdal_glue_core.common.data_models.annotation import AnnotationQuery
from amsdal_glue_core.common.data_models.annotation import ExpressionAnnotation
from amsdal_glue_core.common.data_models.annotation import ValueAnnotation
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
from amsdal_glue_core.common.expressions.common import Combinable
from amsdal_glue_core.common.expressions.common import CombinedExpression
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
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
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='first_name'), table_name='users')
                        ),
                        lookup=FieldLookup.EQ,
                        right=Value('John'),
                    ),
                    Conditions(
                        Condition(
                            left=FieldReferenceExpression(
                                field_reference=FieldReference(field=Field(name='last_name'), table_name='users')
                            ),
                            lookup=FieldLookup.EQ,
                            right=Value('Doe'),
                        ),
                        Condition(
                            left=FieldReferenceExpression(
                                field_reference=FieldReference(field=Field(name='first_name'), table_name='users')
                            ),
                            lookup=FieldLookup.EQ,
                            right=FieldReferenceExpression(
                                field_reference=FieldReference(field=Field(name='last_name'), table_name='users')
                            ),
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
        return parser.parse_sql('SELECT "u".first_name, u.last_name FROM users u WHERE u."last_name" = \'Doe\';')

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
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='last_name'), table_name='u')
                        ),
                        lookup=FieldLookup.EQ,
                        right=Value('Doe'),
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
                                left=FieldReferenceExpression(
                                    field_reference=FieldReference(field=Field(name='id'), table_name='u')
                                ),
                                lookup=FieldLookup.EQ,
                                right=FieldReferenceExpression(
                                    field_reference=FieldReference(field=Field(name='customer_id'), table_name='s')
                                ),
                            ),
                            connector=FilterConnector.AND,
                        ),
                        join_type=JoinType.INNER,
                    ),
                ],
                where=Conditions(
                    Condition(
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='last_name'), table_name='u')
                        ),
                        lookup=FieldLookup.EQ,
                        right=Value('Doe'),
                    ),
                    connector=FilterConnector.AND,
                ),
            ),
        ),
    ]

    assert parser.parse_sql(
        'SELECT u.first_name, u.last_name, s.* '
        'FROM users u '
        'JOIN shippings s ON u.id = s.customer_id '
        "WHERE u.last_name = 'Doe';"
    ) == parser.parse_sql(
        'SELECT u.first_name, u.last_name, s.* '
        'FROM users u '
        'INNER JOIN shippings s ON u.id = s.customer_id '
        "WHERE u.last_name = 'Doe';"
    )


@pytest.mark.parametrize(
    'sql_type,expected',
    [
        ('LEFT JOIN', JoinType.LEFT),
        ('RIGHT JOIN', JoinType.RIGHT),
        ('FULL JOIN', JoinType.FULL),
    ],
)
def test_simple_different_join(sql_type: str, expected: JoinType) -> None:
    parser = Container.services.get(SqlParserBase)

    result = parser.parse_sql(
        'SELECT u.first_name, u.last_name, s.* '  # noqa: S608
        'FROM users u '
        f'{sql_type} shippings s ON u.id = s.customer_id '
        "WHERE u.last_name = 'Doe';"
    )

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
                                left=FieldReferenceExpression(
                                    field_reference=FieldReference(field=Field(name='id'), table_name='u')
                                ),
                                lookup=FieldLookup.EQ,
                                right=FieldReferenceExpression(
                                    field_reference=FieldReference(field=Field(name='customer_id'), table_name='s')
                                ),
                            ),
                            connector=FilterConnector.AND,
                        ),
                        join_type=expected,
                    ),
                ],
                where=Conditions(
                    Condition(
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='last_name'), table_name='u')
                        ),
                        lookup=FieldLookup.EQ,
                        right=Value('Doe'),
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
                                left=FieldReferenceExpression(
                                    field_reference=FieldReference(field=Field(name='id'), table_name='u')
                                ),
                                lookup=FieldLookup.EQ,
                                right=FieldReferenceExpression(
                                    field_reference=FieldReference(field=Field(name='customer_id'), table_name='s')
                                ),
                            ),
                            connector=FilterConnector.AND,
                        ),
                        join_type=JoinType.INNER,
                    ),
                    JoinQuery(
                        table=SchemaReference(name='addresses', version=Version.LATEST, alias='a'),
                        on=Conditions(
                            Condition(
                                left=FieldReferenceExpression(
                                    field_reference=FieldReference(field=Field(name='id'), table_name='u')
                                ),
                                lookup=FieldLookup.EQ,
                                right=FieldReferenceExpression(
                                    field_reference=FieldReference(field=Field(name='customer_id'), table_name='a')
                                ),
                            ),
                            connector=FilterConnector.AND,
                        ),
                        join_type=JoinType.INNER,
                    ),
                ],
                where=Conditions(
                    Condition(
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='last_name'), table_name='u')
                        ),
                        lookup=FieldLookup.EQ,
                        right=Value('Doe'),
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
                                left=FieldReferenceExpression(
                                    field_reference=FieldReference(field=Field(name='id'), table_name='u')
                                ),
                                lookup=FieldLookup.EQ,
                                right=FieldReferenceExpression(
                                    field_reference=FieldReference(field=Field(name='customer_id'), table_name='s')
                                ),
                            ),
                            connector=FilterConnector.AND,
                        ),
                        join_type=JoinType.INNER,
                    ),
                    JoinQuery(
                        table=SchemaReference(name='addresses', version=Version.LATEST, alias='a'),
                        on=Conditions(
                            Condition(
                                left=FieldReferenceExpression(
                                    field_reference=FieldReference(field=Field(name='id'), table_name='u')
                                ),
                                lookup=FieldLookup.EQ,
                                right=FieldReferenceExpression(
                                    field_reference=FieldReference(field=Field(name='customer_id'), table_name='a')
                                ),
                            ),
                            connector=FilterConnector.AND,
                        ),
                        join_type=JoinType.INNER,
                    ),
                ],
                where=Conditions(
                    Condition(
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='last_name'), table_name='u')
                        ),
                        lookup=FieldLookup.EQ,
                        right=Value('Doe'),
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
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='age'), table_name='users')
                        ),
                        lookup=FieldLookup.GT,
                        right=Value('18'),
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
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='age'), table_name='users')
                        ),
                        lookup=FieldLookup.GT,
                        right=Value('18'),
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
                                left=FieldReferenceExpression(
                                    field_reference=FieldReference(field=Field(name='id'), table_name='customers')
                                ),
                                lookup=FieldLookup.EQ,
                                right=FieldReferenceExpression(
                                    field_reference=FieldReference(field=Field(name='customer_id'), table_name='orders')
                                ),
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
                                        left=FieldReferenceExpression(
                                            field_reference=FieldReference(
                                                field=Field(name='user_id'), table_name='orders'
                                            )
                                        ),
                                        lookup=FieldLookup.EQ,
                                        right=FieldReferenceExpression(
                                            field_reference=FieldReference(field=Field(name='id'), table_name='users')
                                        ),
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


def test_select_distinct_single_field(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('SELECT DISTINCT first_name FROM users;')

    result = benchmark(parse_sql)

    assert result == [
        DataQueryOperation(
            query=QueryStatement(
                table=SchemaReference(name='users', version=Version.LATEST),
                only=[
                    FieldReference(field=Field(name='first_name'), table_name='users'),
                ],
                distinct=True,
            ),
        )
    ]


def test_select_distinct_on(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('SELECT DISTINCT ON (first_name) first_name, last_name FROM users;')

    result = benchmark(parse_sql)

    assert result == [
        DataQueryOperation(
            query=QueryStatement(
                table=SchemaReference(name='users', version=Version.LATEST),
                only=[
                    FieldReference(field=Field(name='first_name'), table_name='users'),
                    FieldReference(field=Field(name='last_name'), table_name='users'),
                ],
                distinct=[
                    FieldReference(field=Field(name='first_name'), table_name='users'),
                ],
            ),
        )
    ]


def test_select_distinct_multiple_fields(benchmark) -> None:
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


def test_select_distinct_on_multiple_fields(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('SELECT DISTINCT ON (first_name, last_name) first_name, last_name FROM users;')

    result = benchmark(parse_sql)

    assert result == [
        DataQueryOperation(
            query=QueryStatement(
                table=SchemaReference(name='users', version=Version.LATEST),
                only=[
                    FieldReference(field=Field(name='first_name'), table_name='users'),
                    FieldReference(field=Field(name='last_name'), table_name='users'),
                ],
                distinct=[
                    FieldReference(field=Field(name='first_name'), table_name='users'),
                    FieldReference(field=Field(name='last_name'), table_name='users'),
                ],
            ),
        )
    ]


def test_join_subquery_simple(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql(
            'SELECT u.first_name FROM users as u JOIN (SELECT profile.bio FROM profile) as p ON p.email = u.email'
        )

    result = benchmark(parse_sql)

    assert result == [
        DataQueryOperation(
            query=QueryStatement(
                table=SchemaReference(name='users', alias='u', version=Version.LATEST),
                only=[
                    FieldReference(field=Field(name='first_name'), table_name='u'),
                ],
                joins=[
                    JoinQuery(
                        table=SubQueryStatement(
                            query=QueryStatement(
                                only=[
                                    FieldReference(field=Field(name='bio'), table_name='profile'),
                                ],
                                table=SchemaReference(name='profile', version=Version.LATEST),
                            ),
                            alias='p',
                        ),
                        on=Conditions(
                            Condition(
                                left=FieldReferenceExpression(
                                    field_reference=FieldReference(field=Field(name='email'), table_name='p')
                                ),
                                lookup=FieldLookup.EQ,
                                right=FieldReferenceExpression(
                                    field_reference=FieldReference(field=Field(name='email'), table_name='u')
                                ),
                            ),
                        ),
                        join_type=JoinType.INNER,
                    ),
                ],
            ),
        )
    ]


def test_from_subquery(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql(
            'SELECT u.first_name '
            'FROM ('
            'SELECT first_name, last_name FROM users WHERE is_active = TRUE'
            ') AS u '
            "WHERE u.last_name = 'Doe';"
        )

    result = benchmark(parse_sql)

    assert result == [
        DataQueryOperation(
            query=QueryStatement(
                table=SubQueryStatement(
                    query=QueryStatement(
                        table=SchemaReference(name='users', version=Version.LATEST),
                        only=[
                            FieldReference(field=Field(name='first_name'), table_name='users'),
                            FieldReference(field=Field(name='last_name'), table_name='users'),
                        ],
                        where=Conditions(
                            Condition(
                                left=FieldReferenceExpression(
                                    field_reference=FieldReference(field=Field(name='is_active'), table_name='users')
                                ),
                                lookup=FieldLookup.EQ,
                                right=Value(value=True),
                            ),
                            connector=FilterConnector.AND,
                        ),
                    ),
                    alias='u',
                ),
                only=[
                    FieldReference(field=Field(name='first_name'), table_name='u'),
                ],
                where=Conditions(
                    Condition(
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='last_name'), table_name='u')
                        ),
                        lookup=FieldLookup.EQ,
                        right=Value('Doe'),
                    ),
                    connector=FilterConnector.AND,
                ),
            ),
        )
    ]


def test_select_aliased_query(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('SELECT u.first_name AS fname FROM users AS u')

    result = benchmark(parse_sql)

    assert result == [
        DataQueryOperation(
            query=QueryStatement(
                table=SchemaReference(name='users', alias='u', version=Version.LATEST),
                only=[
                    FieldReferenceAliased(field=Field(name='first_name'), table_name='u', alias='fname'),
                ],
            ),
        )
    ]


def test_select_aggregation_aliased_query(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('SELECT SUM(u.count) AS total_count FROM users AS u')

    result = benchmark(parse_sql)

    assert result == [
        DataQueryOperation(
            query=QueryStatement(
                table=SchemaReference(name='users', alias='u', version=Version.LATEST),
                aggregations=[
                    AggregationQuery(
                        expression=Sum(field=FieldReference(field=Field(name='count'), table_name='u')),
                        alias='total_count',
                    ),
                ],
            ),
        )
    ]


@pytest.mark.parametrize(
    'math_op,glue_math_op',
    [
        ('-', Combinable.SUB),
        ('+', Combinable.ADD),
        ('/', Combinable.DIV),
        ('*', Combinable.MUL),
        ('%', Combinable.MOD),
        ('^', Combinable.XOR),
        ('&', Combinable.AND),
        ('|', Combinable.OR),
    ],
)
def test_select_math_expression(benchmark, math_op, glue_math_op) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql(f'SELECT (u.total_count {math_op} u.city_count) AS diff_count FROM users AS u')  # noqa: S608

    result = benchmark(parse_sql)

    assert result == [
        DataQueryOperation(
            query=QueryStatement(
                table=SchemaReference(name='users', alias='u', version=Version.LATEST),
                annotations=[
                    AnnotationQuery(
                        value=ExpressionAnnotation(
                            expression=CombinedExpression(
                                left=FieldReferenceExpression(
                                    field_reference=FieldReference(field=Field(name='total_count'), table_name='u')
                                ),
                                operator=glue_math_op,
                                right=FieldReferenceExpression(
                                    field_reference=FieldReference(field=Field(name='city_count'), table_name='u')
                                ),
                            ),
                            alias='diff_count',
                        ),
                    ),
                ],
            ),
        )
    ]


def test_select_math_expression_mixed(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('SELECT (u.total_count * 10.25) AS diff_count FROM users AS u')

    result = benchmark(parse_sql)

    assert result == [
        DataQueryOperation(
            query=QueryStatement(
                table=SchemaReference(name='users', alias='u', version=Version.LATEST),
                annotations=[
                    AnnotationQuery(
                        value=ExpressionAnnotation(
                            expression=CombinedExpression(
                                left=FieldReferenceExpression(
                                    field_reference=FieldReference(field=Field(name='total_count'), table_name='u')
                                ),
                                operator=Combinable.MUL,
                                right=Value(10.25),
                            ),
                            alias='diff_count',
                        ),
                    ),
                ],
            ),
        )
    ]


def test_complex_math_mixed(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql(
            'SELECT ((u.total_count * 10.25) - (u.city_count + u.town_count)) AS result FROM users AS u'
        )

    result = benchmark(parse_sql)
    expected = [
        DataQueryOperation(
            query=QueryStatement(
                table=SchemaReference(name='users', alias='u', version=Version.LATEST),
                annotations=[
                    AnnotationQuery(
                        value=ExpressionAnnotation(
                            expression=CombinedExpression(
                                left=CombinedExpression(
                                    left=FieldReferenceExpression(
                                        field_reference=FieldReference(field=Field(name='total_count'), table_name='u')
                                    ),
                                    operator=Combinable.MUL,
                                    right=Value(10.25),
                                ),
                                operator=Combinable.SUB,
                                right=CombinedExpression(
                                    left=FieldReferenceExpression(
                                        field_reference=FieldReference(field=Field(name='city_count'), table_name='u')
                                    ),
                                    operator=Combinable.ADD,
                                    right=FieldReferenceExpression(
                                        field_reference=FieldReference(field=Field(name='town_count'), table_name='u')
                                    ),
                                ),
                            ),
                            alias='result',
                        ),
                    ),
                ],
            ),
        ),
    ]
    assert result == expected


def test_select_pow_expression(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('SELECT POWER(u.total_count, u.city_count) AS result FROM users AS u')

    result = benchmark(parse_sql)

    assert result == [
        DataQueryOperation(
            query=QueryStatement(
                table=SchemaReference(name='users', alias='u', version=Version.LATEST),
                annotations=[
                    AnnotationQuery(
                        value=ExpressionAnnotation(
                            expression=CombinedExpression(
                                left=FieldReferenceExpression(
                                    field_reference=FieldReference(field=Field(name='total_count'), table_name='u')
                                ),
                                operator=Combinable.POW,
                                right=FieldReferenceExpression(
                                    field_reference=FieldReference(field=Field(name='city_count'), table_name='u')
                                ),
                            ),
                            alias='result',
                        ),
                    ),
                ],
            ),
        )
    ]


def test_select_power_mixed(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('SELECT POWER(u.total_count, 10) AS result FROM users AS u')

    result = benchmark(parse_sql)

    assert result == [
        DataQueryOperation(
            query=QueryStatement(
                table=SchemaReference(name='users', alias='u', version=Version.LATEST),
                annotations=[
                    AnnotationQuery(
                        value=ExpressionAnnotation(
                            expression=CombinedExpression(
                                left=FieldReferenceExpression(
                                    field_reference=FieldReference(field=Field(name='total_count'), table_name='u')
                                ),
                                operator=Combinable.POW,
                                right=Value(value=10),
                            ),
                            alias='result',
                        ),
                    ),
                ],
            ),
        )
    ]


@pytest.mark.parametrize(
    'sql_value,python_value',
    [
        (10, 10),
        (20.5, 20.5),
        ("'Hello'", 'Hello'),
        ('TRUE', True),
    ],
)
def test_select_value_expression(benchmark, sql_value, python_value) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql(f'SELECT {sql_value} AS result FROM users AS u')  # noqa: S608

    result = benchmark(parse_sql)

    assert result == [
        DataQueryOperation(
            query=QueryStatement(
                table=SchemaReference(name='users', alias='u', version=Version.LATEST),
                annotations=[
                    AnnotationQuery(
                        value=ValueAnnotation(
                            value=Value(python_value),
                            alias='result',
                        ),
                    ),
                ],
            ),
        )
    ]


def test_select_nested_value_expression(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('SELECT ((((100)))) AS result FROM users AS u')

    result = benchmark(parse_sql)

    assert result == [
        DataQueryOperation(
            query=QueryStatement(
                table=SchemaReference(name='users', alias='u', version=Version.LATEST),
                annotations=[
                    AnnotationQuery(
                        value=ValueAnnotation(
                            value=Value(100),
                            alias='result',
                        ),
                    ),
                ],
            ),
        )
    ]
