# Contributing to Promptware

Thank you for your interest in contributing to Promptware! This document provides guidelines and instructions for contributing.

## Quick Start

1. **Fork the repository**
2. **Clone your fork:** `git clone https://github.com/YOUR-USERNAME/promptware.git`
3. **Create a branch:** `git checkout -b feature/your-feature-name`
4. **Make your changes**
5. **Test your changes:** `pytest tests/`
6. **Commit:** `git commit -m "Add: your feature description"`
7. **Push:** `git push origin feature/your-feature-name`
8. **Create a Pull Request**

## Development Setup

```bash
# Clone the repository
git clone https://github.com/Promptware-dev/promptware.git
cd promptware

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run linter
flake8 promptware/
```

**📚 For detailed development workflow, see [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)**

This includes:
- Complete development workflow
- Testing strategies
- Adding new language features
- Adding new target languages
- Debugging tips
- Release process

## Commit Message Convention

We follow conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Adding or updating tests
- `refactor:` Code refactoring
- `chore:` Build process or auxiliary tool changes

**Example:**
```
feat: add support for Rust code generation
fix: resolve tool execution timeout issue
docs: update quickstart guide with new examples
```

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to all public functions/classes
- Keep functions focused and small
- Write tests for new features

## Testing

- All new features must include tests
- Maintain or improve code coverage
- Run `pytest tests/` before submitting PR
- Test with multiple Python versions if possible (3.9+)

## Pull Request Process

1. **Update documentation** if you're adding/changing functionality
2. **Add tests** for new features
3. **Ensure all tests pass**
4. **Update CHANGELOG.md** with your changes
5. **Reference any related issues** in your PR description
6. **Wait for review** - maintainers will review your PR

## What We're Looking For

**Priority areas for contributions:**

- 🐛 **Bug fixes** - Always welcome
- 📚 **Documentation** - Examples, guides, tutorials
- 🧪 **Tests** - Improve coverage
- 🛠️ **New tools** - Add tools to the tools/ directory
- 🌐 **Language support** - Improve existing generators or add new ones
- ⚡ **Performance** - Optimizations and improvements

## Adding a New Tool

Tools are in the `tools/` directory. To add a new tool:

1. Create `tools/your-tool/adapter.py`
2. Implement the tool interface
3. Add documentation in `tools/your-tool/README.md`
4. Add tests in `tests/test_tools/test_your_tool.py`
5. Update `tools/registry.py`

## Adding Language Support

To add a new language generator:

1. Create `language/mcp_server_generator_LANG.py`
2. Implement `generate_LANG_mcp_server()` function
3. Add templates if needed
4. Add tests in `tests/test_LANG_generator.py`
5. Update CLI to support the new language

## Questions?

- 💬 **Discussions:** https://github.com/Promptware-dev/promptware/discussions
- 🐛 **Issues:** https://github.com/Promptware-dev/promptware/issues
- 📧 **Email:** hello@promptware.dev

## Code of Conduct

Please be respectful and constructive. We're building this together.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to Promptware!** 🚀
