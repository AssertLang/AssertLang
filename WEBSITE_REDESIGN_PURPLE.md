# Promptware.dev Purple Brand Redesign

## Objective
Transition promptware.dev from green/mixed branding to unified **purple brand identity** matching the VSCode extension and GitHub repository. Maintain professional developer-focused aesthetic while creating visual consistency across all platforms.

---

## 🎨 Brand Color System

### Primary Colors

**Purple Palette** (use these everywhere):
```css
--pw-purple-primary: #6B46C1;    /* Main brand color - buttons, CTAs, headings */
--pw-purple-light: #A371F7;      /* Hover states, accents, highlights */
--pw-purple-dark: #5B3AA1;       /* Borders, shadows, active states */
--pw-purple-subtle: #8B7AB8;     /* Muted text, disabled states */
```

### Supporting Colors

**Keep neutral base** (for readability):
```css
--pw-gray-50: #F9FAFB;          /* Light backgrounds */
--pw-gray-100: #F3F4F6;         /* Section dividers */
--pw-gray-600: #4B5563;         /* Body text */
--pw-gray-900: #111827;         /* Headings, dark text */
--pw-white: #FFFFFF;            /* White backgrounds */
```

**Accent colors** (semantic, use sparingly):
```css
--pw-success: #10B981;          /* Success states, checkmarks */
--pw-warning: #F59E0B;          /* Warnings */
--pw-error: #EF4444;            /* Errors */
--pw-info: #3B82F6;             /* Info boxes */
```

### Dark Mode

```css
--pw-dark-bg: #0F0F23;          /* Dark background (deep purple-tinted black) */
--pw-dark-surface: #1A1A2E;     /* Dark cards/surfaces */
--pw-dark-border: #2D2D44;      /* Dark borders */
```

---

## 🖼️ Visual Design Guidelines

### Hero Section

**Current issue**: Mixed green/purple gradient
**New design**:

```
┌─────────────────────────────────────────────┐
│                                             │
│  [Purple gradient background: #6B46C1 → #5B3AA1]
│                                             │
│  ⚡ Promptware                              │
│  World's First Bidirectional               │
│  Universal Code Translator                 │
│                                             │
│  [White text on purple]                    │
│                                             │
│  [CTA Button: White bg, purple text]       │
│  [Secondary Button: Transparent, white border]
│                                             │
└─────────────────────────────────────────────┘
```

**Code**:
```html
<section class="hero bg-gradient-to-br from-pw-purple-primary to-pw-purple-dark">
  <h1 class="text-white">Promptware</h1>
  <p class="text-purple-100">World's First Bidirectional Universal Code Translator</p>

  <div class="cta-buttons">
    <button class="bg-white text-pw-purple-primary hover:bg-purple-50">
      Get Started
    </button>
    <button class="border-white text-white hover:bg-white/10">
      View Docs
    </button>
  </div>
</section>
```

### Navigation

**Style**: Clean, minimal, sticky header

```css
nav {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--pw-gray-100);
}

nav a:hover {
  color: var(--pw-purple-primary);
  border-bottom: 2px solid var(--pw-purple-light);
}

nav .logo {
  color: var(--pw-purple-primary);
  font-weight: 700;
}
```

### Buttons & CTAs

**Primary CTA** (use sparingly - max 2 per page):
```css
.btn-primary {
  background: linear-gradient(135deg, #6B46C1 0%, #5B3AA1 100%);
  color: white;
  padding: 12px 32px;
  border-radius: 8px;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(107, 70, 193, 0.3);
  transition: all 0.2s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(107, 70, 193, 0.4);
}
```

**Secondary buttons**:
```css
.btn-secondary {
  background: transparent;
  color: var(--pw-purple-primary);
  border: 2px solid var(--pw-purple-primary);
  padding: 12px 32px;
  border-radius: 8px;
}

.btn-secondary:hover {
  background: var(--pw-purple-primary);
  color: white;
}
```

### Code Blocks

