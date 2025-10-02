# Good First Issues for Promptware Contributors

Welcome to Promptware! This document contains 20 well-defined issues perfect for new contributors. Each issue is designed to be completed in 2-4 hours and will help you learn the codebase while making meaningful contributions.

## How to Get Started

1. Fork the repository
2. Pick an issue from the list below
3. Comment on the issue (or create it) to claim it
4. Create a branch: `git checkout -b issue-[number]-brief-description`
5. Make your changes and test them
6. Submit a pull request

---

## Documentation Issues (7)

### Issue 1: Add Docstrings to ToolRegistry Class Methods
**Category:** Documentation
**Difficulty:** Easy
**Estimated time:** 2 hours

**Description:**
The `ToolRegistry` class in `tools/registry.py` has good docstrings for some methods but is missing detailed documentation for internal helper methods like `_load_module()` and `_load_schema()`. Add comprehensive docstrings following Google style guide.

**Acceptance criteria:**
- [ ] Add docstrings to `_load_module()` with parameter and return type descriptions
- [ ] Add docstrings to `_load_schema()` with parameter and return type descriptions
- [ ] Include example usage in docstrings where helpful
- [ ] Run existing tests to ensure no functionality is broken

**Helpful resources:**
- File: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/tools/registry.py`
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)

---

### Issue 2: Document Error Codes in MCP Error Handling Module
**Category:** Documentation
**Difficulty:** Easy
**Estimated time:** 2 hours

**Description:**
The `language/mcp_error_handling.py` module generates error handling code but lacks a comprehensive reference document explaining all standard MCP error codes (-32700 to -32007) and when to use each one.

**Acceptance criteria:**
- [ ] Create `docs/error-codes.md` documenting all MCP error codes
- [ ] Include code examples for each error type
- [ ] Add cross-references to where these codes are used in the codebase
- [ ] Update README.md to link to the new error codes documentation

**Helpful resources:**
- File: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/language/mcp_error_handling.py`
- JSON-RPC 2.0 specification for standard error codes

---

### Issue 3: Add Inline Comments to Parser Complex Logic
**Category:** Documentation
**Difficulty:** Easy
**Estimated time:** 2 hours

**Description:**
The DSL parser in `language/parser.py` has complex indentation and state management logic (lines 56-100) that would benefit from inline comments explaining the parsing algorithm.

**Acceptance criteria:**
- [ ] Add inline comments explaining the stack-based parsing approach
- [ ] Document the indentation validation logic (lines 72-77)
- [ ] Add comments explaining the state transitions in the parser
- [ ] Ensure comments are clear and helpful for new contributors

**Helpful resources:**
- File: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/language/parser.py`
- Lines 56-100 contain the main parsing loop

---

### Issue 4: Create Tutorial for Building Custom Tool Adapters
**Category:** Documentation
**Difficulty:** Easy
**Estimated time:** 3 hours

**Description:**
Write a step-by-step tutorial showing how to create a new tool adapter from scratch. Use a simple example like a "calculator" tool that demonstrates the full process.

**Acceptance criteria:**
- [ ] Create `docs/tutorials/custom-tool-adapter.md`
- [ ] Include step-by-step instructions with code examples
- [ ] Show how to create the adapter file structure
- [ ] Demonstrate how to write the schema file
- [ ] Include testing the new tool
- [ ] Add to main documentation index

**Helpful resources:**
- Existing tools in `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/tools/`
- File: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/tools/http/adapters/adapter_py.py` (good example)
- Contributing guide: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/CONTRIBUTING.md`

---

### Issue 5: Improve CLI Help Text with Examples
**Category:** Documentation
**Difficulty:** Easy
**Estimated time:** 2 hours

**Description:**
The CLI in `promptware/cli.py` has basic help text but could be enhanced with more practical examples and better formatting for each command.

**Acceptance criteria:**
- [ ] Add 2-3 practical examples for each CLI command
- [ ] Improve the formatting of help text for readability
- [ ] Add common troubleshooting tips to help messages
- [ ] Test that all help messages display correctly

**Helpful resources:**
- File: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/promptware/cli.py`
- Look at the `create_parser()` function starting at line 81

