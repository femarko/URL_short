from typing import Protocol, Unpack, Any, TypeVar


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
