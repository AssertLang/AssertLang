# 🎉 AssertLang v0.1.1 Released!

We're excited to announce **AssertLang v0.1.1**, a critical bug fix release that makes JavaScript and Python code generation production-ready!

## 🐛 What's Fixed

This release addresses **6 critical transpiler bugs** reported by real-world usage:

### JavaScript Fixes ✅
- **Module exports** - Generated code now includes `module.exports` for Node.js compatibility
- **this vs self** - Class methods correctly use `this.property` instead of `self.property`
- **Built-in functions** - Python builtins now map to JavaScript equivalents (str→String, int→Math.floor, etc.)
- **Constructor calls** - Factory functions properly use the `new` keyword

### Python Fixes ✅
- **Clean constructors** - Uses idiomatic positional arguments instead of `field_0=` syntax

## 📦 Installation

```bash
pip install --upgrade assertlang
```

Or install for the first time:

```bash
pip install assertlang
```

Verify installation:

```bash
asl --version  # Should show: AssertLang 0.1.1
```

## 🚀 Quick Example

Before v0.1.1, generated JavaScript was broken. Now it works!

**Your AssertLang code:**
```al
class VideoSpec {
    function __init__(width: int, height: int) {
        self.width = width;
        self.height = height;
    }

    function getResolution() -> string {
        return str(self.width) + "x" + str(self.height);
    }
}

function createVideoSpec(width: int, height: int) -> VideoSpec {
    return VideoSpec(width, height);
}
```

**Now generates working JavaScript:**
```javascript
class VideoSpec {
    constructor(width, height) {  // ✅ correct
        this.width = width;        // ✅ correct
        this.height = height;
    }

    getResolution() {
        return String(this.width) + "x" + String(this.height);  // ✅ correct
    }
}

function createVideoSpec(width, height) {
    return new VideoSpec(width, height);  // ✅ correct
}

module.exports = { VideoSpec, createVideoSpec };  // ✅ works!
```

## 🧪 Testing

- **33 test cases** added covering all fixes
- **100% pass rate** across all test suites
- **Zero regressions** - all existing tests still passing
- **Real-world validated** with production-like examples

## 📊 Impact

This release transforms AssertLang from "promising but buggy" to **production-ready** for JavaScript and Python transpilation.

## 🔗 Links

- **PyPI:** https://pypi.org/project/assertlang/0.1.1/
- **GitHub Release:** https://github.com/AssertLang/AssertLang/releases/tag/v0.1.1
- **Full Changelog:** https://github.com/AssertLang/AssertLang/blob/main/CHANGELOG.md
- **Documentation:** https://github.com/AssertLang/AssertLang

## 🙏 Thanks

Special thanks to the AI agent who tested AssertLang in production and provided a detailed bug report that made this systematic fix possible!

## 📢 Share the News

If you're using AssertLang, please upgrade and let us know how it goes!

```bash
pip install --upgrade assertlang
asl generate your_agent.al --lang nodejs  # Try it!
```

---

**AssertLang** - Executable contracts for multi-agent systems
*Making multi-language code generation reliable and production-ready*

🐛→✅ v0.1.1 is here!
