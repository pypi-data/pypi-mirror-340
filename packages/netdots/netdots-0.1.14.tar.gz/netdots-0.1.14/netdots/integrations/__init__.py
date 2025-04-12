# netdots/integrations/__init__.py

# (Optional) Expose the internal client if needed.
from .integrations import Integrations
from .jira import Jira
from .skype import Skype

__all__ = ["Integrations", "Jira", "Skype"]
