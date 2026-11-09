# Getting Started

> This library is a python SDK for [FragAPI](https://fragapi.com)

## Installation

```bash theme={"theme":{"light":"github-light-default","dark":"dark-plus"}}
pip install fragapi
```

| Requirement | Version |
| ----------- | ------- |
| Python      | 3.10+   |
| aiohttp     | 3.14+   |
| pydantic    | 2.13+   |

Basic example:

```
import asyncio

from fragapi import FragAPI


async def main() -> None:
    fragapi = FragAPI(token="YOUR_TOKEN_FROM_PANEL")
    me = await fragapi.get_me()
    print(me.balance)  # Your balance


if __name__ == "__main__":
    asyncio.run(main())
```

## Methods

All methods are async and live on the `FragAPI` client.

| Area         | Methods                                                                                 |
| ------------ | --------------------------------------------------------------------------------------- |
| User         | `get_me`                                                                                |
| Stars        | `get_stars_recipient`, `buy_stars`, `buy_stars_bulk`, `get_buy_stars_bulk`, `wait_buy_stars_bulk` |
| Premium      | `get_premium_recipient`, `buy_premium`                                                  |
| Gifts        | `get_collection_gift_model_names`, `get_collection_gift_models`, `get_gift_model`       |
| Deposits     | `request_ton_deposit`, `request_ton_deposit_via_memo`, `list_deposits`                  |
| Transactions | `list_transactions`                                                                     |

Top up your balance by sending TON to the returned address, with either a base64 payload or a plain text memo:

```
deposit = await fragapi.request_ton_deposit(amount=1.5)
print(deposit.address, deposit.amount, deposit.payload)

deposit = await fragapi.request_ton_deposit_via_memo(amount=1.5)
print(deposit.address, deposit.amount, deposit.memo)
```

Bulk stars purchases return right away; wait for the results (or poll `get_buy_stars_bulk` yourself):

```
from fragapi import FragAPI

bulk = await fragapi.buy_stars_bulk(
    items=[
        FragAPI.BuyStars(username="synca", quantity=50),
        FragAPI.BuyStars(username="durov", quantity=100, show_sender=True),
    ]
)
bulk = await fragapi.wait_buy_stars_bulk(id=bulk.id)
for item in bulk.items:
    print(item.username, item.result or item.error)
```

List methods are paginated and return `.items` and `.pagination`:

```
from fragapi.types import TransactionsSorting

transactions = await fragapi.list_transactions(
    page=1, limit=10, sorting=[TransactionsSorting.amount_desc]
)
for transaction in transactions.items:
    print(transaction.amount, transaction.reason)
print(transactions.pagination.max_page)
```

Gift models can be sorted by floor price:

```
from fragapi.types import GiftModelsSorting

models = await fragapi.get_collection_gift_models(
    "plushpepe", sorting=[GiftModelsSorting.floor]
)
```
