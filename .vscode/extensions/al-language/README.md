# AssertLang Language Support

**Syntax highlighting and file icons for AssertLang (.al) contract files**

## Features

- **Syntax Highlighting** - Full colorization for .al files
- **File Icons** - AssertLang logo appears next to .al files
- **Auto-closing** - Brackets, quotes, and parentheses
- **Comment Toggling** - Use Cmd+/ or Ctrl+/ to toggle comments
- **Code Folding** - Collapse/expand code blocks

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

## Links

- **GitHub**: https://github.com/AssertLang/AssertLang
- **Documentation**: https://github.com/AssertLang/AssertLang/tree/main/docs
- **Issues**: https://github.com/AssertLang/AssertLang/issues
