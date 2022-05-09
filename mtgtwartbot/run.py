import random
from .twitter import TwitterAPI
from .scryfall import get_scryfall_cards, download_artwork

if __name__ == "__main__":
    # Launch the API and get the cards
    api = TwitterAPI()
    cards = get_scryfall_cards()

    # Shuffles them up and picks one
    random.shuffle(cards)
    card = random.choice(cards)

    # Builds the text and makes the tweet
    text = f"{card['name']} ({card['set_name']}):\n\n{card['flavour']}\n#MTG #MagicTheGathering"
    img_path = download_artwork(card)

    api.make_image_tweet(img_path, text)