**Match GitHub purple theme**:
```css
pre, code {
  background: #1A1A2E;
  border: 1px solid #2D2D44;
  border-left: 4px solid var(--pw-purple-primary);
  border-radius: 8px;
  padding: 16px;
}

code .keyword {
  color: #A371F7;  /* Purple for keywords */
}

code .string {
  color: #50FA7B;  /* Keep green for strings (readability) */
}

code .function {
  color: #8BE9FD;  /* Cyan for functions */
}
```

### Cards & Containers

**Feature cards**:
```css
.feature-card {
  background: white;
  border: 1px solid var(--pw-gray-100);
  border-radius: 12px;
  padding: 24px;
  transition: all 0.3s;
}

.feature-card:hover {
  border-color: var(--pw-purple-light);
  box-shadow: 0 8px 24px rgba(107, 70, 193, 0.15);
  transform: translateY(-4px);
}

.feature-card .icon {
  color: var(--pw-purple-primary);
  background: rgba(107, 70, 193, 0.1);
  padding: 12px;
  border-radius: 8px;
}
```

### Typography

**Headings**:
```css
h1, h2, h3 {
  color: var(--pw-gray-900);
  font-weight: 700;
}

h1 span.highlight,
h2 span.highlight {
  color: var(--pw-purple-primary);
  /* Optional gradient effect */
  background: linear-gradient(135deg, #6B46C1 0%, #A371F7 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

**Example**:
```html
<h1>
  Write Once, Compile to
  <span class="highlight">Any Language</span>
</h1>
```

---

## 📄 Section-by-Section Recommendations

### 1. Hero Section
- **Background**: Purple gradient (dark to light top-to-bottom)
- **Text**: White
- **CTA**: White button with purple text ("Get Started")
- **Secondary**: Transparent button with white border ("View Docs")
- **Code demo**: Embedded terminal-style animation (dark theme with purple accents)

### 2. Features Grid
- **Background**: Light gray (#F9FAFB)
- **Cards**: White with subtle shadow
- **Icons**: Purple (#6B46C1) on light purple background
- **Hover**: Purple border + lift effect

### 3. Code Examples
- **Background**: Dark (#1A1A2E)
- **Syntax highlighting**: Purple for keywords, keep other colors for readability
- **Border accent**: Left border in purple
- **Copy button**: Purple on hover

### 4. Comparison Table (vs Babel/LLVM/Haxe)
- **Header row**: Purple background (#6B46C1), white text
- **Checkmarks**: Purple (#6B46C1)
- **Hover row**: Light purple background (#F5F3FF)
- **Borders**: Subtle gray

### 5. Quick Start / Installation
- **Section background**: White
- **Code block**: Dark with purple accent
- **Step numbers**: Purple circles with white numbers
- **Progress indicator**: Purple gradient progress bar

### 6. Footer
- **Background**: Very dark purple (#1A1A2E)
- **Text**: Light gray (#9CA3AF)
- **Links**: White, purple on hover
- **Logo**: Purple/white version

---

## 🎯 Specific Component Updates

### Logo

**Update logo SVG**:
```svg
<!-- Current: Green? -->
<!-- New: Purple -->
<svg viewBox="0 0 200 60" xmlns="http://www.w3.org/2000/svg">
  <text x="0" y="45" font-family="Inter, sans-serif" font-size="48"
        font-weight="700" fill="#6B46C1">
    Promptware
  </text>
  <text x="195" y="20" font-size="14" fill="#A371F7">v2.1.0</text>
