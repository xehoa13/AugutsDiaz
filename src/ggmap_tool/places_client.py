import time
from typing import Iterable, Optional

import requests

from ggmap_tool.models import PlaceSummary, ScanRequest

NEARBY_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"


class PlacesClient:
    def __init__(self, api_key: str, session: Optional[requests.Session] = None) -> None:
        self._api_key = api_key
        self._session = session or requests.Session()

    def scan(self, request: ScanRequest, *, sleep_seconds: float = 1.5) -> Iterable[PlaceSummary]:
        params = {
            "key": self._api_key,
            "location": request.location,
            "radius": request.radius_meters,
            "keyword": request.keyword,
        }
        next_page_token: Optional[str] = None
        while True:
            if next_page_token:
                params["pagetoken"] = next_page_token
                time.sleep(sleep_seconds)
            response = self._session.get(NEARBY_SEARCH_URL, params=params, timeout=30)
            response.raise_for_status()
            payload = response.json()
            status = payload.get("status")
            if status == "ZERO_RESULTS":
                break
            if status != "OK":
                error_message = payload.get("error_message")
                detail = f": {error_message}" if error_message else ""
                raise RuntimeError(
                    f"Nearby Search API error ({status or 'missing status'}){detail}"
                )
            for result in payload.get("results", []):
                place_id = result.get("place_id")
                if not place_id:
                    continue
                details = self.fetch_details(place_id)
                if details:
                    yield details
            next_page_token = payload.get("next_page_token")
            if not next_page_token:
                break

    def fetch_details(self, place_id: str) -> Optional[PlaceSummary]:
        params = {
            "key": self._api_key,
            "place_id": place_id,
            "fields": "place_id,name,rating,user_ratings_total,formatted_phone_number,"
            "formatted_address,website,url",
        }
        response = self._session.get(DETAILS_URL, params=params, timeout=30)
        response.raise_for_status()
        payload = response.json()
        if payload.get("status") != "OK":
            return None
        result = payload.get("result", {})
        return PlaceSummary(
            place_id=result.get("place_id", place_id),
            name=result.get("name", ""),
            rating=result.get("rating"),
            user_ratings_total=result.get("user_ratings_total"),
            formatted_phone_number=result.get("formatted_phone_number"),
            address=result.get("formatted_address"),
            website=result.get("website"),
            maps_url=result.get("url"),
        )
