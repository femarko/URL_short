import asyncio
from src.shortener_app.orm_tool.sql_aclchemy_wrapper import orm_conf


asyncio.run(orm_conf.reset_db())
