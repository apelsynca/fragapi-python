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
