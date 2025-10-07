# your code here ...
import requests
import pandas as pd

class Genius:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://api.genius.com"
        self.headers = {"Authorization": f"Bearer {self.access_token}"}

    def get_artist(self, search_term: str) -> dict:
        search_url = f"{self.base_url}/search"
        params = {"q": search_term}
        response = requests.get(search_url, headers=self.headers, params=params)
        response.raise_for_status()
        search_json = response.json()

        hits = search_json.get("response", {}).get("hits", [])
        if not hits:
            raise ValueError(f"No results found for '{search_term}'")

        primary_artist = hits[0]["result"]["primary_artist"]
        artist_id = primary_artist["id"]

        artist_url = f"{self.base_url}/artists/{artist_id}"
        artist_response = requests.get(artist_url, headers=self.headers)
        artist_response.raise_for_status()
        artist_json = artist_response.json()

        return artist_json.get("response", {}).get("artist", {})

    def get_artists(self, search_terms: list[str]) -> pd.DataFrame:
        records = []
        for term in search_terms:
            try:
                artist_data = self.get_artist(term)
                records.append({
                    "search_term": term,
                    "artist_name": artist_data.get("name"),
                    "artist_id": artist_data.get("id"),
                    "followers_count": artist_data.get("followers_count")
                })
            except Exception:
                records.append({
                    "search_term": term,
                    "artist_name": None,
                    "artist_id": None,
                    "followers_count": None
                })
        return pd.DataFrame(records)
