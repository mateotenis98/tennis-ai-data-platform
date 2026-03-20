"""Entrypoint for Sprint 1: extract tennis odds and upload to GCS."""

import os

from dotenv import load_dotenv

from src.ingestion.extract_odds import fetch_odds, upload_to_gcs

load_dotenv()


def main() -> None:
    """Orchestrate odds extraction and GCS upload."""
    bucket_name = os.getenv("GCP_BUCKET_NAME")
    if not bucket_name:
        raise EnvironmentError("GCP_BUCKET_NAME is not set in the environment.")

    data = fetch_odds()
    gcs_uri = upload_to_gcs(data, bucket_name)
    print(f"Done. Data available at: {gcs_uri}")


if __name__ == "__main__":
    main()

