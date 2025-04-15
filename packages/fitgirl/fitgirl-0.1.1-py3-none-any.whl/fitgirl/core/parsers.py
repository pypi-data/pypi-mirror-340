import html
import re
import typing

import bs4

from fitgirl.core.abc import Game, GameData


def get_paragraph(article: bs4.element.Tag, label: str) -> str:
    article_html = article.decode()
    match = re.search(rf"({label}.*?</strong>)", article_html, re.DOTALL)
    if match:
        inner_match = re.search(r"<strong>\s*(.*?)\s*</strong>", match.group(1), re.DOTALL)
        return inner_match.group(1) if inner_match else "N/A"
    return "N/A"


def get_screenshots(article: bs4.element.Tag, label: str) -> typing.List[str]:
    article_html = article.decode()
    section_match = re.search(rf"{label}.*?</p>", article_html, re.DOTALL)
    if section_match:
        return re.findall(r'<img[^>]+src="([^"]+)"', section_match.group(0))
    return []


def get_text(tag: typing.Optional[bs4.element.Tag]) -> str:
    return tag.get_text(strip=True) if tag else "N/A"


def get_attribute(tag: typing.Optional[bs4.element.Tag], attr: str) -> str:
    if tag:
        attribute_value = tag.get(attr, "N/A")
        return " ".join(attribute_value) if isinstance(attribute_value, list) else attribute_value
    return "N/A"


def parse_game_data(html_content: str) -> typing.List[GameData]:
    soup = bs4.BeautifulSoup(html_content, "html.parser")
    games: typing.List[GameData] = []
    for article in soup.find_all("article", class_="post"):
        title_tag = article.find("h1", class_="entry-title").find("a")
        title = get_text(title_tag)
        date = get_attribute(article.find("time", class_="entry-date"), "datetime")
        author = get_text(article.find("span", class_="author vcard").find("a"))
        category = get_text(article.find("span", class_="cat-links").find("a"))
        details_tag = article.find("div", class_="entry-summary")
        details = get_text(details_tag)
        download_links = [link["href"] for link in details_tag.find_all("a", href=True)]
        games.append(
            GameData(
                title=title, date=date, author=author, category=category, details=details, download_links=download_links
            )
        )
    return games


def format_repack_features(raw_features: str) -> str:
    lines = raw_features.strip().splitlines()
    cleaned = [html.unescape(line.strip()) for line in lines if line.strip()]
    return "\n".join(f"- {line}" for line in cleaned)


def get_repack_features(article: bs4.element.Tag, label: str) -> typing.List[str]:
    article_html = article.decode()
    section_match = re.search(rf"{label}.*?</ul>", article_html, re.DOTALL)
    if section_match:
        features = re.findall(r"<li>\s*(.*?)\s*</li>", section_match.group(0), re.DOTALL)
        features = [re.sub(r"<[^>]+>", "", feat).strip() for feat in features]
        if features:
            return [format_repack_features(features[0])]
    return []


def parse_game(html_content: str) -> typing.List[Game]:
    soup = bs4.BeautifulSoup(html_content, "html.parser")
    games: typing.List[Game] = []
    for article in soup.find_all("article", class_="post"):
        title = article.find("h1", class_="entry-title").get_text(strip=True)
        date = article.find("time", class_="entry-date").get("datetime", "N/A")
        author = article.find("span", class_="author vcard").find("a").get_text(strip=True)
        category = article.find("span", class_="cat-links").find("a").get_text(strip=True)
        genres_tags = get_paragraph(article, "Genres/Tags")
        companies = get_paragraph(article, "Companies")
        languages = get_paragraph(article, "Languages")
        original_size = get_paragraph(article, "Original Size")
        repack_size = get_paragraph(article, "Repack Size:")
        screenshots = get_screenshots(article, "Screenshots")
        repack_features = get_repack_features(article, "Repack Features")
        download_links = [link["href"] for link in article.select("h3:contains('Download Mirrors') + ul li a")]
        games.append(
            Game(
                title=title,
                date=date,
                author=author,
                category=category,
                genres_tags=genres_tags,
                companies=companies,
                languages=languages,
                original_size=original_size,
                repack_size=repack_size,
                download_links=download_links,
                screenshots=screenshots,
                repack_features=repack_features,
            )
        )
    return games
