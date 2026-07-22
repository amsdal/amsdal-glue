"""Fixture-driven unit tests for `SchemaAssemblyMixin` -- no DB connection involved."""

from amsdal_glue_connections.sql.connections.base_view_introspection import SchemaAssemblyMixin


def test_assemble_indexes_from_rows():
    rows = [
        {
            'table_name': 't',
            'name': 'ix',
            'is_unique': 0,
            'column_name': 'a',
            'ordinal_position': 0,
            'is_descending': 0,
            'index_type': 'btree',
        },
        {
            'table_name': 't',
            'name': 'ix',
            'is_unique': 0,
            'column_name': 'b',
            'ordinal_position': 1,
            'is_descending': 1,
            'index_type': 'btree',
        },
    ]
    idxs = SchemaAssemblyMixin()._assemble_indexes(rows)  # noqa: SLF001
    assert len(idxs) == 1
    assert [f.name for f in idxs[0].fields] == ['a', 'b']
    assert idxs[0].fields[1].direction.name == 'DESC'
