# MCP Server Testing Plan

**Date:** 2025-09-30
**Status:** All 10 servers connected (green dots in Cursor)
**Goal:** Comprehensive validation of MCP integration

---

## Test Environment

- **Cursor Version:** Latest with built-in MCP support
- **MCP Servers:** 10 Promptware agents via stdio protocol
- **Config:** `.cursor/mcp.json` with all servers defined
- **Connection:** All servers showing green status ✅

---

## Phase 1: Basic Functionality (COMPLETED ✅)

### 1.1 Connection Tests
- [x] All 10 servers start successfully
- [x] Green dots in Cursor Settings → Tools & MCP
- [x] `tools/list` returns valid JSON Schema for all servers

### 1.2 Mock Execution Tests
- [x] `review.approve@v1` (code-reviewer) - Returns `{status, next_step}`
- [x] `task_execute@v1` (monitored-service) - Returns `{result, status}`
- [x] `task.status@v1` (monitored-service) - Returns `{status, progress: 0}`
- [x] `review.analyze@v1` (ai-code-reviewer) - Returns `{summary, issues: [], suggestions: []}`
- [x] `workflow_execute@v1` (deployment-manager + deployment-orchestrator) - Both execute

**Findings:**
- Mock data generation works for string, int, array, object types
- Parameter validation working
- Cursor can call multiple tools with same name from different servers
- Response parsing working correctly

---

## Phase 2: Comprehensive Server Coverage

Test at least one tool from each of the 10 servers:

### 2.1 Tested Servers (5/10)
- [x] **ai-code-reviewer** - `review.analyze@v1`
- [x] **code-reviewer** - `review.approve@v1`
- [x] **monitored-service** - `task_execute@v1`, `task.status@v1`
- [x] **deployment-manager** - `workflow_execute@v1`
- [x] **deployment-orchestrator** - `workflow_execute@v1`

### 2.2 Remaining Servers (5/10)
- [ ] **orchestrator** - Test available tools
- [ ] **data-processor** - Test processing tools
- [ ] **cache-service** - Test cache operations
- [ ] **test-runner** - Test execution tools
- [ ] **unnamed** - Test fixture tools

**Action:** Query each server for tool list, test primary tool from each.

---

## Phase 3: Edge Cases & Error Handling

### 3.1 Parameter Validation
- [ ] **Missing required parameter** - Call tool without required param
  - Expected: Error response with clear message
  - Test: `review.approve@v1` without `review_id`

- [ ] **Wrong parameter type** - Pass string where int expected
  - Expected: Type validation error or coercion
  - Test: `task_execute@v1` with `priority="high"` instead of int

- [ ] **Extra parameters** - Pass unexpected params
  - Expected: Ignored or warning
  - Test: `task.status@v1` with extra field `action="start"`

- [ ] **Empty parameters** - Call with empty object
  - Expected: Works if no required params, else error
  - Test: Tools with all optional params

### 3.2 Tool Discovery
- [ ] **Verb name formats** - Test if both formats work:
  - Original: `review.analyze@v1`
  - Mangled: `review_analyzev1` (dots/@ removed)

- [ ] **Case sensitivity** - Test with different casing
  - Expected: Exact match required

- [ ] **Non-existent tool** - Call tool that doesn't exist
  - Expected: "Tool not found" error

### 3.3 Response Handling
- [ ] **Large responses** - Tool returns >1MB data
  - Expected: Cursor handles gracefully or truncates

- [ ] **Malformed JSON** - Tool returns invalid JSON
  - Expected: Error with details

- [ ] **Timeout** - Tool takes >30 seconds
  - Expected: Timeout error (verify Cursor timeout settings)

### 3.4 Concurrent Execution
- [ ] **Multiple tools in parallel** - Already works (deployment test)
- [ ] **Same tool multiple times** - Call `task.status@v1` with 3 different task_ids
- [ ] **Mixed servers** - Call 5 different tools from 5 different servers

---

## Phase 4: AI-Powered Execution

**Current State:** Agents with `prompt_template` return mock data (no API key).

### 4.1 Without ANTHROPIC_API_KEY (Current)
- [x] AI agents return mock data
- [x] Mock data matches schema correctly
- [x] No errors or crashes

### 4.2 With ANTHROPIC_API_KEY (To Test)
- [ ] Set `ANTHROPIC_API_KEY` in `.cursor/mcp.json` env section
- [ ] Restart Cursor to reload config
- [ ] Test AI agents:
  - [ ] `code-reviewer.review.analyze@v1` - Real code analysis
  - [ ] `ai-code-reviewer.review.analyze@v1` - Real PR review
  - [ ] `deployment-orchestrator.workflow_execute@v1` - Real planning

**Expected Behavior:**
- Agent calls Claude API internally
- Returns real analysis, not mock data
- Response parsing works for LLM-generated JSON

**Questions to Answer:**
1. Do AI agents provide better results than Cursor's built-in AI?
2. Should agents use their own LLM or rely on Cursor's AI?
3. What's the cost/latency trade-off?

---

## Phase 5: Real-World Scenarios

