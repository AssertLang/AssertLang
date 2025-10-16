# How to Enable PW Syntax Highlighting in VS Code

## Quick Setup (Automatic)

Since this extension is in `.vscode/extensions/`, VS Code should automatically load it when you open this workspace.

**To verify it's working:**

1. Open any `.pw` file (e.g., `examples/calculator.pw`)
2. Check the bottom-right corner of VS Code - it should say "PW"
3. You should see syntax highlighting (keywords in purple/blue, strings in orange, etc.)

## If It's Not Working

### Step 1: Reload VS Code

Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux) and run:
```
Developer: Reload Window
```

### Step 2: Check Extension is Loaded

1. Press `Cmd+Shift+P` / `Ctrl+Shift+P`
2. Type "Extensions: Show Installed Extensions"
3. Look for "PW Language Support" in the list

### Step 3: Manual Language Selection

If syntax highlighting still doesn't work:

1. Open a `.pw` file
2. Click the language indicator in bottom-right (might say "Plain Text")
3. Type "PW" or "AssertLang"
4. Select "PW" from the list

### Step 4: Enable File Icons

To see the purple "PW" icon next to `.pw` files:

1. Press `Cmd+Shift+P` / `Ctrl+Shift+P`
2. Type "Preferences: File Icon Theme"
3. Select "PW Icons"

## Color Theme Recommendations

PW syntax highlighting works with any VS Code theme, but looks especially good with:

- **Dark+** (default dark theme)
- **Monokai**
- **One Dark Pro**
- **Dracula Official**

## Troubleshooting

### Problem: No syntax highlighting

**Solution**: Check language mode in bottom-right corner. If it says "Plain Text", manually select "PW".

### Problem: No file icon

**Solution**: Make sure you've selected "PW Icons" as your file icon theme (see Step 4 above).

### Problem: Extension not found

**Solution**: Make sure you're opening VS Code from the AssertLang project root directory. The extension is workspace-specific.

## What Gets Highlighted

- **Purple/Blue**: Keywords (`function`, `if`, `return`, `let`)
- **Orange**: Strings (`"hello"`, `'world'`)
- **Green**: Numbers (`42`, `3.14`)
- **Green**: Comments (`// comment`, `/* block */`)
- **Light Blue**: Types (`int`, `float`, `string`, `bool`)
- **White/Default**: Variables, function names, operators

## Testing

Open `examples/calculator.pw` to see syntax highlighting in action!

---

**Need help?** Open an issue at: https://github.com/AssertLang/AssertLang
