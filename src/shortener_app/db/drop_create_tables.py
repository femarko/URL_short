import asyncio

from src.shortener_app.orm_tool.init_orm_tool import orm_tool


if __name__ == "__main__":
    print(f"From drop_create_tables.py: {orm_tool.db_url = }")
    asyncio.run(orm_tool.reset_db())
