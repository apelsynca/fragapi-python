import asyncio

from fragapi import FragAPI


async def main() -> None:
    fragapi = FragAPI(token="YOUR_TOKEN_FROM_PANEL")
    recipient = await fragapi.get_stars_recipient(username="synca")

    print("Found recipient!", recipient.name, recipient.avatar_url)


if __name__ == "__main__":
    asyncio.run(main())
