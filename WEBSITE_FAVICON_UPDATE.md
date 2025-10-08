# Promptware.dev Favicon & Branding Update

## Priority: HIGH
**Issue**: Browser tab shows Versace logo (hosting provider default) instead of Promptware logo

---

## Files to Upload

Located in: `docs/images/`

1. **favicon.svg** (357 bytes) - Modern browsers
2. **favicon.ico** (15 KB) - Legacy browser support (IE, old browsers)
3. **favicon-16x16.png** (1.5 KB) - Small icon
4. **favicon-32x32.png** (1.7 KB) - Standard icon
5. **apple-touch-icon.png** (60 KB) - iOS home screen

**Color**: Purple (#6B46C1) with white "PW" text

---

## HTML Updates Required

Add to `<head>` section of all pages:

```html
<!-- Favicon -->
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="shortcut icon" href="/favicon.ico">

<!-- Apple Touch Icon -->
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">

<!-- Web App Manifest (optional but recommended) -->
<link rel="manifest" href="/site.webmanifest">
```

---

## Optional: Web App Manifest

Create `/site.webmanifest`:

```json
{
  "name": "Promptware",
  "short_name": "PW",
  "icons": [
    {
      "src": "/favicon-32x32.png",
      "sizes": "32x32",
      "type": "image/png"
    },
    {
      "src": "/apple-touch-icon.png",
      "sizes": "180x180",
      "type": "image/png"
    }
  ],
  "theme_color": "#6B46C1",
  "background_color": "#ffffff",
  "display": "standalone"
}
```

---

## File Locations on Server

Place files in website root:

```
/
├── favicon.svg
├── favicon.ico
├── favicon-16x16.png
├── favicon-32x32.png
├── apple-touch-icon.png
└── site.webmanifest (optional)
```

---

## Color Consistency Update (RECOMMENDED)

**Current**: Website uses green or mixed colors
**Recommended**: Update to purple (#6B46C1) everywhere

**Why purple**:
- ✅ Matches VSCode extension (already purple)
- ✅ Matches GitHub repository branding
- ✅ Stands out from competitors (most dev tools = blue)
- ✅ Modern, technical, creative feel
- ✅ Works in both light and dark mode

**Purple Palette**:
```css
--primary-purple: #6B46C1;
--light-purple: #A371F7;
--dark-purple: #5B3AA1;
```

**Where to update**:
- Logo/branding
- CTA buttons
- Links
- Accents
- Code highlighting

---

## Testing After Update

1. **Clear browser cache**: Hard refresh (Cmd+Shift+R / Ctrl+Shift+F5)
2. **Check multiple browsers**:
   - Chrome (favicon.svg)
   - Safari (favicon.svg or favicon.ico)
   - Firefox (favicon.svg)
   - Mobile Safari (apple-touch-icon.png)
3. **Verify**:
   - Browser tab shows purple "PW" icon
   - No more Versace logo
   - Icon appears on all pages

---

## Visual Preview

**Current**: Versace logo (hosting provider default) ❌
**After update**: Purple square with white "PW" text ✅

Icon will look like:
```
┌────────┐
│   PW   │  (Purple background #6B46C1)
└────────┘  (White text, bold, centered)
```

---

## Additional Recommendations

### 1. Update Open Graph Tags

For social media sharing, add:

```html
<meta property="og:image" content="/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="/og-image.png">
```

(We can generate og-image.png if needed - 1200x630 purple banner with "Promptware" branding)

### 2. Update Theme Color

Add for mobile browsers:

```html
<meta name="theme-color" content="#6B46C1">
```

This colors the browser chrome on mobile to match your brand.

---

## Files Attached

All files are in the GitHub repo at:
`https://github.com/Promptware-dev/promptware/tree/main/docs/images/`

- favicon.svg
- favicon.ico
- favicon-16x16.png
- favicon-32x32.png
- apple-touch-icon.png

Download and upload to website root.

---

**Expected Impact**:
- Professional branding in browser tabs ✅
- Consistent purple brand identity ✅
- Better mobile web app experience ✅
- Improved social media sharing (if OG image added) ✅

**Urgency**: Medium-High (affects brand perception on every page load)

---

**Last Updated**: 2025-10-08
**Created By**: Claude Code - Session 20