---

### Issue 6: Document ToolExecutor Parameter Mapping Logic
**Category:** Documentation
**Difficulty:** Easy
**Estimated time:** 2 hours

**Description:**
The `ToolExecutor` class in `language/tool_executor.py` has a `_map_params_to_tool()` method with TODO comments about future mapping configuration. Document the current mapping strategy and design considerations for future enhancements.

**Acceptance criteria:**
- [ ] Add comprehensive docstring to `_map_params_to_tool()` method
- [ ] Create `docs/architecture/tool-parameter-mapping.md` explaining the design
- [ ] Document examples of parameter mapping scenarios
- [ ] Include design considerations for future explicit mapping configuration

**Helpful resources:**
- File: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/language/tool_executor.py`
- Lines 72-96 contain the mapping logic

---

### Issue 7: Add Architecture Diagram for MCP Server Generation
**Category:** Documentation
**Difficulty:** Easy
**Estimated time:** 3 hours

**Description:**
Create a visual architecture diagram showing how .pw files are parsed and transformed into multi-language MCP servers. Use mermaid.js or ASCII art for easy embedding in markdown.

**Acceptance criteria:**
- [ ] Create diagram showing: .pw input → Parser → Generator → Output (Python/Node/Go/Rust/C#)
- [ ] Include middleware injection points in the diagram
- [ ] Show tool loading and execution flow
- [ ] Add diagram to `docs/architecture/code-generation-flow.md`
- [ ] Ensure diagram renders correctly on GitHub

**Helpful resources:**
- Files in `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/language/` directory
- Main README architecture section for reference
- [Mermaid.js documentation](https://mermaid.js.org/)

---

## Testing Issues (5)

### Issue 8: Add Unit Tests for Parser Error Handling
**Category:** Testing
**Difficulty:** Easy
**Estimated time:** 2 hours

**Description:**
The `PWParseError` exception in `language/parser.py` is used throughout the parser but lacks dedicated unit tests for various error scenarios.

**Acceptance criteria:**
- [ ] Create test file `tests/test_parser_errors.py`
- [ ] Add test for indentation errors (non-multiple of 2 spaces)
- [ ] Add test for invalid syntax errors
- [ ] Add test for proper error code propagation
- [ ] Ensure all tests pass with pytest

**Helpful resources:**
- File: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/language/parser.py`
- Existing test examples in `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/tests/`
- Run tests with: `python3 -m pytest tests/test_parser_errors.py -v`

---

### Issue 9: Add Edge Case Tests for HTTP Tool Adapter
**Category:** Testing
**Difficulty:** Easy
**Estimated time:** 2 hours

**Description:**
The HTTP tool adapter in `tools/http/adapters/adapter_py.py` handles various HTTP methods but lacks tests for edge cases like timeouts, invalid URLs, and error responses.

**Acceptance criteria:**
- [ ] Add test for connection timeout scenarios
- [ ] Add test for invalid URL formats
- [ ] Add test for HTTP error status codes (4xx, 5xx)
- [ ] Add test for missing required parameters
- [ ] All tests should use mocking to avoid external dependencies

