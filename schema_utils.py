from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Mapping

_ROOT = Path(__file__).resolve().parent
_SCHEMA_PATH = _ROOT / "schemas" / "timeline_event.schema.json"


def load_event_schema() -> dict:
    """Return the timeline event JSON schema as a dict."""

    return json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))


def assert_events_match_schema(events: Iterable[Mapping]) -> None:
    """Lightweight validation that events follow the published schema fields."""

    schema = load_event_schema()
    required = set(schema.get("required", []))

    for event in events:
        missing = required - event.keys()
        assert not missing, f"timeline event missing required fields {missing}: {event}"
