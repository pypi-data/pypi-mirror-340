"""Test beer scraping."""

from __future__ import annotations

import pytest

from untappd_scraper.beer import Beer, url_of


@pytest.fixture
def beer(_mock_beer_get: None) -> Beer:
    return Beer(123)


# ----- Tests -----


def test_url_of() -> None:
    result = url_of(12345)

    assert result == "https://untappd.com/beer/12345"


def test_beer(beer: Beer) -> None:
    result = beer

    assert result
    assert result.name
    assert result.brewery
    assert result.beer_id


@pytest.mark.usefixtures("_mock_beer_404")
def test_beer_invalid() -> None:
    with pytest.raises(ValueError, match="Invalid"):
        Beer(123)  # ignored
