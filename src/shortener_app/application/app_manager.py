import src.shortener_app.domain.services as domain_services
import src.shortener_app.domain.errors as domain_errors

from src.shortener_app.domain.protocols import UoWProto
from src.shortener_app.domain.models import URLShortened


"""
Functions of this module make domain layer and database interface layer to interact, providing results, which 
can be requested and received through the application's entry points.
"""


def cut_url(original_url: str) -> str:
    """
    Function that creates a shortened URL using tinyurl.com service.

    :param original_url: URL to be shortened
    :type original_url: str
    :return: shortened URL
    :rtype: str
    :raises: :class:`domain_errors.UnexpectedError` when unexpected server error occurs.
    """
    short_url = domain_services.create_short_url(url=original_url)
    return short_url


async def save_urls(original_url: str, short_url: str, uow: UoWProto) -> tuple[int, bool]:
    """
    Function that saves shortened URL to the database.

    :param original_url: URL to be saved
    :type original_url: str
    :param short_url: shortened URL
    :type short_url: str
    :param uow: unit of work
    :type uow: UoWProto
    :return: id of saved URL and boolean indicating whether URL was saved or just retrieved
    :rtype: tuple[int, bool]
    :raises: :class:`domain_errors.AlreadyExistsError` when URL is already saved in the database
    :raises: :class:`domain_errors.UnexpectedError` when unexpected server error occurs
    """
    try:
        async with uow:
            urls_instance = URLShortened(original_url=original_url, short_url=short_url)
            await uow.url_repo.add(urls_instance)
            await uow.flush()
            new_urls_instance_id: int = urls_instance.id
            await uow.commit()
            return new_urls_instance_id, True
    except domain_errors.AlreadyExistsError:
        async with uow:
            urls_instance = await uow.url_repo.find(original_url=original_url)
            old_urls_instance_id: int = urls_instance.id
            return old_urls_instance_id, False


async def get_original_url(urls_instance_id: int, uow: UoWProto) -> str:
    """
    Function that retrieves original URL from the database.

    :param urls_instance_id: id of shortened URL
    :type urls_instance_id: int
    :param uow: unit of work
    :type uow: UoWProto
    :return: original URL
    :rtype: str
    :raises: :class:`domain_errors.NotFoundError` when URL is not found in the database
    :raises: :class:`domain_errors.UnexpectedError` when unexpected server error occurs
    """
    async with uow:
        try:
            result: URLShortened = await uow.url_repo.get(instance_id=urls_instance_id)
        except Exception as e:
            raise domain_errors.UnexpectedError(message_postfix=str(e))
        if not result:
            raise domain_errors.NotFoundError(message_prefix="The url")
        return result.original_url
