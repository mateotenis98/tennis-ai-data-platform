"""Module for extracting tennis odds from The-Odds-API and uploading to GCS or saving locally."""

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv
from google.cloud import storage

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(levelname)s — %(message)s")
logger = logging.getLogger(__name__)

_BASE_URL = "https://api.the-odds-api.com/v4/sports"
_SPORT = "tennis_atp_miami_open"
_REGIONS = "us"
_MARKETS = "h2h"


def fetch_odds() -> list[dict]:
    """Fetch upcoming tennis H2H odds from The-Odds-API.

    Returns:
        A list of event dicts returned by the API.

    Raises:
        EnvironmentError: If THE_ODDS_API_KEY is not set.
        requests.HTTPError: If the API returns a non-200 status code.
    """
    api_key = os.getenv("THE_ODDS_API_KEY")
    if not api_key:
        raise EnvironmentError("THE_ODDS_API_KEY is not set in the environment.")

    url = f"{_BASE_URL}/{_SPORT}/odds/"
    params = {
        "apiKey": api_key,
        "regions": _REGIONS,
        "markets": _MARKETS,
    }

    logger.info("Fetching %s odds from The-Odds-API (regions=%s, markets=%s)...", _SPORT, _REGIONS, _MARKETS)
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data: list[dict] = response.json()
    logger.info("Fetched %d events successfully.", len(data))
    return data


def save_locally(data: list[dict], output_dir: str = "data/raw") -> Path:
    """Serialize data as JSON and save it to a local directory for sandbox exploration.

    Args:
        data: The list of event dicts to save.
        output_dir: Relative path to the local output directory.

    Returns:
        The Path of the saved file.
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_path = Path(output_dir) / f"tennis_odds_{timestamp}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    logger.info("Saved %d events locally to %s", len(data), out_path)
    return out_path


def upload_to_gcs(data: list[dict], bucket_name: str) -> str:
    """Serialize data as JSON and upload it to a GCS bucket.

    Authentication uses Application Default Credentials (ADC). Run
    ``gcloud auth application-default login`` locally, or attach a
    service account when deploying to GCP.

    Args:
        data: The list of event dicts to upload.
        bucket_name: Target GCS bucket name (without ``gs://`` prefix).

    Returns:
        The full GCS URI of the uploaded object (e.g. ``gs://bucket/raw/...``).

    Raises:
        google.cloud.exceptions.GoogleCloudError: On any GCS failure.
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    blob_name = f"raw/tennis_odds_{timestamp}.json"

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.upload_from_string(
        data=json.dumps(data, indent=2),
        content_type="application/json",
    )

    gcs_uri = f"gs://{bucket_name}/{blob_name}"
    logger.info("Uploaded %d events to %s", len(data), gcs_uri)
    return gcs_uri


if __name__ == "__main__":
    # Sprint 2 sandbox mode: save locally for EDA before promoting to GCP.
    # To upload to GCS instead, call upload_to_gcs() with GCP_BUCKET_NAME.
    odds_data = fetch_odds()
    local_path = save_locally(odds_data)
    print(f"Success! Data saved locally to: {local_path}")
