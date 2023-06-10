from dotenv import load_dotenv

load_dotenv('.env')

import asyncio

from app.services.api.check_api import CheckAPI


async def main():
    api = CheckAPI()
    # a = await api.get_checked_players(steamids)
    a = await api.get_last_check('765611990467009151')
    print(a)


asyncio.run(main())
