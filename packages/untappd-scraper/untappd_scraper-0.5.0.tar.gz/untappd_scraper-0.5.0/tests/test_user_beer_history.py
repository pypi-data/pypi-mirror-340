"""Test user beer history."""

from __future__ import annotations

import pytest
from bs4 import BeautifulSoup

from untappd_scraper.constants import UNTAPPD_BEER_HISTORY_SIZE
from untappd_scraper.structs.web import WebUserHistoryBeer
from untappd_scraper.user_beer_history import id_from_href2, load_user_beer_history

# ----- Tests -----


@pytest.mark.usefixtures("_mock_user_beer_history_get")
def test_load_user_beer_history() -> None:
    result = load_user_beer_history("test")

    assert result
    assert len(result) == UNTAPPD_BEER_HISTORY_SIZE
    assert isinstance(next(iter(result.values())), WebUserHistoryBeer)


def test_id_from_href2() -> None:
    html = """
    <a class="track-click" data-track="distinctbeers" data-href=":firstCheckin" 
        href="/user/mw1414/checkin/1125035430/"><abbr class="">01/30/22</abbr></a>
        """

    soup = BeautifulSoup(html, "html.parser")

    result = id_from_href2(soup)

    assert result == 1125035430


def test_id_from_href2_invalid() -> None:
    html = """
    <a href="nowhere" class="beer-name">Beer Name</a>
    """
    soup = BeautifulSoup(html, "html.parser")

    result = id_from_href2(soup)

    assert result is None


def test_id_from_href2_missing() -> None:
    html = """
    <a data-href="/beer/1234567" class="beer-name">Beer Name</a>
    """
    soup = BeautifulSoup(html, "html.parser")

    result = id_from_href2(soup)

    assert result is None
