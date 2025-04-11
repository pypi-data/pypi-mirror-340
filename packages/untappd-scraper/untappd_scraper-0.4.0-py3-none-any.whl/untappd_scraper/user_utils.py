"""Utilities for Untappd User processing."""
from __future__ import annotations


def url_of(user_id: str, page: str = "", query: str = "") -> str:
    """Return the URL for a user's main page.

    Args:
        user_id (str): user ID
        page (str): specific user page
        query (str): filter for page

    Returns:
        str: url to load to get user's main page
    """
    url = f"https://untappd.com/user/{user_id}"
    if page:
        url += f"/{page}"
    if query:
        url += f"?{query}"
    return url
