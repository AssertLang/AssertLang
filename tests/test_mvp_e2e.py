import time

import requests
from click.testing import CliRunner

from cli.mcp import main as mcp_main


def test_run_hello_world():
    """Test running a simple .pw DSL file"""
    # Create a simple .pw file for testing
    pw_content = """lang python
start python app.py

file app.py:
  from http.server import BaseHTTPRequestHandler, HTTPServer
  class Handler(BaseHTTPRequestHandler):
      def do_GET(self):
          self.send_response(200)
          self.send_header('Content-Type', 'text/plain')
          self.end_headers()
          self.wfile.write(b'Hello, World!')
      def log_message(self, *_args, **_kwargs):
          pass
  if __name__ == '__main__':
      import os
      port = int(os.environ.get('PORT', '8000'))
      server = HTTPServer(('127.0.0.1', port), Handler)
      server.serve_forever()
"""

    runner = CliRunner()
    result = runner.invoke(mcp_main, ["run", pw_content])
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


