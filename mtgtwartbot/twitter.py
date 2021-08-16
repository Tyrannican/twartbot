import tweepy
from os import environ

# API keys and secrets
CONSUMER = environ.get("API_KEY")
CONSUMER_SECRET = environ.get("API_SECRET")
ACCESS = environ.get("ACCESS_KEY")
ACCESS_SECRET = environ.get("ACCESS_SECRET")
KEYS = [CONSUMER, CONSUMER_SECRET, ACCESS, ACCESS_SECRET]

class APIKeysNotSet(Exception):
    """API Keys are not set as environment variables"""

def _make_api() -> tweepy.API:
    """Makes the Tweepy API object

    Raises:
        APIKeysNotSet: No API keys have been set by the user

    Returns:
        tweepy.API: API object
    """

    if not all(KEYS):
        raise APIKeysNotSet("API Keys are not set.")

    auth = tweepy.OAuthHandler(CONSUMER, CONSUMER_SECRET)
    auth.set_access_token(ACCESS, ACCESS_SECRET)
    return tweepy.API(auth)

class TwitterAPI:
    """Class to simplify access to the API
    """

    def __init__(self):
        self.api = _make_api()

    def load_image(self, image: str):
        """Loads an image from disk and uploads it to Twitter as media

        Args:
            image (str): Path to the image

        Returns:
            tweepy.Media: Media object
        """

        return self.api.media_upload(image)

    def make_tweet(self, text: str):
        """Makes a simple string tweet

        Args:
            text (str): Test to tweet
        """

        self.api.update_status(status=text)

    def make_image_tweet(self, image: str, text: str):
        """Makes a tweet with an image.

        Args:
            image (str): Path to the image
            text (str): Text to tweet
        """

        img = self.load_image(image)
        self.api.update_status(status=text, media_ids=[img.media_id])