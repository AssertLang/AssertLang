# 🚀 Promptware

Promptware is a domain-specific language (`.pw`) for writing language-agnostic software.
Write once in `.pw`, run in Python, Node.js, Go, Rust, or .NET — fast, reproducible, and portable.

- One port → 23456 (reserved for Promptware)
- Five verbs → `plan`, `apply`, `run`, `validate`, `report`
- Numeric universality → tool families arranged as 2–3–4–5–6
- File extension → `.pw`

Promptware is designed to be agent-native: AI coding agents can invoke it directly through MCP.
Programs are ephemeral: spin up, run, validate, and vanish — unless persisted.

---

## ✨ Why Promptware?
- Language-agnostic: write `.pw` once, target Python/Node/Go/Rust/.NET
- MCP verbs as primitives: minimal, universal building blocks
- Multi-language tool adapters: 36 tools work across all backends
- Ephemeral execution: live microservices in seconds
- Community extensibility: anyone can build and share tools

---

## 📦 Quickstart

```bash
# Write a .pw file
cat > hello.pw << 'EOF'
lang python
start python app.py

file app.py:
  from http.server import BaseHTTPRequestHandler, HTTPServer
  class Handler(BaseHTTPRequestHandler):
      def do_GET(self):
          self.send_response(200)
          self.wfile.write(b'Hello, World!')
  HTTPServer(('127.0.0.1', 8000), Handler).serve_forever()
EOF

# Run it
promptware run hello.pw

# Output:
# ✅ PASS: http://127.0.0.1:23456/apps/ab12cd/
# Artifacts in .mcpd/ab12cd/
```

**Target different languages:**
```bash
# Same .pw code, different backend
promptware run hello.pw --lang python
promptware run hello.pw --lang node
promptware run hello.pw --lang go
```

---

This repository contains the Promptware mcpd daemon, gateway, runners, CLI, schemas, and tests.

- Gateway port: 23456
- CLI: `promptware run myapp.pw`
- Timeline schema: `schemas/timeline_event.schema.json` for validating interpreter/daemon event payloads

---

## 🛠 Repository Layout

```
/docs               → Manifesto, framework, tool specs, roadmap
/daemon             → Core mcpd daemon (gateway and verbs)
/runners/python     → Python runner
/runners/go         → Go runner
/runners/node       → Node.js runner
/cli                → Command-line interface
/schemas            → JSON schemas for verbs & tools
/tests              → Unit + contract tests
```

---

## 📚 Documentation
- Manifesto — vision & philosophy
- Framework Overview — verbs, numeric families, .pw files
- Tool Specifications — all 36 tools documented
- Development Guide — language bindings, containers, security
- Extensibility — how to add tools & use the marketplace
- Versioning — framework vs. tool versions
- Roadmap — MVP → Beta → Production
- Cheatsheet — quick reference

---

## 🔮 Roadmap (highlights)
- MVP (2–3 months) → CLI + verbs + Python runner
- Alpha (4–6 months) → Add Go + Node runtimes, full 2–3–4–5–6 framework
- Beta (6–9 months) → Marketplace + concurrency + sandbox security
- Production (9–12 months) → Rust runtime, cloud deploy, CI/CD integration

---

## 🧩 Extensibility

Promptware tools are modular.
Build your own with:

```
promptware tool create mytool
```

Then publish to the marketplace with:

```
promptware tool upload mytool
```

---

## 🛡 Security
- Ephemeral containers for isolation
- Default deny-all egress
- Auth and firewall tools for production-ready security

---

## 🌍 Community
- Open-source under Latency Zero
- All contributions welcome — tools, runners, docs, or ideas
- Marketplace will allow tool discovery & sharing

---

## ⚡ Taglines
- Promptware: Software at the Speed of Thought.
- One port. Five verbs. Infinite software.
- Prompted, not programmed.

---

## 🧰 Makefile
Optionally use a Makefile (`make install`, `make run`, `make test`, `make lint`, `make format`, `make clean`) to streamline local dev.
