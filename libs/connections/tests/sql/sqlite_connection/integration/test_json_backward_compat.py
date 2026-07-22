"""Backward compatibility for the TEXT-json -> JSONB migration.

Production databases created under the previous code hold JSON as **spaced** ``json.dumps`` text
(e.g. ``{"ref": {"class_name": "Post"}}`` with a space after every ``:`` and ``,``). The migration
changes *new* writes to minified text and *queries* to the ``jsonb_*`` functions. Because ``jsonb()``
canonicalises whitespace, a value stored the old spaced way still normalises to the same JSONB as a
freshly minified one, so the new query path keeps matching old rows -- **no data migration is needed.**

These tests seed rows the OLD way (spaced ``json.dumps``, bound through a bare ``?`` via
``execute`` -- i.e. exactly what the previous code stored on disk) and then run the NEW query path
against them:

  * whole-column equality  -> ``jsonb(col) = jsonb(?)``
  * the metadata array join -> ``jsonb(object_id) = jsonb_array(CASE WHEN json_valid(x) ...)``

If either stopped matching, the migration would silently break existing apps, so these assertions are
the guard that keeps that from shipping.
"""

import json

from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.join import JoinQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import JoinType
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.jsonb_array import JsonbArray
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection

# A composite-PK reference value, exactly the shape amsdal stores for a foreign key / m2m member.
_POST_REF = {'ref': {'resource': 'sqlite-state', 'class_name': 'Post', 'object_id': 1}}
_TAG_REF = {'ref': {'resource': 'sqlite-state', 'class_name': 'Tag', 'object_id': 2}}


def _spaced(value: object) -> str:
    """The pre-migration on-disk form: default ``json.dumps`` spacing (space after ``:`` and ``,``)."""
    text = json.dumps(value)
    assert ', ' in text or ': ' in text, 'sanity: the fixture must actually be SPACED old-style text'
    return text


def _fref(name: str, table: str) -> FieldReferenceExpression:
    return FieldReferenceExpression(field_reference=FieldReference(field=Field(name=name), table_name=table))


def test_whole_column_equality_matches_old_spaced_row(database_connection: SqliteConnection) -> None:
    """A row stored the OLD spaced way is still found by the NEW ``jsonb(col) = jsonb(?)`` query.

    The migration this test guards is a SPACING change: ``jsonb()`` normalises the pre-migration
    spaced ``json.dumps`` bytes to the same JSONB as a freshly minified param. The Rust port now serialises
    JSON in insertion order (``preserve_order``), so the fixture seeds genuine insertion-order legacy
    bytes (no ``sort_keys``) and still matches.
    """
    database_connection.execute('CREATE TABLE "Doc" ("id" integer, "payload" jsonb)')
    # OLD write: spaced json.dumps text (insertion order) bound through a bare ? -- what the previous
    # code persisted.
    old_spaced = json.dumps(_POST_REF)
    assert ': ' in old_spaced  # sanity: genuinely spaced old-style text
    database_connection.execute('INSERT INTO "Doc" ("id", "payload") VALUES (?, ?)', 1, old_spaced)

    # NEW query path: whole-column equality lowers to jsonb("Doc"."payload") = jsonb(?).
    query = QueryStatement(
        table=SchemaReference(name='Doc', version=Version.LATEST),
        where=Conditions(
            Condition(
                left=_fref('payload', 'Doc'),
                lookup=FieldLookup.EQ,
                right=Value(_POST_REF, output_type=ScalarType.JSONB),
            ),
        ),
    )

    result = list(database_connection.query(query))

    assert [row.data['id'] for row in result] == [1]


