import argparse
import os
import sys
from pathlib import Path
from typing import Sequence

from ggmap_tool.io import export_csv, export_json, phone_suggestion_payload, review_plan_payload
from ggmap_tool.models import PhoneSuggestion, ReviewPlan, ScanRequest
from ggmap_tool.places_client import PlacesClient


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Google Maps helper tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="Scan Google Maps Places API")
    scan_parser.add_argument("--location", required=True, help="lat,lng string")
    scan_parser.add_argument("--radius", required=True, type=int, help="radius in meters")
    scan_parser.add_argument("--keyword", required=True, help="industry keyword")
    scan_parser.add_argument(
        "--api-key",
        default=os.getenv("GOOGLE_MAPS_API_KEY", ""),
        help="Google Maps API key (or set GOOGLE_MAPS_API_KEY)",
    )
    scan_parser.add_argument("--csv", type=Path, help="CSV output path")
    scan_parser.add_argument("--json", type=Path, help="JSON output path")

    review_parser = subparsers.add_parser("review-plan", help="Build a review plan file")
    review_parser.add_argument("--place-id", required=True, help="Target place_id")
    review_parser.add_argument("--rating", required=True, type=int, choices=range(1, 6))
    review_parser.add_argument("--text", required=True, help="Review text content")
    review_parser.add_argument(
        "--image-folder",
        type=Path,
        required=True,
        help="Folder containing images to attach",
    )
    review_parser.add_argument("--json", type=Path, required=True, help="JSON output path")

    phone_parser = subparsers.add_parser("phone-suggest", help="Suggest a phone change")
    phone_parser.add_argument("--place-id", required=True, help="Target place_id")
    phone_parser.add_argument("--current", help="Current phone value")
    phone_parser.add_argument("--suggested", required=True, help="Suggested phone number")
    phone_parser.add_argument("--json", type=Path, required=True, help="JSON output path")

    return parser.parse_args(argv)


def run_scan(args: argparse.Namespace) -> int:
    if not args.api_key:
        raise SystemExit("Missing API key. Provide --api-key or set GOOGLE_MAPS_API_KEY.")
    request = ScanRequest(location=args.location, radius_meters=args.radius, keyword=args.keyword)
    client = PlacesClient(args.api_key)
    results = list(client.scan(request))

    if args.csv:
        export_csv(results, args.csv)
    if args.json:
        export_json(args.json, [result.__dict__ for result in results])
    if not args.csv and not args.json:
        for result in results:
            print(result)
    return 0


def run_review_plan(args: argparse.Namespace) -> int:
    if not args.image_folder.exists():
        raise SystemExit(f"Image folder not found: {args.image_folder}")
    image_paths = tuple(
        str(path)
        for path in sorted(args.image_folder.iterdir())
        if path.is_file()
    )
    plan = ReviewPlan(
        place_id=args.place_id,
        rating=args.rating,
        review_text=args.text,
        image_paths=image_paths,
    )
    export_json(args.json, review_plan_payload(plan))
    return 0


def run_phone_suggest(args: argparse.Namespace) -> int:
    suggestion = PhoneSuggestion(
        place_id=args.place_id,
        current_phone=args.current,
        suggested_phone=args.suggested,
    )
    export_json(args.json, phone_suggestion_payload(suggestion))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(list(argv) if argv is not None else sys.argv[1:])
    if args.command == "scan":
        return run_scan(args)
    if args.command == "review-plan":
        return run_review_plan(args)
    if args.command == "phone-suggest":
        return run_phone_suggest(args)
    raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