**Helpful resources:**
- File: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/tools/http/adapters/adapter_py.py`
- Existing tool tests in `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/tests/tools/`
- Use `pytest-mock` for HTTP request mocking

---

### Issue 10: Add Integration Tests for Tool Registry
**Category:** Testing
**Difficulty:** Easy
**Estimated time:** 3 hours

**Description:**
The `ToolRegistry` class in `tools/registry.py` loads and executes tools dynamically but lacks integration tests that verify the full load-execute cycle with real tool adapters.

**Acceptance criteria:**
- [ ] Create test file `tests/test_tool_registry_integration.py`
- [ ] Test successful tool loading and execution with a real tool
- [ ] Test tool not found scenario
- [ ] Test caching behavior (loading same tool twice)
- [ ] Test error handling when tool execution fails
- [ ] All tests must pass

**Helpful resources:**
- File: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/tools/registry.py`
- Simple tool for testing: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/tools/http/`

---

### Issue 11: Improve Test Coverage for MCP Exception Classes
**Category:** Testing
**Difficulty:** Easy
**Estimated time:** 2 hours

**Description:**
The exception classes in `promptware/exceptions.py` define custom error types but don't have comprehensive tests verifying their attributes and behavior.

**Acceptance criteria:**
- [ ] Create test file `tests/test_exceptions.py`
- [ ] Test each exception class initialization
- [ ] Test exception message formatting
- [ ] Test error code attribute propagation
- [ ] Test inheritance from base `MCPError` class
- [ ] Achieve 100% coverage of exceptions.py

**Helpful resources:**
- File: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/promptware/exceptions.py`
- Look at exception classes: `ConnectionError`, `TimeoutError`, `InvalidVerbError`, etc.

---

### Issue 12: Add Tests for CLI Argument Parsing
**Category:** Testing
**Difficulty:** Easy
**Estimated time:** 3 hours

**Description:**
The CLI in `promptware/cli.py` has a `create_parser()` function that defines all command-line arguments, but there are no tests verifying correct argument parsing for different commands.

**Acceptance criteria:**
- [ ] Create test file `tests/test_cli_parser.py`
- [ ] Test argument parsing for `generate` command with all flags
- [ ] Test argument parsing for `test` command with all flags
- [ ] Test argument parsing for `init` command with templates
- [ ] Test error handling for invalid arguments
- [ ] Use argparse test utilities for isolation

**Helpful resources:**
- File: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/promptware/cli.py`
- Look at `create_parser()` function (line 81)
- Python argparse testing patterns

---

## Code Quality Issues (4)

### Issue 13: Add Type Hints to Tool Executor Module
**Category:** Code Quality
**Difficulty:** Easy
**Estimated time:** 2 hours

**Description:**
The `language/tool_executor.py` module has some type hints but is missing them for several internal methods. Add complete type annotations for better IDE support and type checking.

**Acceptance criteria:**
- [ ] Add type hints to all parameters and return types
- [ ] Add type hints for class attributes in `__init__`
- [ ] Import necessary types from `typing` module
- [ ] Run `mypy` to verify type correctness
- [ ] No new mypy errors introduced

**Helpful resources:**
- File: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/language/tool_executor.py`
- Python typing module documentation
- Run mypy: `mypy language/tool_executor.py`

---

### Issue 14: Extract Magic Strings to Constants in MCP Generators
**Category:** Code Quality
**Difficulty:** Easy
**Estimated time:** 2 hours

**Description:**
The MCP generator files contain repeated magic strings like "jsonrpc", "2.0", error codes, etc. Extract these to named constants for better maintainability.

**Acceptance criteria:**
- [ ] Create `language/mcp_constants.py` with all MCP protocol constants
- [ ] Replace magic strings in Python generator with constants
- [ ] Replace magic strings in Node.js generator with constants
- [ ] Update at least one other language generator
- [ ] Ensure all tests still pass

**Helpful resources:**
- Files: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/language/mcp_server_generator.py`
- Files: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/language/mcp_server_generator_nodejs.py`

---

### Issue 15: Improve Variable Naming in Parser Module
**Category:** Code Quality
**Difficulty:** Easy
**Estimated time:** 2 hours

**Description:**
The parser module uses some abbreviated variable names (`i`, `ctx`, `t`, etc.) that could be more descriptive for better code readability.

**Acceptance criteria:**
- [ ] Rename single-letter loop variables to descriptive names
- [ ] Rename `ctx` to `context` or more specific names
- [ ] Update any abbreviated variable names to full words
- [ ] Ensure all tests pass after renaming
- [ ] No functional changes, only naming improvements

