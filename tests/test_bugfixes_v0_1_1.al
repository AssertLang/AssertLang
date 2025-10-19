// Comprehensive test file for bug fixes in v0.1.1
// Tests all 6 critical bugs reported for JavaScript and Python transpilation

// ============================================================================
// TEST CASE 1: Class with Constructor (Tests Bugs #2, #3)
// ============================================================================
class VideoSpec {
    function __init__(width: int, height: int, framerate: int, codec: string, bitrate: int) {
        self.width = width;
        self.height = height;
        self.framerate = framerate;
        self.codec = codec;
        self.bitrate = bitrate;
    }

    function getResolution() -> string {
        return str(self.width) + "x" + str(self.height);
    }

    function getTotalPixels() -> int {
        return int(self.width * self.height);
    }

    function getDurationInMinutes(seconds: float) -> float {
        return float(seconds) / 60.0;
    }
}

// ============================================================================
// TEST CASE 2: Factory Function (Tests Bug #5, #6)
// ============================================================================
function createVideoSpec(width: int, height: int, framerate: int, codec: string, bitrate: int) -> VideoSpec {
    return VideoSpec(width, height, framerate, codec, bitrate);
}

// ============================================================================
// TEST CASE 3: Type Conversion Functions (Tests Bug #4)
// ============================================================================
function calculate(x: int, y: float) -> string {
    let result = float(x) * y;
    return str(int(result));
}

function testBuiltins(text: string, number: int) -> bool {
    let length = len(text);
    let converted = str(number);
    let floatVal = float(number);
    let intVal = int(floatVal);
    return bool(length > 0);
}

// ============================================================================
// TEST CASE 4: Multiple Functions and Classes (Tests Bug #1 - module.exports)
// ============================================================================
function foo() -> int {
    return 1;
}

function bar() -> int {
    return 2;
}

class MyClass {
    function __init__(value: int) {
        self.value = value;
    }

    function getValue() -> int {
        return self.value;
    }
}

// ============================================================================
// EXPECTED JAVASCRIPT OUTPUT:
// ============================================================================
// - Bug #1: File should end with module.exports = { VideoSpec, createVideoSpec, ... }
// - Bug #2: Class should use constructor(width, height, ...) not __init__
// - Bug #3: Methods should use this.width, not self.width
// - Bug #4: str() → String(), int() → Math.floor(), float() → Number()
// - Bug #5: createVideoSpec should return new VideoSpec(...)

// ============================================================================
// EXPECTED PYTHON OUTPUT:
// ============================================================================
// - Bug #6: createVideoSpec should use VideoSpec(width, height, ...)
//           NOT VideoSpec(field_0=width, field_1=height, ...)
