from mongoengine import get_connection
from pymongo import MongoClient
from pymongo.client_session import ClientSession
import contextvars
from typing import Optional, Any, Type, cast
from contextlib import suppress

from ..utils.env_initlializer import EnvStore

# Global context variable for MongoDB session
mongo_session_context: contextvars.ContextVar[Optional[ClientSession]] = (
    contextvars.ContextVar("mongo_session", default=None)
)


class MongoTransactionContext:
    """Context manager for handling MongoDB transactions with proper session management."""

    def __init__(self, db_alias: Optional[str] = None):
        """Initialize the transaction context.

        Args:
            db_alias: Optional database alias. If not provided, fetches from config.
        """
        self.db_alias = db_alias or cast(str, EnvStore().dbname)
        self.session: Optional[ClientSession] = None
        self.token: Optional[contextvars.Token[Optional[ClientSession]]] = None

    @property
    def client(self) -> MongoClient:
        """Get the MongoDB client instance."""
        connection = get_connection(alias=self.db_alias)

        if not hasattr(connection, "connection") or not hasattr(
            connection.connection, "client"
        ):
            raise ValueError(f"Invalid MongoDB connection for alias {self.db_alias}")

        return connection.connection.client

    def __enter__(self) -> ClientSession:
        """Enter the transaction context.

        Returns:
            Active MongoDB client session.

        Raises:
            ValueError: If MongoDB connection is invalid.
            RuntimeError: If session creation fails.
        """
        try:
            self.session = self.client.start_session()
            self.session.start_transaction()
            self.token = mongo_session_context.set(self.session)
            return self.session

        except Exception as e:
            # Clean up any partially initialized resources
            if self.session:
                with suppress(Exception):
                    self.session.end_session()
            raise RuntimeError(f"Failed to create MongoDB session: {str(e)}") from e

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> None:
        if not self.session:
            return

        try:
            if exc_type is None:
                self.session.commit_transaction()
            else:
                self.session.abort_transaction()

        except Exception:
            with suppress(Exception):
                self.session.abort_transaction()
            raise

        finally:
            if self.token is not None:
                mongo_session_context.reset(self.token)

            with suppress(Exception):
                self.session.end_session()

            self.session = None
            self.token = None
