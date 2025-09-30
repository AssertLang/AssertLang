#!/bin/bash
# Test script for demo MCP agent

echo "=== Testing MCP Agent Demo ==="
echo ""

# 1. Health check
echo "1. Health Check:"
echo '   GET http://127.0.0.1:23456/health'
echo '   Expected: {"status": "healthy", "agent": "code-reviewer", "uptime": 0}'
echo ""

# 2. List verbs
echo "2. List Exposed Verbs:"
echo '   GET http://127.0.0.1:23456/verbs'
echo '   Expected: {"agent": "code-reviewer", "verbs": ["review.submit@v1", "review.status@v1"]}'
echo ""

# 3. Call review.submit@v1
echo "3. Submit Review:"
echo '   POST http://127.0.0.1:23456/mcp'
echo '   Body: {"method": "review.submit@v1", "params": {"pr_url": "https://github.com/test/pr/1"}}'
echo '   Expected: {"ok": true, "version": "v1", "data": {"review_id": "...", "status": "..."}}'
echo ""

# 4. Call review.status@v1
echo "4. Check Review Status:"
echo '   POST http://127.0.0.1:23456/mcp'
echo '   Body: {"method": "review.status@v1", "params": {"review_id": "abc123"}}'
echo '   Expected: {"ok": true, "version": "v1", "data": {"status": "...", "progress": 0, "comments": []}}'
echo ""

echo "=== To Actually Run These Tests ==="
echo ""
echo "1. Install dependencies:"
echo "   pip3 install fastapi uvicorn"
echo ""
echo "2. Start the server:"
echo "   python3 examples/demo_agent_server.py"
echo ""
echo "3. In another terminal, run:"
echo "   curl http://127.0.0.1:23456/health"
echo "   curl http://127.0.0.1:23456/verbs"
echo "   curl -X POST http://127.0.0.1:23456/mcp \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"method\": \"review.submit@v1\", \"params\": {\"pr_url\": \"https://github.com/test/pr/1\"}}'"
echo ""