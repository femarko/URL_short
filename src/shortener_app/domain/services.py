import pyshorteners

import src.shortener_app.domain.errors as domain_errors


def create_short_url(url: str) -> str:
    """
    Function that creates a shortened URL using tinyurl.com service.

    Raises:
        :class:`domain_errors.UnexpectedError`: when unexpected server error occurs.

    :param url: URL to be shortened
    :type url: str
    :return: shortened URL
    :rtype: str
    """
    s = pyshorteners.Shortener()
    try:
        return s.tinyurl.short(url)
    except Exception as e:
        raise domain_errors.UnexpectedError(message_postfix=str(e))