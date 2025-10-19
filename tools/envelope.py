from __future__ import annotations

from typing import Any, Dict, Optional

DEFAULT_VERSION = "v1"


def ok(data: Optional[Dict[str, Any]] = None, version: str = DEFAULT_VERSION) -> Dict[str, Any]:
    return {"ok": True, "version": version, "data": data or {}}


def error(code: str, message: str, details: Optional[Dict[str, Any]] = None, version: str = DEFAULT_VERSION) -> Dict[str, Any]:
    err = {"code": code, "message": message}
    if details:
        err["details"] = details
    return {"ok": False, "version": version, "error": err}


def validate_request(req: Dict[str, Any]) -> Optional[Dict[str, Any]]:  # placeholder schema validation
    # TODO: integrate jsonschema validation against tool schemas
    if not isinstance(req, dict):
        return error("E_SCHEMA", "request must be an object")
    return None




