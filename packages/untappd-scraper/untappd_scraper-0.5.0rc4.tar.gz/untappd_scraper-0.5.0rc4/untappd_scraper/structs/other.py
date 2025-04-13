"""Structures used to represent data not scraped."""
from __future__ import annotations

from dataclasses import astuple, dataclass
from functools import lru_cache

from haversine import haversine


@dataclass(frozen=True)
class Location:
    """Store latitude and longiture and calculate haversine distance between them."""

    lat: float
    lng: float

    @lru_cache
    def distance_from(self, other: Location) -> float:
        """Return km between two Location objects.

        Args:
            other (Location): where to measure distance to

        Returns:
            float: distance between points in km
        """
        return haversine(astuple(self), astuple(other))
