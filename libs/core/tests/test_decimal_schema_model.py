from amsdal_glue_core.common.data_models.schema import DecimalSchemaModel


def test_decimal_schema_model_holds_precision_scale() -> None:
    m = DecimalSchemaModel(precision=10, scale=2)
    assert m.precision == 10
    assert m.scale == 2


def test_decimal_schema_model_allows_unconstrained() -> None:
    m = DecimalSchemaModel(precision=None, scale=None)
    assert m.precision is None
    assert m.scale is None
