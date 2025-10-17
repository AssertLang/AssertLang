# AL Language Support for VS Code

Syntax highlighting and file icons for AL (AssertLang) - executable contracts for multi-agent systems.

## Features

- **Syntax Highlighting**: Full colorization for AL syntax
  - Keywords: `function`, `if`, `else`, `return`, `let`, etc.
  - Types: `int`, `float`, `string`, `bool`, `array`, `map`
  - Comments: `//` and `/* */`
  - Strings, numbers, operators

- **File Icons**: Purple "AL" icon for `.al` files in file explorer

- **Auto-Closing**: Automatic closing of brackets, braces, quotes

- **Comment Toggling**: Use `Cmd+/` (Mac) or `Ctrl+/` (Windows/Linux)

## Installation

### Option 1: Local Development (Current Setup)

The extension is already in `.vscode/extensions/al-language/` and will be automatically loaded when you open this workspace.

### Option 2: Install Globally

```bash
cd .vscode/extensions/al-language
vsce package
code --install-extension al-language-2.0.0.vsix
```

### Option 3: Publish to VS Code Marketplace

(Coming soon!)

## Usage

Just open any `.al` file and enjoy syntax highlighting!

## Example

```al
// AL code with syntax highlighting
function greet(name: string) -> string {
    return "Hello, " + name + "!";
}

function calculate(x: int, y: int) -> int {
    if (x > y) {
        return x - y;
    } else {
        return y - x;
    }
}
```

## Language Features

- C-style syntax with braces `{ }`
- Type annotations (`:` for parameters, `->` for return types)
- C-style comments (`//` and `/* */`)
- Keywords: `function`, `if`, `else`, `return`, `let`, etc.
- Primitive types: `int`, `float`, `string`, `bool`
- Collection types: `array`, `map`, `set`

## Support

For issues or feature requests, visit: https://github.com/AssertLang/AssertLang
