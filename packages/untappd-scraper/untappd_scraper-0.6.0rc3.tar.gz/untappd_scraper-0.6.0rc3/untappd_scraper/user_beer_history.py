"""Untappd user beer history functions."""

from __future__ import annotations

import logging
import random
import time
import warnings
from contextlib import suppress
from datetime import datetime
from typing import TYPE_CHECKING, Any, Final
from urllib.parse import urljoin

import parse
from bs4 import BeautifulSoup, Tag
from dateutil.parser import parse as parse_date
from pydantic import computed_field, dataclasses

from untappd_scraper.client import client
from untappd_scraper.constants import UNTAPPD_BASE_URL, UNTAPPD_BEER_HISTORY_SIZE
from untappd_scraper.html_session import get
from untappd_scraper.logging_config import configure_logging, logger
from untappd_scraper.structs.web import WebUserHistoryBeer
from untappd_scraper.web import id_from_href, make_soup, parse_abv, parse_ibu, url_of

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Collection, Iterable, Mapping, Sequence

    from requests_html import Element, HTMLResponse

configure_logging(
    __name__
)  # TODO this should be moved to the top?  unless we're csalling here direct but shouldn't

logging.getLogger("parse").setLevel(logging.INFO)

logger.info("Loading user beer history...")


def load_user_beer_history(user_id: str) -> Mapping[int, WebUserHistoryBeer]:
    """[DEPRECATED] Use `user_history2` instead.

    Load all availble recent uniques for a user.

    Args:
        user_id (str): user ID to load

    Returns:
        Mapping[int, WebUserHistoryBeer]: last 25 (or so) uniques indexed by beer_id
    """
    warnings.warn(
        "load_user_beer_history() is deprecated and will be removed in a future release. "
        "Use `user_history2()` instead.",
        category=DeprecationWarning,
        stacklevel=2,
    )

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


def parse_web_user_history_beer(beer_item: Tag) -> WebUserHistoryBeer:
    """Parse beer details from a scraped history beer."""
    bid = int(str(beer_item["data-bid"]))

    if name_el := beer_item.select_one(".beer-details p.name a"):
        name = str(name_el.text).strip()
        url = urljoin(UNTAPPD_BASE_URL, str(name_el["href"]))
    else:  # pragma: no cover
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
    else:  # pragma: no cover
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
    else:  # pragma: no cover
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


@dataclasses.dataclass(frozen=True)
class UserHistoryResponse:
    """Response for user beer history."""

    total_expected: int
    results: list[WebUserHistoryBeer]

    @computed_field
    @property
    def total_found(self) -> int:
        """Return number of beers found."""
        return len(self.results)

    @computed_field
    @property
    def found_all(self) -> bool:
        """Return True if we found all beers."""
        return self.total_found >= self.total_expected

    def __repr__(self) -> str:
        """Don't show all the beers. There's heaps."""
        return (
            f"{self.__class__.__name__}("
            f"total_expected={self.total_expected}, "
            f"total_found={self.total_found}, "
            f"found_all={self.found_all}"
            ")"
        )


def user_history2(user_id: str) -> UserHistoryResponse:
    """Scrape the beer history of a user.

    This is expected to be the last 25 unique beers they've had.
    """
    soup = make_soup(url_of(user_id, page="beers"))

    return UserHistoryResponse(
        total_expected=UNTAPPD_BEER_HISTORY_SIZE,
        results=[parse_web_user_history_beer(item) for item in soup.select(".beer-item")],
    )


