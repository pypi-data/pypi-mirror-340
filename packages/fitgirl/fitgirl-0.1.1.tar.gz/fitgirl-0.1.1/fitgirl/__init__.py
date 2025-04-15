"""
FitGirl Repack Client Package.
-----------------------------

This package provides tools to interact with the FitGirl repacks website. It includes both
asynchronous and synchronous clients for retrieving game metadata and detailed game information.
It also offers parsers to convert raw HTML data into structured Game and GameData objects.

Exports:
    - Game, GameData: Data classes for representing game metadata.
    - parse_game, parse_game_data: Functions for parsing HTML content into game data structures.
    - FitGirlClient: Asynchronous client for FitGirl repacks.
    - FitGirlSyncClient: Synchronous client for FitGirl repacks.
"""

from .client import FitGirlClient, FitGirlSyncClient
from .core.abc import Game, GameData
from .core.parsers import parse_game, parse_game_data

__all__ = ["FitGirlClient", "FitGirlSyncClient", "Game", "GameData", "parse_game", "parse_game_data"]
