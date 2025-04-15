import typing

import httpx
from bs4 import BeautifulSoup

from fitgirl.core.abc import Game, GameData
from fitgirl.core.parsers import parse_game, parse_game_data


class FitGirlClient:
    """
    Asynchronous client for interacting with the FitGirl repacks website.

    Attributes:
        BASE_URL (str): The base URL for the FitGirl repacks site.
        session (httpx.AsyncClient): The asynchronous HTTP client session.
    """

    BASE_URL = "https://fitgirl-repacks.site"

    def __init__(self) -> None:
        """Initialize an asynchronous FitGirlClient with a base URL and custom User-Agent header."""
        self.session = httpx.AsyncClient(base_url=self.BASE_URL, headers={"User-Agent": "FitGirlClient/1.0"})

    async def _get_parsed_html(self, url: str) -> str:
        """
        Asynchronously retrieve and parse HTML content from a given URL.

        Args:
            url (str): The URL or path to fetch HTML content from.

        Returns:
            str: A prettified HTML string.
        """
        resp = await self.session.get(url)
        resp.encoding = resp.apparent_encoding  # Ensure proper encoding detection
        soup = BeautifulSoup(resp.text, "html.parser")
        return soup.prettify()

    async def search(self, query: str) -> typing.List[GameData]:
        """
        Search for games based on a query string.

        Args:
            query (str): The search query.

        Returns:
            List[GameData]: A list of parsed GameData objects.
        """
        html_content = await self._get_parsed_html(f"?s={query}")
        return parse_game_data(html_content)

    async def get_game(self, game_slug: str) -> typing.List[Game]:
        """
        Retrieve detailed information for a specific game.

        Args:
            game_slug (str): The slug/identifier for the game.

        Returns:
            List[Game]: A list of parsed Game objects.
        """
        html_content = await self._get_parsed_html(game_slug)
        return parse_game(html_content)

    async def close(self) -> None:
        """Close the asynchronous HTTP client session."""
        await self.session.aclose()

    async def __aenter__(self) -> "FitGirlClient":
        """
        Enter the asynchronous context manager.

        Returns:
            FitGirlClient: The current client instance.
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit the asynchronous context manager and close the session.

        Args:
            exc_type: Exception type, if raised.
            exc_val: Exception value, if raised.
            exc_tb: Traceback, if available.
        """
        await self.close()


class FitGirlSyncClient:
    """
    Synchronous client for interacting with the FitGirl repacks website.

    Attributes:
        BASE_URL (str): The base URL for the FitGirl repacks site.
        session (httpx.Client): The synchronous HTTP client session.
    """

    BASE_URL = "https://fitgirl-repacks.site"

    def __init__(self) -> None:
        """Initialize a synchronous FitGirlSyncClient with a base URL and custom User-Agent header."""
        self.session = httpx.Client(base_url=self.BASE_URL, headers={"User-Agent": "FitGirlSyncClient/1.0"})

    def _get_parsed_html(self, url: str) -> str:
        """
        Retrieve and parse HTML content from a given URL synchronously.

        Args:
            url (str): The URL or path to fetch HTML content from.

        Returns:
            str: A prettified HTML string.
        """
        resp = self.session.get(url)
        resp.encoding = resp.apparent_encoding  # Ensure proper encoding detection
        soup = BeautifulSoup(resp.text, "html.parser")
        return soup.prettify()

    def search(self, query: str) -> typing.List[GameData]:
        """
        Search for games based on a query string synchronously.

        Args:
            query (str): The search query.

        Returns:
            List[GameData]: A list of parsed GameData objects.
        """
        html_content = self._get_parsed_html(f"?s={query}")
        return parse_game_data(html_content)

    def get_game(self, game_slug: str) -> typing.List[Game]:
        """
        Retrieve detailed information for a specific game synchronously.

        Args:
            game_slug (str): The slug/identifier for the game.

        Returns:
            List[Game]: A list of parsed Game objects.
        """
        html_content = self._get_parsed_html(game_slug)
        return parse_game(html_content)

    def close(self) -> None:
        """Close the synchronous HTTP client session."""
        self.session.close()

    def __enter__(self) -> "FitGirlSyncClient":
        """
        Enter the context manager for the synchronous client.

        Returns:
            FitGirlSyncClient: The current client instance.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit the context manager and close the session.

        Args:
            exc_type: Exception type, if raised.
            exc_val: Exception value, if raised.
            exc_tb: Traceback, if available.
        """
        self.close()