def user_brewery_history(
    user_id: str, brewery_id: int, max_resorts: int = 0, *, switch_to_style_scrape: int = 3
) -> UserHistoryResponse:
    """Scrape the beer history of a user for a specific brewery.

    This will agressively re-sort the list (if requested) to extract more uniques.
    It will also filter by style once the number of unfound beers reduces.

    Args:
        user_id (str): user ID to load
        brewery_id (int): brewery ID to filter by
        max_resorts (int): how many times to re-sort the list to get more uniques
        switch_to_style_scrape (int): if this many missing styles, switch to style scrape

    Returns:
        UserHistoryResponse: all found beers user has had from this brewery
    """
    soup = make_soup(url_of(user_id, page="beers", query={"brewery_id": brewery_id}))

    # add 1 to re-sorts to include initial sort "date"
    sort_keys = extract_sort_keys(soup, num_keys=max_resorts + 1, exclude=["brewery"])
    beers_per_brewery = calc_beers_per_brewery(soup)
    beers_per_style, style_to_id = calc_beers_per_style(soup)
    total_for_brewery = beers_per_brewery.get(brewery_id, 0)
    logger.debug("Beers per brewery {}: {}", brewery_id, total_for_brewery)

    # The first page already has unique beers. Processing below is for re-sorts
    beers = {parse_web_user_history_beer(item) for item in soup.select(".beer-item")}

    if (
        len(beers) >= UNTAPPD_BEER_HISTORY_SIZE  # filled a page, there may be more
        and len(beers) < total_for_brewery  # not all beers
        and max_resorts  # user requested re-sorts
    ):
        beers, missing_styles = run_brewery_resorts(
            ReSortContext(user_id, brewery_id, sort_keys, beers, switch_to_style_scrape),
            total_for_brewery=total_for_brewery,
            beers_per_style=beers_per_style,
        )

        if missing_styles:
            logger.debug("Switching to style scraping. Missing styles: {}", missing_styles)

            beers = run_style_resorts(
                ReSortContext(user_id, brewery_id, sort_keys, beers, switch_to_style_scrape),
                missing_styles=missing_styles,
                style_to_id=style_to_id,
            )

    return UserHistoryResponse(
        total_expected=total_for_brewery, results=sorted(beers, key=lambda x: x.beer_id)
    )


@dataclasses.dataclass(frozen=True)
class ReSortContext:
    """Args passed around for re-sorting."""

    user_id: str
    brewery_id: int
    sort_keys: list[str]
    beers: set[WebUserHistoryBeer]
    switch_to_style_scrape: int


def run_brewery_resorts(
    context: ReSortContext, *, total_for_brewery: int, beers_per_style: dict[str, int]
) -> tuple[set[WebUserHistoryBeer], dict[str, int]]:
    """Run the brewery re-sorts to get more beers."""
    missing_styles: dict[str, int] = {}

    for sort_key in context.sort_keys:
        if sort_key == "date":
            continue  # already tried this one implicitly
        logger.debug("Trying sort key {}", sort_key)

        soup = make_soup(
            url_of(
                context.user_id,
                page="beers",
                query={"brewery_id": context.brewery_id, "sort": sort_key},
            )
        )
        fetched = {parse_web_user_history_beer(item) for item in soup.select(".beer-item")}
        context.beers.update(fetched)
        logger.debug("Now got {} beers", len(context.beers))

        if len(context.beers) >= total_for_brewery:
            logger.debug("Got all beers for brewery {}", context.brewery_id)
            break

        missing_styles = calc_missing_styles(context.beers, beers_per_style)
        if len(missing_styles) <= context.switch_to_style_scrape:
            logger.debug("Switching to style scraping. Missing styles: {}", missing_styles)
            break

        logger.debug("sleeping...")
        time.sleep(random.uniform(1, 3))  # noqa: S311
        logger.debug("awake")

    return context.beers, missing_styles


def run_style_resorts(
    context: ReSortContext, *, missing_styles: dict[str, int], style_to_id: dict[str, int]
) -> set[WebUserHistoryBeer]:
    """Run the style re-sorts to get more beers."""
    # Don't want to go wild here. Let's just get the "n" most popular styles
    styles = sorted(missing_styles.items(), key=lambda x: x[1], reverse=True)[
        : context.switch_to_style_scrape
    ]
    for style, num_in_style in styles:
        logger.debug("Trying style {} with {} beers", style, num_in_style)
        for sort_key in context.sort_keys:
            logger.debug("Trying sort key {} for style {}", sort_key, style)
            soup = make_soup(
                url_of(
                    context.user_id,
                    page="beers",
                    query={
                        "brewery_id": context.brewery_id,
                        "sort": sort_key,
                        "type_id": style_to_id[style],
                    },
                )
            )
            fetched = {parse_web_user_history_beer(item) for item in soup.select(".beer-item")}
            context.beers.update(fetched)
            logger.debug("Now got {} beers", len(context.beers))

            beers_of_style = sum(b.style == style for b in context.beers)
            if beers_of_style >= num_in_style:
                logger.debug("Got all beers of style {}", style)
                break

            logger.debug("sleeping...")
            time.sleep(random.uniform(1, 3))  # noqa: S311
            logger.debug("awake")

    return context.beers


