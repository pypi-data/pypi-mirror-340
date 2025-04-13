"""Utilities for Untappd User processing."""

from __future__ import annotations

from typing import TYPE_CHECKING

from httpx import URL

from untappd_scraper.constants import UNTAPPD_BASE_URL

if TYPE_CHECKING:
    from collections.abc import Mapping


def url_of(user_id: str, page: str = "", query: Mapping[str, str | int] | None = None) -> str:
    """Return the URL for a user's main page.

    Args:
        user_id (str): user ID
        page (str): specific user page
        query (dict[str, str]|None): filter for page

    Returns:
        str: url to load to get user's main page
    """
    base = UNTAPPD_BASE_URL

    if user_id:
        base += f"user/{user_id}"
    if page:
        base += f"/{page}"

    url = URL(base)

    if query:
        url = url.copy_merge_params(query)

    return str(url)
