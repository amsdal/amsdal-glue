from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression

from amsdal_glue import CheckConstraint
from amsdal_glue import Condition
from amsdal_glue import Conditions
from amsdal_glue import Field
from amsdal_glue import FieldLookup
from amsdal_glue import FieldReference
from amsdal_glue import IndexSchema
from amsdal_glue import PrimaryKeyConstraint
from amsdal_glue import PropertySchema
from amsdal_glue import Schema
from amsdal_glue import UniqueConstraint
from amsdal_glue import Value
from amsdal_glue import Version

user_schema = Schema(
    name='user',
    version=Version.LATEST,
    properties=[
        PropertySchema(
            name='id',
            type=int,
            required=True,
        ),
        PropertySchema(
            name='email',
            type=str,
            required=True,
        ),
        PropertySchema(
            name='age',
            type=int,
            required=True,
        ),
        PropertySchema(
            name='first_name',
            type=str,
            required=False,
        ),
        PropertySchema(
            name='last_name',
            type=str,
            required=False,
        ),
    ],
    constraints=[
        PrimaryKeyConstraint(name='pk_user', fields=['id']),
        UniqueConstraint(name='uk_user_email', fields=['email'], condition=None),
        CheckConstraint(
            name='ck_user_age',
            condition=Conditions(
                Condition(
                    left=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='age'), table_name='user')
                    ),
                    lookup=FieldLookup.GT,
                    right=Value(value=18),
                ),
            ),
        ),
    ],
    indexes=[
        IndexSchema(name='idx_user_email', fields=['first_name', 'last_name']),
    ],
)