def user_brewery_history_x(
    user_id: str, brewery_id: int, max_resorts: int = 0
) -> list[WebUserHistoryBeer]:
    """Scrape the beer history of a user for a specific brewery.

    This will agressively re-sort the list (if requested) to extract more uniques.
    It will also filter by style once the number of unfound beers reduces.

    Args:
        user_id (str): user ID to load
        brewery_id (int): brewery ID to filter by
        max_resorts (int): how many times to re-sort the list to get more uniques

    Returns:
        list[WebUserHistoryBeer]: all found beers user has had from this brewery
    """
    # First page has sort keys, total uniques and uniques per style
    soup = make_soup(url_of(user_id, page="beers", query={"brewery_id": brewery_id}))

    sort_keys = extract_sort_keys(soup, num_keys=max_resorts, exclude=["brewery"])
    beers_per_brewery = calc_beers_per_brewery(soup)
    beers_per_style, style_to_id = calc_beers_per_style(soup)

    # The first page already has unique beers. Processing below is for re-sorts
    beers = {parse_web_user_history_beer(item) for item in soup.select(".beer-item")}

    if len(beers) < UNTAPPD_BEER_HISTORY_SIZE:
        # No need to scrape any more pages, we got all the beers already
        return sorted(beers, key=lambda x: x.beer_id)

    # ----- Re-sorting to get blood out of a stone -----

    soups = (
        make_soup(
            url_of(user_id, page="beers", query={"brewery_id": brewery_id, "sort": sort_key})
        )
        for sort_key in sort_keys
    )

    total_for_brewery = beers_per_brewery.get(brewery_id, 0)
    missing_styles = {}
    not_many_missing: Final = 3

    for soup in soups:
        fetched = {parse_web_user_history_beer(item) for item in soup.select(".beer-item")}
        beers.update(fetched)

        if len(beers) >= total_for_brewery:
            break

        # Once we get down to only a few styles missing, switch to style-based filtering
        missing_styles = calc_missing_styles(beers, beers_per_style)
        if len(missing_styles) <= not_many_missing:
            break

        # TODO sleep

    # ----- Style-based filtering -----

    for style, num_in_style in missing_styles.items():
        soups = (
            make_soup(
                url_of(
                    user_id,
                    page="beers",
                    query={
                        "brewery_id": brewery_id,
                        "sort": sort_key,
                        "type_id": style_to_id[style],
                    },
                )
            )
            for sort_key in sort_keys
        )

        for soup in soups:
            fetched = {parse_web_user_history_beer(item) for item in soup.select(".beer-item")}
            beers.update(fetched)

            beers_of_style = sum(b.style == style for b in beers)
            if beers_of_style >= num_in_style:
                # We got all the beers of this style, so stop
                logger.debug("Got all beers of style {}", style)
                break

    return sorted(beers, key=lambda x: x.beer_id)


def history_details(
    history_item: Element,
) -> WebUserHistoryBeer:  # TODO should go to next style
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


def load_user_beer_history_more(
    user_id: str, *, brewery_id: int | None = None, max_resorts: int = 0
) -> list[WebUserHistoryBeer]:
    """Load user's unique beer history, with filters and more effort.

    Args:
        user_id (str): user ID to load
        brewery_id (int|None): optional brewery ID to filter by
        max_resorts (0-15): how many times to re-sort the list to get more

    Returns:
        list[WebUserHistoryBeer]: filtered uniques, possibly from multiple sort orders
    """
    params = {}
    if brewery_id:
        params["brewery_id"] = brewery_id

    soup, initial_beers = fetch_sorted_beers(user_id=user_id, params=params)
    sort_keys = extract_sort_keys(soup, num_keys=max_resorts)
    beers_per_brewery = calc_beers_per_brewery(soup)
    beers_per_style, style_to_id = calc_beers_per_style(soup)

    beers: set[WebUserHistoryBeer] = set(initial_beers)

    for sort_key in sort_keys:
        old_len = len(beers)
        logger.debug("Got {} beers already", old_len)
        if old_len < UNTAPPD_BEER_HISTORY_SIZE:  # TODO move this out
            break  # not even filled the first page
        if brewery_id and old_len >= beers_per_brewery.get(brewery_id, 0):
            logger.debug(
                "Think we found all {} beers. Got {} of {}",
                brewery_id,
                old_len,
                beers_per_brewery[brewery_id],
            )
            break  # found them all already!
        logger.debug("Trying sort key {}", sort_key)
        fetched = fetch_sorted_beers(sort_key, user_id=user_id, params=params)[1]
        beers.update(fetched)

        missing_styles = calc_missing_styles(beers, beers_per_style)
        if len(missing_styles) < 3 and all(
            s < UNTAPPD_BEER_HISTORY_SIZE for s in missing_styles.values()
        ):
            # TODO what if we have more than 25 of a style but only 1 style left :(
            # could do the whole sort thing again. this needs to be split out
            # Could actually make a generator with all the options already worked out
            # and skip when had enough. Or two generators - brewery, then brewery and styles
            # But we don't know what styles we'd want. So generate after the style
            # calculation
            print("should try styles")

        # if len(beers) == old_len:
        # break  # no new beers, give it up

        # sleep a random few seconds
        # time.sleep(random.uniform(1, 3))

    return sorted(beers, key=lambda x: x.first_checkin_id, reverse=True)


