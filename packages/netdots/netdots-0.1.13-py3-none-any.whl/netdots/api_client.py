# netdots/api_client.py
import requests

from .integrations.integrations import Integrations

DEFAULT_BASE_URL = "https://api.netdots.com"  # Change this to your production URL as needed.

class Netdots:
    integrations = None

    def __init__(self, api_key: str, base_url: str = DEFAULT_BASE_URL):
        if not api_key:
            raise ValueError("An API key must be provided.")
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.integrations = Integrations(api_key=self.api_key, base_url=self.base_url)


    def _headers(self):
        return {"x-api-key": self.api_key}
        

    def run_agent(self, payload: dict, thread_id: str = None):
        if thread_id:
            payload["thread_id"] = thread_id
        url = f"{self.base_url}/agent"
        response = requests.post(url, json=payload, headers=self._headers())
        response.raise_for_status()
        return response.json()


    def upload_document(self, payload: dict):
        url = f"{self.base_url}/upload_document"
        response = requests.post(url, json=payload, headers=self._headers())
        response.raise_for_status()
        return response.json()

    def get_functions(self):
        url = f"{self.base_url}/functions"
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json()

    def create_thread(self, payload: dict):
        url = f"{self.base_url}/threads"
        response = requests.post(url, json=payload, headers=self._headers())
        response.raise_for_status()
        return response.json()
    
    def retrieve_thread(self, thread_id: str):
        url = f"{self.base_url}/threads/{thread_id}"
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json()
    
    def add_message(self, thread_id: str, payload: dict):
        url = f"{self.base_url}/threads/{thread_id}/messages"
        response = requests.post(url, json=payload, headers=self._headers())
        response.raise_for_status()
        return response.json()
    
    def delete_thread(self, thread_id: str):
        url = f"{self.base_url}/threads/{thread_id}"
        response = requests.delete(url, headers=self._headers())
        response.raise_for_status()
        return response.json()

        

