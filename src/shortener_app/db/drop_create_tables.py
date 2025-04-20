import asyncio

from src.shortener_app.orm_tool.init_orm_tool import orm_tool


if __name__ == "__main__":
    asyncio.run(orm_tool.reset_db())
