from unittest import mock

from tests.sql.postgres.testcases.schema_mutations import add_index
from tests.sql.postgres.testcases.schema_mutations import add_last_name_property
from tests.sql.postgres.testcases.schema_mutations import add_unique_constraint
from tests.sql.postgres.testcases.schema_mutations import create_user_schema
from tests.sql.postgres.testcases.schema_mutations import delete_age_property
from tests.sql.postgres.testcases.schema_mutations import delete_index
from tests.sql.postgres.testcases.schema_mutations import delete_unique_constraint
from tests.sql.postgres.testcases.schema_mutations import delete_user_schema
from tests.sql.postgres.testcases.schema_mutations import rename_user_schema
from tests.sql.postgres.testcases.schema_mutations import update_age_property
from tests.sql.postgres.unit.conftest import MockPostgresConnection


def test_create_schema(database_connection: MockPostgresConnection) -> None:
    create_user_schema(database_connection)

    database_connection.execute_mock.assert_has_calls([
        mock.call(
            'CREATE TABLE "user" ("id" BIGINT NOT NULL, "email" TEXT NOT NULL, "age" BIGINT NOT NULL, '
            '"first_name" TEXT, "last_name" TEXT, CONSTRAINT pk_user PRIMARY KEY ("id") , '
            'CONSTRAINT uk_user_email UNIQUE ("email"), CONSTRAINT ck_user_age CHECK ("user"."age" > 18))',
            (),
        ),
        mock.call('CREATE INDEX "idx_user_email" ON "user" (first_name, last_name)', ()),
    ])


def test_create_schema_with_namespace(database_connection: MockPostgresConnection) -> None:
    create_user_schema(database_connection, namespace='ns1')

    database_connection.execute_mock.assert_has_calls([
        mock.call(
            'CREATE TABLE "ns1"."user" ("id" BIGINT NOT NULL, "email" TEXT NOT NULL, "age" BIGINT NOT NULL, '
            '"first_name" TEXT, "last_name" TEXT, CONSTRAINT pk_user PRIMARY KEY ("id") , '
            'CONSTRAINT uk_user_email UNIQUE ("email"), CONSTRAINT ck_user_age CHECK ("ns1"."user"."age" > 18))',
            (),
        ),
        mock.call('CREATE INDEX "ns1"."idx_user_email" ON "ns1"."user" (first_name, last_name)', ()),
    ])


def test_create_schema_benchmark(database_connection: MockPostgresConnection, benchmark) -> None:
    def _run_command() -> None:
        create_user_schema(database_connection)

    benchmark(_run_command)


def test_rename_schema(database_connection: MockPostgresConnection) -> None:
    rename_user_schema(database_connection)

    database_connection.execute_mock.assert_called_once_with('ALTER TABLE "user" RENAME TO "customer"', ())


def test_rename_schema_with_namespace(database_connection: MockPostgresConnection) -> None:
    rename_user_schema(database_connection, namespace='ns1')

    database_connection.execute_mock.assert_called_once_with('ALTER TABLE "ns1"."user" RENAME TO "customer"', ())


def test_rename_schema_benchmark(database_connection: MockPostgresConnection, benchmark) -> None:
    def _run_command() -> None:
        rename_user_schema(database_connection)

    benchmark(_run_command)


def test_delete_schema(database_connection: MockPostgresConnection) -> None:
    delete_user_schema(database_connection)

    database_connection.execute_mock.assert_called_once_with('DROP TABLE "user"', ())


def test_delete_schema_with_namespace(database_connection: MockPostgresConnection) -> None:
    delete_user_schema(database_connection, namespace='ns1')

    database_connection.execute_mock.assert_called_once_with('DROP TABLE "ns1"."user"', ())


def test_delete_schema_benchmark(database_connection: MockPostgresConnection, benchmark) -> None:
    def _run_command() -> None:
        delete_user_schema(database_connection)

    benchmark(_run_command)


def test_add_property(database_connection: MockPostgresConnection) -> None:
    add_last_name_property(database_connection)

    database_connection.execute_mock.assert_called_once_with('ALTER TABLE "user" ADD COLUMN "last_name" TEXT', ())


def test_add_property_with_namespace(database_connection: MockPostgresConnection) -> None:
    add_last_name_property(database_connection, namespace='ns1')

    database_connection.execute_mock.assert_called_once_with('ALTER TABLE "ns1"."user" ADD COLUMN "last_name" TEXT', ())


