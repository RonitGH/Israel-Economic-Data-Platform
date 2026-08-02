import sys
from typing import Any

import requests
from google.cloud import bigquery


PROJECT_ID = "ronit-data-engineering"
TARGET_TABLE = f"{PROJECT_ID}.control.cbs_catalog"

API_URL = "https://apis.cbs.gov.il/series/data/path"

PARAMS = {
    "id": "26",
    "data_hide": "true",
    "format": "json",
    "download": "false",
    "pagesize": 1000,
}

HEADERS = {
    "User-Agent": "Israel-Economic-Data-Platform/1.0",
    "Accept": "application/json",
}


def find_series(node: Any) -> list[dict[str, Any]]:
    """Recursively find CBS series objects in the API response."""
    results: list[dict[str, Any]] = []

    if isinstance(node, dict):
        if "id" in node and "path" in node:
            results.append(node)

        for value in node.values():
            results.extend(find_series(value))

    elif isinstance(node, list):
        for item in node:
            results.extend(find_series(item))

    return results


def build_row(series: dict[str, Any], source_url: str) -> dict[str, Any]:
    path = series.get("path") or {}

    catalog_path: list[int] = []
    path_names: list[str] = []

    for key, value in path.items():
        if not isinstance(value, dict):
            continue

        code = value.get("value")
        name = value.get("name")

        if key.startswith("level") and code is not None:
            try:
                catalog_path.append(int(code))
            except (TypeError, ValueError):
                pass

        if name:
            path_names.append(str(name))

    name_info = path.get("name_id") or {}
    series_name = (
        name_info.get("name")
        or series.get("name")
        or "Unknown series"
    )

    series_id = series.get("id")
    if series_id is None:
        raise ValueError("Series is missing an id")

    return {
        "catalog_path": catalog_path,
        "catalog_level": len(catalog_path),
        "series_id": int(series_id),
        "series_name": str(series_name),
        "path_description": " > ".join(path_names),
        "source_url": source_url,
    }


def main() -> None:
    try:
        response = requests.get(
            API_URL,
            params=PARAMS,
            headers=HEADERS,
            timeout=60,
        )

        print(f"Request URL: {response.url}")
        print(f"Status code: {response.status_code}")

        response.raise_for_status()
        payload = response.json()

        series_items = find_series(payload)

        rows = [
            build_row(series, response.url)
            for series in series_items
        ]

        if not rows:
            raise RuntimeError(
                "The API returned no recognizable series records."
            )

        client = bigquery.Client(project=PROJECT_ID)

        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        )

        load_job = client.load_table_from_json(
            rows,
            TARGET_TABLE,
            job_config=job_config,
        )

        load_job.result()

        print(f"Loaded {len(rows)} rows into {TARGET_TABLE}")

    except requests.RequestException as exc:
        print(f"CBS API request failed: {exc}", file=sys.stderr)
        sys.exit(1)

    except Exception as exc:
        print(f"Catalog load failed: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
