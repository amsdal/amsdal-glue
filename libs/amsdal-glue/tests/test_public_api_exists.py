"""Public API: `Exists` must be importable from the top-level package."""


def test_exists_is_in_public_namespace() -> None:
    import amsdal_glue

    assert hasattr(amsdal_glue, 'Exists'), 'Exists missing from amsdal_glue public namespace'


def test_exists_importable_from_top_level() -> None:
    from amsdal_glue import Exists  # noqa: F401


def test_exists_in_dunder_all() -> None:
    import amsdal_glue

    assert 'Exists' in amsdal_glue.__all__
