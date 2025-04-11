from typing import Optional, TypedDict

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session, sessionmaker

from ._dbos_config import ConfigFile, DatabaseConfig
from ._error import DBOSWorkflowConflictIDError
from ._schemas.application_database import ApplicationSchema


class TransactionResultInternal(TypedDict):
    workflow_uuid: str
    function_id: int
    output: Optional[str]  # JSON (jsonpickle)
    error: Optional[str]  # JSON (jsonpickle)
    txn_id: Optional[str]
    txn_snapshot: str
    executor_id: Optional[str]


class RecordedResult(TypedDict):
    output: Optional[str]  # JSON (jsonpickle)
    error: Optional[str]  # JSON (jsonpickle)


class ApplicationDatabase:

    def __init__(self, database: DatabaseConfig, *, debug_mode: bool = False):

        app_db_name = database["app_db_name"]

        # If the application database does not already exist, create it
        if not debug_mode:
            postgres_db_url = sa.URL.create(
                "postgresql+psycopg",
                username=database["username"],
                password=database["password"],
                host=database["hostname"],
                port=database["port"],
                database="postgres",
            )
            postgres_db_engine = sa.create_engine(postgres_db_url)
            with postgres_db_engine.connect() as conn:
                conn.execution_options(isolation_level="AUTOCOMMIT")
                if not conn.execute(
                    sa.text("SELECT 1 FROM pg_database WHERE datname=:db_name"),
                    parameters={"db_name": app_db_name},
                ).scalar():
                    conn.execute(sa.text(f"CREATE DATABASE {app_db_name}"))
            postgres_db_engine.dispose()

        # Create a connection pool for the application database
        app_db_url = sa.URL.create(
            "postgresql+psycopg",
            username=database["username"],
            password=database["password"],
            host=database["hostname"],
            port=database["port"],
            database=app_db_name,
        )

        connect_args = {}
        if (
            "connectionTimeoutMillis" in database
            and database["connectionTimeoutMillis"]
        ):
            connect_args["connect_timeout"] = int(
                database["connectionTimeoutMillis"] / 1000
            )

        self.engine = sa.create_engine(
            app_db_url,
            pool_size=database["app_db_pool_size"],
            max_overflow=0,
            pool_timeout=30,
            connect_args=connect_args,
        )
        self.sessionmaker = sessionmaker(bind=self.engine)
        self.debug_mode = debug_mode

        # Create the dbos schema and transaction_outputs table in the application database
        if not debug_mode:
            with self.engine.begin() as conn:
                schema_creation_query = sa.text(
                    f"CREATE SCHEMA IF NOT EXISTS {ApplicationSchema.schema}"
                )
                conn.execute(schema_creation_query)
            ApplicationSchema.metadata_obj.create_all(self.engine)

    def destroy(self) -> None:
        self.engine.dispose()

    @staticmethod
    def record_transaction_output(
        session: Session, output: TransactionResultInternal
    ) -> None:
        try:
            session.execute(
                pg.insert(ApplicationSchema.transaction_outputs).values(
                    workflow_uuid=output["workflow_uuid"],
                    function_id=output["function_id"],
                    output=output["output"],
                    error=None,
                    txn_id=sa.text("(select pg_current_xact_id_if_assigned()::text)"),
                    txn_snapshot=output["txn_snapshot"],
                    executor_id=(
                        output["executor_id"] if output["executor_id"] else None
                    ),
                )
            )
        except DBAPIError as dbapi_error:
            if dbapi_error.orig.sqlstate == "23505":  # type: ignore
                raise DBOSWorkflowConflictIDError(output["workflow_uuid"])
            raise

    def record_transaction_error(self, output: TransactionResultInternal) -> None:
        if self.debug_mode:
            raise Exception("called record_transaction_error in debug mode")
        try:
            with self.engine.begin() as conn:
                conn.execute(
                    pg.insert(ApplicationSchema.transaction_outputs).values(
                        workflow_uuid=output["workflow_uuid"],
                        function_id=output["function_id"],
                        output=None,
                        error=output["error"],
                        txn_id=sa.text(
                            "(select pg_current_xact_id_if_assigned()::text)"
                        ),
                        txn_snapshot=output["txn_snapshot"],
                        executor_id=(
                            output["executor_id"] if output["executor_id"] else None
                        ),
                    )
                )
        except DBAPIError as dbapi_error:
            if dbapi_error.orig.sqlstate == "23505":  # type: ignore
                raise DBOSWorkflowConflictIDError(output["workflow_uuid"])
            raise

    @staticmethod
    def check_transaction_execution(
        session: Session, workflow_uuid: str, function_id: int
    ) -> Optional[RecordedResult]:
        rows = session.execute(
            sa.select(
                ApplicationSchema.transaction_outputs.c.output,
                ApplicationSchema.transaction_outputs.c.error,
            ).where(
                ApplicationSchema.transaction_outputs.c.workflow_uuid == workflow_uuid,
                ApplicationSchema.transaction_outputs.c.function_id == function_id,
            )
        ).all()
        if len(rows) == 0:
            return None
        result: RecordedResult = {
            "output": rows[0][0],
            "error": rows[0][1],
        }
        return result
