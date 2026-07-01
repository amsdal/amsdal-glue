"""Virtual table registry constants for schema introspection.

These constants define virtual table names that map to database system catalogs
via temporary views. They can be used with ``QueryStatement`` to query schema
metadata through the same SQL generation pipeline as regular data queries.

Available registries
--------------------
- ``TABLE_REGISTRY`` - base tables (columns: ``name``)
- ``TABLE_PROPERTY_REGISTRY`` - columns (``table_name``, ``name``, ``type``, ...)
- ``TABLE_CONSTRAINT_REGISTRY`` - constraints (``table_name``, ``name``, ``type``)
- ``TABLE_INDEX_REGISTRY`` - non-PK indexes (``table_name``, ``name``, ``index_type``, ``is_unique``)
"""

TABLE_REGISTRY = '__table_registry'
TABLE_PROPERTY_REGISTRY = '__property_registry'
TABLE_CONSTRAINT_REGISTRY = '__constraint_registry'
TABLE_INDEX_REGISTRY = '__index_registry'
