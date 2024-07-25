from typing import Any

import uvicorn
from fastapi import FastAPI

from amsdal_glue_api_server.routes import register_routes


class AmsdalGlueServerApp:
    """
    AmsdalGlueServerApp is responsible for running the FastAPI server.

    Attributes:
        app (FastAPI): An instance of FastAPI.
        _enable_rest_api (bool): Enable the REST API.
        _enable_general_api (bool): Enable the General API.
        _enable_sql_api (bool): Enable the SQL API.
    """

    def __init__(
        self,
        app: FastAPI | None = None,
        *,
        enable_rest_api: bool = True,
        enable_general_api: bool = True,
        enable_sql_api: bool = True,
    ) -> None:
        """
        Initializes the AmsdalGlueServerApp with the given parameters.

        Args:
            app (FastAPI | None): An instance of FastAPI. If not provided, a new instance will be created.
            enable_rest_api (bool): Enable the REST API.
            enable_general_api (bool): Enable the General API.
            enable_sql_api (bool): Enable the SQL API.
        """
        self.app = app or FastAPI()

        self._enable_rest_api = enable_rest_api
        self._enable_general_api = enable_general_api
        self._enable_sql_api = enable_sql_api

    def register_routes(self) -> None:
        """
        Register routes based on provided arguments.
        """
        register_routes(
            self.app,
            enable_rest_api=self._enable_rest_api,
            enable_general_api=self._enable_general_api,
            enable_sql_api=self._enable_sql_api,
        )

    def run(self, host='0.0.0.0', port=8000, log_level='info', **kwargs: Any) -> None:  # noqa: S104
        """
        Run the FastAPI server.

        Args:
            host (str): The host to bind the server to.
            port (int): The port to bind the server to.
            log_level (str): The log level for the server.
            **kwargs: Additional keyword arguments to pass to uvicorn.
        """
        self.register_routes()

        uvicorn.run(self.app, host=host, port=port, log_level=log_level, **kwargs)
