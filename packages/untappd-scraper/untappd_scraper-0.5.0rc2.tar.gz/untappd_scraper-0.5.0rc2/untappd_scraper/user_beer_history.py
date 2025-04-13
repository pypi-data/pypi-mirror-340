"""Untappd user beer history functions."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Literal
from urllib.parse import urljoin

import parse
from bs4 import BeautifulSoup, Tag
from dateutil.parser import parse as parse_date

from untappd_scraper.client import client
from untappd_scraper.constants import UNTAPPD_BASE_URL
from untappd_scraper.html_session import get
from untappd_scraper.structs.web import WebUserHistoryBeer
from untappd_scraper.user_utils import url_of
from untappd_scraper.web import id_from_href, parse_abv, parse_ibu

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
    resp = get(url_of(user_id, page="beers"))  # pyright: ignore[reportArgumentType]

    return {beer.beer_id: beer for beer in user_history(resp)}  # pyright: ignore[reportArgumentType]


def user_history(resp: HTMLResponse) -> Collection[WebUserHistoryBeer]:
    """Parse each history beer on this page.

    Args:
        resp (HTMLResponse): page to scrape

    Returns:
        Collection[WebUserHistoryBeer]: each beer found in history
    """
    return {history_details(history) for history in resp.html.find(".beer-item")}  # pyright: ignore[reportGeneralTypeIssues]


def history_details(history_item: Element) -> WebUserHistoryBeer:
    """Extract beer details from a had beer.

    Args:
        history_item (Element): single had beer from user's history

    Returns:
        WebUserHistoryBeer: Interesting details for a had beer
    """
    beer_name_el = history_item.find(".name a", first=True)
    beer_name = beer_name_el.text  # pyright: ignore[reportAttributeAccessIssue]
    beer_url = beer_name_el.absolute_links.pop()  # pyright: ignore[reportAttributeAccessIssue]

    brewery_a = history_item.find(".brewery a", first=True)
    brewery = brewery_a.text  # pyright: ignore[reportAttributeAccessIssue]

    rating_text = history_item.find(".beer-details .ratings", first=True).text  # pyright: ignore[reportAttributeAccessIssue]

    dates = history_item.find(".details .date")
    first_checkin = parse_date(dates[0].find(".date-time", first=True).text)  # pyright: ignore[reportIndexIssue, reportAttributeAccessIssue]
    first_checkin_id = id_from_href(dates[0].find("a", first=True))  # pyright: ignore[reportIndexIssue, reportArgumentType]
    recent_checkin = parse_date(dates[1].find(".date-time", first=True).text)  # pyright: ignore[reportIndexIssue, reportAttributeAccessIssue]
    recent_checkin_id = id_from_href(dates[1].find("a", first=True))  # pyright: ignore[reportIndexIssue, reportArgumentType]

    abv = parse_abv(history_item.find(".details .abv", first=True).text)  # pyright: ignore[reportAttributeAccessIssue]
    ibu = parse_ibu(history_item.find(".details .ibu", first=True).text)  # pyright: ignore[reportAttributeAccessIssue]

    total_checkins = parse.search(  # pyright: ignore[reportOptionalSubscript, reportIndexIssue]
        "Total: {:d}",
        history_item.find(".details p.check-ins", first=True).text,  # pyright: ignore[reportAttributeAccessIssue]
    )[0]

    return WebUserHistoryBeer(
        beer_id=int(history_item.attrs["data-bid"]),
        name=beer_name,
        brewery=brewery,
        style=history_item.find(".beer-details .style", first=True).text,  # pyright: ignore[reportAttributeAccessIssue]
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


NumReSorts = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]


def load_user_beer_history_more(
    user_id: str, *, brewery_id: int | None = None, max_resort: NumReSorts = 0
) -> list[WebUserHistoryBeer]:
    """Load user's unique beer history, with filters and more effort.

    Args:
        user_id (str): user ID to load
        brewery_id (int|None): optional brewery ID to filter by
        max_resort (0-15): how many times to re-sort the list to get more

    Returns:
        list[WebUserHistoryBeer]: filtered uniques, possibly from multiple sort orders
    """
    params = {}
    if brewery_id:
        params["brewery_id"] = brewery_id

    soup, initial_beers = fetch_sorted_beers(user_id=user_id, params=params)
    sort_keys = extract_sort_keys(soup, num_keys=max_resort)

    beers: set[WebUserHistoryBeer] = set(initial_beers)

    for sort_key in sort_keys:
        old_len = len(beers)
        fetched = fetch_sorted_beers(sort_key, user_id=user_id, params=params)[1]
        beers.update(fetched)
        if len(beers) == old_len:
            break  # no new beers, give it up

    return sorted(beers, key=lambda x: x.first_checkin_id, reverse=True)


def extract_sort_keys(soup: BeautifulSoup, num_keys: NumReSorts) -> list[str]:
    """Extract the sort keys from the page.

    Args:
        soup (BeautifulSoup): soup object to parse
        num_keys (NumReSorts): how many sort keys to return

    Returns:
        list[str]: list of sort keys to try, based on effort
    """
    sorting = soup.select_one("ul.menu-sorting")
    if not sorting:
        return []
    sort_keys = [str(item["data-sort-key"]) for item in sorting.select("li.sort-items")]

    # "date" is default, so move it to the front
    if "date_asc" in sort_keys:
        sort_keys.remove("date_asc")
        sort_keys.insert(0, "date_asc")
    if "date" in sort_keys:
        sort_keys.remove("date")
        # don't re-insert as it's default and already queried

    return sort_keys[:num_keys]


def fetch_sorted_beers(
    sort_key: str | None = None, *, user_id: str, params: dict[str, Any] | None = None
) -> tuple[BeautifulSoup, list[WebUserHistoryBeer]]:
    """Fetch beers sorted by the given key.

    Args:
        sort_key (str|None): sort key to use, or None for default
        user_id (str): user ID to load
        params (dict[str, Any]|None): additional query parameters

    Returns:
        tuple[BeautifulSoup, list[WebUserHistoryBeer]]: soup object and beers
    """
    params_with_sort = params or {}

    if sort_key:
        params_with_sort["sort"] = sort_key
    url = url_of(user_id, page="beers", query=params_with_sort)

    resp = client.get(url, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    return soup, [history_details_more(item) for item in soup.select("div.beer-item")]


def history_details_more(beer_item: Tag) -> WebUserHistoryBeer:
    """Extract beer details from a had beer."""
    bid = int(str(beer_item["data-bid"]))

    if name_el := beer_item.select_one(".beer-details p.name a"):
        name = str(name_el.text).strip()
        url = urljoin(UNTAPPD_BASE_URL, str(name_el["href"]))
    else:
        name = ""
        url = None

    # Brewery
    brewery_el = beer_item.select_one(".beer-details p.brewery a")
    brewery = str(brewery_el.text.strip() if brewery_el else "")

    # Style
    style_el = beer_item.select_one(".beer-details p.style")
    style = str(style_el.text.strip() if style_el else "")

    # First/Recent check-in dates
    date_els = beer_item.select(".details p.date")
    if len(date_els) == 2:  # noqa: PLR2004
        first, recent = date_els

        first_checkin = date_from_details(first)
        recent_checkin = date_from_details(recent)
        first_checkin_id = id_from_href2(first)
        recent_checkin_id = id_from_href2(recent)
    else:
        first_checkin = None
        first_checkin_id = None
        recent_checkin = None
        recent_checkin_id = None

    total_checkins = 0
    total_el = beer_item.select_one(".details p.check-ins")
    if total_el and (total := parse.search("Total: {:d}", str(total_el.text))):
        assert isinstance(total, parse.Result)
        total_checkins = total[0]

    # Ratings
    if ratings := beer_item.select_one(".ratings"):
        user_rating = parse_rating("their", ratings.text)
        global_rating = parse_rating("global", ratings.text)
    else:
        user_rating = None
        global_rating = None

    # ABV
    abv_el = beer_item.select_one(".details p.abv")
    abv = parse_abv(str(abv_el.text)) if abv_el else None

    # IBU
    ibu_el = beer_item.select_one(".details p.ibu")
    ibu = parse_ibu(str(ibu_el.text)) if ibu_el else None

    return WebUserHistoryBeer(
        beer_id=bid,
        name=name,
        brewery=brewery,
        style=style,
        url=url,
        first_checkin=first_checkin or datetime.min,
        first_checkin_id=first_checkin_id or 0,
        recent_checkin=recent_checkin or datetime.min,
        recent_checkin_id=recent_checkin_id or 0,
        total_checkins=total_checkins,
        user_rating=user_rating,
        global_rating=global_rating,
        abv=float(abv) if abv else None,
        ibu=ibu,
    )


# TODO should these go in web.py?
def date_from_details(details: Tag) -> datetime | None:
    """Extract a date that may be present.

    Args:
        details (Tag): html element containing date

    Returns:
        datetime: parsed date
    """
    dt = details.select_one(".date-time")

    return parse_date(dt.text) if dt else None


def id_from_href2(details: Tag) -> int | None:
    """Extract the ID from a data-href.

    Args:
        details (Tag): html element containing date

    Returns:
        int: parsed ID
    """
    if href := details.a and details.a["href"]:
        # grab the checkin ID from, eg, '/user/mw1414/checkin/1469499948/'
        split = str(href).split("/")

        return int(split[-2])

    return None


def parse_rating(which: str, ratings: str) -> float | None:
    """Find the requested rating in the supplied string.

    Args:
        which (str): which rating to look for
        ratings (str): full rating string with all ratings

    Returns:
        float: rating found, if any
    """
    ratings_match = parse.search(which + " rating ({:g})", ratings)
    return ratings_match[0] if ratings_match else None  # pyright: ignore[reportIndexIssue]
