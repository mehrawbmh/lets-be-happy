from dependencies.depends import get_main_db
from asyncio import run


async def test_function():
    db = await get_main_db()
    print(await db.test.find_one())

if __name__ == '__main__':
    run(test_function())
