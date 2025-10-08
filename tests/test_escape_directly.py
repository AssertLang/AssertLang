#!/usr/bin/env python3

# Test the escaping logic directly
part = "\nHello World\n"
print(f"Original: {repr(part)}")

escaped = part
escaped = escaped.replace("\\", "\\\\")
print(f"After \\\\ escape: {repr(escaped)}")

escaped = escaped.replace('"', '\\"')
print(f"After quote escape: {repr(escaped)}")

escaped = escaped.replace("\n", "\\n")
print(f"After newline escape: {repr(escaped)}")

# What gets generated
format_str = escaped
result = f'"{format_str}"'
print(f"\nFinal: {result}")
print(f"Final repr: {repr(result)}")
