"""Test user scraping."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from untappd_scraper.constants import UNTAPPD_BEER_HISTORY_SIZE
from untappd_scraper.user import User
from untappd_scraper.user_lists import WebUserList

# sourcery skip: dont-import-test-modules
if TYPE_CHECKING:  # pragma: no cover
    from tests.conftest import MockResponse


@pytest.fixture
def user(
    _mock_user_get: None,
    _mock_user_beer_history_get: None,
    _mock_user_venue_history_get: None,
    _mock_user_lists_get: None,
) -> User:
    return User("test")


# ----- Tests -----


def test_user(user: User) -> None:
    result = user

    assert result
    assert result.name
    assert result.user_id


@pytest.mark.usefixtures("_mock_user_404")
def test_user_invalid() -> None:
    with pytest.raises(ValueError, match="Invalid"):
        User("123")  # ignored


def test_activity(user: User) -> None:
    result = user.activity()

    assert result
    assert result[0].checkin_id
    assert result[0].beer_id


def test_beer_history(user: User) -> None:
    history = user.beer_history()
    assert history
    assert len(history) == UNTAPPD_BEER_HISTORY_SIZE

    result = next(iter(history))

    assert result
    assert result.name
    assert result.brewery
    assert result.recent_checkin_id


# NOTE: live web scraping
# TODO: add a mark to make this test optional
def test_beer_history_more_lots() -> None:
    """Test the new improved history."""
    user = User("mw1414")

    # As of Apr 2025, Wardy had 68 bucketty's beers
    # So, 5 resorts should be too many and it should give up
    result = user.beer_history_more(brewery_id=484738, max_resorts=5)

    assert len(result) > UNTAPPD_BEER_HISTORY_SIZE * 2
    assert all("Bucketty" in r.brewery for r in result)


# NOTE: live web scraping
# TODO: add a mark to make this test optional
def test_beer_history_more_not_many() -> None:
    """Test the new improved history."""
    user = User("mw1414")

    # As of Apr 2025, Wardy had 2 Ten Toes beers
    # So, it should give up after the first query and no re-sorts
    result = user.beer_history_more(brewery_id=253657, max_resorts=5)

    assert len(result) < UNTAPPD_BEER_HISTORY_SIZE
    assert all("Toes" in r.brewery for r in result)


def test_lists(user: User) -> None:
    lists = user.lists()
    assert len(lists) == 13

    result = lists[0]

    assert result.description
    assert result.num_items


def test_lists_detail(
    user: User,
    list_page_1_resp: MockResponse,
    list_page_2_resp: MockResponse,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    lists = user.lists()
    fridge = lists[1]  # should be fridge
    monkeypatch.setattr(
        "untappd_scraper.user_lists.list_page_all_sorts",
        lambda _: (list_page_1_resp, list_page_2_resp),
    )  # pyright: ignore[reportCallIssue]
    lists = user.lists_detail(fridge.name)
    assert len(lists) == 1

    result = lists[0]

    assert isinstance(result, WebUserList)
    assert len(result.beers) == result.num_items
    assert result.full_scrape


def test_venue_history(user: User) -> None:
    history = user.venue_history()
    assert len(history) == UNTAPPD_BEER_HISTORY_SIZE

    result = next(iter(history))

    assert result.venue_id
    assert result.first_checkin_id
    assert result.last_checkin_id
