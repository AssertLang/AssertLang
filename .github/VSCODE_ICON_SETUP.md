# VS Code Icon Setup for .al Files

**How to show the AssertLang logo next to .al files in VS Code**

---

## Option 1: Use AssertLang Icons Theme (Recommended) ✅

This is the **easiest** and works alongside Seti for everything else.

### Steps:

1. **Reload VS Code:**
   ```
   Cmd+Shift+P (Mac) or Ctrl+Shift+P (Windows/Linux)
   Type: "Developer: Reload Window"
   Press Enter
   ```

2. **Select AssertLang Icons:**
   ```
   Cmd+Shift+P (Mac) or Ctrl+Shift+P (Windows/Linux)
   Type: "Preferences: File Icon Theme"
   Select: "AssertLang Icons"
   ```

3. **Verify:**
   - Open any .al file: `examples/agent_coordination/user_service_contract.al`
   - Look at the file tree - you should see the AssertLang logo!

**Result:** .al files show AssertLang logo, everything else uses VS Code default icons.

---

## Option 2: Keep Seti Theme + Add .al Icon

If you want to keep using Seti for ALL files and just add .al support:

### Method A: Use Workspace Settings (Already Done!)

The `.vscode/settings.json` file is already configured. You have two choices:

**Choice 1 - Use AssertLang Icons (current default):**
```json
{
  "workbench.iconTheme": "AssertLang Icons"
}
```

**Choice 2 - Keep Seti, manual configuration:**
1. Edit `.vscode/settings.json`
2. Comment out line 6
3. Uncomment lines 8-13
4. Reload VS Code

**Note:** Method A (AssertLang Icons) is simpler and recommended.

### Method B: User Settings Override

Add to your **user settings** (Cmd+Shift+P → "Preferences: Open User Settings (JSON)"):

```json
{
  "workbench.iconTheme": "vs-seti",
  "vsicons.associations.files": [
    { "icon": "assertlang", "extensions": ["al"], "format": "svg" }
  ]
}
```

Then copy `.vscode/extensions/al-language/icons/al-icon.svg` to your VS Code icons directory.

---

## Option 3: Install Material Icon Theme + Custom Association

If you use Material Icon Theme:

1. Install Material Icon Theme from VS Code marketplace
2. Add to settings.json:
   ```json
   {
     "material-icon-theme.files.associations": {
       "*.al": "../../.vscode/extensions/al-language/icons/al-icon"
     }
   }
   ```
3. Reload VS Code

---

## Comparison of Options

| Option | Pros | Cons |
|--------|------|------|
| **AssertLang Icons** | ✅ Easy<br>✅ No config needed<br>✅ Works immediately | ⚠️ Only shows icons for .al files |
| **Seti + Manual** | ✅ Keeps Seti theme<br>✅ Shows all file icons | ❌ Requires manual setup<br>❌ More complex |
| **Material Icons** | ✅ Full icon set<br>✅ Customizable | ❌ Requires extension install<br>❌ Additional dependency |

---

## Recommended Setup

**For AssertLang development (this repository):**
```
Use: AssertLang Icons
Reason: Shows logo for .al files, simple setup
```

**For personal use (if you love Seti):**
```
Use: Seti + Manual configuration (Option 2, Method B)
Reason: Keeps your preferred icon theme
```

---

## Current Configuration

The AssertLang repository is configured to use **AssertLang Icons** by default.

**What's set up:**
- `.vscode/extensions/al-language/` - Extension folder
- `.vscode/extensions/al-language/icons/al-icon.svg` - Logo (86KB)
- `.vscode/settings.json` - Workspace settings
- `.vscode/extensions.json` - Recommended extensions

**To activate:** Just reload VS Code! (`Cmd+Shift+P` → `Developer: Reload Window`)

---

## Troubleshooting

### Logo not showing?

**1. Reload VS Code**
```
Cmd+Shift+P → "Developer: Reload Window"
```

**2. Check icon theme is selected**
```
Cmd+Shift+P → "Preferences: File Icon Theme"
Should show "AssertLang Icons" selected
```

**3. Verify extension folder exists**
```
ls .vscode/extensions/al-language/icons/al-icon.svg
```

**4. Check file association**
```
# Open any .al file
# Bottom-right corner should say "AL" (language mode)
# If it says "Plain Text", click it and select "AL"
```

### Want to use a different theme?

Edit `.vscode/settings.json`:
```json
{
  "workbench.iconTheme": "vs-seti"  // or "material-icon-theme", etc.
}
```

Then follow Option 2 or 3 above to add .al support.

---

## File Structure

```
AssertLang/
├── .vscode/
│   ├── extensions/
│   │   └── al-language/
│   │       ├── package.json           # Extension manifest
│   │       ├── icons/
│   │       │   └── al-icon.svg       # AssertLang logo
│   │       ├── syntaxes/
│   │       │   └── al.tmLanguage.json # Syntax highlighting
│   │       └── iconTheme.json        # Icon theme definition
│   ├── extensions.json                # Recommended extensions
│   └── settings.json                  # Workspace settings
```

---

## Summary

**Easiest way:** Use AssertLang Icons (already set up!)

**Steps:**
1. Reload VS Code: `Cmd+Shift+P` → `Developer: Reload Window`
2. Select icon theme: `Cmd+Shift+P` → `Preferences: File Icon Theme` → `AssertLang Icons`
3. Open any .al file to see the logo!

**Done!** 🎉

---

**Last Updated:** 2025-10-17
**Extension Version:** 1.0.0
**Icon File:** `.vscode/extensions/al-language/icons/al-icon.svg` (86KB)
