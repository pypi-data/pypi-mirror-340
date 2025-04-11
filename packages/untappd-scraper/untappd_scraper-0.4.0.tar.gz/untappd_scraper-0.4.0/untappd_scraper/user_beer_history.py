"""Untappd user beer history functions."""

from __future__ import annotations

from typing import TYPE_CHECKING

import parse
from dateutil.parser import parse as parse_date

from untappd_scraper.html_session import get
from untappd_scraper.structs.web import WebUserHistoryBeer
from untappd_scraper.user_utils import url_of
from untappd_scraper.web import id_from_href, parse_abv, parse_ibu, slug_from_href

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Collection, Mapping

    from requests_html import Element, HTMLResponse


def load_user_beer_history(user_id: str) -> Mapping[int, WebUserHistoryBeer]:
    """Load all availble recent uniques for a user.

    Args:
        user_id (str): user ID to load

    Returns:
        Mapping[int, WebUserHistoryBeer]: last 25 (or so) uniques indexed by beer_id
    """
    resp = get(url_of(user_id, page="beers"))

    return {beer.beer_id: beer for beer in user_history(resp)}


def user_history(resp: HTMLResponse) -> Collection[WebUserHistoryBeer]:
    """Parse each history beer on this page.

    Args:
        resp (HTMLResponse): page to scrape

    Returns:
        Collection[WebUserHistoryBeer]: each beer found in history
    """
    return {history_details(history) for history in resp.html.find(".beer-item")}


def history_details(history_item: Element) -> WebUserHistoryBeer:
    """Extract beer details from a had beer.

    Args:
        history_item (Element): single had beer from user's history

    Returns:
        WebUserHistoryBeer: Interesting details for a had beer
    """
    beer_name_el = history_item.find(".name a", first=True)
    beer_name = beer_name_el.text
    beer_url = beer_name_el.absolute_links.pop()

    brewery_a = history_item.find(".brewery a", first=True)
    brewery = brewery_a.text
    brewery_slug = slug_from_href(brewery_a)

    rating_text = history_item.find(".beer-details .ratings", first=True).text

    dates = history_item.find(".details .date")
    first_checkin = parse_date(dates[0].find(".date-time", first=True).text)
    first_checkin_id = id_from_href(dates[0].find("a", first=True))
    recent_checkin = parse_date(dates[1].find(".date-time", first=True).text)
    recent_checkin_id = id_from_href(dates[1].find("a", first=True))

    abv = parse_abv(history_item.find(".details .abv", first=True).text)
    ibu = parse_ibu(history_item.find(".details .ibu", first=True).text)

    total_checkins = parse.search(
        "Total: {:d}", history_item.find(".details p.check-ins", first=True).text
    )[0]

    return WebUserHistoryBeer(
        beer_id=int(history_item.attrs["data-bid"]),
        name=beer_name,
        brewery=brewery,
        brewery_slug=brewery_slug,
        style=history_item.find(".beer-details .style", first=True).text,
        url=beer_url,
        first_checkin=first_checkin,
        first_checkin_id=first_checkin_id,
        recent_checkin=recent_checkin,
        recent_checkin_id=recent_checkin_id,
        total_checkins=total_checkins,
        user_rating=parse_rating("their", rating_text),
        global_rating=parse_rating("global", rating_text),
        abv=abv,
        ibu=ibu,
    )


def parse_rating(which: str, ratings: str) -> float | None:
    """Find the requested rating in the supplied string.

    Args:
        which (str): which rating to look for
        ratings (str): full rating string with all ratings

    Returns:
        float: rating found, if any
    """
    ratings_match = parse.search(which + " rating ({:g})", ratings)
    if ratings_match:
        return ratings_match[0]

    return None
