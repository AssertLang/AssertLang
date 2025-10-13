#!/usr/bin/env python3
"""
Promptware Operations MCP Server

Provides 107 universal programming operations as MCP tools.
Each operation can return implementations for Python, Rust, Go, JavaScript, C++.

Version: 1.0.0
Protocol: MCP (JSON-RPC 2.0 over stdio)
"""

import json
import sys
from typing import Dict, List, Any, Optional

# ============================================================================
# OPERATION DATABASE
# Complete collection of 107 universal programming operations
# ============================================================================

OPERATIONS = {
    # CATEGORY 1: FILE I/O (12 operations)
    "file.read": {
        "description": "Read entire file contents as string",
        "pw_syntax": "file.read(path) -> str",
        "parameters": {
            "path": {"type": "string", "description": "File path to read"}
        },
        "ir": {
            "type": "call",
            "function": {"type": "property_access", "object": "file", "property": "read"},
            "args": [{"type": "identifier", "name": "path"}]
        },
        "implementations": {
            "python": {
                "imports": ["from pathlib import Path"],
                "code": "Path({path}).read_text()",
                "alt": "open({path}, 'r').read()",
                "ast": {
                    "type": "Call",
                    "func": {"type": "Attribute", "value": {"type": "Name", "id": "Path"}, "attr": "read_text"},
                    "args": [],
                    "keywords": []
                }
            },
            "rust": {
                "imports": ["use std::fs;"],
                "code": "fs::read_to_string({path})?",
                "notes": "Returns Result<String, std::io::Error>",
                "ast": {
                    "type": "MethodCall",
                    "receiver": {"type": "Path", "segments": ["fs"]},
                    "method": "read_to_string",
                    "args": [{"type": "Ident", "name": "path"}]
                }
            },
            "go": {
                "imports": ["import \"os\""],
                "code": "os.ReadFile({path})",
                "notes": "Returns ([]byte, error)",
                "ast": {
                    "type": "CallExpr",
                    "fun": {"type": "SelectorExpr", "x": {"type": "Ident", "name": "os"}, "sel": "ReadFile"},
                    "args": [{"type": "Ident", "name": "path"}]
                }
            },
            "javascript": {
                "imports": ["const fs = require('fs');"],
                "code": "fs.readFileSync({path}, 'utf8')",
                "alt": "await fs.promises.readFile({path}, 'utf8')",
                "ast": {
                    "type": "CallExpression",
                    "callee": {"type": "MemberExpression", "object": {"type": "Identifier", "name": "fs"}, "property": {"type": "Identifier", "name": "readFileSync"}},
                    "arguments": [{"type": "Identifier", "name": "path"}, {"type": "Literal", "value": "utf8"}]
                }
            },
            "cpp": {
                "imports": ["#include <fstream>", "#include <string>"],
                "code": "std::ifstream f({path}); std::string((std::istreambuf_iterator<char>(f)), std::istreambuf_iterator<char>())",
                "ast": {
                    "type": "CompoundStmt",
                    "body": [
                        {"type": "DeclStmt", "var": "f", "init": {"type": "CXXConstructExpr", "type": "ifstream", "args": [{"type": "Ident", "name": "path"}]}},
                        {"type": "CXXConstructExpr", "type": "string", "args": [{"type": "CallExpr", "name": "istreambuf_iterator"}]}
                    ]
                }
            }
        }
    },
    "file.write": {
        "description": "Write string to file (overwrite)",
        "pw_syntax": "file.write(path, content) -> void",
        "parameters": {
            "path": {"type": "string", "description": "File path to write"},
            "content": {"type": "string", "description": "Content to write"}
        },
        "implementations": {
            "python": {
                "imports": ["from pathlib import Path"],
                "code": "Path({path}).write_text({content})",
                "alt": "open({path}, 'w').write({content})"
            },
            "rust": {
                "imports": ["use std::fs;"],
                "code": "fs::write({path}, {content})?",
                "notes": "Returns Result<(), std::io::Error>"
            },
            "go": {
                "imports": ["import \"os\""],
                "code": "os.WriteFile({path}, []byte({content}), 0644)"
            },
            "javascript": {
                "imports": ["const fs = require('fs');"],
                "code": "fs.writeFileSync({path}, {content})",
                "alt": "await fs.promises.writeFile({path}, {content})"
            },
            "cpp": {
                "imports": ["#include <fstream>"],
                "code": "std::ofstream f({path}); f << {content};"
            }
        }
    },
    "file.append": {
        "description": "Append string to file",
        "pw_syntax": "file.append(path, content) -> void",
        "parameters": {
            "path": {"type": "string", "description": "File path to append to"},
            "content": {"type": "string", "description": "Content to append"}
        },
        "implementations": {
            "python": {
                "imports": [],
                "code": "open({path}, 'a').write({content})"
            },
            "rust": {
                "imports": ["use std::fs::OpenOptions;", "use std::io::Write;"],
                "code": "OpenOptions::new().append(true).open({path})?.write_all({content}.as_bytes())?",
                "notes": "Returns Result<(), std::io::Error>"
            },
            "go": {
                "imports": ["import \"os\""],
                "code": "f, _ := os.OpenFile({path}, os.O_APPEND|os.O_WRONLY, 0644); f.WriteString({content})"
            },
            "javascript": {
                "imports": ["const fs = require('fs');"],
                "code": "fs.appendFileSync({path}, {content})"
            },
            "cpp": {
                "imports": ["#include <fstream>"],
                "code": "std::ofstream f({path}, std::ios::app); f << {content};"
            }
        }
    },
    "file.exists": {
        "description": "Check if file exists",
        "pw_syntax": "file.exists(path) -> bool",
        "parameters": {
            "path": {"type": "string", "description": "File path to check"}
        },
        "implementations": {
            "python": {
                "imports": ["from pathlib import Path"],
                "code": "Path({path}).exists()",
                "alt": "os.path.exists({path})"
            },
            "rust": {
                "imports": ["use std::path::Path;"],
                "code": "Path::new({path}).exists()"
            },
            "go": {
                "imports": ["import \"os\""],
                "code": "_, err := os.Stat({path}); err == nil"
            },
            "javascript": {
                "imports": ["const fs = require('fs');"],
                "code": "fs.existsSync({path})"
            },
            "cpp": {
                "imports": ["#include <fstream>"],
                "code": "std::ifstream f({path}); return f.good();",
                "alt": "#include <filesystem>\nstd::filesystem::exists({path})"
            }
        }
    },
    "file.delete": {
        "description": "Delete file",
        "pw_syntax": "file.delete(path) -> void",
        "parameters": {
            "path": {"type": "string", "description": "File path to delete"}
        },
        "implementations": {
            "python": {
                "imports": ["from pathlib import Path"],
                "code": "Path({path}).unlink()",
                "alt": "os.remove({path})"
            },
            "rust": {
                "imports": ["use std::fs;"],
                "code": "fs::remove_file({path})?",
                "notes": "Returns Result<(), std::io::Error>"
            },
            "go": {
                "imports": ["import \"os\""],
                "code": "os.Remove({path})"
            },
            "javascript": {
                "imports": ["const fs = require('fs');"],
                "code": "fs.unlinkSync({path})"
            },
            "cpp": {
                "imports": ["#include <cstdio>"],
                "code": "remove({path}.c_str())",
                "alt": "#include <filesystem>\nstd::filesystem::remove({path})"
            }
        }
    },
    "file.read_lines": {
        "description": "Read file as array of lines",
        "pw_syntax": "file.read_lines(path) -> List<str>",
        "parameters": {
            "path": {"type": "string", "description": "File path to read"}
        },
        "implementations": {
            "python": {
                "imports": ["from pathlib import Path"],
                "code": "Path({path}).read_text().splitlines()",
                "alt": "open({path}).readlines()"
            },
            "rust": {
                "imports": ["use std::fs::File;", "use std::io::{BufRead, BufReader};"],
                "code": "BufReader::new(File::open({path})?).lines().collect::<Result<Vec<_>, _>>()?",
                "notes": "Returns Result<Vec<String>, std::io::Error>"
            },
            "go": {
                "imports": ["import \"os\"", "import \"strings\""],
                "code": "data, _ := os.ReadFile({path}); strings.Split(string(data), \"\\n\")"
            },
            "javascript": {
                "imports": ["const fs = require('fs');"],
                "code": "fs.readFileSync({path}, 'utf8').split('\\n')"
            },
            "cpp": {
                "imports": ["#include <fstream>", "#include <string>", "#include <vector>"],
                "code": "std::ifstream f({path}); std::string line; std::vector<std::string> lines; while(std::getline(f, line)) lines.push_back(line);"
            }
        }
    },
    "file.write_lines": {
        "description": "Write array of strings as lines",
        "pw_syntax": "file.write_lines(path, lines) -> void",
        "parameters": {
            "path": {"type": "string", "description": "File path to write"},
            "lines": {"type": "array", "description": "Array of lines to write"}
        },
        "implementations": {
            "python": {
                "imports": [],
                "code": "open({path}, 'w').writelines(line + '\\n' for line in {lines})"
            },
            "rust": {
                "imports": ["use std::fs;"],
                "code": "fs::write({path}, {lines}.join(\"\\n\"))?",
                "notes": "Returns Result<(), std::io::Error>"
            },
            "go": {
                "imports": ["import \"os\"", "import \"strings\""],
                "code": "os.WriteFile({path}, []byte(strings.Join({lines}, \"\\n\")), 0644)"
            },
            "javascript": {
                "imports": ["const fs = require('fs');"],
                "code": "fs.writeFileSync({path}, {lines}.join('\\n'))"
            },
            "cpp": {
                "imports": ["#include <fstream>"],
                "code": "std::ofstream f({path}); for(auto& line : {lines}) f << line << '\\n';"
            }
        }
    },
    "file.list_dir": {
        "description": "List files/directories in path",
        "pw_syntax": "file.list_dir(path) -> List<str>",
        "parameters": {
            "path": {"type": "string", "description": "Directory path to list"}
        },
        "implementations": {
            "python": {
                "imports": ["import os"],
                "code": "os.listdir({path})",
                "alt": "[f.name for f in Path({path}).iterdir()]"
            },
            "rust": {
                "imports": ["use std::fs;"],
                "code": "fs::read_dir({path})?.map(|e| e.unwrap().file_name().to_string_lossy().to_string()).collect::<Vec<_>>()",
                "notes": "Returns Result<Vec<String>, std::io::Error>"
            },
            "go": {
                "imports": ["import \"os\""],
                "code": "entries, _ := os.ReadDir({path}); names := make([]string, len(entries)); for i, e := range entries { names[i] = e.Name() }"
            },
            "javascript": {
                "imports": ["const fs = require('fs');"],
                "code": "fs.readdirSync({path})"
            },
            "cpp": {
                "imports": ["#include <filesystem>", "#include <vector>"],
                "code": "std::vector<std::string> files; for(auto& p: std::filesystem::directory_iterator({path})) files.push_back(p.path().filename());"
            }
        }
    },
    "file.mkdir": {
        "description": "Create directory (and parents if needed)",
        "pw_syntax": "file.mkdir(path) -> void",
        "parameters": {
            "path": {"type": "string", "description": "Directory path to create"}
        },
        "implementations": {
            "python": {
                "imports": ["from pathlib import Path"],
                "code": "Path({path}).mkdir(parents=True, exist_ok=True)",
                "alt": "os.makedirs({path}, exist_ok=True)"
            },
            "rust": {
                "imports": ["use std::fs;"],
                "code": "fs::create_dir_all({path})?",
                "notes": "Returns Result<(), std::io::Error>"
            },
            "go": {
                "imports": ["import \"os\""],
                "code": "os.MkdirAll({path}, 0755)"
            },
            "javascript": {
                "imports": ["const fs = require('fs');"],
                "code": "fs.mkdirSync({path}, {recursive: true})"
            },
            "cpp": {
                "imports": ["#include <filesystem>"],
                "code": "std::filesystem::create_directories({path})"
            }
        }
    },
    "file.rmdir": {
        "description": "Delete directory recursively",
        "pw_syntax": "file.rmdir(path) -> void",
        "parameters": {
            "path": {"type": "string", "description": "Directory path to delete"}
        },
        "implementations": {
            "python": {
                "imports": ["import shutil"],
                "code": "shutil.rmtree({path})"
            },
            "rust": {
                "imports": ["use std::fs;"],
                "code": "fs::remove_dir_all({path})?",
                "notes": "Returns Result<(), std::io::Error>"
            },
            "go": {
                "imports": ["import \"os\""],
                "code": "os.RemoveAll({path})"
            },
            "javascript": {
                "imports": ["const fs = require('fs');"],
                "code": "fs.rmSync({path}, {recursive: true, force: true})"
            },
            "cpp": {
                "imports": ["#include <filesystem>"],
                "code": "std::filesystem::remove_all({path})"
            }
        }
    },
    "file.size": {
        "description": "Get file size in bytes",
        "pw_syntax": "file.size(path) -> int",
        "parameters": {
            "path": {"type": "string", "description": "File path to check size"}
        },
        "implementations": {
            "python": {
                "imports": ["from pathlib import Path"],
                "code": "Path({path}).stat().st_size",
                "alt": "os.path.getsize({path})"
            },
            "rust": {
                "imports": ["use std::fs;"],
                "code": "fs::metadata({path})?.len()",
                "notes": "Returns Result<u64, std::io::Error>"
            },
            "go": {
                "imports": ["import \"os\""],
                "code": "info, _ := os.Stat({path}); info.Size()"
            },
            "javascript": {
                "imports": ["const fs = require('fs');"],
                "code": "fs.statSync({path}).size"
            },
            "cpp": {
                "imports": ["#include <filesystem>"],
                "code": "std::filesystem::file_size({path})"
            }
        }
    },
    "file.copy": {
        "description": "Copy file from src to dest",
        "pw_syntax": "file.copy(src, dest) -> void",
        "parameters": {
            "src": {"type": "string", "description": "Source file path"},
            "dest": {"type": "string", "description": "Destination file path"}
        },
        "implementations": {
            "python": {
                "imports": ["import shutil"],
                "code": "shutil.copy2({src}, {dest})"
            },
            "rust": {
                "imports": ["use std::fs;"],
                "code": "fs::copy({src}, {dest})?",
                "notes": "Returns Result<u64, std::io::Error>"
            },
            "go": {
                "imports": ["import \"os\""],
                "code": "input, _ := os.ReadFile({src}); os.WriteFile({dest}, input, 0644)"
            },
            "javascript": {
                "imports": ["const fs = require('fs');"],
                "code": "fs.copyFileSync({src}, {dest})"
            },
            "cpp": {
                "imports": ["#include <filesystem>"],
                "code": "std::filesystem::copy_file({src}, {dest})"
            }
        }
    },

    # CATEGORY 2: STRING OPERATIONS (15 operations)
    "str.len": {
        "description": "Get string length",
        "pw_syntax": "str.len(s) -> int",
        "parameters": {
            "s": {"type": "string", "description": "String to measure"}
        },
        "implementations": {
            "python": {"imports": [], "code": "len({s})"},
            "rust": {"imports": [], "code": "{s}.len()"},
            "go": {"imports": [], "code": "len({s})"},
            "javascript": {"imports": [], "code": "{s}.length"},
            "cpp": {"imports": [], "code": "{s}.length()"}
        }
    },
    "str.substring": {
        "description": "Extract substring from start to end index",
        "pw_syntax": "s[start:end]",
        "parameters": {
            "s": {"type": "string", "description": "String to slice"},
            "start": {"type": "integer", "description": "Start index"},
            "end": {"type": "integer", "description": "End index"}
        },
        "implementations": {
            "python": {"imports": [], "code": "{s}[{start}:{end}]"},
            "rust": {"imports": [], "code": "&{s}[{start}..{end}]"},
            "go": {"imports": [], "code": "{s}[{start}:{end}]"},
            "javascript": {"imports": [], "code": "{s}.substring({start}, {end})", "alt": "{s}.slice({start}, {end})"},
            "cpp": {"imports": [], "code": "{s}.substr({start}, {end}-{start})"}
        }
    },
    "str.contains": {
        "description": "Check if string contains substring",
        "pw_syntax": "substring in s",
        "parameters": {
            "s": {"type": "string", "description": "String to search in"},
            "substring": {"type": "string", "description": "Substring to find"}
        },
        "implementations": {
            "python": {"imports": [], "code": "{substring} in {s}"},
            "rust": {"imports": [], "code": "{s}.contains({substring})"},
            "go": {"imports": ["import \"strings\""], "code": "strings.Contains({s}, {substring})"},
            "javascript": {"imports": [], "code": "{s}.includes({substring})"},
            "cpp": {"imports": [], "code": "{s}.find({substring}) != std::string::npos"}
        }
    },
    "str.starts_with": {
        "description": "Check if string starts with prefix",
        "pw_syntax": "str.starts_with(s, prefix) -> bool",
        "parameters": {
            "s": {"type": "string", "description": "String to check"},
            "prefix": {"type": "string", "description": "Prefix to match"}
        },
        "implementations": {
            "python": {"imports": [], "code": "{s}.startswith({prefix})"},
            "rust": {"imports": [], "code": "{s}.starts_with({prefix})"},
            "go": {"imports": ["import \"strings\""], "code": "strings.HasPrefix({s}, {prefix})"},
            "javascript": {"imports": [], "code": "{s}.startsWith({prefix})"},
            "cpp": {"imports": [], "code": "{s}.rfind({prefix}, 0) == 0"}
        }
    },
    "str.ends_with": {
        "description": "Check if string ends with suffix",
        "pw_syntax": "str.ends_with(s, suffix) -> bool",
        "parameters": {
            "s": {"type": "string", "description": "String to check"},
            "suffix": {"type": "string", "description": "Suffix to match"}
        },
        "implementations": {
            "python": {"imports": [], "code": "{s}.endswith({suffix})"},
            "rust": {"imports": [], "code": "{s}.ends_with({suffix})"},
            "go": {"imports": ["import \"strings\""], "code": "strings.HasSuffix({s}, {suffix})"},
            "javascript": {"imports": [], "code": "{s}.endsWith({suffix})"},
            "cpp": {"imports": [], "code": "{s}.size() >= {suffix}.size() && {s}.compare({s}.size()-{suffix}.size(), {suffix}.size(), {suffix}) == 0"}
        }
    },
    "str.split": {
        "description": "Split string by delimiter",
        "pw_syntax": "str.split(s, delimiter) -> List<str>",
        "parameters": {
            "s": {"type": "string", "description": "String to split"},
            "delimiter": {"type": "string", "description": "Delimiter to split on"}
        },
        "implementations": {
            "python": {
                "imports": [],
                "code": "{s}.split({delimiter})",
                "ast": {
                    "type": "Call",
                    "func": {"type": "Attribute", "value": {"type": "Name", "id": "s"}, "attr": "split"},
                    "args": [{"type": "Name", "id": "delimiter"}]
                }
            },
            "rust": {
                "imports": [],
                "code": "{s}.split({delimiter}).collect::<Vec<_>>()",
                "ast": {
                    "type": "MethodCall",
                    "receiver": {"type": "MethodCall", "receiver": {"type": "Ident", "name": "s"}, "method": "split", "args": [{"type": "Ident", "name": "delimiter"}]},
                    "method": "collect",
                    "turbofish": ["Vec<_>"]
                }
            },
            "go": {
                "imports": ["import \"strings\""],
                "code": "strings.Split({s}, {delimiter})",
                "ast": {
                    "type": "CallExpr",
                    "fun": {"type": "SelectorExpr", "x": {"type": "Ident", "name": "strings"}, "sel": "Split"},
                    "args": [{"type": "Ident", "name": "s"}, {"type": "Ident", "name": "delimiter"}]
                }
            },
            "javascript": {
                "imports": [],
                "code": "{s}.split({delimiter})",
                "ast": {
                    "type": "CallExpression",
                    "callee": {"type": "MemberExpression", "object": {"type": "Identifier", "name": "s"}, "property": {"type": "Identifier", "name": "split"}},
                    "arguments": [{"type": "Identifier", "name": "delimiter"}]
                }
            },
            "cpp": {"imports": [], "code": "/* No built-in split in C++ - requires custom implementation */"}
        }
    },
    "str.join": {
        "description": "Join array of strings with separator",
        "pw_syntax": "str.join(strings, separator) -> str",
        "parameters": {
            "strings": {"type": "array", "description": "Array of strings to join"},
            "separator": {"type": "string", "description": "Separator string"}
        },
        "implementations": {
            "python": {"imports": [], "code": "{separator}.join({strings})"},
            "rust": {"imports": [], "code": "{strings}.join({separator})"},
            "go": {"imports": ["import \"strings\""], "code": "strings.Join({strings}, {separator})"},
            "javascript": {"imports": [], "code": "{strings}.join({separator})"},
            "cpp": {"imports": [], "code": "/* No built-in join in C++ - requires custom implementation */"}
        }
    },
    "str.trim": {
        "description": "Remove whitespace from both ends",
        "pw_syntax": "str.trim(s) -> str",
        "parameters": {
            "s": {"type": "string", "description": "String to trim"}
        },
        "implementations": {
            "python": {"imports": [], "code": "{s}.strip()"},
            "rust": {"imports": [], "code": "{s}.trim()"},
            "go": {"imports": ["import \"strings\""], "code": "strings.TrimSpace({s})"},
            "javascript": {"imports": [], "code": "{s}.trim()"},
            "cpp": {"imports": [], "code": "/* No built-in trim in C++ - requires custom implementation */"}
        }
    },
    "str.upper": {
        "description": "Convert string to uppercase",
        "pw_syntax": "str.upper(s) -> str",
        "parameters": {
            "s": {"type": "string", "description": "String to convert"}
        },
        "implementations": {
            "python": {"imports": [], "code": "{s}.upper()"},
            "rust": {"imports": [], "code": "{s}.to_uppercase()"},
            "go": {"imports": ["import \"strings\""], "code": "strings.ToUpper({s})"},
            "javascript": {"imports": [], "code": "{s}.toUpperCase()"},
            "cpp": {"imports": ["#include <algorithm>"], "code": "std::transform({s}.begin(), {s}.end(), {s}.begin(), ::toupper)"}
        }
    },
    "str.lower": {
        "description": "Convert string to lowercase",
        "pw_syntax": "str.lower(s) -> str",
        "parameters": {
            "s": {"type": "string", "description": "String to convert"}
        },
        "implementations": {
            "python": {"imports": [], "code": "{s}.lower()"},
            "rust": {"imports": [], "code": "{s}.to_lowercase()"},
            "go": {"imports": ["import \"strings\""], "code": "strings.ToLower({s})"},
            "javascript": {"imports": [], "code": "{s}.toLowerCase()"},
            "cpp": {"imports": ["#include <algorithm>"], "code": "std::transform({s}.begin(), {s}.end(), {s}.begin(), ::tolower)"}
        }
    },
    "str.replace": {
        "description": "Replace all occurrences of old with new",
        "pw_syntax": "str.replace(s, old, new) -> str",
        "parameters": {
            "s": {"type": "string", "description": "String to modify"},
            "old": {"type": "string", "description": "Substring to replace"},
            "new": {"type": "string", "description": "Replacement substring"}
        },
        "implementations": {
            "python": {"imports": [], "code": "{s}.replace({old}, {new})"},
            "rust": {"imports": [], "code": "{s}.replace({old}, {new})"},
            "go": {"imports": ["import \"strings\""], "code": "strings.ReplaceAll({s}, {old}, {new})"},
            "javascript": {"imports": [], "code": "{s}.replaceAll({old}, {new})"},
            "cpp": {"imports": [], "code": "/* No built-in replace in C++ - requires loop */"}
        }
    },
    "str.index_of": {
        "description": "Find first index of substring (-1 if not found)",
        "pw_syntax": "str.index_of(s, substring) -> int",
        "parameters": {
            "s": {"type": "string", "description": "String to search in"},
            "substring": {"type": "string", "description": "Substring to find"}
        },
        "implementations": {
            "python": {"imports": [], "code": "{s}.find({substring})"},
            "rust": {"imports": [], "code": "{s}.find({substring}).map(|i| i as i32).unwrap_or(-1)"},
            "go": {"imports": ["import \"strings\""], "code": "strings.Index({s}, {substring})"},
            "javascript": {"imports": [], "code": "{s}.indexOf({substring})"},
            "cpp": {"imports": [], "code": "{s}.find({substring})"}
        }
    },
    "str.reverse": {
        "description": "Reverse string",
        "pw_syntax": "str.reverse(s) -> str",
        "parameters": {
            "s": {"type": "string", "description": "String to reverse"}
        },
        "implementations": {
            "python": {"imports": [], "code": "{s}[::-1]"},
            "rust": {"imports": [], "code": "{s}.chars().rev().collect::<String>()"},
            "go": {"imports": [], "code": "runes := []rune({s}); for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 { runes[i], runes[j] = runes[j], runes[i] }"},
            "javascript": {"imports": [], "code": "{s}.split('').reverse().join('')"},
            "cpp": {"imports": ["#include <algorithm>"], "code": "std::reverse({s}.begin(), {s}.end())"}
        }
    },
    "str.is_empty": {
        "description": "Check if string is empty",
        "pw_syntax": "str.is_empty(s) -> bool",
        "parameters": {
            "s": {"type": "string", "description": "String to check"}
        },
        "implementations": {
            "python": {"imports": [], "code": "len({s}) == 0", "alt": "not {s}"},
            "rust": {"imports": [], "code": "{s}.is_empty()"},
            "go": {"imports": [], "code": "len({s}) == 0"},
            "javascript": {"imports": [], "code": "{s}.length === 0", "alt": "!{s}"},
            "cpp": {"imports": [], "code": "{s}.empty()"}
        }
    },

    # CATEGORY 3: HTTP/NETWORK (8 operations)
    "http.get": {
        "description": "Make HTTP GET request, return body as string",
        "pw_syntax": "http.get(url) -> str",
        "parameters": {
            "url": {"type": "string", "description": "URL to request"}
        },
        "ir": {
            "type": "call",
            "function": {"type": "property_access", "object": "http", "property": "get"},
            "args": [{"type": "identifier", "name": "url"}]
        },
        "implementations": {
            "python": {
                "imports": ["import requests"],
                "code": "requests.get({url}).text",
                "alt": "urllib.request.urlopen({url}).read().decode()",
                "ast": {
                    "type": "Attribute",
                    "value": {"type": "Call", "func": {"type": "Attribute", "value": {"type": "Name", "id": "requests"}, "attr": "get"}, "args": [{"type": "Name", "id": "url"}]},
                    "attr": "text"
                }
            },
            "rust": {
                "imports": ["use reqwest;"],
                "code": "reqwest::blocking::get({url})?.text()?",
                "alt": "reqwest::get({url}).await?.text().await?",
                "ast": {
                    "type": "Try",
                    "expr": {"type": "MethodCall", "receiver": {"type": "Try", "expr": {"type": "Call", "path": "reqwest::blocking::get", "args": [{"type": "Ident", "name": "url"}]}}, "method": "text", "args": []}
                }
            },
            "go": {
                "imports": ["import \"net/http\"", "import \"io\""],
                "code": "resp, _ := http.Get({url}); body, _ := io.ReadAll(resp.Body); string(body)",
                "ast": {
                    "type": "BlockStmt",
                    "list": [
                        {"type": "AssignStmt", "lhs": ["resp", "_"], "tok": ":=", "rhs": [{"type": "CallExpr", "fun": {"type": "SelectorExpr", "x": "http", "sel": "Get"}, "args": ["url"]}]},
                        {"type": "AssignStmt", "lhs": ["body", "_"], "tok": ":=", "rhs": [{"type": "CallExpr", "fun": {"type": "SelectorExpr", "x": "io", "sel": "ReadAll"}, "args": [{"type": "SelectorExpr", "x": "resp", "sel": "Body"}]}]},
                        {"type": "CallExpr", "fun": "string", "args": ["body"]}
                    ]
                }
            },
            "javascript": {
                "imports": [],
                "code": "(await fetch({url})).text()",
                "alt": "require('https').get({url}, res => {...})",
                "ast": {
                    "type": "CallExpression",
                    "callee": {"type": "MemberExpression", "object": {"type": "AwaitExpression", "argument": {"type": "CallExpression", "callee": {"type": "Identifier", "name": "fetch"}, "arguments": [{"type": "Identifier", "name": "url"}]}}, "property": {"type": "Identifier", "name": "text"}},
                    "arguments": []
                }
            },
            "cpp": {"imports": [], "code": "/* Requires external library like libcurl */"}
        }
    },
    "http.post": {
        "description": "Make HTTP POST request with body",
        "pw_syntax": "http.post(url, body) -> str",
        "parameters": {
            "url": {"type": "string", "description": "URL to request"},
            "body": {"type": "string", "description": "Request body"}
        },
        "implementations": {
            "python": {"imports": ["import requests"], "code": "requests.post({url}, data={body}).text"},
            "rust": {"imports": ["use reqwest;"], "code": "reqwest::blocking::Client::new().post({url}).body({body}).send()?.text()?"},
            "go": {"imports": ["import \"net/http\"", "import \"strings\"", "import \"io\""], "code": "resp, _ := http.Post({url}, \"text/plain\", strings.NewReader({body})); data, _ := io.ReadAll(resp.Body); string(data)"},
            "javascript": {"imports": [], "code": "(await fetch({url}, {method: 'POST', body: {body}})).text()"},
            "cpp": {"imports": [], "code": "/* Requires libcurl */"}
        }
    },
    "http.get_json": {
        "description": "Make HTTP GET, parse JSON response",
        "pw_syntax": "http.get_json(url) -> Map<str, any>",
        "parameters": {
            "url": {"type": "string", "description": "URL to request"}
        },
        "implementations": {
            "python": {"imports": ["import requests"], "code": "requests.get({url}).json()"},
            "rust": {"imports": ["use reqwest;"], "code": "reqwest::blocking::get({url})?.json::<serde_json::Value>()?"},
            "go": {"imports": ["import \"net/http\"", "import \"encoding/json\"", "import \"io\""], "code": "resp, _ := http.Get({url}); var data interface{}; json.NewDecoder(resp.Body).Decode(&data)"},
            "javascript": {"imports": [], "code": "(await fetch({url})).json()"},
            "cpp": {"imports": [], "code": "/* Requires JSON library + HTTP library */"}
        }
    },
    "http.post_json": {
        "description": "POST JSON data, return JSON response",
        "pw_syntax": "http.post_json(url, data) -> Map<str, any>",
        "parameters": {
            "url": {"type": "string", "description": "URL to request"},
            "data": {"type": "object", "description": "JSON data to send"}
        },
        "implementations": {
            "python": {"imports": ["import requests"], "code": "requests.post({url}, json={data}).json()"},
            "rust": {"imports": ["use reqwest;"], "code": "reqwest::blocking::Client::new().post({url}).json(&{data}).send()?.json::<serde_json::Value>()?"},
            "go": {"imports": ["import \"net/http\"", "import \"encoding/json\"", "import \"bytes\""], "code": "jsonData, _ := json.Marshal({data}); resp, _ := http.Post({url}, \"application/json\", bytes.NewBuffer(jsonData))"},
            "javascript": {"imports": [], "code": "(await fetch({url}, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({data})})).json()"},
            "cpp": {"imports": [], "code": "/* Requires JSON + HTTP libraries */"}
        }
    },
    "http.download": {
        "description": "Download file from URL to local path",
        "pw_syntax": "http.download(url, path) -> void",
        "parameters": {
            "url": {"type": "string", "description": "URL to download from"},
            "path": {"type": "string", "description": "Local path to save to"}
        },
        "implementations": {
            "python": {"imports": ["import urllib.request"], "code": "urllib.request.urlretrieve({url}, {path})", "alt": "open({path}, 'wb').write(requests.get({url}).content)"},
            "rust": {"imports": ["use std::fs;", "use reqwest;"], "code": "fs::write({path}, reqwest::blocking::get({url})?.bytes()?)?"},
            "go": {"imports": ["import \"net/http\"", "import \"os\"", "import \"io\""], "code": "resp, _ := http.Get({url}); out, _ := os.Create({path}); io.Copy(out, resp.Body)"},
            "javascript": {"imports": ["const fs = require('fs');"], "code": "fs.writeFileSync({path}, await (await fetch({url})).arrayBuffer())"},
            "cpp": {"imports": [], "code": "/* Requires libcurl + file I/O */"}
        }
    },
    "url.encode": {
        "description": "URL-encode string (percent encoding)",
        "pw_syntax": "url.encode(s) -> str",
        "parameters": {
            "s": {"type": "string", "description": "String to encode"}
        },
        "implementations": {
            "python": {"imports": ["import urllib.parse"], "code": "urllib.parse.quote({s})"},
            "rust": {"imports": ["use urlencoding;"], "code": "urlencoding::encode({s})"},
            "go": {"imports": ["import \"net/url\""], "code": "url.QueryEscape({s})"},
            "javascript": {"imports": [], "code": "encodeURIComponent({s})"},
            "cpp": {"imports": [], "code": "/* Manual implementation required */"}
        }
    },
    "url.decode": {
        "description": "Decode URL-encoded string",
        "pw_syntax": "url.decode(s) -> str",
        "parameters": {
            "s": {"type": "string", "description": "String to decode"}
        },
        "implementations": {
            "python": {"imports": ["import urllib.parse"], "code": "urllib.parse.unquote({s})"},
            "rust": {"imports": ["use urlencoding;"], "code": "urlencoding::decode({s})?"},
            "go": {"imports": ["import \"net/url\""], "code": "url.QueryUnescape({s})"},
            "javascript": {"imports": [], "code": "decodeURIComponent({s})"},
            "cpp": {"imports": [], "code": "/* Manual implementation */"}
        }
    },
    "url.parse": {
        "description": "Parse URL into components (scheme, host, path, query)",
        "pw_syntax": "url.parse(url) -> Map<str, str>",
        "parameters": {
            "url": {"type": "string", "description": "URL to parse"}
        },
        "implementations": {
            "python": {"imports": ["import urllib.parse"], "code": "urllib.parse.urlparse({url})"},
            "rust": {"imports": ["use url::Url;"], "code": "Url::parse({url})?"},
            "go": {"imports": ["import \"net/url\""], "code": "url.Parse({url})"},
            "javascript": {"imports": [], "code": "new URL({url})"},
            "cpp": {"imports": [], "code": "/* Requires external library */"}
        }
    },

    # CATEGORY 4: JSON OPERATIONS (4 operations)
    "json.parse": {
        "description": "Parse JSON string to data structure",
        "pw_syntax": "json.parse(s) -> any",
        "parameters": {
            "s": {"type": "string", "description": "JSON string to parse"}
        },
        "implementations": {
            "python": {"imports": ["import json"], "code": "json.loads({s})"},
            "rust": {"imports": ["use serde_json;"], "code": "serde_json::from_str::<serde_json::Value>({s})?"},
            "go": {"imports": ["import \"encoding/json\""], "code": "var data interface{}; json.Unmarshal([]byte({s}), &data)"},
            "javascript": {"imports": [], "code": "JSON.parse({s})"},
            "cpp": {"imports": ["#include <nlohmann/json.hpp>"], "code": "json::parse({s})"}
        }
    },
    "json.stringify": {
        "description": "Convert data structure to JSON string",
        "pw_syntax": "json.stringify(data) -> str",
        "parameters": {
            "data": {"type": "object", "description": "Data to stringify"}
        },
        "implementations": {
            "python": {"imports": ["import json"], "code": "json.dumps({data})"},
            "rust": {"imports": ["use serde_json;"], "code": "serde_json::to_string(&{data})?"},
            "go": {"imports": ["import \"encoding/json\""], "code": "jsonData, _ := json.Marshal({data}); string(jsonData)"},
            "javascript": {"imports": [], "code": "JSON.stringify({data})"},
            "cpp": {"imports": [], "code": "{data}.dump()"}
        }
    },
    "json.stringify_pretty": {
        "description": "Convert to pretty-printed JSON",
        "pw_syntax": "json.stringify_pretty(data) -> str",
        "parameters": {
            "data": {"type": "object", "description": "Data to stringify"}
        },
        "implementations": {
            "python": {"imports": ["import json"], "code": "json.dumps({data}, indent=2)"},
            "rust": {"imports": ["use serde_json;"], "code": "serde_json::to_string_pretty(&{data})?"},
            "go": {"imports": ["import \"encoding/json\""], "code": "jsonData, _ := json.MarshalIndent({data}, \"\", \"  \"); string(jsonData)"},
            "javascript": {"imports": [], "code": "JSON.stringify({data}, null, 2)"},
            "cpp": {"imports": [], "code": "{data}.dump(2)"}
        }
    },
    "json.validate": {
        "description": "Check if string is valid JSON",
        "pw_syntax": "json.validate(s) -> bool",
        "parameters": {
            "s": {"type": "string", "description": "String to validate"}
        },
        "implementations": {
            "python": {"imports": ["import json"], "code": "try:\n    json.loads({s})\n    return True\nexcept:\n    return False"},
            "rust": {"imports": ["use serde_json;"], "code": "serde_json::from_str::<serde_json::Value>({s}).is_ok()"},
            "go": {"imports": ["import \"encoding/json\""], "code": "var js json.RawMessage; err := json.Unmarshal([]byte({s}), &js); err == nil"},
            "javascript": {"imports": [], "code": "try { JSON.parse({s}); return true; } catch { return false; }"},
            "cpp": {"imports": [], "code": "try { json::parse({s}); return true; } catch { return false; }"}
        }
    },

    # CATEGORY 5: MATH OPERATIONS (10 operations)
    "math.abs": {
        "description": "Absolute value",
        "pw_syntax": "abs(n) -> number",
        "parameters": {
            "n": {"type": "number", "description": "Number to get absolute value of"}
        },
        "implementations": {
            "python": {"imports": [], "code": "abs({n})"},
            "rust": {"imports": [], "code": "{n}.abs()"},
            "go": {"imports": ["import \"math\""], "code": "math.Abs({n})"},
            "javascript": {"imports": [], "code": "Math.abs({n})"},
            "cpp": {"imports": ["#include <cmath>"], "code": "abs({n})", "alt": "fabs({n})"}
        }
    },
    "math.min": {
        "description": "Minimum of two numbers",
        "pw_syntax": "min(a, b) -> number",
        "parameters": {
            "a": {"type": "number", "description": "First number"},
            "b": {"type": "number", "description": "Second number"}
        },
        "implementations": {
            "python": {"imports": [], "code": "min({a}, {b})"},
            "rust": {"imports": [], "code": "{a}.min({b})"},
            "go": {"imports": ["import \"math\""], "code": "math.Min({a}, {b})"},
            "javascript": {"imports": [], "code": "Math.min({a}, {b})"},
            "cpp": {"imports": ["#include <algorithm>"], "code": "std::min({a}, {b})"}
        }
    },
    "math.max": {
        "description": "Maximum of two numbers",
        "pw_syntax": "max(a, b) -> number",
        "parameters": {
            "a": {"type": "number", "description": "First number"},
            "b": {"type": "number", "description": "Second number"}
        },
        "implementations": {
            "python": {"imports": [], "code": "max({a}, {b})"},
            "rust": {"imports": [], "code": "{a}.max({b})"},
            "go": {"imports": ["import \"math\""], "code": "math.Max({a}, {b})"},
            "javascript": {"imports": [], "code": "Math.max({a}, {b})"},
            "cpp": {"imports": ["#include <algorithm>"], "code": "std::max({a}, {b})"}
        }
    },
    "math.pow": {
        "description": "Raise base to exponent",
        "pw_syntax": "base ** exp",
        "parameters": {
            "base": {"type": "number", "description": "Base number"},
            "exp": {"type": "number", "description": "Exponent"}
        },
        "implementations": {
            "python": {"imports": [], "code": "{base} ** {exp}", "alt": "pow({base}, {exp})"},
            "rust": {"imports": [], "code": "{base}.powf({exp})"},
            "go": {"imports": ["import \"math\""], "code": "math.Pow({base}, {exp})"},
            "javascript": {"imports": [], "code": "Math.pow({base}, {exp})", "alt": "{base} ** {exp}"},
            "cpp": {"imports": ["#include <cmath>"], "code": "pow({base}, {exp})"}
        }
    },
    "math.sqrt": {
        "description": "Square root",
        "pw_syntax": "sqrt(n) -> float",
        "parameters": {
            "n": {"type": "number", "description": "Number to get square root of"}
        },
        "implementations": {
            "python": {"imports": ["import math"], "code": "math.sqrt({n})", "alt": "{n} ** 0.5"},
            "rust": {"imports": [], "code": "{n}.sqrt()"},
            "go": {"imports": ["import \"math\""], "code": "math.Sqrt({n})"},
            "javascript": {"imports": [], "code": "Math.sqrt({n})"},
            "cpp": {"imports": ["#include <cmath>"], "code": "sqrt({n})"}
        }
    },
    "math.floor": {
        "description": "Round down to integer",
        "pw_syntax": "floor(n) -> int",
        "parameters": {
            "n": {"type": "number", "description": "Number to floor"}
        },
        "implementations": {
            "python": {"imports": ["import math"], "code": "math.floor({n})"},
            "rust": {"imports": [], "code": "{n}.floor() as i32"},
            "go": {"imports": ["import \"math\""], "code": "math.Floor({n})"},
            "javascript": {"imports": [], "code": "Math.floor({n})"},
            "cpp": {"imports": ["#include <cmath>"], "code": "floor({n})"}
        }
    },
    "math.ceil": {
        "description": "Round up to integer",
        "pw_syntax": "ceil(n) -> int",
        "parameters": {
            "n": {"type": "number", "description": "Number to ceil"}
        },
        "implementations": {
            "python": {"imports": ["import math"], "code": "math.ceil({n})"},
            "rust": {"imports": [], "code": "{n}.ceil() as i32"},
            "go": {"imports": ["import \"math\""], "code": "math.Ceil({n})"},
            "javascript": {"imports": [], "code": "Math.ceil({n})"},
            "cpp": {"imports": ["#include <cmath>"], "code": "ceil({n})"}
        }
    },
    "math.round": {
        "description": "Round to nearest integer",
        "pw_syntax": "round(n) -> int",
        "parameters": {
            "n": {"type": "number", "description": "Number to round"}
        },
        "implementations": {
            "python": {"imports": [], "code": "round({n})"},
            "rust": {"imports": [], "code": "{n}.round() as i32"},
            "go": {"imports": ["import \"math\""], "code": "math.Round({n})"},
            "javascript": {"imports": [], "code": "Math.round({n})"},
            "cpp": {"imports": ["#include <cmath>"], "code": "round({n})"}
        }
    },
    "math.random": {
        "description": "Random float between 0 and 1",
        "pw_syntax": "random() -> float",
        "parameters": {},
        "implementations": {
            "python": {"imports": ["import random"], "code": "random.random()"},
            "rust": {"imports": ["use rand;"], "code": "rand::random::<f64>()"},
            "go": {"imports": ["import \"math/rand\""], "code": "rand.Float64()"},
            "javascript": {"imports": [], "code": "Math.random()"},
            "cpp": {"imports": ["#include <cstdlib>"], "code": "(double)rand() / RAND_MAX"}
        }
    },
    "math.random_int": {
        "description": "Random integer between min and max (inclusive)",
        "pw_syntax": "random_int(min, max) -> int",
        "parameters": {
            "min": {"type": "integer", "description": "Minimum value (inclusive)"},
            "max": {"type": "integer", "description": "Maximum value (inclusive)"}
        },
        "implementations": {
            "python": {"imports": ["import random"], "code": "random.randint({min}, {max})"},
            "rust": {"imports": ["use rand::Rng;"], "code": "rand::thread_rng().gen_range({min}..={max})"},
            "go": {"imports": ["import \"math/rand\""], "code": "rand.Intn({max}-{min}+1) + {min}"},
            "javascript": {"imports": [], "code": "Math.floor(Math.random() * ({max} - {min} + 1)) + {min}"},
            "cpp": {"imports": ["#include <cstdlib>"], "code": "rand() % ({max} - {min} + 1) + {min}"}
        }
    },

    # CATEGORY 6: TIME/DATE (8 operations)
    "time.now": {
        "description": "Current Unix timestamp (seconds since epoch)",
        "pw_syntax": "time.now() -> int",
        "parameters": {},
        "implementations": {
            "python": {"imports": ["import time"], "code": "int(time.time())"},
            "rust": {"imports": ["use std::time::{SystemTime, UNIX_EPOCH};"], "code": "SystemTime::now().duration_since(UNIX_EPOCH)?.as_secs()"},
            "go": {"imports": ["import \"time\""], "code": "time.Now().Unix()"},
            "javascript": {"imports": [], "code": "Math.floor(Date.now() / 1000)"},
            "cpp": {"imports": ["#include <chrono>"], "code": "std::chrono::system_clock::now().time_since_epoch().count()"}
        }
    },
    "time.now_ms": {
        "description": "Current timestamp in milliseconds",
        "pw_syntax": "time.now_ms() -> int",
        "parameters": {},
        "implementations": {
            "python": {"imports": ["import time"], "code": "int(time.time() * 1000)"},
            "rust": {"imports": ["use std::time::{SystemTime, UNIX_EPOCH};"], "code": "SystemTime::now().duration_since(UNIX_EPOCH)?.as_millis()"},
            "go": {"imports": ["import \"time\""], "code": "time.Now().UnixMilli()"},
            "javascript": {"imports": [], "code": "Date.now()"},
            "cpp": {"imports": ["#include <chrono>"], "code": "std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count()"}
        }
    },
    "time.sleep": {
        "description": "Sleep for N seconds",
        "pw_syntax": "sleep(seconds) -> void",
        "parameters": {
            "seconds": {"type": "number", "description": "Seconds to sleep"}
        },
        "implementations": {
            "python": {"imports": ["import time"], "code": "time.sleep({seconds})"},
            "rust": {"imports": ["use std::thread;", "use std::time::Duration;"], "code": "thread::sleep(Duration::from_secs({seconds}))"},
            "go": {"imports": ["import \"time\""], "code": "time.Sleep(time.Duration({seconds}) * time.Second)"},
            "javascript": {"imports": [], "code": "await new Promise(resolve => setTimeout(resolve, {seconds} * 1000))"},
            "cpp": {"imports": ["#include <thread>", "#include <chrono>"], "code": "std::this_thread::sleep_for(std::chrono::seconds({seconds}))"}
        }
    },
    "time.sleep_ms": {
        "description": "Sleep for N milliseconds",
        "pw_syntax": "sleep_ms(milliseconds) -> void",
        "parameters": {
            "milliseconds": {"type": "integer", "description": "Milliseconds to sleep"}
        },
        "implementations": {
            "python": {"imports": ["import time"], "code": "time.sleep({milliseconds} / 1000)"},
            "rust": {"imports": ["use std::thread;", "use std::time::Duration;"], "code": "thread::sleep(Duration::from_millis({milliseconds}))"},
            "go": {"imports": ["import \"time\""], "code": "time.Sleep(time.Duration({milliseconds}) * time.Millisecond)"},
            "javascript": {"imports": [], "code": "await new Promise(resolve => setTimeout(resolve, {milliseconds}))"},
            "cpp": {"imports": ["#include <thread>", "#include <chrono>"], "code": "std::this_thread::sleep_for(std::chrono::milliseconds({milliseconds}))"}
        }
    },
    "time.format": {
        "description": "Format Unix timestamp to string",
        "pw_syntax": "time.format(timestamp, format) -> str",
        "parameters": {
            "timestamp": {"type": "integer", "description": "Unix timestamp"},
            "format": {"type": "string", "description": "Format string"}
        },
        "implementations": {
            "python": {"imports": ["from datetime import datetime"], "code": "datetime.fromtimestamp({timestamp}).strftime({format})"},
            "rust": {"imports": [], "code": "/* Requires chrono crate */"},
            "go": {"imports": ["import \"time\""], "code": "time.Unix({timestamp}, 0).Format({format})"},
            "javascript": {"imports": [], "code": "new Date({timestamp} * 1000).toISOString()"},
            "cpp": {"imports": [], "code": "/* Complex - requires time formatting */"}
        }
    },
    "time.parse": {
        "description": "Parse date string to Unix timestamp",
        "pw_syntax": "time.parse(date_string, format) -> int",
        "parameters": {
            "date_string": {"type": "string", "description": "Date string to parse"},
            "format": {"type": "string", "description": "Format string"}
        },
        "implementations": {
            "python": {"imports": ["from datetime import datetime"], "code": "int(datetime.strptime({date_string}, {format}).timestamp())"},
            "rust": {"imports": [], "code": "/* Requires chrono crate */"},
            "go": {"imports": ["import \"time\""], "code": "t, _ := time.Parse({format}, {date_string}); t.Unix()"},
            "javascript": {"imports": [], "code": "Math.floor(new Date({date_string}).getTime() / 1000)"},
            "cpp": {"imports": [], "code": "/* Complex - requires parsing library */"}
        }
    },
    "time.now_iso": {
        "description": "Current date/time in ISO 8601 format",
        "pw_syntax": "time.now_iso() -> str",
        "parameters": {},
        "implementations": {
            "python": {"imports": ["from datetime import datetime"], "code": "datetime.now().isoformat()"},
            "rust": {"imports": ["use chrono::Utc;"], "code": "Utc::now().to_rfc3339()"},
            "go": {"imports": ["import \"time\""], "code": "time.Now().Format(time.RFC3339)"},
            "javascript": {"imports": [], "code": "new Date().toISOString()"},
            "cpp": {"imports": [], "code": "/* Requires date library */"}
        }
    },
    "time.add_days": {
        "description": "Add days to timestamp",
        "pw_syntax": "time.add_days(timestamp, days) -> int",
        "parameters": {
            "timestamp": {"type": "integer", "description": "Unix timestamp"},
            "days": {"type": "integer", "description": "Days to add"}
        },
        "implementations": {
            "python": {"imports": [], "code": "{timestamp} + ({days} * 86400)"},
            "rust": {"imports": [], "code": "{timestamp} + ({days} * 86400)"},
            "go": {"imports": ["import \"time\""], "code": "time.Unix({timestamp}, 0).AddDate(0, 0, {days}).Unix()"},
            "javascript": {"imports": [], "code": "{timestamp} + ({days} * 86400)"},
            "cpp": {"imports": [], "code": "{timestamp} + ({days} * 86400)"}
        }
    },

    # CATEGORY 7: PROCESS/SYSTEM (6 operations)
    "process.run": {
        "description": "Execute shell command, return output",
        "pw_syntax": "process.run(cmd) -> str",
        "parameters": {
            "cmd": {"type": "string", "description": "Command to execute"}
        },
        "implementations": {
            "python": {"imports": ["import subprocess"], "code": "subprocess.check_output({cmd}, shell=True).decode()"},
            "rust": {"imports": ["use std::process::Command;"], "code": "String::from_utf8(Command::new(\"sh\").arg(\"-c\").arg({cmd}).output()?.stdout)?"},
            "go": {"imports": ["import \"os/exec\""], "code": "out, _ := exec.Command(\"sh\", \"-c\", {cmd}).Output(); string(out)"},
            "javascript": {"imports": ["const {execSync} = require('child_process');"], "code": "execSync({cmd}).toString()"},
            "cpp": {"imports": [], "code": "/* popen or system() - complex */"}
        }
    },
    "env.get": {
        "description": "Get environment variable",
        "pw_syntax": "env.get(key) -> str",
        "parameters": {
            "key": {"type": "string", "description": "Environment variable name"}
        },
        "implementations": {
            "python": {"imports": ["import os"], "code": "os.environ.get({key}, \"\")"},
            "rust": {"imports": ["use std::env;"], "code": "env::var({key}).unwrap_or_default()"},
            "go": {"imports": ["import \"os\""], "code": "os.Getenv({key})"},
            "javascript": {"imports": [], "code": "process.env[{key}] || \"\""},
            "cpp": {"imports": ["#include <cstdlib>"], "code": "getenv({key}.c_str())"}
        }
    },
    "env.set": {
        "description": "Set environment variable",
        "pw_syntax": "env.set(key, value) -> void",
        "parameters": {
            "key": {"type": "string", "description": "Environment variable name"},
            "value": {"type": "string", "description": "Value to set"}
        },
        "implementations": {
            "python": {"imports": ["import os"], "code": "os.environ[{key}] = {value}"},
            "rust": {"imports": ["use std::env;"], "code": "env::set_var({key}, {value})"},
            "go": {"imports": ["import \"os\""], "code": "os.Setenv({key}, {value})"},
            "javascript": {"imports": [], "code": "process.env[{key}] = {value}"},
            "cpp": {"imports": ["#include <cstdlib>"], "code": "setenv({key}.c_str(), {value}.c_str(), 1)"}
        }
    },
    "process.exit": {
        "description": "Exit program with code",
        "pw_syntax": "exit(code) -> void",
        "parameters": {
            "code": {"type": "integer", "description": "Exit code"}
        },
        "implementations": {
            "python": {"imports": ["import sys"], "code": "sys.exit({code})"},
            "rust": {"imports": ["use std::process;"], "code": "std::process::exit({code})"},
            "go": {"imports": ["import \"os\""], "code": "os.Exit({code})"},
            "javascript": {"imports": [], "code": "process.exit({code})"},
            "cpp": {"imports": ["#include <cstdlib>"], "code": "exit({code})"}
        }
    },
    "process.cwd": {
        "description": "Get current working directory",
        "pw_syntax": "process.cwd() -> str",
        "parameters": {},
        "implementations": {
            "python": {"imports": ["import os"], "code": "os.getcwd()"},
            "rust": {"imports": ["use std::env;"], "code": "env::current_dir()?.to_str()?"},
            "go": {"imports": ["import \"os\""], "code": "os.Getwd()"},
            "javascript": {"imports": [], "code": "process.cwd()"},
            "cpp": {"imports": ["#include <filesystem>"], "code": "std::filesystem::current_path()"}
        }
    },
    "process.chdir": {
        "description": "Change working directory",
        "pw_syntax": "process.chdir(path) -> void",
        "parameters": {
            "path": {"type": "string", "description": "Directory path to change to"}
        },
        "implementations": {
            "python": {"imports": ["import os"], "code": "os.chdir({path})"},
            "rust": {"imports": ["use std::env;"], "code": "env::set_current_dir({path})?"},
            "go": {"imports": ["import \"os\""], "code": "os.Chdir({path})"},
            "javascript": {"imports": [], "code": "process.chdir({path})"},
            "cpp": {"imports": ["#include <filesystem>"], "code": "std::filesystem::current_path({path})"}
        }
    },

    # CATEGORY 8: ARRAY OPERATIONS (10 operations)
    "array.len": {
        "description": "Get array length",
        "pw_syntax": "len(arr) -> int",
        "parameters": {
            "arr": {"type": "array", "description": "Array to measure"}
        },
        "implementations": {
            "python": {"imports": [], "code": "len({arr})"},
            "rust": {"imports": [], "code": "{arr}.len()"},
            "go": {"imports": [], "code": "len({arr})"},
            "javascript": {"imports": [], "code": "{arr}.length"},
            "cpp": {"imports": [], "code": "{arr}.size()"}
        }
    },
    "array.push": {
        "description": "Add item to end of array",
        "pw_syntax": "arr.push(item) -> void",
        "parameters": {
            "arr": {"type": "array", "description": "Array to modify"},
            "item": {"type": "any", "description": "Item to add"}
        },
        "implementations": {
            "python": {"imports": [], "code": "{arr}.append({item})"},
            "rust": {"imports": [], "code": "{arr}.push({item})"},
            "go": {"imports": [], "code": "{arr} = append({arr}, {item})"},
            "javascript": {"imports": [], "code": "{arr}.push({item})"},
            "cpp": {"imports": [], "code": "{arr}.push_back({item})"}
        }
    },
    "array.pop": {
        "description": "Remove and return last item",
        "pw_syntax": "arr.pop() -> any",
        "parameters": {
            "arr": {"type": "array", "description": "Array to modify"}
        },
        "implementations": {
            "python": {"imports": [], "code": "{arr}.pop()"},
            "rust": {"imports": [], "code": "{arr}.pop()"},
            "go": {"imports": [], "code": "item := {arr}[len({arr})-1]; {arr} = {arr}[:len({arr})-1]"},
            "javascript": {"imports": [], "code": "{arr}.pop()"},
            "cpp": {"imports": [], "code": "auto item = {arr}.back(); {arr}.pop_back(); return item;"}
        }
    },
    "array.contains": {
        "description": "Check if array contains item",
        "pw_syntax": "item in arr",
        "parameters": {
            "arr": {"type": "array", "description": "Array to search"},
            "item": {"type": "any", "description": "Item to find"}
        },
        "implementations": {
            "python": {"imports": [], "code": "{item} in {arr}"},
            "rust": {"imports": [], "code": "{arr}.contains(&{item})"},
            "go": {"imports": [], "code": "/* Requires loop */"},
            "javascript": {"imports": [], "code": "{arr}.includes({item})"},
            "cpp": {"imports": ["#include <algorithm>"], "code": "std::find({arr}.begin(), {arr}.end(), {item}) != {arr}.end()"}
        }
    },
    "array.index_of": {
        "description": "Find index of item (-1 if not found)",
        "pw_syntax": "arr.index_of(item) -> int",
        "parameters": {
            "arr": {"type": "array", "description": "Array to search"},
            "item": {"type": "any", "description": "Item to find"}
        },
        "implementations": {
            "python": {"imports": [], "code": "{arr}.index({item}) if {item} in {arr} else -1"},
            "rust": {"imports": [], "code": "{arr}.iter().position(|x| x == &{item}).map(|i| i as i32).unwrap_or(-1)"},
            "go": {"imports": [], "code": "/* Requires loop */"},
            "javascript": {"imports": [], "code": "{arr}.indexOf({item})"},
            "cpp": {"imports": ["#include <algorithm>"], "code": "std::find({arr}.begin(), {arr}.end(), {item}) - {arr}.begin()"}
        }
    },
    "array.slice": {
        "description": "Extract subarray from start to end",
        "pw_syntax": "arr[start:end]",
        "parameters": {
            "arr": {"type": "array", "description": "Array to slice"},
            "start": {"type": "integer", "description": "Start index"},
            "end": {"type": "integer", "description": "End index"}
        },
        "implementations": {
            "python": {"imports": [], "code": "{arr}[{start}:{end}]"},
            "rust": {"imports": [], "code": "&{arr}[{start}..{end}]"},
            "go": {"imports": [], "code": "{arr}[{start}:{end}]"},
            "javascript": {"imports": [], "code": "{arr}.slice({start}, {end})"},
            "cpp": {"imports": ["#include <vector>"], "code": "std::vector<T>({arr}.begin()+{start}, {arr}.begin()+{end})"}
        }
    },
    "array.reverse": {
        "description": "Reverse array",
        "pw_syntax": "arr.reverse() -> array",
        "parameters": {
            "arr": {"type": "array", "description": "Array to reverse"}
        },
        "implementations": {
            "python": {"imports": [], "code": "{arr}[::-1]", "alt": "list(reversed({arr}))"},
            "rust": {"imports": [], "code": "{arr}.iter().rev().cloned().collect::<Vec<_>>()"},
            "go": {"imports": [], "code": "/* Requires loop */"},
            "javascript": {"imports": [], "code": "[...{arr}].reverse()"},
            "cpp": {"imports": ["#include <algorithm>"], "code": "std::reverse({arr}.begin(), {arr}.end())"}
        }
    },
    "array.sort": {
        "description": "Sort array (ascending)",
        "pw_syntax": "sorted(arr) -> array",
        "parameters": {
            "arr": {"type": "array", "description": "Array to sort"}
        },
        "implementations": {
            "python": {"imports": [], "code": "sorted({arr})"},
            "rust": {"imports": [], "code": "{arr}.sort(); {arr}"},
            "go": {"imports": ["import \"sort\""], "code": "sort.Ints({arr})"},
            "javascript": {"imports": [], "code": "[...{arr}].sort((a,b) => a-b)"},
            "cpp": {"imports": ["#include <algorithm>"], "code": "std::sort({arr}.begin(), {arr}.end())"}
        }
    },

    # CATEGORY 9: ENCODING/DECODING (6 operations)
    "base64.encode": {
        "description": "Encode bytes/string to base64",
        "pw_syntax": "base64.encode(data) -> str",
        "parameters": {
            "data": {"type": "string", "description": "Data to encode"}
        },
        "implementations": {
            "python": {"imports": ["import base64"], "code": "base64.b64encode({data}.encode()).decode()"},
            "rust": {"imports": ["use base64;"], "code": "base64::encode({data})"},
            "go": {"imports": ["import \"encoding/base64\""], "code": "base64.StdEncoding.EncodeToString([]byte({data}))"},
            "javascript": {"imports": [], "code": "Buffer.from({data}).toString('base64')"},
            "cpp": {"imports": [], "code": "/* Requires library */"}
        }
    },
    "base64.decode": {
        "description": "Decode base64 to string",
        "pw_syntax": "base64.decode(encoded) -> str",
        "parameters": {
            "encoded": {"type": "string", "description": "Base64 string to decode"}
        },
        "implementations": {
            "python": {"imports": ["import base64"], "code": "base64.b64decode({encoded}).decode()"},
            "rust": {"imports": ["use base64;"], "code": "String::from_utf8(base64::decode({encoded})?)?"},
            "go": {"imports": ["import \"encoding/base64\""], "code": "decoded, _ := base64.StdEncoding.DecodeString({encoded}); string(decoded)"},
            "javascript": {"imports": [], "code": "Buffer.from({encoded}, 'base64').toString()"},
            "cpp": {"imports": [], "code": "/* Requires library */"}
        }
    },
    "hex.encode": {
        "description": "Encode bytes to hex string",
        "pw_syntax": "hex.encode(data) -> str",
        "parameters": {
            "data": {"type": "string", "description": "Data to encode"}
        },
        "implementations": {
            "python": {"imports": [], "code": "{data}.encode().hex()"},
            "rust": {"imports": ["use hex;"], "code": "hex::encode({data})"},
            "go": {"imports": ["import \"encoding/hex\""], "code": "hex.EncodeToString([]byte({data}))"},
            "javascript": {"imports": [], "code": "Buffer.from({data}).toString('hex')"},
            "cpp": {"imports": [], "code": "/* Manual implementation */"}
        }
    },
    "hex.decode": {
        "description": "Decode hex string to bytes",
        "pw_syntax": "hex.decode(encoded) -> str",
        "parameters": {
            "encoded": {"type": "string", "description": "Hex string to decode"}
        },
        "implementations": {
            "python": {"imports": [], "code": "bytes.fromhex({encoded}).decode()"},
            "rust": {"imports": ["use hex;"], "code": "String::from_utf8(hex::decode({encoded})?)?"},
            "go": {"imports": ["import \"encoding/hex\""], "code": "decoded, _ := hex.DecodeString({encoded}); string(decoded)"},
            "javascript": {"imports": [], "code": "Buffer.from({encoded}, 'hex').toString()"},
            "cpp": {"imports": [], "code": "/* Manual implementation */"}
        }
    },
    "hash.md5": {
        "description": "Compute MD5 hash",
        "pw_syntax": "hash.md5(data) -> str",
        "parameters": {
            "data": {"type": "string", "description": "Data to hash"}
        },
        "implementations": {
            "python": {"imports": ["import hashlib"], "code": "hashlib.md5({data}.encode()).hexdigest()"},
            "rust": {"imports": ["use md5;"], "code": "format!(\"{:x}\", md5::compute({data}))"},
            "go": {"imports": ["import \"crypto/md5\"", "import \"fmt\""], "code": "fmt.Sprintf(\"%x\", md5.Sum([]byte({data})))"},
            "javascript": {"imports": ["const crypto = require('crypto');"], "code": "crypto.createHash('md5').update({data}).digest('hex')"},
            "cpp": {"imports": [], "code": "/* Requires OpenSSL or similar */"}
        }
    },
    "hash.sha256": {
        "description": "Compute SHA-256 hash",
        "pw_syntax": "hash.sha256(data) -> str",
        "parameters": {
            "data": {"type": "string", "description": "Data to hash"}
        },
        "implementations": {
            "python": {"imports": ["import hashlib"], "code": "hashlib.sha256({data}.encode()).hexdigest()"},
            "rust": {"imports": ["use sha2::{Sha256, Digest};"], "code": "format!(\"{:x}\", Sha256::digest({data}))"},
            "go": {"imports": ["import \"crypto/sha256\"", "import \"fmt\""], "code": "fmt.Sprintf(\"%x\", sha256.Sum256([]byte({data})))"},
            "javascript": {"imports": ["const crypto = require('crypto');"], "code": "crypto.createHash('sha256').update({data}).digest('hex')"},
            "cpp": {"imports": [], "code": "/* Requires OpenSSL or similar */"}
        }
    },

    # CATEGORY 10: TYPE CONVERSIONS (8 operations)
    "type.str": {
        "description": "Convert any value to string",
        "pw_syntax": "str(value) -> str",
        "parameters": {
            "value": {"type": "any", "description": "Value to convert"}
        },
        "implementations": {
            "python": {"imports": [], "code": "str({value})"},
            "rust": {"imports": [], "code": "{value}.to_string()", "alt": "format!(\"{}\", {value})"},
            "go": {"imports": ["import \"fmt\""], "code": "fmt.Sprint({value})"},
            "javascript": {"imports": [], "code": "String({value})", "alt": "{value}.toString()"},
            "cpp": {"imports": ["#include <string>"], "code": "std::to_string({value})"}
        }
    },
    "type.int": {
        "description": "Convert string to integer",
        "pw_syntax": "int(s) -> int",
        "parameters": {
            "s": {"type": "string", "description": "String to convert"}
        },
        "implementations": {
            "python": {"imports": [], "code": "int({s})"},
            "rust": {"imports": [], "code": "{s}.parse::<i32>()?"},
            "go": {"imports": ["import \"strconv\""], "code": "strconv.Atoi({s})"},
            "javascript": {"imports": [], "code": "parseInt({s}, 10)", "alt": "Number({s})"},
            "cpp": {"imports": ["#include <string>"], "code": "std::stoi({s})"}
        }
    },
    "type.float": {
        "description": "Convert string to float",
        "pw_syntax": "float(s) -> float",
        "parameters": {
            "s": {"type": "string", "description": "String to convert"}
        },
        "implementations": {
            "python": {"imports": [], "code": "float({s})"},
            "rust": {"imports": [], "code": "{s}.parse::<f64>()?"},
            "go": {"imports": ["import \"strconv\""], "code": "strconv.ParseFloat({s}, 64)"},
            "javascript": {"imports": [], "code": "parseFloat({s})", "alt": "Number({s})"},
            "cpp": {"imports": ["#include <string>"], "code": "std::stod({s})"}
        }
    },
    "type.bool": {
        "description": "Convert string to boolean",
        "pw_syntax": "bool(s) -> bool",
        "parameters": {
            "s": {"type": "string", "description": "String to convert"}
        },
        "implementations": {
            "python": {"imports": [], "code": "{s}.lower() in ('true', '1', 'yes')"},
            "rust": {"imports": [], "code": "{s}.parse::<bool>()?"},
            "go": {"imports": ["import \"strconv\""], "code": "strconv.ParseBool({s})"},
            "javascript": {"imports": [], "code": "{s}.toLowerCase() === 'true'"},
            "cpp": {"imports": [], "code": "{s} == \"true\" || {s} == \"1\""}
        }
    },
    "type.is_string": {
        "description": "Check if value is string type",
        "pw_syntax": "typeof(value) == \"string\"",
        "parameters": {
            "value": {"type": "any", "description": "Value to check"}
        },
        "implementations": {
            "python": {"imports": [], "code": "isinstance({value}, str)"},
            "rust": {"imports": [], "code": "/* Compile-time type checking */"},
            "go": {"imports": [], "code": "/* Compile-time type checking */"},
            "javascript": {"imports": [], "code": "typeof {value} === 'string'"},
            "cpp": {"imports": [], "code": "/* Compile-time type checking */"}
        }
    },
    "type.is_int": {
        "description": "Check if value is integer type",
        "pw_syntax": "typeof(value) == \"int\"",
        "parameters": {
            "value": {"type": "any", "description": "Value to check"}
        },
        "implementations": {
            "python": {"imports": [], "code": "isinstance({value}, int)"},
            "rust": {"imports": [], "code": "/* Compile-time type checking */"},
            "go": {"imports": [], "code": "/* Compile-time type checking */"},
            "javascript": {"imports": [], "code": "Number.isInteger({value})"},
            "cpp": {"imports": [], "code": "/* Compile-time type checking */"}
        }
    },
    "type.is_float": {
        "description": "Check if value is float type",
        "pw_syntax": "typeof(value) == \"float\"",
        "parameters": {
            "value": {"type": "any", "description": "Value to check"}
        },
        "implementations": {
            "python": {"imports": [], "code": "isinstance({value}, float)"},
            "rust": {"imports": [], "code": "/* Compile-time type checking */"},
            "go": {"imports": [], "code": "/* Compile-time type checking */"},
            "javascript": {"imports": [], "code": "typeof {value} === 'number' && !Number.isInteger({value})"},
            "cpp": {"imports": [], "code": "/* Compile-time type checking */"}
        }
    },
    "type.is_bool": {
        "description": "Check if value is boolean type",
        "pw_syntax": "typeof(value) == \"bool\"",
        "parameters": {
            "value": {"type": "any", "description": "Value to check"}
        },
        "implementations": {
            "python": {"imports": [], "code": "isinstance({value}, bool)"},
            "rust": {"imports": [], "code": "/* Compile-time type checking */"},
            "go": {"imports": [], "code": "/* Compile-time type checking */"},
            "javascript": {"imports": [], "code": "typeof {value} === 'boolean'"},
            "cpp": {"imports": [], "code": "/* Compile-time type checking */"}
        }
    }
}

