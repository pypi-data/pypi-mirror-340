# netdots/__init__.py

# Global API key that the user must set.
api_key = None

# (Optional) Expose the internal client if needed.
from .api_client import Netdots

try:
    from .integrations import *
    #except ImportError:
except Exception as e:
    print(f"WARNING: Integrations not found. Ensure the server integrations are properly set up. {e}")

__all__ = ["api_key", "Netdots", "integrations"]
