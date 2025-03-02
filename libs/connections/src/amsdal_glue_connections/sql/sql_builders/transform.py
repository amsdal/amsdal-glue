from collections.abc import Callable
from enum import Enum
from functools import partial
from typing import Any
from typing import ClassVar


class TransformTypes(Enum):
    TABLE_SEPARATOR = 'table_separator'
    TABLE_QUOTE = 'table_quote'
    FIELD_QUOTE = 'field_quote'
    NESTED_FIELD = 'nested_field'
    VALUE_PLACEHOLDER = 'value_placeholder'
    VALUE = 'value'
    MATH_OPERATOR = 'math_operator'
    OPERATOR_CONSTRUCTOR = 'operator_constructor'
    BUILD_ONLY = 'build_only'
    NULL_VALUE = 'null_value'
    VALUE_TYPE = 'value_type'
    CAST = 'cast'
    FUNC = 'func'


class Transform:
    @staticmethod
    def str_wrapper(quote: str, value: str) -> str:
        if not value:
            return value
        return f'{quote}{value}{quote}'

    @staticmethod
    def str_joiner(separator: str, *values: str) -> str:
        return separator.join(filter(None, values))

    _registry: ClassVar[dict[Any, Callable]] = {
        TransformTypes.TABLE_SEPARATOR: partial(str_joiner, '.'),
        TransformTypes.TABLE_QUOTE: partial(str_wrapper, "'"),
        TransformTypes.FIELD_QUOTE: partial(str_wrapper, "'"),
        TransformTypes.NULL_VALUE: lambda: 'NULL',
    }

    def __init__(self) -> None:
        from amsdal_glue_connections.sql.sql_builders.build_only_constructor import default_build_only
        from amsdal_glue_connections.sql.sql_builders.math_operator_transform import default_math_operator_transform
        from amsdal_glue_connections.sql.sql_builders.nested_field_transform import default_nested_field_transform
        from amsdal_glue_connections.sql.sql_builders.operator_constructor import default_operator_constructor

        self._registry = self._registry.copy()  # type: ignore[misc]
        self._registry[TransformTypes.MATH_OPERATOR] = default_math_operator_transform
        self._registry[TransformTypes.NESTED_FIELD] = default_nested_field_transform
        self._registry[TransformTypes.BUILD_ONLY] = default_build_only
        self._registry[TransformTypes.OPERATOR_CONSTRUCTOR] = default_operator_constructor

    def register(self, target_type: Any, func: Callable) -> None:
        self._registry[target_type] = func

    def apply(self, target_type: Any, *args, **kwargs) -> Any:
        return self._registry[target_type](*args, **kwargs)

    def resolve(self, target_type: Any) -> Callable:
        return self._registry[target_type]

    def __copy__(self) -> 'Transform':
        _transform = Transform()
        _transform._registry = self._registry.copy()  # type: ignore[misc]

        return _transform
