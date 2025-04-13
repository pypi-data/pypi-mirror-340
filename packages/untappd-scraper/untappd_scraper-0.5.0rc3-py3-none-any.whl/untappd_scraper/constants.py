"""Untapdd scraping constants."""

from __future__ import annotations

from typing import Final, Literal

UNTAPPD_BASE_URL: Final[str] = "https://untappd.com/"


"""Max number of times to resort the beer list before stopping."""
NumReSorts = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
