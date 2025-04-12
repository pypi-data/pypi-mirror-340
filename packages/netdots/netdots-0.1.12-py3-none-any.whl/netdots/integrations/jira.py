import requests

class Jira:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = f"{base_url}/jira"

    def _headers(self):
        return {"x-api-key": self.api_key}

    def test(self, payload: dict):
        url = f"{self.base_url}/test"
        response = requests.post(url, json=payload, headers=self._headers())
        response.raise_for_status()
        return response.json()