import asyncio

from fragapi import FragAPI


async def main() -> None:
    fragapi = FragAPI(token="YOUR_TOKEN_FROM_PANEL")
    me = await fragapi.get_me()

    print(me.balance)  # Your balance


if __name__ == "__main__":
    asyncio.run(main())
