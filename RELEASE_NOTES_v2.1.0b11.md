# Promptware v2.1.0b11 Release Notes

**Release Date:** 2025-10-09

## Highlights

- ✅ Fixes Bug #18: map return values accessed with dot notation now translate to the correct bracket notation in generated Python code.
- ✅ Extends flow-sensitive type tracking so methods invoked via `self` retain their declared return types during assignment analysis.

## Details

### Flow-Sensitive Map Handling

- Track the current class while generating methods in `language/python_generator_v2.py`, allowing `self.validate_token()` and similar calls to resolve their declared map return types.
- Update the inference pipeline so variables receiving map-returning methods are marked as maps, ensuring property access becomes `result["field"]` instead of `result.field`.

### Testing

- Added `tests/test_bug18_map_return_value_access.py` with three coverage scenarios (direct map literal, class method return, re-used map variable).
- Regression suite: 54/54 tests passing across Bug #14–#18 coverage (NOT operator, map access, class access, string concat, map return).

## Upgrade Guidance

No migration work required. Pull the latest code and rebuild as usual:

```bash
git fetch origin
git checkout main
git reset --hard origin/main
pip install -e .
```

---
Published to PyPI as `promptware-dev==2.1.0b11`. Tagging `v2.1.0b11` keeps GitHub in sync.
