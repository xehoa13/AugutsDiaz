from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ScanRequest:
    location: str
    radius_meters: int
    keyword: str


@dataclass(frozen=True)
class PlaceSummary:
    place_id: str
    name: str
    rating: Optional[float]
    user_ratings_total: Optional[int]
    formatted_phone_number: Optional[str]
    address: Optional[str]
    website: Optional[str]
    maps_url: Optional[str]


@dataclass(frozen=True)
class ReviewPlan:
    place_id: str
    rating: int
    review_text: str
    image_paths: tuple[str, ...]


@dataclass(frozen=True)
class PhoneSuggestion:
    place_id: str
    current_phone: Optional[str]
    suggested_phone: str
