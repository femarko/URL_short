from src.shortener_app.domain.models import URLShortened
from src.shortener_app.infrastructure.orm_tool.sql_alchemy_wrapper import get_orm_tool


def get_initialized_orm_tool():
    """
    Get initialized ORM tool.

    Returns
    -------
    :class:`ORMTool`
        Initialized ORM tool.
    """
    return get_orm_tool(domain_models=(URLShortened,))