**Helpful resources:**
- File: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/language/parser.py`
- Focus on the main parsing loop (lines 56-100)
- Run tests: `pytest tests/test_agent_parser.py -v`

---

### Issue 16: Refactor Duplicate Error Handling Code in Generators
**Category:** Code Quality
**Difficulty:** Easy
**Estimated time:** 3 hours

**Description:**
Multiple generator files (Python, Node.js, Go, etc.) contain similar error handling code. Extract common error handling patterns into shared utility functions.

**Acceptance criteria:**
- [ ] Identify duplicate error handling patterns across generators
- [ ] Create shared utility functions in `language/mcp_error_handling.py`
- [ ] Refactor Python generator to use shared utilities
- [ ] Refactor Node.js generator to use shared utilities
- [ ] Ensure all generated servers still work correctly
- [ ] Reduce code duplication by at least 30%

**Helpful resources:**
- Files: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/language/mcp_server_generator*.py`
- File: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/language/mcp_error_handling.py`

---

## Feature Issues (3)

### Issue 17: Add --dry-run Flag to Generate Command
**Category:** Feature
**Difficulty:** Easy
**Estimated time:** 3 hours

**Description:**
Add a `--dry-run` flag to the `generate` command that shows what would be generated without actually writing files. This helps users preview output before generating.

**Acceptance criteria:**
- [ ] Add `--dry-run` argument to generate command parser
- [ ] Implement dry-run mode that prints file paths and sizes
- [ ] Show summary of what would be generated
- [ ] Don't create any files in dry-run mode
- [ ] Add test for dry-run functionality
- [ ] Update CLI documentation

**Helpful resources:**
- File: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/promptware/cli.py`
- Look at the `generate` command implementation
- README mentions this feature: line 249

---

### Issue 18: Add JSON Output Format for Test Command
**Category:** Feature
**Difficulty:** Easy
**Estimated time:** 3 hours

**Description:**
Add a `--json` flag to the `test` command that outputs results in JSON format for easier parsing by CI/CD tools.

**Acceptance criteria:**
- [ ] Add `--json` argument to test command parser
- [ ] Implement JSON output formatter for test results
- [ ] Include all test metrics (pass/fail counts, timing, etc.)
- [ ] Maintain backwards compatibility with regular output
- [ ] Add example JSON output to documentation
- [ ] Test with CI/CD tools if possible

**Helpful resources:**
- File: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/promptware/cli.py`
- Test command implementation
- Standard JSON Schema for test results

---

### Issue 19: Improve Error Messages for Missing Tool Dependencies
**Category:** Feature
**Difficulty:** Easy
**Estimated time:** 2 hours

**Description:**
When a tool fails to load due to missing dependencies, the error message is generic. Enhance error messages to suggest the specific package that needs to be installed.

**Acceptance criteria:**
- [ ] Update `ToolRegistry._load_module()` to catch `ImportError`
- [ ] Parse the import error to identify missing package
- [ ] Provide helpful error message with install command
- [ ] Add test for helpful error message generation
- [ ] Document common tool dependencies

**Helpful resources:**
- File: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/tools/registry.py`
- Method: `_load_module()` at line 72

---

## Tooling Issues (1)

### Issue 20: Add Pre-commit Hook Configuration
**Category:** Tooling
**Difficulty:** Easy
**Estimated time:** 2 hours

**Description:**
Set up pre-commit hooks to automatically run code formatting (black), linting (flake8), and basic tests before commits. This ensures code quality consistency.

**Acceptance criteria:**
- [ ] Create `.pre-commit-config.yaml` file
- [ ] Add black formatter hook
- [ ] Add flake8 linting hook
- [ ] Add trailing whitespace check
- [ ] Add instructions to CONTRIBUTING.md for setting up pre-commit
- [ ] Test hooks work correctly

**Helpful resources:**
- [pre-commit framework](https://pre-commit.com/)
- File: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/CONTRIBUTING.md` (to update)
- Check setup.py for dev dependencies

---

## Getting Help

- **Questions?** Open a discussion on GitHub Discussions
- **Stuck?** Comment on the issue and tag @maintainers
- **Ready to submit?** Create a PR and reference the issue number

## Recognition

All contributors will be:
- Added to CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in commit messages

Thank you for contributing to Promptware!
