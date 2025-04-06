import pyshorteners


def create_short_url(url: str) -> str:
    """
    Shortens a given URL using the TinyURL service.

    :param url: The URL to be shortened.
    :type url: str
    :return: The shortened URL.
    :rtype: str
    :raises pyshorteners.exceptions.ShorteningErrorException: If the TinyURL service returns an error.
    """
    s = pyshorteners.Shortener()
    return s.tinyurl.short(url)
