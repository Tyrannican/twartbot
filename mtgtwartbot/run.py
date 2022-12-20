import random
from .twitter import TwitterAPI
from .scryfall import download_cards, download_artwork

if __name__ == "__main__":
    # Launch the API and get the cards
    api = TwitterAPI()
    cards = download_cards()

    # Shuffles them up and picks one
    random.shuffle(cards)
    card = random.choice(cards)

    # Builds the text and makes the tweet
    artist = f'\n\nArtist: {card["artist"]}' if card["artist"] else ''
    text = f"{card['name']} ({card['set_name']}):\n\n{card['flavour']}{artist}\n\n#MTG #MagicTheGathering #MTGA #MTGArena"

    # Checks the length of the tweet to make sure it's short enough
    while len(text) > 280:
        card = random.choice(cards)
        text = f"{card['name']} ({card['set_name']}):\n\n{card['flavour']}\n\n#MTG #MagicTheGathering #MTGA #MTGArena"

    img_path = download_artwork(card)

    api.make_image_tweet(img_path, text)
