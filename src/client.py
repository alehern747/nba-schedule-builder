import requests
import os
import datetime
from datetime import date

API_KEY = os.getenv("BALLDONTLIE_API_KEY")
BASE_URL = "https://api.balldontlie.io/v1"

_session = requests.Session()
_session.headers.update({"Authorization": API_KEY})

def format_datetime(year, month, day) -> str:
    """Formats and returns a valid date"""
    formatted = date(year, month, day)
    # remove comment after testing previous date
    # if start_date <= date.today():
        # raise ValueError
    # if start_date.year > date.today().year + 1:
        # raise ValueError
    return formatted.isoformat()

def get_all_pages(endpoint: str, params: dict):
    """Retrieves JSON data from all pages of endpoint, if games past 100"""
    results = []
    cursor = None

    while True:
        if cursor:
            params["cursor"] = cursor
        body = get(endpoint, params)
        results.extend(body["data"])

        cursor = body.get("meta", {}).get("next_cursor")
        if not cursor:
            break

    return results


def get(endpoint: str, params: dict) -> dict:
    """Builds URL, sends request to API endpoint to fetch JSON data"""
    if API_KEY is None:
        raise RuntimeError("No API Key")

    response = _session.get(f"{BASE_URL}/{endpoint}", params=params)
    response.raise_for_status()
    return response.json()


def parse_all(data: list[dict], parser) -> list:
    """Returns all JSON data in formatted structure"""
    parsed = []
    for x in data:
        parsed.append(parser(x))

    return parsed