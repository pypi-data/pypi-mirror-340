"""Untappd user functions."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from core.mixins import SimpleRepr

from untappd_scraper.beer import checkin_activity
from untappd_scraper.html_session import get
from untappd_scraper.structs.web import (
    WebActivityBeer,
    WebUserDetails,
    WebUserHistoryBeer,
    WebUserHistoryVenue,
)
from untappd_scraper.user_beer_history import load_user_beer_history
from untappd_scraper.user_lists import WebUserList, load_user_lists, scrape_list_beers
from untappd_scraper.user_utils import url_of
from untappd_scraper.user_venue_history import load_user_venue_history

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Collection, Mapping

    from requests_html import HTMLResponse


class User(SimpleRepr):
    """Untappd user."""

    def __init__(self, user_id: str) -> None:
        """Initiate a User object, storing the user ID and loading details.

        Raises:
            ValueError: invalid user id

        Args:
            user_id (str): user ID
        """
        self.user_id = user_id

        self._page: HTMLResponse = get(url_of(user_id))
        if not self._page.ok:
            msg = f"Invalid userid {user_id} ({self._page})"
            raise ValueError(msg)
        self._user_details: WebUserDetails = user_details(resp=self._page)

        self._activity_details: tuple[WebActivityBeer, ...] | None = None
        self._beer_history: Mapping[int, WebUserHistoryBeer] = {}
        self._lists: list[WebUserList] = []
        self._venue_history: Collection[WebUserHistoryVenue] = set()

    def activity(self) -> tuple[WebActivityBeer, ...]:
        """Return a user's recent checkins.

        Returns:
            tuple[WebActivityBeer]: last 5 (or so) checkins
        """
        if self._activity_details is None:
            self._activity_details = tuple(checkin_activity(self._page))

        return self._activity_details

    def beer_history(self) -> Collection[WebUserHistoryBeer]:
        """Scrape last 25 (or so) of a user's uniques.

        Returns:
            Collection[WebUserHistoryBeer]: user's recent uniques
        """
        if not self._beer_history:
            self._beer_history = load_user_beer_history(self.user_id)

        return self._beer_history.values()

    def lists(self) -> list[WebUserList]:
        """Scrape user's list page and return all visible listed beers.

        Returns:
            Collection[WebUserList]: all user's lists with 15 (or so) visible beers
        """
        if not self._lists:
            self._lists = load_user_lists(self.user_id)

        return self._lists

    def lists_detail(self, list_name: str) -> list[WebUserList]:
        """Return populated details of a user's list.

        Args:
            list_name (str): list name (or part thereof, case-insensitive)

        Returns:
            list[WebUserList]: matching lists with detail filled in
        """
        matching = [
            user_list
            for user_list in self.lists()
            if list_name.casefold() in user_list.name.casefold()
        ]

        for user_list in matching:
            user_list.beers.update(scrape_list_beers(user_list))

        return matching

    def venue_history(self) -> Collection[WebUserHistoryVenue]:
        """Scrape last 25 (or so) of a user's visited venues.

        Returns:
            Collection[WebUserHistoryVenue]: user's recent venues
        """
        if not self._venue_history:
            self._venue_history = load_user_venue_history(self.user_id)

        return self._venue_history

    def __getattr__(self, name: str) -> Any:
        """Return unknown attributes from user details.

        Args:
            name (str): attribute to lookup

        Returns:
            Any: attribute value
        """
        return getattr(self._user_details, name)


# ----- user details processing -----


def user_details(resp: HTMLResponse) -> WebUserDetails:
    """Parse a user's main page into user details.

    Args:
        resp (HTMLResponse): user's main page loaded

    Returns:
        WebUserDetails: general user details
    """
    user_info_el = resp.html.find(".user-info .info", first=True)
    user_name = user_info_el.find("h1", first=True).text.strip()
    user_id = user_info_el.find(".user-details p.username", first=True).text
    user_location = user_info_el.find(".user-details p.location", first=True).text

    stats_el = user_info_el.find(".stats", first=True)
    total_beers = stats_el.find('[data-href=":stats/general"] span', first=True).text
    total_uniques = stats_el.find('[data-href=":stats/beerhistory"] span', first=True).text
    total_badges = stats_el.find('[data-href=":stats/badges"] span', first=True).text
    total_friends = stats_el.find('[data-href=":stats/friends"] span', first=True).text

    return WebUserDetails(
        user_id=user_id,
        name=user_name,
        location=user_location,
        url=user_info_el.url,
        total_beers=str_to_int(total_beers),
        total_uniques=str_to_int(total_uniques),
        total_badges=str_to_int(total_badges),
        total_friends=str_to_int(total_friends),
    )


def str_to_int(numeric_string: str) -> int:
    """Convert a string to an integer.

    Args:
        numeric_string (str): amount with commas

    Returns:
        int: value as an integer
    """
    return int(numeric_string.replace(",", ""))
