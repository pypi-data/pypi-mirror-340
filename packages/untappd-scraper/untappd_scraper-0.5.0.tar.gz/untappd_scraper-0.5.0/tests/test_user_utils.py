"""Test user utils."""

from untappd_scraper.user_utils import url_of


def test_url_of() -> None:
    result = url_of("test", page="2", query={"search": "me"})

    assert result == "https://untappd.com/user/test/2?search=me"
