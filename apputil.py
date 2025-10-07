# your code here ...
import requests
import pandas as pd

class Genius:
    """
        A simple Genius API client for searching artists and retrieving their details.
    """

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://api.genius.com"
        self.headers = {"Authorization": f"Bearer {self.access_token}"}

    def get_artist(self, search_term: str) -> dict:
        """Search for an artist and return the full JSON response."""
        # 1. Search for the artist
        search_url = f"{self.base_url}/search"
        response = requests.get(search_url, headers=self.headers, params={"q": search_term})
        response.raise_for_status()
        data = response.json()

        # 2. Extract artist ID
        hits = data.get("response", {}).get("hits", [])
        if not hits:
            raise ValueError(f"No results found for '{search_term}'")

        artist_id = hits[0]["result"]["primary_artist"]["id"]

        # 3. Get artist details
        artist_url = f"{self.base_url}/artists/{artist_id}"
        artist_response = requests.get(artist_url, headers=self.headers)
        artist_response.raise_for_status()
        artist_data = artist_response.json()

        # 4. Return the WHOLE JSON, not just artist
        return artist_data


    def get_artists(self, search_terms: list[str]) -> pd.DataFrame:
        """Search for multiple artists and return a DataFrame with their details."""
        records = []
        for term in search_terms:
            try:
                artist_data = self.get_artist(term)
                artist_info = artist_data.get("response", {}).get("artist", {})
                records.append({
                    "search_term": term,
                    "artist_name": artist_info.get("name"),
                    "artist_id": artist_info.get("id"),
                    "followers_count": artist_info.get("followers_count")
                })
            except Exception:
                records.append({
                    "search_term": term,
                    "artist_name": None,
                    "artist_id": None,
                    "followers_count": None
                })
        return pd.DataFrame(records)
