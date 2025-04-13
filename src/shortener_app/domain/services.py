import pyshorteners

import src.shortener_app.domain.errors as domain_errors


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
    try:
        return s.tinyurl.short(url)
    except Exception as e:
        raise domain_errors.UnexpectedError(message_postfix=str(e))