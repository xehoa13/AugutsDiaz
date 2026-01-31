import csv
import json
from pathlib import Path
from typing import Iterable

from ggmap_tool.models import PhoneSuggestion, PlaceSummary, ReviewPlan


def export_csv(rows: Iterable[PlaceSummary], path: Path) -> None:
    fieldnames = [
        "place_id",
        "name",
        "rating",
        "user_ratings_total",
        "formatted_phone_number",
        "address",
        "website",
        "maps_url",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "place_id": row.place_id,
                    "name": row.name,
                    "rating": row.rating,
                    "user_ratings_total": row.user_ratings_total,
                    "formatted_phone_number": row.formatted_phone_number,
                    "address": row.address,
                    "website": row.website,
                    "maps_url": row.maps_url,
                }
            )


def export_json(path: Path, payload: object) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def review_plan_payload(plan: ReviewPlan) -> dict:
    return {
        "place_id": plan.place_id,
        "rating": plan.rating,
        "review_text": plan.review_text,
        "image_paths": list(plan.image_paths),
    }


def phone_suggestion_payload(suggestion: PhoneSuggestion) -> dict:
    return {
        "place_id": suggestion.place_id,
        "current_phone": suggestion.current_phone,
        "suggested_phone": suggestion.suggested_phone,
    }
