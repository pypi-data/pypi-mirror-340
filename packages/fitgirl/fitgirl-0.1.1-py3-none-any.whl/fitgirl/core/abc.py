from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass(slots=True)
class GameData:
    """
    Represents the basic metadata for a game.

    Attributes:
        title (str): The title of the game.
        date (str): The release or publication date of the game.
        author (str): The author or creator of the game.
        category (str): The category or genre of the game.
        details (str): Additional details or description of the game.
        download_links (List[str]): A list of URLs for downloading the game.
    """

    title: str
    date: str
    author: str
    category: str
    details: str
    download_links: List[str] = field(default_factory=list)


@dataclass(slots=True)
class Game:
    """
    Represents comprehensive metadata for a game including additional attributes
    for genres, companies involved, supported languages, file sizes, screenshots,
    and repack features.

    Attributes:
        title (str): The title of the game.
        date (str): The release date of the game.
        author (str): The author or developer of the game.
        category (str): The category or genre of the game.
        genres_tags (str): Tags or identifiers indicating the specific genres.
        companies (str): The companies or developers associated with the game.
        languages (str): Supported languages for the game.
        original_size (str): The original size of the game.
        repack_size (str): The size of the repacked version of the game.
        download_links (List[str]): A list of download URLs.
        screenshots (List[str]): A list of URLs pointing to game screenshots.
        repack_features (List[str]): A list of features included in the repack.
    """

    title: str
    date: str
    author: str
    category: str
    genres_tags: str
    companies: str
    languages: str
    original_size: str
    repack_size: str
    download_links: List[str] = field(default_factory=list)
    screenshots: List[str] = field(default_factory=list)
    repack_features: List[str] = field(default_factory=list)
