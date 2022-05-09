import os
import time
import json
import requests
from typing import List, Dict

# Filepath handling
LOCAL = os.path.dirname(os.path.abspath(__file__))
SCRYFALL_FILE = os.path.join(LOCAL, "scryfall.json")

# Bulk Data from Scryfall
URL = 'https://api.scryfall.com/bulk-data'

class NoScryfallDownloadLink(Exception):
    """No download link found on Scryfall Bulk Data page."""

class ScryfallDownloadError(Exception):
    """Unable to download file from Scryfall"""

class NoArtwork(Exception):
    """Card has no valid artwork"""

def write_json_file(data: Dict):
    """Writes dictionary to JSON file

    Args:
        data (Dict): Data to write to JSON
    """

    with open(SCRYFALL_FILE, "w") as fd:
        json.dump(data, fd, indent=4)

def read_json_file() -> Dict:
    """Read a JSON file and return the data

    Returns:
        Dict: JSON data
    """

    with open(SCRYFALL_FILE) as fd:
        return json.load(fd)

def fetch_download_url() -> str:
    """Fetches the download link from the Scryfall Bulk Data page using
    Beautiful Soup to scrape the page.
    So the file is always up to date

    Raises:
        ScryfallDownloadError: Unable to access the Scryfall page.

    Returns:
        str: Download link
    """

    print("Fetching Scryfall download link...")
    page = requests.get(URL)
    if page.status_code != 200:
        raise ScryfallDownloadError(
            "Unable to access Scryfall main download page!"
        )

    return [
        i for i in page.json()['data']
        if i['type'] == 'oracle_cards'
    ][0]['download_uri']

def download() -> List[Dict]:
    """Downloads the latest bulk data from Scryfall and sanitises the data.

    Raises:
        ScryfallDownloadError: Unable to download the page data
        ScryfallDownloadError: Unable to download the page data

    Returns:
        List[Dict]: Sanitised Card data
    """
    download_link = fetch_download_url()

    if download_link is None or download_link == '':
        raise ScryfallDownloadError("No download link available!")

    print("Fetching Scryfall card data...")
    r = requests.get(download_link)
    if r.status_code != 200:
        raise ScryfallDownloadError(
            f"Unable to download Scryfall oracle cards: {URL}"
        )

    cards_json = r.json()
    cards = sanitise_cards(cards_json)
    write_json_file(cards)

    return cards

def sanitise_cards(cards: List[Dict]) -> List[Dict]:
    """Sanitises the data to trim down the unwanted information.

    Args:
        cards (List[Dict]): List of cards to sanitise

    Returns:
        List[Dict]: Cleaned data
    """

    sanitised = []
    for card in cards:
        card = sanitise_card(card)
        if card is not None:
            sanitised.append(card)

    return sanitised

def sanitise_card(card: Dict) -> Dict:
    """Sanitises an individual card.
    Checks for invalid data and builds custom structure to hold desired data.

    Args:
        card (Dict): Card to sanitise

    Returns:
        Dict: Sanitised data
    """

    info = {}

    if is_invalid(card):
        return None

    info["name"] = card["name"]
    info["cost"] = card["mana_cost"] if "mana_cost" in card else ""
    info["images"] = card["image_uris"] if "image_uris" in card else {}
    info["cmc"] = card["cmc"]
    info["type"] = card["type_line"].replace("\u2014", "-")
    info["colors"] = card["colors"] if 'colors' in card else []
    info["color_identity"] = card["color_identity"]
    info["text"] = card["oracle_text"].replace("\u2014", "-").replace("\u2022", "*") if "oracle_text" in card else ""
    info["legal"] = [k for k, v in card["legalities"].items() if v != "not_legal"]
    info["set"] = card["set"]
    info["set_name"] = card["set_name"]
    info["keywords"] = card["keywords"]
    info["rarity"] = card["rarity"]
    info["flavour"] = card["flavor_text"]

    return info

def is_invalid(card: Dict) -> bool:
    """Checks the card for unwanted fields.

    Args:
        card (Dict): Card to check

    Returns:
        bool: Invalid or not
    """

    set_name = card["set_name"]

    if (
        "Unglued" in set_name or "Unhinged" in set_name
        or "Unstable" in set_name or "Unsanctioned" in set_name
    ):
        return True

    if "flavor_text" not in card:
        return True
    
    return False

def get_scryfall_cards() -> List[Dict]:
    """Downloads the cards or laods them from disk.
    Re-downloads the cards if a cetain tim has passed.

    Returns:
        List[Dict]: Card Data
    """

    if os.path.exists(SCRYFALL_FILE):
        curr_time = time.time()
        if curr_time > os.path.getmtime(SCRYFALL_FILE) + (12 * 60 * 60):
            cards = download()
        else:
            cards = read_json_file()
    else:
        cards = download()

    return cards

def download_artwork(card: Dict) -> str:
    """Downloads the artwork crop from Scryfall.

    Args:
        card (Dict): Card information

    Raises:
        NoArtwork: No artwork available for the card

    Returns:
        str: Filepath where the image is saved.
    """

    if "art_crop" not in card["images"]:
        raise NoArtwork(f"No artwork for {card['name']}")

    image_uri = card["images"]["art_crop"]
    r = requests.get(image_uri)
    img_path = os.path.join(LOCAL, "image.jpg")

    with open(img_path, "wb") as fd:
        fd.write(r.content)
    
    return img_path
