# 🚀 Promptware

Promptware is a new programming language for the AI-native era.  
It turns natural language prompts into running software — fast, reproducible, and language-agnostic.

- One port → 23456 (reserved for Promptware)  
- Five verbs → `plan`, `apply`, `run`, `validate`, `report`  
- Numeric universality → tool families arranged as 2–3–4–5–6  
- File extension → `.pw`

Promptware is designed to be agent-native: AI coding agents can invoke it directly through MCP.  
Programs are ephemeral: spin up, run, validate, and vanish — unless persisted.

---

## ✨ Why Promptware?
- Simplicity over syntax: minimal verbs instead of complex languages.  
- Universality: bindings for Python, Go, Rust, TypeScript.  
- Ephemeral execution: live microservices in seconds.  
- Community extensibility: anyone can build and share tools.  

---

## 📦 Quickstart

```bash
# Run a prompt directly
promptware run "create a REST API that returns 'hello world'"

# Output:
# ✅ PASS: http://127.0.0.1:23456/apps/ab12cd/
# Artifacts in .mcpd/ab12cd/
```

---

This repository contains the Promptware mcpd daemon, gateway, runners, CLI, schemas, and tests.

- Gateway port: 23456
- CLI: `mcp run "Create a web service that responds 'Hello, World!'"`
- Timeline schema: `schemas/timeline_event.schema.json` (also published at https://promptware.dev/schemas/timeline-event.json) for validating interpreter/daemon `events` payloads.

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
