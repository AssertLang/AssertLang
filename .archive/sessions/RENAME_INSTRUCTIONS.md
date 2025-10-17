# Rename Folder: Promptware → AssertLang

**Status:** Optional (folder name doesn't affect functionality)
**Time:** 5 minutes
**Risk:** Low (easy rollback)

---

## Why Rename?

The root folder is still called `Promptware` but everything else is `AssertLang`. Renaming the folder completes the rebrand.

**What works without renaming:**
- ✅ Git repository
- ✅ Python package (`assertlang`)
- ✅ CLI command (`asl`)
- ✅ All code and imports
- ✅ CI/CD on GitHub

**What needs fixing after rename:**
- ⚠️ `.cursor/mcp.json` (hardcoded paths)
- ⚠️ `.venv` (virtual environment paths)

---

## Automated Rename (Recommended)

**One command does everything:**

```bash
# From inside the Promptware folder:
./rename_to_assertlang.sh
```

**What it does:**
1. ✅ Creates git checkpoint (safety backup)
2. ✅ Renames folder `Promptware` → `AssertLang`
3. ✅ Fixes `.cursor/mcp.json` paths (11 MCP servers)
4. ✅ Recreates `.venv` with correct paths
5. ✅ Reinstalls package in editable mode
6. ✅ Verifies everything works

**Output:**
```
🔄 Renaming Promptware → AssertLang

📝 Step 1/5: Creating safety checkpoint...
📁 Step 2/5: Renaming folder...
   ✓ Renamed folder
   ✓ Entered AssertLang
🔧 Step 3/5: Fixing MCP configuration...
   ✓ Updated 33 paths in .cursor/mcp.json
   ✓ Backup saved: .cursor/mcp.json.bak
🐍 Step 4/5: Recreating virtual environment...
   ✓ Removed old .venv
   ✓ Created new .venv
   ✓ Activated .venv
   ✓ Installed package in editable mode
✅ Step 5/5: Verifying setup...
   ✓ Git repository: OK
   ✓ Python import: OK
   ✓ CLI command (asl): OK

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ SUCCESS: Renamed to AssertLang
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 New location: /Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/AssertLang
```

**Time:** ~2 minutes (mostly `pip install`)

---

## Manual Rename (If You Prefer)

**Step-by-step:**

### 1. Create Checkpoint
```bash
git add -A
git commit -m "Pre-rename checkpoint"
```

### 2. Rename Folder
```bash
cd /Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/
mv Promptware AssertLang
cd AssertLang
```

### 3. Fix MCP Config
```bash
sed -i '' 's|/Promptware/|/AssertLang/|g' .cursor/mcp.json
```

### 4. Recreate Virtual Environment
```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 5. Verify
```bash
git status
python -c "import assertlang; print('✅ Import works')"
asl --version
```

---

## Rollback (If Something Breaks)

**Quick rollback:**
```bash
cd /Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/
mv AssertLang Promptware
cd Promptware
git reset --hard HEAD~1  # Undo checkpoint commit
```

---

## What Gets Updated

### .cursor/mcp.json (11 servers × 3 paths each = 33 changes)
```json
// BEFORE
"command": "/Users/.../Promptware/.venv/bin/python3",
"args": ["/Users/.../Promptware/language/mcp_stdio_server.py", ...],
"env": {"PYTHONPATH": "/Users/.../Promptware"}

// AFTER
"command": "/Users/.../AssertLang/.venv/bin/python3",
"args": ["/Users/.../AssertLang/language/mcp_stdio_server.py", ...],
"env": {"PYTHONPATH": "/Users/.../AssertLang"}
```

### .venv (Recreated with New Paths)
```bash
# OLD (broken after rename)
.venv/bin/activate: VIRTUAL_ENV="/Users/.../Promptware/.venv"

# NEW (working)
.venv/bin/activate: VIRTUAL_ENV="/Users/.../AssertLang/.venv"
```

---

## Testing After Rename

**Run these to verify everything works:**

```bash
# Activate venv
source .venv/bin/activate

# Test git
git status

# Test Python import
python -c "import assertlang; print('✅ Package works')"

# Test CLI
asl --version

# Test full test suite (optional, ~30 seconds)
pytest tests/

# Test MCP servers (optional)
# Open Cursor and check MCP servers still connect
```

---

## When to Rename

**Rename now if:**
- You want 100% consistency (folder name matches brand)
- You're about to do fresh git clone somewhere
- You're setting up on a new machine

**Wait to rename if:**
- You're in the middle of work (finish first)
- You're about to create PR/release (do after)
- You're not sure (it's optional!)

---

## FAQ

**Q: Will this break my git history?**
A: No - git tracks content, not folder names. All history stays intact.

**Q: Will this affect GitHub?**
A: No - GitHub repo name is separate from local folder name.

**Q: Can I undo it?**
A: Yes - just `mv AssertLang Promptware` and reset git checkpoint.

**Q: Do I have to do this?**
A: No - it's optional. Everything works fine with old folder name.

**Q: Will this affect the package on PyPI?**
A: No - package name comes from `pyproject.toml`, not folder name.

**Q: What if I have multiple terminal windows open?**
A: Close them first, or they'll still be in old directory and get confused.

---

## Recommendation

**Use the automated script:**
```bash
./rename_to_assertlang.sh
```

It's safe, fast, and handles everything correctly.

---

**Questions?** The script shows rollback instructions if anything breaks.
