# AssertLang Logo Usage Guide

**Logo File:** `.github/assets/logo2.svg`
**Size:** 86,628 bytes
**Format:** SVG (Scalable Vector Graphics)
**Last Updated:** 2025-10-17

---

## Logo Location

The official AssertLang logo is located at:

```
.github/assets/logo2.svg
```

This logo is:
- ✅ Tracked in git (visible on GitHub)
- ✅ Used in official documentation
- ✅ Used in README.md header
- ✅ Referenced in package metadata
- ✅ Available for community use

---

## Current Usage

### 1. README.md Header ✅

The logo appears at the top of the README with centered formatting:

```html
<p align="center">
  <img src=".github/assets/logo2.svg" alt="AssertLang Logo" width="200" height="200">
</p>
```

**Location:** Line 1-3 of `README.md`

### 2. Documentation References ✅

The logo is referenced in:
- `docs/VS_CODE_EXTENSION.md` - Line 125, 143, 446

**Example:**
```markdown
🎨 **Logo:** Available at `.github/assets/logo2.svg` (official AssertLang logo)
```

### 3. GitHub Repository ✅

When viewed on GitHub, the logo appears:
- At the top of the README (first thing visitors see)
- In the `.github/assets/` directory
- In documentation pages

---

## Recommended Additional Usage

### 1. Package Metadata

**pyproject.toml** - Add project URL:

```toml
[project.urls]
Homepage = "https://github.com/AssertLang/AssertLang"
Logo = "https://raw.githubusercontent.com/AssertLang/AssertLang/main/.github/assets/logo2.svg"
```

### 2. GitHub Repository Settings

**Social Preview Image:**
1. Go to GitHub repository settings
2. Upload `.github/assets/logo2.svg` as social preview
3. This shows when sharing on Twitter, Slack, etc.

### 3. Documentation Sites

If you build a documentation website (docs.assertlang.dev):
- Use logo in header/nav bar
- Use as favicon (convert to .ico or .png)
- Use in footer

### 4. PyPI Package Page

When you update the PyPI package:
- Add logo to package description
- Include in long_description_content_type

---

## Logo Specifications

**File:** `logo2.svg`

**Characteristics:**
- Format: SVG (scales to any size)
- File size: 86KB
- Colors: Uses AssertLang brand colors
- Transparent background: Yes
- Optimized: Yes

**Recommended Sizes:**

| Use Case | Size | Format |
|----------|------|--------|
| README Header | 200x200px | SVG |
| Favicon | 16x16, 32x32, 48x48px | PNG/ICO |
| Social Media | 1200x630px | PNG |
| GitHub Profile | 400x400px | PNG/SVG |
| Documentation Nav | 40-50px height | SVG |
| Print | Any size | SVG or high-res PNG |

---

## How to Use the Logo

### In Markdown Files

**Centered with specific size:**
```html
<p align="center">
  <img src=".github/assets/logo2.svg" alt="AssertLang Logo" width="200" height="200">
</p>
```

**Inline:**
```markdown
![AssertLang Logo](.github/assets/logo2.svg)
```

**With link:**
```markdown
[![AssertLang](. github/assets/logo2.svg)](https://github.com/AssertLang/AssertLang)
```

### In HTML Files

```html
<img src=".github/assets/logo2.svg" alt="AssertLang Logo" width="200" height="200">
```

### In Python/Package Metadata

```python
# setup.py
setup(
    name="assertlang",
    project_urls={
        "Homepage": "https://github.com/AssertLang/AssertLang",
        "Logo": "https://raw.githubusercontent.com/AssertLang/AssertLang/main/.github/assets/logo2.svg",
    }
)
```

###In Documentation Sites (MkDocs, Sphinx, etc.)

**MkDocs (mkdocs.yml):**
```yaml
theme:
  logo: .github/assets/logo2.svg
  favicon: .github/assets/favicon.ico
```

**Sphinx (_static/ folder):**
```python
# conf.py
html_logo = '../.github/assets/logo2.svg'
html_favicon = '../.github/assets/favicon.ico'
```

---

## Creating Favicons from Logo

Convert SVG to favicon formats:

```bash
# Install ImageMagick if needed
brew install imagemagick  # macOS
# or: apt-get install imagemagick  # Linux

# Convert to PNG sizes
convert -background none .github/assets/logo2.svg -resize 16x16 favicon-16.png
convert -background none .github/assets/logo2.svg -resize 32x32 favicon-32.png
convert -background none .github/assets/logo2.svg -resize 48x48 favicon-48.png

# Combine into .ico
convert favicon-16.png favicon-32.png favicon-48.png favicon.ico
```

Or use online tool: https://favicon.io/favicon-converter/

---

## Logo in Social Media

### Twitter/X Card

When sharing GitHub link, Twitter shows logo if you set up:
1. GitHub repository social preview image
2. Or add to README as first image (which you've done! ✅)

### LinkedIn/Slack/Discord

These platforms automatically preview the logo from GitHub's social preview or the first image in README.

**Current Status:** ✅ Logo appears in README header, so it will show in previews!

---

## VS Code Extension

### Local Extension (Current)

The local `.vscode/extensions/` directory was removed from git tracking during cleanup.

**If you want a VS Code extension icon:**

1. Create a small icon version:
   ```bash
   convert -background none .github/assets/logo2.svg -resize 128x128 .vscode/extension-icon.png
   ```

2. Reference in `package.json`:
   ```json
   {
     "icon": "extension-icon.png"
   }
   ```

**Note:** This is for local development only (not tracked in git).

---

## File Structure

```
AssertLang/
├── .github/
│   └── assets/
│       └── logo2.svg          ✅ Official logo (tracked in git)
│
├── README.md                  ✅ Uses logo in header
│
├── docs/
│   └── VS_CODE_EXTENSION.md   ✅ References logo location
│
└── .vscode/                   ❌ Not tracked in git (local only)
    └── extensions/
        └── (extension-icon.png if needed)
```

---

## Branding Consistency Checklist

- ✅ Logo file named `logo2.svg` (in `.github/assets/`)
- ✅ Used in README.md header
- ✅ Referenced in documentation
- ✅ Visible on GitHub
- ⏳ Add to pyproject.toml project URLs
- ⏳ Create favicon variants
- ⏳ Set GitHub social preview image
- ⏳ Update PyPI package description

---

## License & Usage Rights

**Logo:** Part of AssertLang project (MIT License)

**Allowed Uses:**
- ✅ Official AssertLang documentation
- ✅ Community projects using AssertLang
- ✅ Blog posts/articles about AssertLang
- ✅ Educational materials
- ✅ Conference presentations about AssertLang

**Attribution:**
- Not required but appreciated
- Example: "AssertLang logo © AssertLang Contributors"

**Prohibited Uses:**
- ❌ Implying official endorsement without permission
- ❌ Modifications that damage brand
- ❌ Use in competing products claiming to be AssertLang

---

## Summary

**Current Implementation:** ✅ **COMPLETE**

The AssertLang logo (logo2.svg) is:
1. ✅ Stored in `.github/assets/logo2.svg`
2. ✅ Displayed in README.md header
3. ✅ Referenced in documentation
4. ✅ Tracked in git (visible on GitHub)
5. ✅ Ready for community use

**Next Steps (Optional):**
1. Add logo URL to pyproject.toml
2. Create favicon variants
3. Set GitHub social preview image
4. Add to PyPI package page

**Logo is production-ready and properly integrated!** 🎨✅

---

**Last Updated:** 2025-10-17
**Maintained By:** AssertLang Contributors
**Logo File:** `.github/assets/logo2.svg` (86KB SVG)
