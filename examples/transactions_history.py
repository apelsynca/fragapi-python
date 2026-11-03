import asyncio

from fragapi import FragAPI
from fragapi.types import TransactionsSorting


async def main() -> None:
    fragapi = FragAPI(token="YOUR_TOKEN_FROM_PANEL")

    # get 10 transactions, sorted biggest in amount to lowest
    transactions = await fragapi.list_transactions(
        sorting=[TransactionsSorting.amount_desc], limit=10
    )
    for transaction in transactions.items:
        print(transaction)


if __name__ == "__main__":
    asyncio.run(main())
