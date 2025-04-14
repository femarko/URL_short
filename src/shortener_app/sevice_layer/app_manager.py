import src.shortener_app.domain.services as domain_services
import src.shortener_app.domain.errors as domain_errors

from src.shortener_app.sevice_layer.unit_of_work import UnitOfWork
from src.shortener_app.domain.models import URLShortened


def cut_url(original_url: str) -> str:
    short_url = domain_services.create_short_url(url=original_url)
    return short_url


async def save_urls(original_url: str, short_url: str, uow: UnitOfWork) -> tuple[int, bool]:
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


async def get_original_url(urls_instance_id: int, uow: UnitOfWork) -> str:
    async with uow:
        try:
            result: URLShortened = await uow.url_repo.get(instance_id=urls_instance_id)
        except Exception as e:
            raise domain_errors.UnexpectedError(message_postfix=str(e))
        if not result:
            raise domain_errors.NotFoundError(message_prefix="The url")
        return result.original_url


async def delete_url(urls_instance_id: int, uow: UnitOfWork) -> dict[str, str | int]:
    async with uow:
        urls_instance_to_delete = await uow.url_repo.get(instance_id=urls_instance_id)
        if not urls_instance_to_delete:
            raise domain_errors.NotFoundError
        deleted_urls_params: dict[str, str | int] = urls_instance_to_delete.get_params()
        await uow.url_repo.delete(urls_instance_to_delete)
        await uow.commit()
    return deleted_urls_params
