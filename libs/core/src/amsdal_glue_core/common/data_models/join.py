from dataclasses import dataclass

from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.enums import JoinType


@dataclass(kw_only=True)
class JoinQuery:
    """Represents a join query.

    Attributes:
        table (SchemaReference | SubQueryStatement): The table or subquery being joined.
        on (Conditions): The conditions for the join.
        join_type (JoinType): The type of join. Defaults to JoinType.INNER.
    """

    table: SchemaReference | SubQueryStatement
    on: Conditions
    join_type: JoinType = JoinType.INNER
