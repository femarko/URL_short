from typing import Generic
from typing_extensions import Unpack

from src.shortener_app.domain.models import URLShortened, URLShortenedDict
from src.shortener_app.domain import errors as domain_errors
from src.shortener_app.orm_tool.init_orm_tool import get_initialized_orm_tool
from src.shortener_app.domain.protocols import T, RepoProto, SessionProto

orm_tool = get_initialized_orm_tool()


class Repository(Generic[T], RepoProto[T]):
    """
    Generic repository class.

    This class provides interface for database operations using ORMTool instance
    which encapsulates all objects and functions of the specific ORM.

    :param session: ORM session object.
    :type session: SessionProto
    :param db_error: ORM database exception class.
    :type db_error: orm_tool.db_error
    :param select: ORM function for creating select SQL statement.
    :type select: orm_tool.sql_select
    :param model_cl: Domain model.
    :type model_cl: type[T]
    """
    def __init__(self,
                 session: SessionProto,
                 db_error: orm_tool.db_error,
                 select: orm_tool.sql_select,
                 model_cl: type[T]) -> None:
        self.session = session
        self.model_cl = model_cl
        self.db_error = db_error
        self.select = select

    async def add(self, instance: T) -> None:
        """
        Adds a new instance of the model to the database.

        :param instance: an instance of the model to be added
        :type instance: T
        :raises domain_errors.DBError: if an error occurs while interacting with the database
        """
        try:
            self.session.add(instance)
        except self.db_error as e:
            raise domain_errors.DBError(message=str(e))

    async def get(self, instance_id: int) -> T | None:
        """
        Retrieves an instance of the model from the database by its ID.

        :param instance_id: ID of the instance to retrieve
        :type instance_id: int
        :return: instance of the model with the given ID, or None if not found
        :type: T | None
        :raises domain_errors.DBError: if an error occurs while interacting with the database
        """
        try:
            return await self.session.get(self.model_cl, instance_id)
        except self.db_error as e:
            raise domain_errors.DBError(message=str(e))

    async def find(self, **kwargs: Unpack[URLShortenedDict]) -> T | None:  # type: ignore
        """
        Finds an instance of the model in the database by the given keyword arguments.

        :param kwargs: keyword arguments to filter by
        :type kwargs: Unpack[URLShortenedDict]
        :return: an instance of the model if found, None otherwise
        :rtype: T | None
        :raises domain_errors.DBError: if an error occurs while interacting with the database
        """
        stmt = self.select(self.model_cl).filter_by(**kwargs)
        try:
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except self.db_error as e:
            raise domain_errors.DBError(message=str(e))

    async def delete(self, instance: T) -> None:
        """
        Deletes an instance of the model from the database.

        :param instance: an instance of the model to be deleted
        :type instance: T
        :raises domain_errors.DBError: if an error occurs while interacting with the database
        """
        try:
            await self.session.delete(instance)
        except self.db_error as e:
            raise domain_errors.DBError(message=str(e))


class URLRepository(Repository[URLShortened]):
    """
    :class:`URLRepository` - a repository for handling operations related to the `URLShortened` model.

    This class provides a concrete implementation of the `Repository` interface for the `URLShortened` model,
    encapsulating database operations specific to URL shortening.

    :param session: ORM session object.
    :type session: SessionProto
    """
    def __init__(self, session: SessionProto):
        super().__init__(
            session=session, model_cl=URLShortened, db_error=orm_tool.db_error, select=orm_tool.sql_select
        )
