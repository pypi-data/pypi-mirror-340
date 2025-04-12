"""Test user beer history."""

from __future__ import annotations

import pytest

from untappd_scraper.structs.web import WebUserHistoryBeer
from untappd_scraper.user_beer_history import load_user_beer_history

# ----- Tests -----


@pytest.mark.usefixtures("_mock_user_beer_history_get")
def test_load_user_beer_history() -> None:
    result = load_user_beer_history("test")

    assert result
    assert len(result) == 25
    assert isinstance(next(iter(result.values())), WebUserHistoryBeer)
