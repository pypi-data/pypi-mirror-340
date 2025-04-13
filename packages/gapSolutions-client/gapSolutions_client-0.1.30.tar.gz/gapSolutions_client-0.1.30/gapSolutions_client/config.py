# config.py

# Default base URL
_base_url = "https://testapp.gapsolutions.dk/api"

def set_base_url(url: str):
    global _base_url
    _base_url = url.rstrip("/")  # Remove trailing slash for consistency

def get_base_url() -> str:
    return _base_url
