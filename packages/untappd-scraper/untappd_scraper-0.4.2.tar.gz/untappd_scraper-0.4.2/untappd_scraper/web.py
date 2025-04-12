"""Utilities to process web data."""

from __future__ import annotations

from typing import TYPE_CHECKING

import parse
from dateutil.parser import parse as parse_date

if TYPE_CHECKING:  # pragma: no cover
    from datetime import datetime

    from requests_html import Element


def id_from_href(element: Element) -> int:
    """Extract last past of a URL, which is an ID.

    Args:
        element (Element): element to extract href from

    Raises:
        ValueError: last part of url wasn't an integer

    Returns:
        int: last part of href, which is an id
    """
    last_bit: str = slug_from_href(element)
    try:
        return int(last_bit)
    except ValueError as excp:  # pragma: no cover
        msg = f"Cannot extract integer id from {last_bit=} element ({element.html})"
        raise ValueError(msg) from excp


def slug_from_href(element: Element) -> str:
    """Extract last past of a URL, which is a slug.

    Args:
        element (Element): element to extract href from

    Returns:
        str: last part of href
    """
    href: str = element.attrs["href"].removesuffix("/")
    return href.rpartition("/")[-1]


def date_from_data_href(
    element: Element, label: str, *, date_only: bool = False
) -> datetime | None:
    """Extract a date that may be present.

    Args:
        element (Element): html element containing date
        label (str): data-href value
        date_only (bool): only parse the date (not the time)?

    Returns:
        datetime: parsed date
    """
    href = element.find(f'.date [data-href="{label}"]', first=True)
    if href:
        dt = parse_date(href.text).astimezone()
        if date_only:
            return dt.date()
        return dt  # pragma: no cover

    return None


def parse_abv(abv_data: str) -> float | None:
    """Parse the ABV data buried in text.

    Args:
        abv_data (str): text version, eg '7.5% ABV'

    Returns:
        float: ABV as a number
    """
    try:
        return float(parse.search("{:g}%", abv_data)[0])
    except TypeError:  # pragma: no cover
        return None


def parse_ibu(ibu_data: str) -> int | None:
    """Parse the IBU data buried in text.

    Args:
        ibu_data (str): text version, eg '15 IBU'

    Returns:
        int: IBU as a number
    """
    try:
        return int(parse.search("{:d} IBU", ibu_data)[0])
    except TypeError:
        return None


def parsed_value(fmt: str, string: str) -> str | int | float | None:
    """Search for a value in a string and return it.

    Args:
        fmt (str): parse module's format string
        string (str): string to search for fmt pattern

    Returns:
        found value, if any
    """
    match = parse.search(fmt, string)
    return match[0] if match else None
