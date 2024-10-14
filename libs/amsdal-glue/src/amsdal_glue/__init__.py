"""
AMSDAL Glue is a library that provides a set of tools to help you build your own data access layer.
"""

from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection
from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_core.common.data_models.aggregation import AggregationQuery
from amsdal_glue_core.common.data_models.annotation import AnnotationQuery
from amsdal_glue_core.common.data_models.annotation import ExpressionAnnotation
from amsdal_glue_core.common.data_models.annotation import ValueAnnotation
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
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
from amsdal_glue_core.common.data_models.metadata import Metadata
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.results.data import DataResult
from amsdal_glue_core.common.data_models.results.data import LockResult
from amsdal_glue_core.common.data_models.results.data import TransactionResult
from amsdal_glue_core.common.data_models.results.schema import SchemaResult
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import FilterConnector
from amsdal_glue_core.common.enums import JoinType
from amsdal_glue_core.common.enums import LockAction
from amsdal_glue_core.common.enums import LockMode
from amsdal_glue_core.common.enums import LockParameter
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import TransactionAction
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.aggregation import Avg
from amsdal_glue_core.common.expressions.aggregation import Count
from amsdal_glue_core.common.expressions.aggregation import Max
from amsdal_glue_core.common.expressions.aggregation import Min
from amsdal_glue_core.common.expressions.aggregation import Sum
from amsdal_glue_core.common.expressions.raw import RawExpression
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.commands import DataCommand
from amsdal_glue_core.common.operations.commands import LockCommand
from amsdal_glue_core.common.operations.commands import LockSchemaReference
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.commands import TransactionCommand
from amsdal_glue_core.common.operations.mutations.data import DeleteData
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.data import UpdateData
from amsdal_glue_core.common.operations.mutations.schema import AddConstraint
from amsdal_glue_core.common.operations.mutations.schema import AddIndex
from amsdal_glue_core.common.operations.mutations.schema import AddProperty
from amsdal_glue_core.common.operations.mutations.schema import ChangeSchema
from amsdal_glue_core.common.operations.mutations.schema import DeleteConstraint
from amsdal_glue_core.common.operations.mutations.schema import DeleteIndex
from amsdal_glue_core.common.operations.mutations.schema import DeleteProperty
from amsdal_glue_core.common.operations.mutations.schema import DeleteSchema
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.operations.mutations.schema import RenameProperty
from amsdal_glue_core.common.operations.mutations.schema import RenameSchema
from amsdal_glue_core.common.operations.mutations.schema import SchemaMutation
from amsdal_glue_core.common.operations.mutations.schema import UpdateProperty
from amsdal_glue_core.common.operations.queries import DataQueryOperation
from amsdal_glue_core.common.operations.queries import SchemaQueryOperation
from amsdal_glue_core.containers import Container
from amsdal_glue_core.containers import Singleton

from amsdal_glue.connections.connection_manager import DefaultConnectionManager
from amsdal_glue.connections.connection_pool import DefaultConnectionPool
from amsdal_glue.initialize import init_default_containers
from amsdal_glue.interfaces import ConnectionManager
from amsdal_glue.managers.runtime_manager import DefaultRuntimeManager

__all__ = [
    'init_default_containers',
    # DI Container and base class services
    'Container',
    'Singleton',
    # Runtime Manager
    'DefaultRuntimeManager',
    # Connections
    'ConnectionManager',
    'DefaultConnectionManager',
    'DefaultConnectionPool',
    'SqliteConnection',
    'PostgresConnection',
    # Schema data classes
    'Schema',
    'SchemaReference',
    'Version',
    'PropertySchema',
    'PrimaryKeyConstraint',
    'ForeignKeyConstraint',
    'UniqueConstraint',
    'CheckConstraint',
    'IndexSchema',
    # Query statement data classes
    'QueryStatement',
    'SubQueryStatement',
    'FieldReference',
    'FieldReferenceAliased',
    'Field',
    'AnnotationQuery',
    'ValueAnnotation',
    'ExpressionAnnotation',
    'AggregationQuery',
    'Sum',
    'Count',
    'Avg',
    'Min',
    'Max',
    'RawExpression',
    'JoinQuery',
    'JoinType',
    'Conditions',
    'Condition',
    'FilterConnector',
    'FieldLookup',
    'Value',
    'GroupByQuery',
    'OrderByQuery',
    'OrderDirection',
    'LimitQuery',
    # Data classes for schema commands
    'SchemaMutation',
    'SchemaCommand',
    'RegisterSchema',
    'ChangeSchema',
    'DeleteSchema',
    'RenameSchema',
    'AddProperty',
    'DeleteProperty',
    'RenameProperty',
    'UpdateProperty',
    'AddConstraint',
    'DeleteConstraint',
    'AddIndex',
    'DeleteIndex',
    # Data classes for schema queries
    'SchemaQueryOperation',
    # Data classes for data commands
    'DataCommand',
    'InsertData',
    'UpdateData',
    'DeleteData',
    'Data',
    'Metadata',
    # Data classes for data queries
    'DataQueryOperation',
    # Data classes for transaction commands
    'TransactionCommand',
    'TransactionAction',
    # Data classes for lock commands
    'LockCommand',
    'LockAction',
    'LockMode',
    'LockParameter',
    'LockSchemaReference',
    # Results data classes
    'SchemaResult',
    'DataResult',
    'TransactionResult',
    'LockResult',
]
