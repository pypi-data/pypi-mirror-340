"""Test user beer history."""

from __future__ import annotations

import pytest

from untappd_scraper.structs.web import WebUserHistoryBeer
from untappd_scraper.user_beer_history import (
    load_user_beer_history,
    load_user_beer_history_more,
)

# ----- Tests -----


@pytest.mark.usefixtures("_mock_user_beer_history_get")
def test_load_user_beer_history() -> None:
    result = load_user_beer_history("test")

    assert result
    assert len(result) == 25
    assert isinstance(next(iter(result.values())), WebUserHistoryBeer)


# @pytest.mark.usefixtures("_mock_user_beer_history_get")
def test_load_user_beer_history_more() -> None:
    result = load_user_beer_history_more(
        "mw1414", brewery_id=484738, max_resort=4
    )  # Buckettys

    assert result
    assert len(result) > 50
    assert all("Bucketty" in r.brewery for r in result)
