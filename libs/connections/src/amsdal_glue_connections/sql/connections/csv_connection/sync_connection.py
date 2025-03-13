import logging
import uuid
from collections.abc import Callable
from pathlib import Path
from typing import Any
from typing import TYPE_CHECKING

from amsdal_glue_core.commands.lock_command_node import ExecutionLockCommand
from amsdal_glue_core.common.data_models.annotation import AnnotationQuery
from amsdal_glue_core.common.data_models.annotation import ExpressionAnnotation
from amsdal_glue_core.common.data_models.annotation import ValueAnnotation
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions import aggregation as aggr_expr
from amsdal_glue_core.common.expressions.aggregation import AggregationExpression
from amsdal_glue_core.common.expressions.expression import Expression
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.interfaces.connection import ConnectionBase
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.commands import TransactionCommand
from amsdal_glue_core.common.operations.mutations.data import DataMutation
from amsdal_glue_core.common.operations.mutations.data import DeleteData
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.data import UpdateData
from amsdal_glue_core.common.operations.mutations.schema import DeleteSchema
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.operations.mutations.schema import RenameSchema

if TYPE_CHECKING:
    import pandas as pd

logger = logging.getLogger(__name__)


class CsvConnection(ConnectionBase):
    def __init__(self) -> None:
        super().__init__()
        self._db_path: Path | None = None
        self._transaction_id: str | None = None
        self._backup_dfs: dict[str, pd.DataFrame] = {}
        self._column_mapping_by_table: dict[tuple[str, str], str] = {}

    def connect(self, db_path: Path, **kwargs: Any) -> None:  # noqa: ARG002, C901
        """Connect to a CSV file or directory of CSV files."""
        try:
            import pandas as pd
        except ImportError:
            _msg = (
                '"pandas" package is required for CsvConnection. '
                'Use "pip install amsdal-glue-connections[csv]" to install it.'
            )
            raise ImportError(_msg) from None

        db_path = Path(db_path)
        self._db_path = db_path

        if not db_path.exists():
            msg = f'File or directory not found: {db_path}'
            raise FileNotFoundError(msg)

        if db_path.is_file() and db_path.suffix.lower() != '.csv':
            msg = f'File is not a CSV file: {db_path}'
            raise ValueError(msg)

        if db_path.is_file():
            try:
                pd.read_csv(db_path)
            except Exception as e:
                msg = f'Failed to read CSV file: {db_path}. Error: {e!s}'
                raise ValueError(msg) from e

        elif db_path.is_dir():
            csv_files = []
            for file in db_path.iterdir():
                if file.is_file() and file.suffix.lower() == '.csv':
                    csv_files.append(file)
                    try:
                        pd.read_csv(file)
                    except Exception as e:
                        msg = f'Failed to read CSV file: {file}. Error: {e!s}'
                        raise ValueError(msg) from e

            if not csv_files:
                msg = f'No CSV files found in directory: {db_path}'
                logger.warning(msg)

    @property
    def db_path(self) -> Path:
        if self._db_path is None:
            msg = 'Connection not established. Call connect() first.'
            raise RuntimeError(msg)
        return self._db_path

    def acquire_lock(self, lock: ExecutionLockCommand) -> None:  # noqa: ARG002
        """Acquire a lock for the execution. Not applicable for CSV connections."""
        return

    def begin_transaction(self, transaction: TransactionCommand | str | None = None) -> Any:
        """Begin a transaction by creating a backup of the current dataframes."""
        if transaction is None:
            self._transaction_id = str(uuid.uuid4())
        else:
            self._transaction_id = transaction if isinstance(transaction, str) else transaction.transaction_id

        # Backup all dataframes for rollback if needed
        self._backup_dfs.clear()

        if self.db_path.is_file():
            import pandas as pd

            self._backup_dfs[self.db_path.stem] = pd.read_csv(self.db_path)
        elif self.db_path.is_dir():
            import pandas as pd

            for file in self.db_path.iterdir():
                if file.is_file() and file.suffix == '.csv':
                    self._backup_dfs[file.stem] = pd.read_csv(file)

        return self._transaction_id

    def commit_transaction(self, transaction: TransactionCommand | str | None = None) -> Any:  # noqa: ARG002
        """Commit a transaction by clearing the backup dataframes."""
        # Clear backups as we want to commit changes
        self._backup_dfs.clear()
        self._transaction_id = None
        return None

    def disconnect(self) -> None:
        """Disconnect from the CSV file(s)."""
        self._db_path = None
        self._backup_dfs.clear()
        self._transaction_id = None

    @property
    def is_alive(self) -> bool:
        """Check if the connection is alive."""
        return self._db_path is not None

    @property
    def is_connected(self) -> bool:
        """Check if the connection is established."""
        return self._db_path is not None

    @property
    def queries(self) -> list[str]:
        """Return the list of executed queries (not applicable for CSV)."""
        return []

    def query(self, query: QueryStatement) -> list[Data]:  # noqa: C901, PLR0912, PLR0915
        """Execute a query on the CSV data."""
        import pandas as pd

        try:
            # Reset column mapping
            self._column_mapping_by_table = {}

            if not isinstance(query.table, SchemaReference):
                msg = 'Only SchemaReference is supported for CSV connections'
                raise ValueError(msg)  # noqa: TRY004, TRY301

            # Get the main table data
            table_name = query.table.name
            df = self._get_df(table_name)

            # Handle JOINs
            if query.joins:
                for join in query.joins:
                    if not isinstance(join.table, SchemaReference):
                        msg = 'Only SchemaReference is supported for CSV connections'
                        raise ValueError(msg)  # noqa: TRY004, TRY301
                    join_table_name = join.table.name
                    join_table_alias = join.table.alias or join_table_name

                    try:
                        # Get the joined table data
                        joined_df = self._get_df(join_table_name)

                        # Process join conditions
                        left_on, right_on = [], []

                        for condition in join.on.children:
                            if (
                                isinstance(condition, Condition)
                                and isinstance(condition.left, FieldReferenceExpression)
                                and isinstance(condition.right, FieldReferenceExpression)
                            ):
                                left_field = condition.left.field_reference.field.name
                                left_table = condition.left.field_reference.table_name or table_name

                                right_field = condition.right.field_reference.field.name

                                if left_table in (join_table_name, join_table_alias):
                                    # Swap if left condition references the right table
                                    left_on.append(right_field)
                                    right_on.append(left_field)
                                else:
                                    left_on.append(left_field)
                                    right_on.append(right_field)

                        # Perform the join
                        df = pd.merge(
                            df,
                            joined_df,
                            how=join.join_type.value.lower(),
                            left_on=left_on,
                            right_on=right_on,
                            suffixes=(f'_{table_name}', f'_{join_table_name}'),
                        )

                        # Store original column names for later use
                        for col in df.columns:
                            if col.endswith(f'_{join_table_name}'):
                                base_col = col[: -(len(f'_{join_table_name}'))]
                                self._column_mapping_by_table[(join_table_name, base_col)] = col
                            elif col.endswith(f'_{table_name}'):
                                base_col = col[: -(len(f'_{table_name}'))]
                                self._column_mapping_by_table[(table_name, base_col)] = col
                    except Exception as e:
                        msg = f'Failed to join table {join_table_name}: {e!s}'
                        raise ValueError(msg) from e

            # Handle WHERE conditions
            if query.where:
                try:
                    condition_mask = self._get_conditions(query.where, df)
                    df = df[condition_mask]
                except Exception as e:
                    msg = f'Failed to apply WHERE conditions: {e!s}'
                    raise ValueError(msg) from e

            # Handle GROUP BY and aggregations
            result_df = df.copy()

            if query.group_by and query.aggregations:
                # Group by specified columns
                try:
                    # Get the full column names for group by fields
                    group_by_columns = []
                    table_field_mapping = {}  # Maps original field reference to actual column name

                    for group_by in query.group_by:
                        field_name = group_by.field.field.name
                        table_name = group_by.field.table_name

                        # Find the actual column name in the DataFrame
                        actual_column = self._find_column_for_field(df, field_name, table_name)

                        if actual_column is None:
                            msg = f"Group by column '{field_name}' from table '{table_name}' not found in {df.columns}"
                            raise ValueError(msg)  # noqa: TRY301

                        group_by_columns.append(actual_column)
                        # Store mapping for later column renaming
                        key = f'{table_name}.{field_name}' if table_name else field_name
                        table_field_mapping[key] = actual_column

                    # Group the data
                    grouped = df.groupby(group_by_columns, as_index=False)

                    # Apply aggregations
                    agg_dict = {}
                    for agg in query.aggregations:
                        field_name = agg.expression.field.field.name
                        table_name = agg.expression.field.table_name

                        # Find the actual column name in the DataFrame
                        actual_field_name = self._find_column_for_field(df, field_name, table_name)

                        if actual_field_name is None:
                            msg = (
                                f"Aggregation column '{field_name}' from table '{table_name}' not found in {df.columns}"
                            )
                            raise ValueError(msg)  # noqa: TRY301

                        agg_type = self._get_aggregation_type(agg.expression)
                        agg_dict[actual_field_name] = agg_type

                    # Create DataFrame with aggregations
                    result_df = grouped.agg(agg_dict)

                    # Rename columns for aliases after aggregation
                    column_renames = {}

                    # First handle aggregation aliases
                    for agg in query.aggregations:
                        field_name = agg.expression.field.field.name
                        table_name = agg.expression.field.table_name

                        # Find the actual column name that was aggregated
                        for col in agg_dict:
                            # Match the aggregated column to its alias
                            if agg.alias and (col.endswith(f'_{field_name}') or col == field_name):
                                column_renames[col] = agg.alias
                                break

                    # Then handle table prefix removals for group by fields
                    for table_field, actual_column in table_field_mapping.items():
                        field_name = table_field.split('.')[-1]  # Get just the field name part
                        # Only rename if not already handled by aggregation aliases and if different
                        if actual_column != field_name and actual_column not in column_renames:
                            column_renames[actual_column] = field_name

                    if column_renames:
                        result_df = result_df.rename(columns=column_renames)
                except Exception as e:
                    msg = f'Failed to apply GROUP BY and aggregations: {e!s}'
                    raise ValueError(msg) from e

            elif query.aggregations and not query.group_by:
                # Apply aggregations without grouping
                try:
                    agg_results = {}
                    for agg in query.aggregations:
                        field_name = agg.expression.field.field.name
                        table_name = agg.expression.field.table_name
                        alias = agg.alias if agg.alias else field_name

                        # Find the actual column name in the DataFrame
                        actual_field_name = self._find_column_for_field(df, field_name, table_name)

                        if actual_field_name is None:
                            msg = (
                                f"Aggregation column '{field_name}' from table '{table_name}' not found in {df.columns}"
                            )
                            raise ValueError(msg)  # noqa: TRY301

                        agg_func = self._get_aggregation_function(agg.expression)
                        agg_results[alias] = agg_func(df[actual_field_name])

                    result_df = pd.DataFrame([agg_results])
                except Exception as e:
                    msg = f'Failed to apply aggregations: {e!s}'
                    raise ValueError(msg) from e

            # Handle SELECT fields
            if query.only:
                try:
                    selected_columns = []
                    column_aliases = {}

                    for field in query.only:
                        field_name = field.field.name
                        table_name = field.table_name

                        # Find the actual column name in the DataFrame
                        actual_col: str | None = self._find_column_for_field(result_df, field_name, table_name)

                        if actual_col:
                            selected_columns.append(actual_col)
                            # If the column has a prefix or suffix, rename it back to the plain field name
                            if actual_col != field_name:
                                column_aliases[actual_col] = field_name
                        else:
                            msg = f"Column '{field_name}' from table '{table_name}' not found - skipping"
                            logger.warning(msg)

                    # Make sure to include any aggregation columns that might be needed
                    if query.aggregations:
                        for agg in query.aggregations:
                            if agg.alias and agg.alias in result_df.columns and agg.alias not in selected_columns:
                                selected_columns.append(agg.alias)

                    # Filter columns to only those requested
                    if selected_columns:
                        available_columns = set(result_df.columns)
                        actual_columns = [col for col in selected_columns if col in available_columns]
                        result_df = result_df[actual_columns]

                        # Rename columns to remove table prefixes if needed
                        result_df = result_df.rename(columns=column_aliases)
                except Exception as e:
                    msg = f'Failed to select columns: {e!s}'
                    raise ValueError(msg) from e

            # Handle DISTINCT
            if query.distinct:
                try:
                    if isinstance(query.distinct, list):
                        distinct_columns = []
                        for field in query.distinct:
                            field_name = field.field.name
                            table_name = field.table_name

                            # Find the actual column name in the DataFrame
                            actual_col = self._find_column_for_field(result_df, field_name, table_name)
                            if actual_col:
                                distinct_columns.append(actual_col)

                        if distinct_columns:
                            result_df = result_df.drop_duplicates(subset=distinct_columns)
                        else:
                            result_df = result_df.drop_duplicates()
                    else:
                        result_df = result_df.drop_duplicates()
                except Exception as e:
                    msg = f'Failed to apply DISTINCT: {e!s}'
                    raise ValueError(msg) from e

            # Handle ORDER BY
            if query.order_by:
                try:
                    sort_columns = []
                    ascending = []

                    for order in query.order_by:
                        field_name = order.field.field.name
                        table_name = order.field.table_name

                        # Find the actual column name in the DataFrame
                        actual_col = self._find_column_for_field(result_df, field_name, table_name)

                        if actual_col:
                            sort_columns.append(actual_col)
                            ascending.append(order.direction.value == 'ASC')
                        else:
                            msg = f"Order by column '{field_name}' from table '{table_name}' not found - skipping"
                            logger.warning(msg)

                    if sort_columns:
                        result_df = result_df.sort_values(by=sort_columns, ascending=ascending)
                except Exception as e:
                    msg = f'Failed to apply ORDER BY: {e!s}'
                    raise ValueError(msg) from e

            # Handle annotations
            if query.annotations:
                for annotation in query.annotations:
                    try:
                        result_df = self._process_annotation(annotation, result_df)
                    except Exception as e:  # noqa: PERF203
                        msg = f'Failed to apply annotation: {e!s}'
                        raise ValueError(msg) from e

            # Handle LimitQuery.limit and LimitQuery.offset
            if query.limit:
                try:
                    limit = query.limit.limit
                    offset = query.limit.offset
                    result_df = result_df.iloc[offset : offset + limit]
                except Exception as e:
                    msg = f'Failed to apply LIMIT and OFFSET: {e!s}'
                    raise ValueError(msg) from e

            # Convert result to list of Data objects
            if isinstance(result_df, pd.Series):
                return [Data(data=result_df.to_dict())]

            return [Data(data=row.to_dict()) for _, row in result_df.iterrows()]

        except Exception as e:
            msg = f'Error executing query: {e!s}'
            logger.exception(msg)
            raise

    def _find_column_for_field(self, df: 'pd.DataFrame', field_name: str, table_name: str | None = None) -> str | None:  # noqa: C901, PLR0911
        """Find the actual column name in a DataFrame for a given field and table."""
        if field_name == '*':
            return next(iter(df.columns), None)

        # First, check if we have an exact match
        if field_name in df.columns:
            return field_name

        # Check if we have a mapped column for this table and field
        if table_name and (table_name, field_name) in self._column_mapping_by_table:
            mapped_col = self._column_mapping_by_table[(table_name, field_name)]
            if mapped_col in df.columns:
                return mapped_col

        # Try table-specific patterns
        if table_name:
            # Try common suffix patterns
            for pattern in [f'{field_name}_{table_name}', f'{table_name}_{field_name}', f'{field_name}']:
                if pattern in df.columns:
                    return pattern

        # Look for columns with suffixes containing our field
        for col in df.columns:
            # Check for column ending with our field name (after an underscore)
            if col.endswith(f'_{field_name}'):
                return col
            # Check for column starting with our field name (before an underscore)
            if col.startswith(f'{field_name}_'):
                return col

        # If we get here, we couldn't find a match
        return None

    def _get_aggregation_type(self, expr: Expression | AggregationExpression) -> str:
        """Get the aggregation type for a pandas groupby operation."""
        if isinstance(expr, aggr_expr.Sum):
            return 'sum'
        if isinstance(expr, aggr_expr.Count):
            return 'count'
        if isinstance(expr, aggr_expr.Avg):
            return 'mean'
        if isinstance(expr, aggr_expr.Min):
            return 'min'
        if isinstance(expr, aggr_expr.Max):
            return 'max'

        msg = f'Unsupported aggregation type: {type(expr)}'
        raise ValueError(msg)

    def _get_aggregation_function(self, expr: Expression | AggregationExpression) -> Callable:
        """Get the aggregation function for a pandas Series operation."""

        if isinstance(expr, aggr_expr.Sum):
            return lambda x: x.sum()
        if isinstance(expr, aggr_expr.Count):
            return lambda x: x.count()
        if isinstance(expr, aggr_expr.Avg):
            return lambda x: x.mean()
        if isinstance(expr, aggr_expr.Min):
            return lambda x: x.min()
        if isinstance(expr, aggr_expr.Max):
            return lambda x: x.max()

        msg = f'Unsupported aggregation type: {type(expr)}'
        raise ValueError(msg)

    def _process_annotation(self, annotation: AnnotationQuery, df: 'pd.DataFrame') -> 'pd.DataFrame':
        """Process an annotation and add it to the DataFrame."""
        if isinstance(annotation.value, SubQueryStatement):
            # For each row in the main DataFrame, run the subquery with the appropriate filter
            result_column = []
            for _, row in df.iterrows():
                # Modify the subquery to use the current row's values
                subquery = self._prepare_subquery_for_row(annotation.value.query, row)

                # Execute the subquery
                subquery_result = self.query(subquery)

                # Extract the result value
                if subquery_result and len(subquery_result) > 0:
                    # Use the first result and extract the alias value
                    alias = annotation.value.alias
                    if alias in subquery_result[0].data:
                        result_column.append(subquery_result[0].data[alias])
                    else:
                        # Try to get first column value if alias not found
                        first_key = next(iter(subquery_result[0].data.keys()), None)
                        if first_key:
                            result_column.append(subquery_result[0].data[first_key])
                        else:
                            result_column.append(None)
                else:
                    result_column.append(None)

            # Add the result column to the DataFrame
            df[annotation.value.alias] = result_column

        elif isinstance(annotation.value, ValueAnnotation):
            df[annotation.value.alias] = annotation.value.value

        elif isinstance(annotation.value, ExpressionAnnotation):
            df[annotation.value.alias] = self._process_expression(annotation.value.expression, df)

        return df

    def _prepare_subquery_for_row(self, query: QueryStatement, row: 'pd.Series') -> QueryStatement:
        """Prepare a subquery for execution with values from the current row."""
        import copy

        # Create a deep copy of the query to avoid modifying the original
        modified_query = copy.deepcopy(query)

        # If there are conditions, update field references to use current row values
        if modified_query.where:
            self._update_conditions_with_row_values(modified_query.where, row)

        return modified_query

    def _update_conditions_with_row_values(self, conditions: Conditions, row: 'pd.Series') -> None:
        """Update conditions to use values from the current row."""
        for i, condition in enumerate(conditions.children):
            if isinstance(condition, Conditions):
                self._update_conditions_with_row_values(condition, row)
            # Check if right side is a field reference that needs to be replaced with a value
            elif isinstance(condition.right, FieldReferenceExpression):
                field_name = condition.right.field_reference.field.name

                # If this is a reference to the outer query row
                if field_name in row:
                    # Replace with a Value expression
                    from amsdal_glue_core.common.expressions.value import Value

                    # Create a new condition with the same properties but with a Value instead of
                    # FieldReferenceExpression
                    new_condition = Condition(
                        left=condition.left, lookup=condition.lookup, right=Value(row[field_name])
                    )

                    # Replace the old condition with the new one
                    conditions.children[i] = new_condition

    def _process_expression(self, expression: Expression, df: 'pd.DataFrame') -> Any:
        """Process an expression and return its value."""
        if isinstance(expression, FieldReferenceExpression):
            return df[expression.field_reference.field.name]

        if isinstance(expression, Value):
            return expression.value

        msg = f'Unsupported expression type: {type(expression)}'
        raise ValueError(msg)

    def _process_on(self, conditions: Conditions, *, left_on: bool) -> list[str]:
        """Process JOIN ON conditions and return the field names."""
        on = []
        for condition in conditions.children:
            if isinstance(condition, Conditions):
                on.extend(self._process_on(condition, left_on=left_on))
                continue

            if left_on:
                if isinstance(condition.left, FieldReferenceExpression):
                    on.append(condition.left.field_reference.field.name)
            elif isinstance(condition.right, FieldReferenceExpression):
                on.append(condition.right.field_reference.field.name)

        return on

    def query_schema(self, filters: Conditions | None = None) -> list[Schema]:
        """Query the schema of the CSV file(s)."""
        if not self.db_path.exists():
            msg = f'File not found: {self.db_path}'
            raise FileNotFoundError(msg)

        if self.db_path.is_file():
            return [self._file_path_to_schema(self.db_path)]

        schemas = []
        for file in self.db_path.iterdir():
            if file.is_file() and file.suffix.lower() == '.csv':
                try:
                    schema = self._file_path_to_schema(file)

                    # Apply filters if provided
                    if filters is None or self._schema_matches_filters(schema, filters):
                        schemas.append(schema)
                except Exception as e:  # noqa: BLE001
                    msg = f'Failed to get schema for {file}: {e!s}'
                    logger.warning(msg)

        return schemas

    def _schema_matches_filters(self, schema: Schema, filters: Conditions) -> bool:
        """Check if a schema matches the given filters."""
        # Basic implementation - can be expanded based on requirements
        for condition in filters.children:
            if isinstance(condition, Condition) and condition.lookup == 'EQ':
                if not isinstance(condition.left, FieldReferenceExpression):
                    msg = 'Only FieldReferenceExpression is supported for schema filters'
                    raise ValueError(msg)

                if not isinstance(condition.right, Value):
                    msg = 'Only Value is supported for schema filters'
                    raise ValueError(msg)

                if condition.left.field_reference.field.name == 'name':
                    return schema.name == condition.right.value
        return True

    def _file_path_to_schema(self, file_path: Path) -> Schema:
        """Convert a CSV file path to a Schema object."""
        import pandas as pd

        try:
            df = pd.read_csv(file_path)
            schema_name = file_path.stem

            # Get properties from DataFrame columns
            properties = []
            for col in df.columns:
                col_type = self._type_to_glue_type(df[col].dtype)
                properties.append(PropertySchema(name=col, type=col_type, required=False))

            return Schema(
                name=schema_name,
                version=Version.LATEST,
                properties=properties,
            )
        except Exception as e:
            msg = f'Failed to create schema from {file_path}: {e!s}'
            raise ValueError(msg) from e

    def _type_to_glue_type(self, type_: Any) -> Any:
        """Convert pandas data types to Python types."""
        import pandas as pd

        # Handle different pandas/numpy data types
        if pd.api.types.is_integer_dtype(type_):
            return int
        if pd.api.types.is_float_dtype(type_):
            return float
        if pd.api.types.is_bool_dtype(type_):
            return bool
        if pd.api.types.is_datetime64_dtype(type_):
            return pd.Timestamp
        if pd.api.types.is_string_dtype(type_) or pd.api.types.is_object_dtype(type_):
            return str

        # Default fallback
        return str

    def release_lock(self, lock: ExecutionLockCommand) -> Any:  # noqa: ARG002
        """Release a lock. Not applicable for CSV connections."""
        return None

    def revert_transaction(self, transaction: TransactionCommand | str | None = None) -> Any:
        """Revert a transaction (alias for rollback)."""
        return self.rollback_transaction(transaction)

    def rollback_transaction(self, transaction: TransactionCommand | str | None = None) -> Any:  # noqa: ARG002
        """Rollback a transaction by restoring the backup dataframes."""
        if not self._backup_dfs:
            logger.warning('No transaction to rollback')
            return None

        # Restore all backed up dataframes
        for schema_name, df in self._backup_dfs.items():
            self._save_df(df, schema_name)

        # Clear backups
        self._backup_dfs.clear()
        self._transaction_id = None

        return None

    def run_mutations(self, mutations: list[DataMutation]) -> list[list[Data] | None]:
        """Run data mutations (insert, update, delete)."""
        results: list[list[Data] | None] = []

        for mutation in mutations:
            try:
                if isinstance(mutation, InsertData):
                    self._run_insert_data(mutation)
                    results.append(None)  # No return data for inserts

                elif isinstance(mutation, UpdateData):
                    self._run_update_data(mutation)
                    results.append(None)  # No return data for updates

                elif isinstance(mutation, DeleteData):
                    self._run_delete_data(mutation)
                    results.append(None)  # No return data for deletes

                else:
                    msg = f'Unsupported mutation type: {type(mutation)}'
                    raise ValueError(msg)  # noqa: TRY004, TRY301

            except Exception as e:  # noqa: PERF203
                msg = f'Error executing mutation: {e!s}'
                logger.exception(msg)
                raise

        return results

    def _run_insert_data(self, mutation: InsertData) -> None:
        """Insert data into a CSV file."""
        import pandas as pd

        try:
            # Get existing data
            try:
                df = self._get_df(mutation.schema.name)
            except FileNotFoundError as e:
                msg = f'Failed to insert data: {e!s}'
                raise ValueError(msg) from e

            # Append new data
            if mutation.data:
                new_data = pd.DataFrame([data.data for data in mutation.data])

                # Ensure all required columns exist
                for col in df.columns:
                    if col not in new_data.columns:
                        new_data[col] = None

                # Concatenate with existing data
                df = pd.concat([df, new_data], ignore_index=True)

            # Save the updated DataFrame
            self._save_df(df, mutation.schema.name)

        except Exception as e:
            msg = f'Failed to insert data: {e!s}'
            raise ValueError(msg) from e

    def run_schema_command(self, command: SchemaCommand) -> list[Schema | None]:
        """Run schema commands (register, rename, delete schema)."""
        results: list[Schema | None] = []

        for mutation in command.mutations:
            try:
                if isinstance(mutation, RegisterSchema):
                    self._register_schema(mutation)
                    results.append(mutation.schema)

                elif isinstance(mutation, RenameSchema):
                    self._rename_schema(mutation)
                    results.append(None)

                elif isinstance(mutation, DeleteSchema):
                    self._delete_schema(mutation)
                    results.append(None)

                else:
                    msg = f'Unsupported schema mutation: {type(mutation)}'
                    logger.warning(msg)
                    results.append(None)

            except Exception as e:  # noqa: PERF203
                msg = f'Error executing schema command: {e!s}'
                logger.exception(msg)
                raise

        return results

    def _register_schema(self, mutation: RegisterSchema) -> None:
        """Register a new schema by creating a CSV file."""
        import pandas as pd

        schema_name = mutation.get_schema_name()
        file_path = self.db_path / f'{schema_name}.csv'

        if file_path.exists():
            msg = f'File already exists: {file_path}'
            raise FileExistsError(msg)

        try:
            # Create DataFrame with columns from schema properties
            columns = [prop.name for prop in mutation.schema.properties]
            df = pd.DataFrame(columns=columns)

            # Ensure parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Save empty DataFrame as CSV
            df.to_csv(file_path, index=False)

        except Exception as e:
            msg = f"Failed to register schema '{schema_name}': {e!s}"
            raise ValueError(msg) from e

    def _rename_schema(self, mutation: RenameSchema) -> None:
        """Rename a schema by renaming the CSV file."""
        old_schema_name = mutation.get_schema_name()
        new_schema_name = mutation.new_schema_name

        old_file_path = self.db_path / f'{old_schema_name}.csv'
        new_file_path = self.db_path / f'{new_schema_name}.csv'

        if not old_file_path.exists():
            msg = f'File not found: {old_file_path}'
            raise FileNotFoundError(msg)

        if new_file_path.exists():
            msg = f'File already exists: {new_file_path}'
            raise FileExistsError(msg)

        try:
            # Ensure parent directory exists
            new_file_path.parent.mkdir(parents=True, exist_ok=True)

            # Rename the file
            old_file_path.rename(new_file_path)

        except Exception as e:
            msg = f"Failed to rename schema from '{old_schema_name}' to '{new_schema_name}': {e!s}"
            raise ValueError(msg) from e

    def _delete_schema(self, mutation: DeleteSchema) -> None:
        """Delete a schema by deleting the CSV file."""
        schema_name = mutation.get_schema_name()
        file_path = self.db_path / f'{schema_name}.csv'

        if not file_path.exists():
            msg = f'File not found: {file_path}'
            raise FileNotFoundError(msg)

        try:
            # Delete the file
            file_path.unlink()
        except Exception as e:
            msg = f"Failed to delete schema '{schema_name}': {e!s}"
            raise ValueError(msg) from e

    def _get_df(self, schema_name: str) -> 'pd.DataFrame':
        """Get a DataFrame from a CSV file."""
        import pandas as pd

        try:
            if self.db_path.is_file():
                return pd.read_csv(self.db_path)

            file_path = self.db_path / f'{schema_name}.csv'
            if not file_path.exists():
                msg = f'CSV file not found: {file_path}'
                raise FileNotFoundError(msg)  # noqa: TRY301

            return pd.read_csv(file_path)

        except Exception as e:
            if isinstance(e, FileNotFoundError):
                raise

            msg = f"Failed to read CSV file for schema '{schema_name}': {e!s}"
            raise ValueError(msg) from e

    def _save_df(self, df: 'pd.DataFrame', schema_name: str) -> None:
        """Save a DataFrame to a CSV file."""
        try:
            if self.db_path.is_file():
                df.to_csv(self.db_path, index=False)
                return

            file_path = self.db_path / f'{schema_name}.csv'
            file_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(file_path, index=False)

        except Exception as e:
            msg = f"Failed to save CSV file for schema '{schema_name}': {e!s}"
            raise ValueError(msg) from e

    def _process_condition(self, condition: Condition, df: 'pd.DataFrame') -> 'pd.Series':  # noqa: C901, PLR0911, PLR0912
        """Process a single condition and return a Boolean mask."""
        import pandas as pd

        try:
            if isinstance(condition.left, FieldReferenceExpression):
                field_name = condition.left.field_reference.field.name
                table_name = condition.left.field_reference.table_name

                # Find the actual field name in the dataframe
                actual_field = self._find_column_for_field(df, field_name, table_name)

                if actual_field is None:
                    msg = f"Field '{field_name}' from table '{table_name}' not found in dataframe columns"
                    raise ValueError(msg)  # noqa: TRY301

                field = actual_field
                # Handle different lookup types
                lookup = condition.lookup

                if isinstance(condition.right, Value):
                    value = condition.right.value

                    if lookup == 'EQ':
                        return df[field] == value
                    if lookup == 'NE':
                        return df[field] != value
                    if lookup == 'GT':
                        return df[field] > value
                    if lookup == 'GE':
                        return df[field] >= value
                    if lookup == 'LT':
                        return df[field] < value
                    if lookup == 'LE':
                        return df[field] <= value
                    if lookup == 'IN':
                        return df[field].isin(value if isinstance(value, list) else [value])
                    if lookup == 'NOT_IN':
                        return ~df[field].isin(value if isinstance(value, list) else [value])
                    if lookup == 'LIKE':
                        if not pd.api.types.is_string_dtype(df[field]):
                            df[field] = df[field].astype(str)
                        return df[field].str.contains(str(value), regex=True, na=False)
                    if lookup == 'NOT_LIKE':
                        if not pd.api.types.is_string_dtype(df[field]):
                            df[field] = df[field].astype(str)
                        return ~df[field].str.contains(str(value), regex=True, na=False)
                    if lookup == 'IS_NULL':
                        return df[field].isna()
                    if lookup == 'IS_NOT_NULL':
                        return ~df[field].isna()

                elif isinstance(condition.right, FieldReferenceExpression):
                    right_field_name = condition.right.field_reference.field.name
                    right_table_name = condition.right.field_reference.table_name

                    # Find the right field in the dataframe
                    right_actual_field = self._find_column_for_field(df, right_field_name, right_table_name)

                    if right_actual_field is None:
                        msg = (
                            f"Right field '{right_field_name}' from table "
                            f"'{right_table_name}' not found in dataframe columns"
                        )
                        raise ValueError(msg)  # noqa: TRY301

                    right_field = right_actual_field

                    if lookup == 'EQ':
                        return df[field] == df[right_field]
                    if lookup == 'NE':
                        return df[field] != df[right_field]
                    if lookup == 'GT':
                        return df[field] > df[right_field]
                    if lookup == 'GE':
                        return df[field] >= df[right_field]
                    if lookup == 'LT':
                        return df[field] < df[right_field]
                    if lookup == 'LE':
                        return df[field] <= df[right_field]

            # Default case for unsupported conditions
            msg = f'Unsupported condition: {condition}'
            logger.warning(msg)
            return pd.Series([True] * len(df))

        except Exception as e:
            msg = f'Error processing condition: {e!s}'
            logger.exception(msg)
            raise ValueError(msg) from e

    def _get_conditions(self, conditions: Conditions, df: 'pd.DataFrame') -> 'pd.Series':
        """Process conditions and return a Boolean mask for filtering."""
        import pandas as pd

        if not conditions.children:
            return pd.Series([True] * len(df))

        result = None

        for _, condition in enumerate(conditions.children):
            if isinstance(condition, Conditions):
                # Process nested conditions recursively
                condition_result = self._get_conditions(condition, df)
            else:
                # Process individual condition
                condition_result = self._process_condition(condition, df)

            # Combine with previous results based on operator
            if result is None:
                result = condition_result
            elif conditions.connector == 'AND':
                result = result & condition_result
            elif conditions.connector == 'OR':
                result = result | condition_result

        return result if result is not None else pd.Series([True] * len(df))

    def _run_update_data(self, mutation: UpdateData) -> None:
        """Update data in a CSV file."""
        try:
            # Get existing data
            df = self._get_df(mutation.schema.name)

            # Filter rows to update based on query
            if mutation.query:
                update_mask = self._get_conditions(mutation.query, df)

                # Update values in the filtered rows
                for field, value in mutation.data.data.items():
                    df.loc[update_mask, field] = value
            else:
                # Update all rows if no query provided
                for field, value in mutation.data.data.items():
                    df[field] = value

            # Save the updated DataFrame
            self._save_df(df, mutation.schema.name)

        except Exception as e:
            msg = f'Failed to update data: {e!s}'
            raise ValueError(msg) from e

    def _run_delete_data(self, mutation: DeleteData) -> None:
        """Delete data from a CSV file."""
        try:
            # Get existing data
            df = self._get_df(mutation.schema.name)

            # Filter rows to delete based on query
            if mutation.query:
                delete_mask = self._get_conditions(mutation.query, df)
                df = df[~delete_mask]  # Keep rows that don't match the condition
            else:
                # Delete all rows if no query provided
                df = df.iloc[0:0]  # Empty DataFrame but keep columns

            # Save the updated DataFrame
            self._save_df(df, mutation.schema.name)

        except Exception as e:
            msg = f'Failed to delete data: {e!s}'
            raise ValueError(msg) from e
