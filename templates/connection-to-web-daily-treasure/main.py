from datetime import datetime
from pprint import pprint

from amsdal_glue.initialize import init_default_containers
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.value import Value
from utils import *


def main():
    init_default_containers()
    register_connections()

    # Fetch existing schemas (tables)
    all_schemas = fetch_schemas()

    print(f'All schemas (total: {len(all_schemas)}):')

    for schema in all_schemas:
        pprint(schema)

    # query all "Daily Treasury Real Long-Term Rates"
    query = QueryStatement(
        table=SchemaReference(name='daily_treasury_real_long_term', version=Version.LATEST),
    )
    data: list[Data] = query_data(query)
    print('Found records:', len(data))
    print('First record:')
    pprint(data[0])

    # query and filter "Daily Treasury Par Yield Curve Rates" for 07/01/2024
    query = QueryStatement(
        table=SchemaReference(name='daily_treasury_yield_curve', version=Version.LATEST),
        where=Conditions(
            Condition(
                field=FieldReference(
                    field=Field(name='NEW_DATE'),
                    table_name='daily_treasury_yield_curve',
                ),
                lookup=FieldLookup.EQ,
                value=Value('2024-07-01'),
            ),
        ),
    )
    data: list[Data] = query_data(query)
    print('Found records:', len(data))
    pprint(data)


if __name__ == '__main__':
    main()
