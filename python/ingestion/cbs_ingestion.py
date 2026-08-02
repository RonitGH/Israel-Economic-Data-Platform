import json
import sys

import requests


API_URL = "https://apis.cbs.gov.il/series/catalog/level"

PARAMS = {
    "id": 2,
    "subject": 26,
    "format": "json",
    "download": "false",
    "pagesize": 1000,
}

HEADERS = {
    "User-Agent": "Israel-Economic-Data-Platform/1.0",
    "Accept": "application/json",
}


def main() -> None:
    try:
        response = requests.get(
            API_URL,
            params=PARAMS,
            headers=HEADERS,
            timeout=30,
        )

        print(f"Request URL: {response.url}")
        print(f"Status code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")

        response.raise_for_status()

        data = response.json()
        print(json.dumps(data, ensure_ascii=False, indent=2))

    except requests.exceptions.RequestException as exc:
        print(f"API request failed: {exc}", file=sys.stderr)

        if "response" in locals():
            print(response.text[:2000], file=sys.stderr)

        sys.exit(1)

    except ValueError as exc:
        print(f"The response was not valid JSON: {exc}", file=sys.stderr)
        print(response.text[:2000], file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
