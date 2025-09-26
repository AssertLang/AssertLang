import time
import requests

from cli.mcp import main as mcp_main
from click.testing import CliRunner


def test_run_hello_world():
    runner = CliRunner()
    result = runner.invoke(mcp_main, ["run", "Create a web service that responds 'Hello, World!'"])
    assert result.exit_code == 0
    # Parse printed URL
    lines = result.output.splitlines()
    url = None
    for ln in lines:
        if "http://127.0.0.1:23456/apps/" in ln:
            url = ln.split()[-1]
            break
    assert url is not None
    # Probe
    for _ in range(30):
        try:
            r = requests.get(url, timeout=2)
            if r.status_code == 200 and "Hello, World!" in r.text:
                return
        except Exception:
            time.sleep(0.2)
    raise AssertionError("Service did not respond correctly")


