# PW Language Support for VS Code

Syntax highlighting and file icons for PW (Promptware) - the universal programming language.

## Features

- **Syntax Highlighting**: Full colorization for PW syntax
  - Keywords: `function`, `if`, `else`, `return`, `let`, etc.
  - Types: `int`, `float`, `string`, `bool`, `array`, `map`
  - Comments: `//` and `/* */`
  - Strings, numbers, operators

- **File Icons**: Purple "PW" icon for `.pw` files in file explorer

- **Auto-Closing**: Automatic closing of brackets, braces, quotes

- **Comment Toggling**: Use `Cmd+/` (Mac) or `Ctrl+/` (Windows/Linux)

## Installation

### Option 1: Local Development (Current Setup)

The extension is already in `.vscode/extensions/pw-language/` and will be automatically loaded when you open this workspace.

### Option 2: Install Globally

```bash
cd .vscode/extensions/pw-language
vsce package
code --install-extension pw-language-0.1.0.vsix
```

### Option 3: Publish to VS Code Marketplace

(Coming soon!)

## Usage

Just open any `.pw` file and enjoy syntax highlighting!

## Example

```pw
// PW code with syntax highlighting
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

For issues or feature requests, visit: https://github.com/Promptware-dev/promptware
