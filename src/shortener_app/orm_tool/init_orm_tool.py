from src.shortener_app.domain.models import URLShortened
from src.shortener_app.orm_tool.sql_alchemy_wrapper import get_orm_tool


def get_inialized_orm_tool():
    return get_orm_tool(domain_models=(URLShortened,))
