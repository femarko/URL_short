import os
import asyncio

from src.shortener_app.orm_tool.init_orm_tool import get_inialized_orm_tool


if __name__ == "__main__":
    orm_tool = get_inialized_orm_tool()
    print(f"From drop_create_tables.py: {orm_tool.db_url = }")
    print(f"From drop_create_tables.py: {os.getenv('MODE') = }")
    print(f"From drop_create_tables.py: {os.getenv('POSTGRES_HOST') = }")
    asyncio.run(orm_tool.reset_db())
