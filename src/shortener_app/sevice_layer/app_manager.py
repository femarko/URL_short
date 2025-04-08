from src.shortener_app.domain.services import create_short_url
from src.shortener_app.domain import errors as domain_errors, models
from src.shortener_app.sevice_layer.unit_of_work import UnitOfWork
from src.shortener_app.domain.models import URLShortened


def cut_url(original_url: str) -> str:
    short_url = create_short_url(url=original_url)
    return short_url


def save_urls(original_url: str, short_url: str, uow: UnitOfWork) -> int:
    try:
        with uow:
            urls_instance = URLShortened(original_url=original_url, short_url=short_url)
            uow.url_repo.add(urls_instance)
            uow.commit()
            urls_instance_id: int = urls_instance.id
    except domain_errors.AlreadyExistsError:
        urls_instance_id = uow.url_repo.find(original_url=original_url).id
    return urls_instance_id


def get_original_url(urls_instance_id: int, uow: UnitOfWork) -> str:
    with uow:
        result: URLShortened = uow.url_repo.get(instance_id=urls_instance_id)
    return result.original_url


def delete_url(urls_instance_id: int, uow: UnitOfWork) -> dict[str, str | int]:
    with uow:
        urls_instance_to_delete = uow.url_repo.get(instance_id=urls_instance_id)
        if not urls_instance_to_delete:
            raise domain_errors.NotFoundError
        deleted_urls_params: dict[str, str | int] = urls_instance_to_delete.get_params()
        uow.url_repo.delete(urls_instance_to_delete)
        uow.commit()
    return deleted_urls_params
