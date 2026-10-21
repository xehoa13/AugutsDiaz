# AugutsDiaz

## ggmap_tool (safe helper)

Small helper CLI that uses the **official Google Places API** to scan locations
and export results (rating, review count, phone if available). It also produces
JSON payloads you can manually use to **suggest** a phone update or to **draft**
a review plan (rating + images), without automating edits or postings.

### Why this approach?
Automating edits/reviews or using multiple profiles/proxies for Google Maps can
violate platform policies and local laws. This tool is intentionally designed to
**avoid automation** of sensitive actions and instead outputs data you can review
and submit manually, using official APIs and normal user flows.

### Install
```bash
pip install -r requirements.txt
```

### Usage
```bash
# Scan places by location (lat,lng), radius (meters), and keyword
python -m ggmap_tool.cli scan \
  --location "10.762622,106.660172" \
  --radius 2000 \
  --keyword "cafe" \
  --api-key "$GOOGLE_MAPS_API_KEY" \
  --csv output.csv \
  --json output.json

# Create a draft review plan (manual submission later)
python -m ggmap_tool.cli review-plan \
  --place-id "ChIJN1t_tDeuEmsRUsoyG83frY4" \
  --rating 5 \
  --text "Dịch vụ tốt, không gian sạch sẽ." \
  --image-folder ./review_images \
  --json review_plan.json

# Create a phone change suggestion payload (manual submission later)
python -m ggmap_tool.cli phone-suggest \
  --place-id "ChIJN1t_tDeuEmsRUsoyG83frY4" \
  --current "+84 28 1234 5678" \
  --suggested "+84 28 9999 8888" \
  --json phone_suggestion.json
```

### Outputs
- `scan`: `output.csv` or `output.json` containing place id, rating, review count,
  phone, address, website, and maps URL.
- `review-plan`: `review_plan.json` with rating, review text, and image file paths.
- `phone-suggest`: `phone_suggestion.json` with current and suggested phone numbers.

### Notes
- Requires a valid **Google Places API** key.
- Rate limits apply; be mindful of API quotas.
