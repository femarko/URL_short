from src.shortener_app.domain.models import URLShortened
from src.shortener_app.orm_tool.sql_aclchemy_wrapper import get_orm_tool

orm_tool = get_orm_tool(domain_models=(URLShortened,))
