from pprint import pprint

from amsdal_glue import Condition
from amsdal_glue import Conditions
from amsdal_glue import Field
from amsdal_glue import FieldLookup
from amsdal_glue import FieldReference
from amsdal_glue import SchemaReference
from amsdal_glue import Value
from amsdal_glue import Version
from amsdal_glue import init_default_containers
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression

from utils import *


def main():
    init_default_containers()
    register_connections()

    # Fetch existing schemas (tables)
    all_schemas = fetch_schemas()

    print(f"All schemas (total: {len(all_schemas)}):")

    for schema in all_schemas:
        pprint(schema)

    # query all "Daily Treasury Real Long-Term Rates"
    query = QueryStatement(
        table=SchemaReference(
            name="daily_treasury_real_long_term", version=Version.LATEST
        ),
    )
    data: list[Data] = query_data(query)
    print("Found records:", len(data))
    print("First record:")
    pprint(data[0])

    # query and filter "Daily Treasury Par Yield Curve Rates" for 07/01/2024
    query = QueryStatement(
        table=SchemaReference(
            name="daily_treasury_yield_curve", version=Version.LATEST
        ),
        where=Conditions(
            Condition(
                left=FieldReferenceExpression(
                    field_reference=FieldReference(
                        field=Field(name="NEW_DATE"),
                        table_name="daily_treasury_yield_curve",
                    )
                ),
                lookup=FieldLookup.EQ,
                right=Value("2024-07-01"),
            ),
        ),
    )
    data: list[Data] = query_data(query)
    print("Found records:", len(data))
    pprint(data)


if __name__ == "__main__":
    main()
