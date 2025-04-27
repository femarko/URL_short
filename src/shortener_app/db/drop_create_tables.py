import os
import asyncio

from src.shortener_app.orm_tool.init_orm_tool import get_inialized_orm_tool


if __name__ == "__main__":
    orm_tool = get_inialized_orm_tool()
    asyncio.run(orm_tool.reset_db())
