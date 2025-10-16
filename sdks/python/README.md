# AssertLang SDK (Python)

Host SDK for integrating with AssertLang daemon via MCP (Model Context Protocol).

## Installation

```bash
pip install promptware-sdk
```

## Quick Start

```python
from promptware_sdk import mcp, TimelineReader

# Create and execute a plan
plan = mcp.plan_create_v1("""
call http_client as api {
    url: "https://api.example.com/data"
    method: "GET"
}
""", format="dsl")

run_id = mcp.run_start_v1(plan)

# Stream timeline events
reader = TimelineReader(run_id)
for event in reader.events():
    print(f"{event['phase']}: {event.get('alias', '')} - {event['status']}")

# Wait for completion
status = reader.wait_for_completion(timeout=60)
print(f"Run completed with status: {status}")

# Report finish
mcp.report_finish_v1(run_id, status)
```

## Features

- **MCP Verb Wrappers**: `plan_create_v1`, `run_start_v1`, `httpcheck_assert_v1`, `report_finish_v1`
- **Timeline Streaming**: Real-time execution event streaming
- **Error Handling**: Standard error taxonomy matching daemon (`E_RUNTIME`, `E_POLICY`, etc.)
- **Type Hints**: Full type annotations for IDE support

## Documentation

See [docs/sdk/](../../docs/sdk/) for:
- Package design and architecture
- API reference
- Integration examples
- Testing guide

## Requirements

- Python 3.10+
- AssertLang daemon 0.1.0+

## Development

```bash
# Install in editable mode
pip install -e .[dev]

# Run tests
pytest

# Format code
black src tests

# Lint
ruff check src tests
```

## License

MIT