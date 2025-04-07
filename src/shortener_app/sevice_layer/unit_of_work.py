from typing import Callable, Protocol

import src.shortener_app.domain.errors as domain_errors
from src.shortener_app.orm_tool.sql_aclchemy_wrapper import orm_conf
from src.shortener_app.repository.repository import URLRepository, RepoProto


class SessionProto(Protocol):
    def commit(self): pass
    def rollback(self): pass
    def close(self): pass


class UnitOfWork:
    def __init__(self, session_maker: Callable = orm_conf.session_maker):
        self.session_maker = session_maker

    def __enter__(self):
        self.session: SessionProto = self.session_maker()
        self.url_repo: RepoProto = URLRepository(session=self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
            self.session.close()
        self.session.close()

    def rollback(self):
        self.session.rollback()

    def commit(self):
        try:
            self.session.commit()
        except orm_conf.integrity_error:
            raise domain_errors.AlreadyExistsError
