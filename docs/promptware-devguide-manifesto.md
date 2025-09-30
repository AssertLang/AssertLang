Got it — thanks for clarifying. Since you lost the text in your repo, I’ll give you back the full detailed version of the Promptware Manifesto & Development Guide (not shortened). You can copy this directly into /docs/promptware_manifesto.md or wherever you want it in your repo.

⸻

Promptware Manifesto & Development Guide

Vision

Promptware is the universal protocol for autonomous agent communication in cloud-native AI systems.

Instead of agents written in different languages (Python, Node, Go, Rust, .NET) using incompatible protocols, all agents speak `.pw` — a shared MCP-based language for bidirectional coordination. Agents expose capabilities as MCP verbs and call other agents' verbs, enabling language-agnostic orchestration at scale.

Core principles:
	•	Agent-first → designed for autonomous agents coordinating via MCP, not just apps.
	•	Bidirectional → agents both expose verbs AND call other agents' verbs.
	•	Language-agnostic → same `.pw` definitions work across Python/Node/Go/Rust/.NET/Java/C++.
	•	MCP-native → built on Model Context Protocol for AI-native infrastructure.
	•	Cloud-native → port 23456 standard, service discovery, health monitoring.
	•	Polyglot → write agent once in `.pw`, deploy in any language.

⸻

Core Concepts

### Agents as MCP Peers

Agents are autonomous programs that:
	1.	**Expose MCP verbs** → define capabilities other agents can call
	2.	**Call other agents' verbs** → coordinate with peers via `.pw` syntax
	3.	**Run on port 23456** → standard port for agent MCP servers
	4.	**Speak `.pw` protocol** → language-agnostic coordination layer

### MCP Verbs

Agents define custom MCP verbs using `expose` blocks in `.pw`:

```pw
expose task.execute@v1:
  params:
    task_id string
    priority int
  returns:
    status string
    result object
```

Other agents call these verbs:

```pw
call code-reviewer review.submit@v1 pr_url="https://..."
```

All verbs are versioned (@v1, @v2) for compatibility.

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

