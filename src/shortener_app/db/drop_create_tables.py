import asyncio
from src.shortener_app.orm_tool.sql_aclchemy_wrapper import orm_conf
from src.config import settings

print(settings.db_url)
asyncio.run(orm_conf.reset_db())