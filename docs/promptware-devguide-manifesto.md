Got it — thanks for clarifying. Since you lost the text in your repo, I’ll give you back the full detailed version of the Promptware Manifesto & Development Guide (not shortened). You can copy this directly into /docs/promptware_manifesto.md or wherever you want it in your repo.

⸻

Promptware Manifesto & Development Guide

Vision

Promptware is the future of software creation: language-agnostic, not language-locked.
Instead of writing Python, Node, Go, Rust, or .NET separately, you write once in .pw and target any backend language. Applications become ephemeral artifacts compiled on demand from .pw DSL source. A user (or AI coding agent) writes .pw code, and Promptware turns that into a live, validated application — running instantly at a single, stable port: 23456.

Core principles:
	•	Simplicity → minimal, universal building blocks (five verbs).
	•	Universality → polyglot runners make it language-neutral.
	•	Ephemerality → apps spin up, do their job, and vanish or evolve via patches.
	•	Agent-native → designed so AI coding agents can operate seamlessly.
	•	Proof-oriented → every run produces verifiable logs, artifacts, and verdicts.

⸻

Core Verbs

Promptware defines five verbs, the smallest surface necessary to cover the full lifecycle of ephemeral software:
	1.	plan.create@v1 → parse .pw DSL source into an execution plan.
	2.	fs.apply@v1 → write files from that plan into the sandbox.
	3.	run.start@v1 → start the program inside a controlled runner (Python/Node/Go/Rust/.NET).
	4.	httpcheck.assert@v1 → validate outputs with probes (status, body checks).
	5.	report.finish@v1 → package source, artifacts, logs, and a verdict.

These verbs are versioned (@v1, @v2) so the framework can evolve without breaking clients.

⸻

Architecture

Daemon (mcpd)
	•	Exposes the verbs via MCP.
	•	Orchestrates tasks, sandboxes, and lifecycles.

Gateway
	•	Listens at Port 23456 (memorable, stable).
	•	Maps /apps/<task_id>/ requests to backend runners via UDS (Unix Domain Socket) or, if necessary, ephemeral high-range TCP (61000–64999).
	•	Cleans up routes when tasks exit.

Runners
	•	Polyglot language adapters that execute code from file plans.
	•	Tier-1: Python, Node.js, Go.
	•	Tier-2: Rust, Java, .NET.
	•	Communicate with daemon via JSON-RPC over stdin/stdout.

Artifacts
	•	Each task has .mcpd/<task_id>/ containing manifest, plan, logs, validation results, and patches.
	•	Enables debugging, re-use, and export to GitHub.

⸻

Workflow
	1.	User/agent writes .pw file:

lang python
tool rest.server as api
call api port=8080


	2.	User runs: promptware run myapp.pw
	3.	plan.create parses .pw DSL into execution plan.
	4.	fs.apply writes generated source files.
	5.	run.start spawns runner (Python/Node/Go/etc.).
	6.	httpcheck.assert validates expected responses.
	7.	report.finish returns verdict + URL + artifacts.

Example output:

✅ PASS: http://127.0.0.1:23456/apps/ab12cd/
Artifacts in .mcpd/ab12cd/


⸻

Roadmap

M1 (2–3 weeks)
	•	mcpd daemon with all five verbs.
	•	Python runner (Flask “Hello, World”).
	•	Gateway at Port 23456.
	•	CLI: run, list.

M2 (4–6 weeks)
	•	Node.js + Go runners.
	•	mcp change for patching.
	•	Artifact indexing + auto-cleanup.

M3 (6–10 weeks)
	•	Rust runner (Axum/WASI).
	•	GitHub Action integration.
	•	Dependency allowlist + basic SAST (security scans).

M4 (10–16 weeks)
	•	Java/.NET runners.
	•	Managed gateway (auth, hostnames).
	•	RBAC and observability.

⸻

Identity
	•	Framework name: Promptware
	•	Anchor: Port 23456
	•	Taglines:
	•	Promptware: Write Once, Run Anywhere.
	•	Port 23456: One Port to Rule Them All.
	•	One Language, Eight Backends.

⸻

Novelty

Promptware is not:
	•	A no-code/low-code tool (still supports full complexity).
	•	A coding assistant (not just snippets, but end-to-end apps).
	•	IDE tooling (it’s a framework-level system).

Instead, it's a category-defining standard for ephemeral, just-in-time software. Similar to how Docker standardized containers, Promptware standardizes language-agnostic application deployment.

⸻

Closing

The future of software is ephemeral, bespoke, and language-agnostic. Promptware defines the smallest possible universal language and architecture to make this future real.

One port. Five verbs. Infinite software.
Promptware. Write once, run anywhere.

