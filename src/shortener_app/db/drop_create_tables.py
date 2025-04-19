import asyncio
import src.shortener_app.db
from src.shortener_app.orm_tool.sql_aclchemy_wrapper import orm_conf
from src.shortener_app.domain.models import URLShortened


orm_conf.init_table(domain=URLShortened)
asyncio.run(orm_conf.reset_db())