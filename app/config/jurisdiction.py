"""
Jurisdiction configuration loader.

All county- and court-specific data lives in app/assets/forms.json under the
"jurisdiction" key. The forms, resources, and zoom_court sections remain
separate so the same file can drive both the county template and the forms
library without changing existing consumers.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

_JURISDICTION_PATH = Path(__file__).parent.parent / "assets" / "forms.json"
_jurisdiction_data: Optional[Dict[str, Any]] = None


def _load_data() -> Dict[str, Any]:
    """Load the jurisdiction data file once and cache it."""
    global _jurisdiction_data
    if _jurisdiction_data is None:
        with open(_JURISDICTION_PATH, "r", encoding="utf-8") as f:
            _jurisdiction_data = json.load(f)
    return _jurisdiction_data


def get_config() -> Dict[str, Any]:
    """Return the full configuration object."""
    return _load_data()


def get_jurisdiction() -> Dict[str, Any]:
    """Return the county/jurisdiction metadata block."""
    return _load_data().get("jurisdiction", {})


def get_forms() -> List[Dict[str, Any]]:
    """Return all court forms."""
    return _load_data().get("forms", [])


def get_form_by_id(form_id: str) -> Optional[Dict[str, Any]]:
    """Return a single form by its id, or None."""
    for form in get_forms():
        if form.get("id") == form_id:
            return form
    return None


def get_resources() -> List[Dict[str, Any]]:
    """Return legal aid and court resources."""
    return _load_data().get("resources", [])


def get_zoom_court(key: Optional[str] = None) -> Dict[str, Any]:
    """Return the zoom court config for the active county (or all)."""
    data = _load_data().get("zoom_court", {})
    if key:
        return data.get(key, {})
    default_key = get_jurisdiction().get("zoom_court_key")
    return data.get(default_key, data) if default_key else data


def get_subtitle(lang: str = "en") -> str:
    """Return the localized county subtitle, if available."""
    subtitles = get_jurisdiction().get("subtitles", {})
    return subtitles.get(lang, subtitles.get("en", ""))


def get_display_name() -> str:
    """Return the human-readable app name for this county."""
    return get_jurisdiction().get("display_name", "Eviction Defense")


def get_court_info() -> Dict[str, Any]:
    """Return court name, address, phone, and other contact info."""
    return {
        "name": get_jurisdiction().get("court", ""),
        "county": get_jurisdiction().get("county", ""),
        "jurisdiction": get_jurisdiction().get("name", ""),
        "address": get_jurisdiction().get("court_address", ""),
        "phone": get_jurisdiction().get("court_phone", ""),
    }


def get_deadline_days_for(form_id: str) -> Optional[int]:
    """Return the configured deadline_days for a given form, if any."""
    form = get_form_by_id(form_id)
    if form:
        return form.get("deadline_days")
    return None


class JurisdictionProxy:
    """Hashable read-only proxy for jurisdiction config so it can live in
    Jinja2 globals without breaking template caching.
    """

    __slots__ = ("_data",)

    def __init__(self, data: Dict[str, Any]):
        self._data = data

    def __getattr__(self, name: str) -> Any:
        try:
            return self._data[name]
        except KeyError as exc:
            raise AttributeError(f"No jurisdiction field named {name!r}") from exc

    def __getitem__(self, name: str) -> Any:
        return self._data[name]

    def __iter__(self):
        return iter(self._data)

    def get(self, name: str, default: Any = None) -> Any:
        return self._data.get(name, default)

    def __hash__(self) -> int:
        # The proxy wraps a mutable dict; we only need a stable identity so
        # Jinja2 can build a cache key. Re-loading config returns the same
        # cached data, so the default object id is consistent within a process.
        return id(self)

    def __repr__(self) -> str:
        return f"JurisdictionProxy({self._data})"


def get_jurisdiction_proxy() -> JurisdictionProxy:
    """Return a hashable, read-only proxy for the jurisdiction config."""
    return JurisdictionProxy(get_jurisdiction())
