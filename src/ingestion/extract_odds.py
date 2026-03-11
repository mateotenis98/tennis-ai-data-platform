"""Module for extracting tennis odds from The-Odds-API and uploading to GCS."""

import json
import logging
import os
from datetime import datetime

import requests
from dotenv import load_dotenv
from google.cloud import storage

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(levelname)s — %(message)s")
logger = logging.getLogger(__name__)

_BASE_URL = "https://api.the-odds-api.com/v4/sports"
_SPORT = "upcoming"
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
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
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
