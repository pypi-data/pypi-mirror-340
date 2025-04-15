
# hive_intelligence/client.py

import requests
from .types import HiveSearchRequest, HiveSearchResponse
from .errors import HiveSearchAPIError

class HiveSearchClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.hiveintelligence.xyz/v1/search"

    def search(self, params: HiveSearchRequest) -> HiveSearchResponse:
        try:
            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=params.model_dump(exclude_none=True),
            )
            response.raise_for_status()
            return HiveSearchResponse(**response.json())
        except requests.exceptions.HTTPError as http_err:
            try:
                error_details = response.json()
                # Try to extract message from common fields
                message = error_details.get("error") or error_details.get("message") or str(error_details)
            except Exception:
                message = response.text[:200]  # fallback

            raise HiveSearchAPIError(
                status_code=response.status_code,
                reason=response.reason,
                message=message,
            ) from http_err
        except Exception as err:
            raise Exception("Unknown error occurred while calling HiveSearch API") from err

