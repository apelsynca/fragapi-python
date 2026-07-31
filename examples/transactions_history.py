import asyncio

from fragapi import FragAPI
from fragapi.types import TransactionsSorting


async def main() -> None:
    fragapi = FragAPI(token="YOUR_TOKEN_FROM_PANEL")

    # get 10 transactions, sorted biggest in amount to lowest
    async for transaction in fragapi.iter_transactions(
        sorting=TransactionsSorting.amount_desc, limit=10
    ):
        print(transaction)

    # also fragapi.list_transactions available!


if __name__ == "__main__":
    asyncio.run(main())
