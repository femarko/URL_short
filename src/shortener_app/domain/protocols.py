from typing import TypeVar, Protocol, Any, Callable
from typing_extensions import Unpack


T = TypeVar("T")


class RepoProto(Protocol[T]):
    """
    This class defines interface of a repository.

    Concrete implementations of this class are supposed to encapsulate
    operations with database or other data storage.
    """
    async def add(self, instance: T) -> None: ...
    async def get(self, instance_id: int) -> T | None: ...
    async def find(self, **kwargs: Unpack[dict[str, Any]]) -> T | None: ...
    async def delete(self, instance: T) -> None: ...


class SessionProto(Protocol):
    """
    Protocol for ORM session object.

    This protocol describes interface for asynchronous database
    session object. It's used in Repository class to define interface
    of database operations.
    """
    async def execute(self, *args: Any, **kwargs: Any) -> Any: ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
    async def close(self) -> None: ...
    async def flush(self) -> None: ...
    async def get(self, model_cl: Any, instance_id: int) -> Any: ...
    def add(self, instance: Any) -> None: ...
    async def delete(self, instance: Any) -> None: ...


class UoWProto(Protocol):
    """
    Protocol for Unit of Work object.

    This protocol defines interface for asynchronous unit of work object.
    It abstracts the transaction handling, allowing for consistent and manageable
    interaction with the database.
    """

    session_maker: Callable[..., SessionProto]
    url_repo: RepoProto

    async def __aenter__(self) -> "UoWProto":
        """Starts a new unit of work and returns the UoW instance."""
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Handles the exit from the unit of work context, committing or rolling back."""
        pass

    async def rollback(self) -> None:
        """Rolls back the current transaction, discarding all changes."""
        pass

    async def commit(self) -> None:
        """Commits the current transaction, persisting all changes to the database."""
        pass

    async def flush(self) -> None:
        """Flushes changes to the database without committing the transaction."""
        pass
