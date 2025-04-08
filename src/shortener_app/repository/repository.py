from typing import Any, Protocol
from src.shortener_app.domain.models import URLShortened


class NotFoundError(Exception):
    pass


class RepoProto(Protocol):
    def add(self, instance) -> None:
        pass

    def get(self, instance_id: int) -> Any:
        pass

    def delete(self, instance) -> None:
        pass

    def find(self, **kwargs) -> Any:
        pass


class Repository:
    def __init__(self, session):
        self.session = session
        self.model_cl = None

    def add(self, instance) -> None:
        self.session.add(instance)

    def get(self, instance_id: int) -> Any:
        return self.session.get(self.model_cl, instance_id)

    def find(self, **kwargs) -> Any:
        return self.session.query(self.model_cl).filter_by(**kwargs).first()

    def delete(self, instance) -> None:
        self.session.delete(instance)


class URLRepository(Repository):
    def __init__(self, session):
        super().__init__(session=session)
        self.model_cl = URLShortened