# ============================================================================
# MCP SERVER IMPLEMENTATION
# ============================================================================

class PWOperationsMCPServer:
    """MCP Server for Promptware Universal Operations"""

    def __init__(self):
        self.operations = OPERATIONS
        self.protocol_version = "2024-11-05"
        self.server_version = "1.0.0"

    def generate_ir(self, op_id: str, op_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate PW IR representation for an operation."""
        if "ir" in op_data:
            return op_data["ir"]

        # Auto-generate IR based on operation structure
        syntax = op_data["pw_syntax"]

        # Parse operation syntax to determine IR structure
        if "." in op_id:
            # Namespaced operation: file.read, str.split, etc.
            namespace, method = op_id.split(".", 1)
            params = list(op_data["parameters"].keys())

            return {
                "type": "call",
                "function": {
                    "type": "property_access",
                    "object": namespace,
                    "property": method
                },
                "args": [{"type": "identifier", "name": p} for p in params]
            }
        elif "(" in syntax:
            # Built-in function: len(), abs(), etc.
            func_name = syntax.split("(")[0]
            params = list(op_data["parameters"].keys())

            return {
                "type": "call",
                "function": {"type": "identifier", "name": func_name},
                "args": [{"type": "identifier", "name": p} for p in params]
            }
        elif " in " in syntax:
            # Operator: "x in arr"
            return {
                "type": "binary_op",
                "operator": "in",
                "left": {"type": "identifier", "name": "item"},
                "right": {"type": "identifier", "name": "collection"}
            }
        elif "[" in syntax and ":" in syntax:
            # Slice: arr[start:end]
            return {
                "type": "slice",
                "object": {"type": "identifier", "name": "array"},
                "start": {"type": "identifier", "name": "start"},
                "stop": {"type": "identifier", "name": "end"}
            }
        else:
            # Fallback: generic call
            params = list(op_data["parameters"].keys())
            return {
                "type": "call",
                "function": {"type": "identifier", "name": op_id},
                "args": [{"type": "identifier", "name": p} for p in params]
            }

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle JSON-RPC 2.0 request."""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        if method == "initialize":
            return self.initialize(request_id)
        elif method == "tools/list":
            return self.list_tools(request_id)
        elif method == "tools/call":
            return self.call_tool(request_id, params)
        else:
            return self.error(request_id, -32601, f"Method not found: {method}")

    def initialize(self, request_id: Optional[Any]) -> Dict[str, Any]:
        """Initialize MCP server."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": self.protocol_version,
                "serverInfo": {
                    "name": "pw-operations-server",
                    "version": self.server_version
                },
                "capabilities": {
                    "tools": {}
                }
            }
        }

    def list_tools(self, request_id: Optional[Any]) -> Dict[str, Any]:
        """List all 107 operations as MCP tools."""
        tools = []
        for op_id, op_data in self.operations.items():
            # Build parameter schema
            properties = {
                "target": {
                    "type": "string",
                    "enum": ["python", "rust", "go", "javascript", "cpp"],
                    "description": "Target language for code generation"
                }
            }

            # Add operation-specific parameters
            for param_name, param_spec in op_data["parameters"].items():
                properties[param_name] = param_spec

            tools.append({
                "name": op_id,
                "description": f"{op_data['description']} | PW Syntax: {op_data['pw_syntax']}",
                "inputSchema": {
                    "type": "object",
                    "properties": properties,
                    "required": ["target"]
                }
            })

        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"tools": tools}
        }

    def call_tool(self, request_id: Optional[Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tool and return implementation for target language."""
        tool_name = params.get("name")
        args = params.get("arguments", {})
        target = args.get("target")

        if tool_name not in self.operations:
            return self.error(request_id, -32602, f"Unknown operation: {tool_name}")

        if not target:
            return self.error(request_id, -32602, "Missing required parameter: target")

        op = self.operations[tool_name]
        impl = op["implementations"].get(target)

        if not impl:
            return self.error(request_id, -32602, f"Target {target} not supported for {tool_name}")

        # Substitute parameters in code template
        code = impl["code"]
        for param_name in op["parameters"].keys():
            if param_name in args:
                value = args[param_name]

                # Determine if this is a variable reference or a literal value
                if isinstance(value, str):
                    # Check if it looks like a variable name (identifier)
                    # Variable names: content, text, myVar, user_id
                    # Literal strings: "hello.txt", "data", "/path/to/file"
                    if value.isidentifier():
                        # It's a variable reference - use as-is
                        code = code.replace(f"{{{param_name}}}", value)
                    else:
                        # It's a literal string - quote it
                        code = code.replace(f"{{{param_name}}}", repr(value))
                else:
                    # Non-string values (int, float, bool, etc.)
                    code = code.replace(f"{{{param_name}}}", str(value))

        # Build response with IR, AST, and code
        result = {
            "operation": tool_name,
            "target": target,
            "pw_syntax": op["pw_syntax"],
            "ir": self.generate_ir(tool_name, op),  # PW IR representation
            "imports": impl.get("imports", []),
            "code": code
        }

        # Add target-language AST if available
        if "ast" in impl:
            result["ast"] = impl["ast"]

        if "alt" in impl:
            result["alternative"] = impl["alt"]
        if "notes" in impl:
            result["notes"] = impl["notes"]

        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [{
                    "type": "text",
                    "text": json.dumps(result, indent=2)
                }]
            }
        }

    def error(self, request_id: Optional[Any], code: int, message: str) -> Dict[str, Any]:
        """Return JSON-RPC error response."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": code, "message": message}
        }

    def run(self):
        """Run MCP server (stdio transport)."""
        for line in sys.stdin:
            try:
                request = json.loads(line.strip())
                response = self.handle_request(request)
                print(json.dumps(response), flush=True)
            except Exception as e:
                error_response = self.error(None, -32603, f"Internal error: {str(e)}")
                print(json.dumps(error_response), flush=True)

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    server = PWOperationsMCPServer()
    server.run()