def test_add_property_benchmark(database_connection: MockPostgresConnection, benchmark) -> None:
    def _run_command() -> None:
        add_last_name_property(database_connection)

    benchmark(_run_command)


def test_delete_property(database_connection: MockPostgresConnection) -> None:
    delete_age_property(database_connection)

    database_connection.execute_mock.assert_called_once_with('ALTER TABLE "user" DROP COLUMN "age"', ())


def test_delete_property_with_namespace(database_connection: MockPostgresConnection) -> None:
    delete_age_property(database_connection, namespace='ns1')

    database_connection.execute_mock.assert_called_once_with('ALTER TABLE "ns1"."user" DROP COLUMN "age"', ())


def test_delete_property_benchmark(database_connection: MockPostgresConnection, benchmark) -> None:
    def _run_command() -> None:
        delete_age_property(database_connection)

    benchmark(_run_command)


def test_update_property(database_connection: MockPostgresConnection) -> None:
    update_age_property(database_connection)

    database_connection.execute_mock.assert_called_once_with('ALTER TABLE "user" ALTER COLUMN "age" TYPE TEXT', ())


def test_update_property_with_namespace(database_connection: MockPostgresConnection) -> None:
    update_age_property(database_connection, namespace='ns1')

    database_connection.execute_mock.assert_called_once_with(
        'ALTER TABLE "ns1"."user" ALTER COLUMN "age" TYPE TEXT',
        (),
    )


def test_update_property_benchmark(database_connection: MockPostgresConnection, benchmark) -> None:
    def _run_command() -> None:
        update_age_property(database_connection)

    benchmark(_run_command)


def test_add_constraint(database_connection: MockPostgresConnection) -> None:
    add_unique_constraint(database_connection)

    database_connection.execute_mock.assert_called_once_with(
        'ALTER TABLE "user" ADD CONSTRAINT uk_user_email_unique UNIQUE ("email", "age")', ()
    )


def test_add_constraint_with_namespace(database_connection: MockPostgresConnection) -> None:
    add_unique_constraint(database_connection, namespace='ns1')

    database_connection.execute_mock.assert_called_once_with(
        'ALTER TABLE "ns1"."user" ADD CONSTRAINT uk_user_email_unique UNIQUE ("email", "age")', ()
    )


def test_add_constraint_benchmark(database_connection: MockPostgresConnection, benchmark) -> None:
    def _run_command() -> None:
        add_unique_constraint(database_connection)

    benchmark(_run_command)


def test_drop_constraint(database_connection: MockPostgresConnection) -> None:
    delete_unique_constraint(database_connection)

    database_connection.execute_mock.assert_called_once_with(
        'ALTER TABLE "user" DROP CONSTRAINT "uk_user_email_unique"', ()
    )


def test_drop_constraint_with_namespace(database_connection: MockPostgresConnection) -> None:
    delete_unique_constraint(database_connection, namespace='ns1')

    database_connection.execute_mock.assert_called_once_with(
        'ALTER TABLE "ns1"."user" DROP CONSTRAINT "uk_user_email_unique"', ()
    )


def test_drop_constraint_benchmark(database_connection: MockPostgresConnection, benchmark) -> None:
    def _run_command() -> None:
        delete_unique_constraint(database_connection)

    benchmark(_run_command)


def test_add_index(database_connection: MockPostgresConnection) -> None:
    add_index(database_connection)

    database_connection.execute_mock.assert_called_once_with('CREATE INDEX "idx_user_email" ON "user" (email, age)', ())


def test_add_index_with_namespace(database_connection: MockPostgresConnection) -> None:
    add_index(database_connection, namespace='ns1')

    database_connection.execute_mock.assert_called_once_with(
        'CREATE INDEX "ns1"."idx_user_email" ON "ns1"."user" (email, age)',
        (),
    )


def test_add_index_benchmark(database_connection: MockPostgresConnection, benchmark) -> None:
    def _run_command() -> None:
        add_index(database_connection)

    benchmark(_run_command)


def test_delete_index(database_connection: MockPostgresConnection) -> None:
    delete_index(database_connection)

    database_connection.execute_mock.assert_called_once_with('DROP INDEX "idx_user_email"', ())


def test_delete_index_with_namespace(database_connection: MockPostgresConnection) -> None:
    delete_index(database_connection, namespace='ns1')

    database_connection.execute_mock.assert_called_once_with('DROP INDEX "ns1"."idx_user_email"', ())


def test_delete_index_benchmark(database_connection: MockPostgresConnection, benchmark) -> None:
    def _run_command() -> None:
        delete_index(database_connection)

    benchmark(_run_command)