def extract_sort_keys(
    soup: BeautifulSoup, num_keys: int, *, exclude: Sequence[str] = ()
) -> list[str]:
    """Extract the sort keys from the page.

    Args:
        soup (BeautifulSoup): soup object to parse
        num_keys (NumReSorts): how many sort keys to return
        exclude (Sequence[str]): sort keys to exclude

    Returns:
        list[str]: list of sort keys to try, based on effort
    """
    sorting = soup.select_one("ul.menu-sorting")
    if not sorting:
        return []  # pragma: no cover
    sort_keys = [str(item["data-sort-key"]) for item in sorting.select("li.sort-items")]

    # "date" is default, so move it to the front
    if "date_asc" in sort_keys:
        sort_keys.remove("date_asc")
        sort_keys.insert(0, "date_asc")
    if "date" in sort_keys:
        sort_keys.remove("date")
        sort_keys.insert(0, "date")

    # remove any sort that matches our exclude list
    to_remove = [key for key in sort_keys if any(key.startswith(excl) for excl in exclude)]
    for key in to_remove:
        sort_keys.remove(key)

    return sort_keys[:num_keys]


# TODO also write one of these for style
# TODO think about what styles we have and what's missing
# NOTE these numbers don't seem to line up
def calc_beers_per_brewery(soup: BeautifulSoup) -> dict[int, int]:
    """Calculate the number of beers per brewery based of the pull down option text.

    Tag looks like `<option value="4792">Hallertau Brewery (3)</option>`

    Args:
        soup (BeautifulSoup): soup object to parse. Should be main beer history page.

    Returns:
        dict[int, int]: brewery ID to number of beers
    """
    beers: dict[int, int] = {}

    options = soup.select("#brewery_picker option")

    for option in options:
        if option["value"] == "all":
            continue
        brewery_id = int(str(option["value"]))
        if brewery_count := parse.search(r"({:d})", str(option.text)):
            assert isinstance(brewery_count, parse.Result)
            beers[brewery_id] = int(brewery_count[0])

    return beers


def calc_beers_per_style(soup: BeautifulSoup) -> tuple[dict[str, int], dict[str, int]]:
    """Calculate the number of beers per style based of the pull down option text.

    Tag looks like `<option value="128">IPA - American (12)</option>`

    Args:
        soup (BeautifulSoup): soup object to parse. Should be main beer history page.

    Returns:
        tuple[dict[str, int], dict[str, int]]: style to # beers, style to ID
    """
    beers: dict[str, int] = {}
    id_of_style: dict[str, int] = {}

    options = soup.select("#style_picker option")

    for option in options:
        if option["value"] == "all":
            continue
        style_info = parse.parse("{style} ({count:d})", str(option.text))
        if isinstance(style_info, parse.Result):
            beers[style_info["style"]] = int(style_info["count"])
            id_of_style[style_info["style"]] = int(str(option["value"]))

    return beers, id_of_style


def calc_missing_styles(
    beers: Iterable[WebUserHistoryBeer], beers_per_style: dict[str, int]
) -> dict[str, int]:
    """Calculate how many beers per style have not yet been scraped.

    Args:
        beers (Iterable[WebUserHistoryBeer]): beers already scraped
        style_counts (dict[str,int]): number of beers per style user has had
    """
    missing_styles = {
        style: expected
        for style, expected in beers_per_style.items()
        if sum(b.style == style for b in beers) < expected
    }

    return missing_styles


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

    return soup, [parse_web_user_history_beer(item) for item in soup.select("div.beer-item")]


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
    with suppress(IndexError, KeyError):
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
