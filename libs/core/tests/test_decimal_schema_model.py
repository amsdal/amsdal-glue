from amsdal_glue_core.common.data_models.types import CustomType


def test_custom_type_holds_precision_scale() -> None:
    m = CustomType(name='numeric', params={'precision': 10, 'scale': 2})
    assert m.params is not None
    assert m.params['precision'] == 10
    assert m.params['scale'] == 2


def test_custom_type_allows_no_params() -> None:
    m = CustomType(name='numeric', params=None)
    assert m.params is None
