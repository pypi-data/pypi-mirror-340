# FitGirl Repack Client Library 🎮📦

Welcome to the **FitGirl Repack Client Library** – your one-stop solution for fetching, parsing, and exploring game data from the [fitgirl-repacks](https://fitgirl-repacks.site) website! This library provides both **asynchronous** and **synchronous** clients to suit your needs, ensuring you can integrate game data into your projects seamlessly and efficiently. 🚀

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Asynchronous Usage](#asynchronous-usage)
  - [Synchronous Usage](#synchronous-usage)
- [Guidelines & What Not to Do](#guidelines--what-not-to-do)
- [License](#license)
- [Contact](#contact)

---

## Overview

The **FitGirl Repack Client Library** lets you search for and retrieve detailed information about games available on FitGirl Repacks. Whether you're building a personal game database, integrating game data into your website, or just exploring how such data is parsed, this library is designed to provide a clean and simple interface. 💡

The library includes:
- **Game Data Classes:** Structured representations of game metadata.
- **Parsers:** Functions to convert raw HTML into structured data.
- **Asynchronous Client:** Ideal for scalable, non-blocking operations.
- **Synchronous Client:** Perfect for simple scripts or environments where async is not needed.

---

## Features

- **Lightweight & Fast:** Written with performance in mind using [httpx](https://www.python-httpx.org/) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/).
- **Dual Client Support:** Choose between asynchronous (`FitGirlClient`) and synchronous (`FitGirlSyncClient`) operations.
- **Clean API:** Well-documented and user-friendly for quick integration.
- **Robust Parsing:** Extracts relevant details like title, author, category, download links, and more.
- **Context Manager Friendly:** Utilize Python's `with` statement for safe and predictable resource management. 🛡️

---

## Installation

You can install the library using [pip](https://pip.pypa.io/en/stable/):

```bash
pip install fitgirl
```

---

## Usage

### Asynchronous Usage

Using the asynchronous client is perfect when you have multiple concurrent requests or need to integrate with other async frameworks like [FastAPI](https://fastapi.tiangolo.com/).

```python
import asyncio
from fitgirl import FitGirlClient

async def main():
    async with FitGirlClient() as client:
        # Search for games
        game_data_list = await client.search("adventure")
        for game in game_data_list:
            print(f"Title: {game.title} | Author: {game.author}")

        # Retrieve a specific game detail
        game_details = await client.get_game("game-slug-example")
        for detail in game_details:
            print(f"Game Detail: {detail.title} - {detail.category}")

# Run the asynchronous main function
asyncio.run(main())
```

### Synchronous Usage

When simplicity is your goal or your application does not require asynchronicity, use the synchronous client.

```python
from fitgirl import FitGirlSyncClient

with FitGirlSyncClient() as client:
    # Search for games
    game_data_list = client.search("strategy")
    for game in game_data_list:
        print(f"Title: {game.title} | Date: {game.date}")

    # Retrieve a specific game detail
    game_details = client.get_game("another-game-slug")
    for game in game_details:
        print(f"Title: {game.title} | Download Links: {game.download_links}")
```

---

## Guidelines & What Not to Do

### Do's ✅
- **Use Context Managers:** Always utilize the context managers (`async with` or `with`) to ensure sessions are closed properly.
- **Handle Exceptions:** Wrap your API calls in try-except blocks to manage network errors gracefully.
- **Optimize Queries:** Keep your queries specific to reduce overhead on the server.

### Don'ts ❌
- **Avoid Hardcoding:** Do not hardcode URLs or endpoints; let the library handle the base URL.
- **Spamming Requests:** Do not flood the FitGirl Repacks website with too many requests in a short span – respect the service and its traffic limits. 🚦
- **Ignore Parsing Errors:** If a parsing issue arises, ensure you handle it in your application logic rather than ignoring it.
- **Overcomplicate:** Avoid adding unnecessary complexity in how you call or manage the client. The API is designed to be straightforward and efficient!

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Contact

For questions, issues, or suggestions, please open an issue on our [github repository](https://github.com/xsyncio/fitgirl/issue).