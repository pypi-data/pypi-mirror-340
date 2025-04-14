import requests
from typing import List, Optional, Dict, Any

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

    def search_places(self, text_query: str, field_mask: str = "places.displayName,places.formattedAddress,places.priceLevel,places.photos") -> List[Dict[str, Any]]:
        try:
            url = f"{self.base_url}/places:searchText"
            payload = {"textQuery": text_query}
            headers = {**self.headers, "X-Goog-FieldMask": field_mask}
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data.get("places", [])  # Devuelve una lista de diccionarios con los resultados
        except Exception as error:
            self.handle_error(error)
            return []

    def get_place_details(self, place_id: str, field_mask: str = "places.displayName,places.formattedAddress,places.priceLevel,places.photos") -> Optional[Dict[str, Any]]:
        try:
            url = f"{self.base_url}/places/{place_id}"
            headers = {**self.headers, "X-Goog-FieldMask": field_mask}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data if data else None  # Devuelve los datos como un diccionario si existen
        except Exception as error:
            self.handle_error(error)
            return None

    def autocomplete_places(self, input_text: str, field_mask: str = "places.displayName,places.formattedAddress") -> Dict[str, Any]:
        try:
            url = f"{self.base_url}/places:autocomplete"
            payload = {"input": input_text}
            headers = {**self.headers, "X-Goog-FieldMask": field_mask}
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data.get("predictions", [])  # Devuelve las predicciones como lista de diccionarios
        except Exception as error:
            self.handle_error(error)
            return []

    def handle_error(self, error: Exception) -> None:
        if isinstance(error, requests.RequestException):
            print(f"Error fetching data: {error}")
            if error.response:
                print(f"Error data: {error.response.text}")
                print(f"Error status: {error.response.status_code}")
        else:
            print(f"Unexpected error: {error}")