### 5.1 Code Review Workflow
```
User: "Review this code for security issues"
Cursor: Calls code-reviewer.review.analyze@v1
Agent: Analyzes code (AI or mock)
Cursor: Displays results to user
```

**Test:**
- Provide actual code snippet
- Check if analysis is useful
- Verify all issues/suggestions shown

### 5.2 Deployment Workflow
```
User: "Deploy to staging"
Cursor: Calls deployment-manager.workflow_execute@v1
Agent: Executes deployment (mock for now)
Cursor: Reports status
```

**Test:**
- Simulate deployment command
- Check if mock response is realistic
- Verify Cursor can poll status

### 5.3 Task Management
```
User: "Start task-123 with high priority"
Cursor: Calls monitored-service.task_execute@v1
Agent: Executes task (mock)
User: "Check status"
Cursor: Calls monitored-service.task.status@v1
Agent: Returns status
```

**Test:**
- Multi-step workflow
- State persistence (if any)
- Error recovery

---

## Phase 6: Performance & Reliability

### 6.1 Latency
- [ ] Measure tool call response time
  - Tools/list: <100ms expected
  - Tools/call (mock): <200ms expected
  - Tools/call (AI): <5s expected

- [ ] Test with 10 rapid calls
  - Check if servers queue or handle in parallel

### 6.2 Stability
- [ ] Run 100 tool calls
  - Check for crashes, memory leaks
  - Verify all servers still green after test

- [ ] Restart Cursor
  - Check if all servers reconnect
  - Verify state is clean

### 6.3 Error Recovery
- [ ] Kill an MCP server process manually
  - Check if Cursor shows red dot
  - Test if auto-restarts or requires manual restart

- [ ] Corrupt `.cursor/mcp.json`
  - Check error messages
  - Verify other servers unaffected

---

## Phase 7: Documentation & Validation

### 7.1 Schema Validation
- [ ] Verify all tools have complete schemas
  - All parameters documented
  - All return types specified
  - Descriptions are clear

- [ ] Check for schema inconsistencies
  - Type mismatches (int vs integer)
  - Missing required fields
  - Duplicate tool names across servers

### 7.2 Documentation
- [ ] Update `docs/session_summary.md` with test results
- [ ] Document which agents are AI-powered vs mock
- [ ] Create troubleshooting guide for common errors
- [ ] Add screenshots of successful tool calls

### 7.3 Automated Tests
- [ ] Create `tests/test_mcp_stdio_server.py`
  - Test initialize, tools/list, tools/call
  - Mock LLM responses for AI tests
  - Test error handling

- [ ] Add integration tests
  - Spawn MCP server subprocess
  - Send JSON-RPC via stdin
  - Verify stdout responses

---

## Test Execution Checklist

### Quick Smoke Test (5 minutes)
1. Open Cursor Settings → Tools & MCP
2. Verify all 10 servers show green dots
3. Open Cursor Composer
4. Call one tool from each server
5. Verify responses make sense

### Full Test (30 minutes)
1. Run Phase 2: Test all 10 servers
2. Run Phase 3: Edge cases (10 test cases)
3. Run Phase 5: Real-world scenarios (3 workflows)
4. Document any failures or unexpected behavior

### With API Key (15 minutes)
1. Add `ANTHROPIC_API_KEY` to config
2. Restart Cursor
3. Test 3 AI agents with real code
4. Compare AI vs mock responses
5. Measure latency and cost

---

## Success Criteria

**Minimum (MVP):**
- [x] All 10 servers connect successfully
- [x] At least 5 tools tested and working
- [x] Mock execution returns valid data
- [ ] No crashes or errors in normal use

**Full (Production-Ready):**
- [ ] All servers tested with at least 1 tool
- [ ] Edge cases handled gracefully
- [ ] AI execution working (with API key)
- [ ] Performance acceptable (<5s per call)
- [ ] Documentation complete
- [ ] Automated tests passing

**Stretch (Ideal):**
- [ ] 100% tool coverage tested
- [ ] Load testing (100+ calls)
- [ ] Multi-editor support (Windsurf, Cline)
- [ ] CI/CD integration
- [ ] Public demo/tutorial

---

## Known Issues

1. **Unnamed server** - Test fixture in config, should filter out
2. **API key not set** - AI agents return mock data only
3. **No automated tests** - Manual testing only so far
4. **No timeout handling** - Long-running tools may hang

---

## Next Actions

1. **Complete Phase 2** - Test remaining 5 servers
2. **Run Phase 3** - Edge case testing
3. **Decide on AI strategy** - Own LLM vs Cursor's AI
4. **Add ANTHROPIC_API_KEY** - Test real AI execution
5. **Document findings** - Update session_summary.md

---

**Test Log:**

| Date | Phase | Result | Notes |
|------|-------|--------|-------|
| 2025-09-30 | 1.1-1.2 | ✅ Pass | All basic tests working |
| 2025-09-30 | 2.1 | ✅ Pass | 5/10 servers tested |
| TBD | 2.2 | Pending | Test remaining 5 servers |
| TBD | 3.x | Pending | Edge case testing |
| TBD | 4.2 | Pending | AI execution with key |
