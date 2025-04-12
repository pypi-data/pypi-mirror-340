from .skype import Skype
from .jira import Jira

class Integrations:
    skype = None
    jira = None

    def __init__(self, api_key: str, base_url: str):

        base_url = f"{base_url}/integrations"

        self.skype = Skype(api_key, base_url)
        self.jira = Jira(api_key, base_url)
