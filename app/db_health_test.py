from asyncio import run

from dependencies.database import get_main_db


async def test_function():
    db = await get_main_db()
    print(await db.testi.find_one())

if __name__ == '__main__':
    run(test_function())