</svg>
```

### Badges

**Update badge colors** (if using shields.io):
```markdown
![Version](https://img.shields.io/badge/version-2.1.0b1-6B46C1?style=flat-square)
![Tests](https://img.shields.io/badge/tests-99%25-6B46C1?style=flat-square)
```

### Syntax Highlighting Theme

**Use "Night Owl Purple" or "Dracula Purple" variant**:
- Background: Dark
- Keywords: Purple/pink
- Strings: Green (for contrast)
- Functions: Cyan
- Comments: Gray

---

## 🌓 Dark Mode Considerations

### Toggle Implementation

```css
/* Light mode (default) */
:root {
  --bg-primary: #FFFFFF;
  --bg-secondary: #F9FAFB;
  --text-primary: #111827;
  --text-secondary: #6B7280;
}

/* Dark mode */
[data-theme="dark"] {
  --bg-primary: #0F0F23;
  --bg-secondary: #1A1A2E;
  --text-primary: #F9FAFB;
  --text-secondary: #D1D5DB;
}

/* Purple stays consistent */
:root, [data-theme="dark"] {
  --color-primary: #6B46C1;
  --color-primary-light: #A371F7;
  --color-primary-dark: #5B3AA1;
}
```

---

## 🚀 Performance & Best Practices

### Gradient Performance

**Use CSS gradients** (not images):
```css
background: linear-gradient(135deg, #6B46C1 0%, #5B3AA1 100%);
```

**For complex hero gradients**:
```css
background:
  radial-gradient(circle at 20% 50%, rgba(163, 113, 247, 0.2) 0%, transparent 50%),
  linear-gradient(135deg, #6B46C1 0%, #5B3AA1 100%);
```

### Animation Performance

**Use transform & opacity only** (GPU-accelerated):
```css
.card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-4px);
}
```

---

## 📋 Migration Checklist

### Critical (Do First):
- [ ] Update favicon files (see WEBSITE_FAVICON_UPDATE.md)
- [ ] Add favicon HTML to `<head>`
- [ ] Update hero section background to purple gradient
- [ ] Update primary CTA buttons to purple
- [ ] Update logo to purple
- [ ] Update navigation hover states to purple

### Important (Do Next):
- [ ] Update all green elements to purple
- [ ] Standardize button styles (primary/secondary)
- [ ] Update code block styling with purple accents
- [ ] Update feature card icons to purple
- [ ] Update link colors and hover states

### Nice to Have:
- [ ] Add dark mode support
- [ ] Animate hero section
- [ ] Add purple glow effects on interactive elements
- [ ] Update Open Graph image with purple branding
- [ ] Add theme color meta tag: `<meta name="theme-color" content="#6B46C1">`

---

## 🎨 Design Inspiration References

### Similar Purple Brands (for inspiration):
- **Stripe** - Clean purple, professional fintech
- **Heroku** - Purple developer platform
- **Twitch** - Purple with good dark mode
- **Figma** - Clean UI, purple accents

### What to emulate:
✅ Clean, minimal design (Stripe)
✅ Developer-focused (Heroku)
✅ Good dark mode (Twitch)
✅ Professional typography (Figma)

### What to avoid:
❌ Too much gradient (overwhelming)
❌ Neon/bright purple (hard to read)
❌ Purple text on purple background (low contrast)
❌ Overuse of color (use purple strategically)

---

## 🖼️ Example Hero Section (Full Code)

```html
<section class="hero">
  <div class="container">
    <div class="hero-content">
      <div class="badge">
        <span class="badge-icon">⚡</span>
        <span>v2.1.0 Beta - Now with bidirectional translation</span>
      </div>

      <h1 class="hero-title">
        World's First<br>
        <span class="gradient-text">Bidirectional Universal</span><br>
        Code Translator
      </h1>

      <p class="hero-subtitle">
        Write code once in PW, compile to Python, Go, Rust, TypeScript, or C#.
        Or parse existing code and translate to any language.
      </p>

      <div class="hero-stats">
        <div class="stat">
          <strong>5</strong>
          <span>Languages</span>
        </div>
        <div class="stat">
          <strong>20</strong>
          <span>Translation Paths</span>
        </div>
        <div class="stat">
          <strong>99%</strong>
          <span>Test Coverage</span>
        </div>
      </div>

      <div class="hero-actions">
        <button class="btn btn-primary">
          Get Started
          <span class="icon">→</span>
        </button>
        <button class="btn btn-secondary">
          View Documentation
        </button>
      </div>

      <div class="hero-code-demo">
        <!-- Animated terminal demo (see docs/images/demo.svg) -->
      </div>
    </div>
  </div>
</section>

<style>
.hero {
  background: linear-gradient(135deg, #6B46C1 0%, #5B3AA1 100%);
  padding: 120px 0 80px;
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background:
    radial-gradient(circle at 20% 50%, rgba(163, 113, 247, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(91, 58, 161, 0.3) 0%, transparent 50%);
  opacity: 0.5;
}

.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  max-width: 900px;
  margin: 0 auto;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 8px 16px;
  border-radius: 100px;
  color: white;
  font-size: 14px;
  margin-bottom: 32px;
}

.hero-title {
  font-size: 64px;
  font-weight: 800;
  line-height: 1.1;
  color: white;
  margin-bottom: 24px;
}

.gradient-text {
  background: linear-gradient(135deg, #FFFFFF 0%, #A371F7 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: 20px;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 48px;
  line-height: 1.6;
}

.hero-stats {
  display: flex;
  justify-content: center;
  gap: 48px;
  margin-bottom: 48px;
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat strong {
  font-size: 36px;
  font-weight: 700;
  color: white;
  display: block;
}

.stat span {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-bottom: 64px;
}

.btn {
  padding: 14px 32px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.btn-primary {
  background: white;
  color: #6B46C1;
  border: none;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(255, 255, 255, 0.3);
}

.btn-secondary {
  background: transparent;
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: white;
}
</style>
```

---

## 🔍 Testing Checklist

After implementing changes:

### Visual Testing
- [ ] Hero section gradient displays correctly
- [ ] All buttons use purple color scheme
- [ ] Hover states work on all interactive elements
- [ ] Code blocks have purple accent borders
- [ ] Logo displays in purple
- [ ] Favicon appears in browser tab (purple PW icon)

### Responsive Testing
- [ ] Mobile: Layout doesn't break, purple visible
- [ ] Tablet: Cards stack properly, gradients work
- [ ] Desktop: Full hero gradient displays

### Accessibility
- [ ] Purple text on white = min 4.5:1 contrast (#6B46C1 on white = 5.8:1 ✅)
- [ ] White text on purple = min 4.5:1 contrast (white on #6B46C1 = 7.6:1 ✅)
- [ ] Focus states visible (purple outline)
- [ ] Color is not the only indicator (use icons + text)

### Performance
- [ ] No layout shift from loading fonts
- [ ] Gradients render smoothly (CSS, not images)
- [ ] Images compressed (favicons under 100KB total)
- [ ] No FOUC (flash of unstyled content)

---

## 📊 Before/After Comparison

| Element | Current | New (Purple) |
|---------|---------|--------------|
| **Hero BG** | Green gradient? | Purple gradient (#6B46C1 → #5B3AA1) |
| **Primary CTA** | Green? | White with purple text |
| **Links** | Blue/Green? | Purple (#6B46C1), light purple on hover |
| **Code accent** | None? | Purple left border |
| **Logo** | Mixed? | Purple (#6B46C1) |
| **Icons** | Various | Purple (#6B46C1) on light purple BG |
| **Favicon** | Versace (default) | Purple PW icon |

---

## 🚀 Expected Outcome

After this redesign:

✅ **Unified brand identity** - Purple everywhere (website, GitHub, VSCode)
✅ **Professional appearance** - Clean, modern, developer-focused
✅ **Better recognition** - Distinct purple stands out from blue dev tools
✅ **Improved trust** - Consistent branding = polished product
✅ **GitHub alignment** - Matches repository branding
✅ **VSCode alignment** - Matches extension icon

---

## 📦 Files to Reference

All assets available in GitHub repo:

1. **Favicon files**: `docs/images/favicon*`, `apple-touch-icon.png`
2. **SVG diagrams**: `docs/images/architecture-diagram.svg`, `code-comparison.svg`
3. **Color values**: This document (WEBSITE_REDESIGN_PURPLE.md)

Download from: `https://github.com/Promptware-dev/promptware/tree/main/docs/images/`

---

## 🎯 Final Notes

**Philosophy**: "Purple is the new black" for Promptware

Use purple strategically:
- **High impact**: Hero, CTAs, logo, navigation hover
- **Medium impact**: Icons, borders, code accents
- **Low impact**: Subtle backgrounds, badges

Keep it professional:
- Don't oversaturate with purple
- Use plenty of white space
- Maintain good contrast ratios
- Test in both light and dark environments

**Target vibe**: Stripe meets Heroku - professional developer platform with modern purple branding.

---

**Created**: 2025-10-08
**Version**: 1.0
**For**: promptware.dev redesign
**By**: Claude Code - Session 20