def test_metadata_array_join_matches_old_spaced_rows(database_connection: SqliteConnection) -> None:
    """The m2m metadata join finds an OLD spaced ``object_id`` via ``jsonb_array(...)`` unwrapping.

    ``object_id`` holds a spaced JSON *array* of composite-PK references; ``post`` / ``tag`` hold the
    spaced member objects. The join lowers to
    ``jsonb(object_id) = jsonb_array(CASE WHEN json_valid(x) THEN jsonb(x) ELSE x END, ...)``, which
    must still match despite the stored spacing.
    """
    database_connection.execute('CREATE TABLE "Meta" ("object_id" jsonb)')
    database_connection.execute('CREATE TABLE "PostTags" ("post" jsonb, "tag" jsonb)')

    # OLD writes: spaced object_id array + spaced member objects.
    database_connection.execute('INSERT INTO "Meta" ("object_id") VALUES (?)', _spaced([_POST_REF, _TAG_REF]))
    database_connection.execute(
        'INSERT INTO "PostTags" ("post", "tag") VALUES (?, ?)', _spaced(_POST_REF), _spaced(_TAG_REF)
    )
    # A decoy row that must NOT match.
    database_connection.execute(
        'INSERT INTO "PostTags" ("post", "tag") VALUES (?, ?)', _spaced(_TAG_REF), _spaced(_POST_REF)
    )

    query = QueryStatement(
        table=SchemaReference(name='Meta', version=Version.LATEST),
        joins=[
            JoinQuery(
                table=SchemaReference(name='PostTags', version=Version.LATEST),
                on=Conditions(
                    Condition(
                        left=_fref('object_id', 'Meta'),
                        lookup=FieldLookup.EQ,
                        right=JsonbArray(items=[_fref('post', 'PostTags'), _fref('tag', 'PostTags')]),
                    ),
                ),
                join_type=JoinType.INNER,
            ),
        ],
    )

    result = list(database_connection.query(query))

    # Exactly the one correctly-ordered PostTags row joins the single Meta row.
    assert len(result) == 1


def test_reverse_fk_extraction_vs_array_join_matches(database_connection: SqliteConnection) -> None:
    """The composite-PK reverse-FK join: a `->>` extraction compared to a ``jsonb_array``.

    The FK column ``team`` holds a reference ``{"ref": {"object_id": [1, "alpha"]}}``; the join lowers
    to ``jsonb(team->'ref'->>'object_id') = jsonb_array(org_id, team_code)``. The extraction yields the
    array's JSON text, which ``jsonb()`` parses back to the same blob the array builds -- so it must
    match. (Guards the regression where the un-wrapped TEXT extraction never equalled the BLOB array.)
    """
    database_connection.execute('CREATE TABLE "Rel" ("team" jsonb)')
    database_connection.execute('CREATE TABLE "T" ("org_id" integer, "team_code" text)')

    database_connection.execute('INSERT INTO "Rel" ("team") VALUES (?)', _spaced({'ref': {'object_id': [1, 'alpha']}}))
    database_connection.execute('INSERT INTO "T" ("org_id", "team_code") VALUES (?, ?)', 1, 'alpha')
    database_connection.execute('INSERT INTO "T" ("org_id", "team_code") VALUES (?, ?)', 2, 'beta')  # decoy

    team_object_id = FieldReferenceExpression(
        field_reference=FieldReference(
            field=Field(name='team', child=Field(name='ref', child=Field(name='object_id'))),
            table_name='Rel',
        ),
    )

    query = QueryStatement(
        table=SchemaReference(name='Rel', version=Version.LATEST),
        joins=[
            JoinQuery(
                table=SchemaReference(name='T', version=Version.LATEST),
                on=Conditions(
                    Condition(
                        left=team_object_id,
                        lookup=FieldLookup.EQ,
                        right=JsonbArray(items=[_fref('org_id', 'T'), _fref('team_code', 'T')]),
                    ),
                ),
                join_type=JoinType.INNER,
            ),
        ],
    )

    result = list(database_connection.query(query))

    assert len(result) == 1


def test_scalar_pk_array_join_matches_old_row(database_connection: SqliteConnection) -> None:
    """The same join for single-scalar PKs: ``object_id`` is a spaced array of plain strings."""
    database_connection.execute('CREATE TABLE "Meta2" ("object_id" jsonb)')
    database_connection.execute('CREATE TABLE "Rel" ("a" text, "b" text)')

    database_connection.execute('INSERT INTO "Meta2" ("object_id") VALUES (?)', json.dumps(['p-1', 't-1']))
    database_connection.execute('INSERT INTO "Rel" ("a", "b") VALUES (?, ?)', 'p-1', 't-1')

    query = QueryStatement(
        table=SchemaReference(name='Meta2', version=Version.LATEST),
        joins=[
            JoinQuery(
                table=SchemaReference(name='Rel', version=Version.LATEST),
                on=Conditions(
                    Condition(
                        left=_fref('object_id', 'Meta2'),
                        lookup=FieldLookup.EQ,
                        right=JsonbArray(items=[_fref('a', 'Rel'), _fref('b', 'Rel')]),
                    ),
                ),
                join_type=JoinType.INNER,
            ),
        ],
    )

    result = list(database_connection.query(query))

    assert len(result) == 1
