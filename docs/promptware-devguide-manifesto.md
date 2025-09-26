Got it — thanks for clarifying. Since you lost the text in your repo, I’ll give you back the full detailed version of the Promptware Manifesto & Development Guide (not shortened). You can copy this directly into /docs/promptware_manifesto.md or wherever you want it in your repo.

⸻

Promptware Manifesto & Development Guide

Vision

Promptware is the future of software creation: prompted, not programmed.
Instead of static code written and maintained over months or years, applications become ephemeral artifacts generated on demand from natural language intent. A user (or AI coding agent) simply describes what they want, and Promptware turns that into a live, validated application — running instantly at a single, stable port: 23456.

Core principles:
	•	Simplicity → minimal, universal building blocks (five verbs).
	•	Universality → polyglot runners make it language-neutral.
	•	Ephemerality → apps spin up, do their job, and vanish or evolve via patches.
	•	Agent-native → designed so AI coding agents can operate seamlessly.
	•	Proof-oriented → every run produces verifiable logs, artifacts, and verdicts.

⸻

Core Verbs

Promptware defines five verbs, the smallest surface necessary to cover the full lifecycle of ephemeral software:
	1.	plan.create@v1 → transform a natural language prompt into a file plan.
	2.	fs.apply@v1 → write files from that plan into the sandbox.
	3.	run.start@v1 → start the program inside a controlled runner.
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
	1.	User/agent runs:

mcp run "Create a web service that responds 'Hello, World!'"


	2.	plan.create generates file plan.
	3.	fs.apply writes source files.
	4.	run.start spawns runner on UDS.
	5.	httpcheck.assert validates expected responses.
	6.	report.finish returns verdict + URL + artifacts.

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
	•	Promptware: Software at the Speed of Thought.
	•	Port 23456: One Port to Rule Them All.
	•	Prompted, not programmed.

⸻

Novelty

Promptware is not:
	•	A no-code/low-code tool (still supports full complexity).
	•	A coding assistant (not just snippets, but end-to-end apps).
	•	IDE tooling (it’s a framework-level system).

Instead, it’s a category-defining standard for ephemeral, just-in-time software. Similar to how Docker standardized containers, Promptware standardizes prompt-driven applications.

⸻

Closing

The future of software is ephemeral, bespoke, and prompt-driven. Promptware defines the smallest possible universal language and architecture to make this future real.

One port. Five verbs. Infinite software.
Promptware. Prompted, not programmed.

