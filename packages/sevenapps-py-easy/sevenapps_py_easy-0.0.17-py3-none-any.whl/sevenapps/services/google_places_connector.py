import requests
from typing import List, Optional, Dict, Any

class Place:
    def __init__(self, display_name: Optional[str] = None, formatted_address: Optional[str] = None,
                 price_level: Optional[int] = None, photos: Optional[List[str]] = None):
        self.display_name = display_name
        self.formatted_address = formatted_address
        self.price_level = price_level
        self.photos = photos


class AutocompleteResult:
    def __init__(self, predictions: Optional[List[str]] = None):
        self.predictions = predictions or []


class GooglePlacesService:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Google Places API Key is required.")
        self.api_key = api_key
        self.base_url = "https://places.googleapis.com/v1"
        self.headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
        }

    def search_places(self, text_query: str, field_mask: str = "places.displayName,places.formattedAddress,places.priceLevel,places.photos") -> List[Place]:
        try:
            url = f"{self.base_url}/places:searchText"
            payload = {"textQuery": text_query}
            headers = {**self.headers, "X-Goog-FieldMask": field_mask}
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return [Place(**place) for place in data.get("places", [])]
        except Exception as error:
            self.handle_error(error)
            return []

    def get_place_details(self, place_id: str, field_mask: str = "places.displayName,places.formattedAddress,places.priceLevel,places.photos") -> Optional[Place]:
        try:
            url = f"{self.base_url}/places/{place_id}"
            headers = {**self.headers, "X-Goog-FieldMask": field_mask}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return Place(**data) if data else None
        except Exception as error:
            self.handle_error(error)
            return None

    def autocomplete_places(self, input_text: str, field_mask: str = "places.displayName,places.formattedAddress") -> AutocompleteResult:
        try:
            url = f"{self.base_url}/places:autocomplete"
            payload = {"input": input_text}
            headers = {**self.headers, "X-Goog-FieldMask": field_mask}
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return AutocompleteResult(predictions=data.get("predictions", []))
        except Exception as error:
            self.handle_error(error)
            return AutocompleteResult()

    def handle_error(self, error: Exception) -> None:
        if isinstance(error, requests.RequestException):
            print(f"Error fetching data: {error}")
            if error.response:
                print(f"Error data: {error.response.text}")
                print(f"Error status: {error.response.status_code}")
        else:
            print(f"Unexpected error: {error}")