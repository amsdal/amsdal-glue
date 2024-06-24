from dataclasses import dataclass

from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.enums import JoinType


@dataclass(kw_only=True)
class JoinQuery:
    table: SchemaReference | SubQueryStatement
    on: Conditions
    join_type: JoinType = JoinType.INNER
