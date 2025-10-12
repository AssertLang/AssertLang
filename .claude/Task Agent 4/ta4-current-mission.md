## Mission: Ecosystem, Packaging, and Governance Launch

**Assigned branch:** `feature/pw-ecosystem-launch` (create from `upstream/main`)  
**Primary objective:** Build the ecosystem scaffolding—package manager, benchmarks, governance, and public messaging—that makes Promptware feel trustworthy and production-ready.

### Scope & Priorities
1. **Package Manager (`pwpm`)**
   - Implement CLI workflow: `pwpm init`, `pwpm add`, `pwpm build`, `pwpm publish`.
   - Define lockfile format (content-addressed artifacts) and caching strategy.
   - Stand up minimal registry service (even local JSON index) with clear API spec documented in `docs/pwpm/REGISTRY_SPEC.md`.
2. **Benchmarking & Performance Transparency**
   - Create `benchmarks/` suite comparing Promptware vs Python/Go for fs, JSON, HTTP, async scheduling.
   - Automate baseline runs (ensure determinism via fixed seeds/capabilities).
   - Publish results + methodology in `docs/benchmarks/RESULTS.md`.
3. **Governance & Roadmap**
   - Introduce RFC process: create `rfcs/` directory with template `RFC-0001.md`.
   - Draft `docs/governance/ROADMAP.md` mapping project phases, stability policy, versioning (SemVer).
   - Set up communication touchpoints: weekly changelog skeleton, Discord/Discourse plan (documented in `docs/community/COMMUNICATION.md`).
4. **Branding & Messaging**
   - Produce “Why Promptware” explainer (`docs/overview/VISION.md`) aligned with runtime + stdlib direction.
   - Craft flagship demo storyline (e.g., cross-runtime orchestration app) referencing contributions from TA1/TA2.
   - Coordinate with marketing assets (landing page copy draft, one-page PDF).
5. **Release Process Automation**
   - Design GitHub Actions blueprint for publish-on-tag (PyPI + release notes).
   - Document manual fallback steps in `docs/release/PROCESS.md` until automation lands.

### Exit Criteria
- `pwpm` commands operational with sample package published/installed locally.
- Benchmark suite runs and reports performance deltas vs reference languages.
- Public roadmap + RFC process published; governance story clear to external devs.
- Messaging collateral ready (vision doc, demo narrative, landing copy).
- Release process documented with next steps for automation implementation.

### Coordination
- Work with **TA2** to ensure runtime exports manifest metadata required by `pwpm`.
- Collaborate with **TA1** to package stdlib modules under new registry.
- Share benchmark insights with all agents to inform optimization priorities.
- Update `.claude/Task Agent 4/ta4-current-progress.md` after milestones (pwpm alpha, benchmark publish, governance docs).
