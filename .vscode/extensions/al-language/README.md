# AssertLang Language Support

**Syntax highlighting and file icons for AssertLang (.al) contract files**

Write executable contracts once, transpile to Python, JavaScript, TypeScript, Go, Rust, or C#. Deterministic multi-agent coordination for CrewAI, LangGraph, and AutoGen.

## Features

- **Syntax Highlighting** - Full colorization for .al contract files
- **File Icons** - AssertLang logo appears next to .al files in explorer
- **Auto-closing** - Brackets, quotes, and parentheses
- **Comment Toggling** - Use Cmd+/ or Ctrl+/ to toggle comments
- **Code Folding** - Collapse/expand functions and classes

## Installation

This extension loads automatically when you open the AssertLang workspace in VS Code.

### Manual Installation

If you want to install globally:

1. Package the extension:
   ```bash
   cd .vscode/extensions/al-language
   npm install -g vsce
   vsce package
   ```

2. Install the .vsix file:
   ```bash
   code --install-extension al-language-1.0.0.vsix
   ```

## Usage

1. Open any `.al` file
2. Syntax highlighting applies automatically
3. AssertLang logo appears next to .al files in the file tree

### Enable File Icons

1. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
2. Type: `Preferences: File Icon Theme`
3. Select: `AssertLang Icons`

## Supported File Types

- `.al` - AssertLang contract files

## Keywords Highlighted

- **Control Flow**: `if`, `else`, `for`, `while`, `return`, `break`, `continue`
- **Declarations**: `function`, `let`, `const`, `var`, `class`, `contract`
- **Error Handling**: `try`, `catch`, `finally`, `throw`
- **Types**: `int`, `float`, `string`, `bool`, `list`, `map`, `Option`, `Result`

## License

MIT License - See LICENSE file in the AssertLang repository

## Example Contract

```al
// user_service.al
function createUser(name: string, email: string) -> Result<User, Error> {
    if (str.length(name) < 1) {
        return Error("name", "Name cannot be empty");
    }

    if (!str.contains(email, "@")) {
        return Error("email", "Invalid email format");
    }

    return Ok(User(name, email));
}
```

Transpile to any language:
```bash
asl build user_service.al --lang python -o user_service.py
asl build user_service.al --lang javascript -o user_service.js
```

## Links

- **Website**: https://assertlang.dev
- **GitHub**: https://github.com/AssertLang/AssertLang
- **Documentation**: https://github.com/AssertLang/AssertLang#readme
- **Examples**: https://github.com/AssertLang/AssertLang/tree/main/examples
- **Issues**: https://github.com/AssertLang/AssertLang/issues

## About AssertLang

AssertLang v0.1.6 is production-ready for Python with 67/67 tests passing and zero manual fixes required. Multi-language transpilation supports 6 target languages with proven deterministic coordination.
