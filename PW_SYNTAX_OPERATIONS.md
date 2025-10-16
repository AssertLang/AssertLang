# AssertLang Universal Operations: Canonical Syntax Design
**Version:** 1.0
**Date:** 2025-10-13
**Purpose:** Define optimal PW syntax for 107 universal programming operations based on cross-language research

---

## DESIGN PRINCIPLES

1. **Brevity**: Minimize keystrokes without sacrificing clarity
2. **Clarity**: Obvious intent from name alone
3. **Consistency**: Similar operations use similar patterns
4. **Namespacing**: Group related operations (file.*, str.*, http.*, etc.)
5. **Universality**: Avoid language-specific idioms
6. **Natural Reading**: Code reads like English
7. **Idiomatic**: Match patterns developers expect from modern languages

---

## CATEGORY 1: FILE I/O (12 operations)

### Operation: read_file
**ID**: `file.read`
**Description**: Read entire file contents as string

**Cross-Language Analysis**:
- **Python**: `open(path, 'r').read()` | `Path(path).read_text()` ← pathlib is modern standard
- **Rust**: `fs::read_to_string(path)` ← idiomatic one-liner, most popular
- **Go**: `os.ReadFile(path)` ← standard library (replaced ioutil)
- **JavaScript**: `fs.readFileSync(path, 'utf8')` ← Node.js standard
- **C++**: `ifstream f(path); string((istreambuf_iterator<char>(f))...)` ← verbose

**Common Patterns**:
- Function-style: All languages use function call (not method on string)
- Namespace prefix: Rust (`fs::`), Python (`Path`), JS (`fs.`)
- Single argument: path as string
- Return: string content

**PW Syntax (RECOMMENDED)**:
```pw
file.read(path) -> str
```

**Rationale**:
- `file.` namespace groups all file operations
- `read` is universal verb (Rust, Python pathlib, Node.js)
- 11 chars total: `file.read()`
- Reads naturally: "file read path"
- Matches modern API design (Rust's `fs::read_to_string`)

---

### Operation: write_file
**ID**: `file.write`
**Description**: Write string to file (overwrite)

**Cross-Language Analysis**:
- **Python**: `Path(path).write_text(content)` ← modern pathlib idiom
- **Rust**: `fs::write(path, content)` ← most concise, idiomatic
- **Go**: `os.WriteFile(path, []byte(content), 0644)` ← standard
- **JavaScript**: `fs.writeFileSync(path, content)` ← sync version
- **C++**: `ofstream f(path); f << content;` ← requires stream setup

**Common Patterns**:
- Two arguments: path, content
- Overwrite semantics by default
- Most concise: Rust `fs::write`

**PW Syntax (RECOMMENDED)**:
```pw
file.write(path, content) -> void
```

**Rationale**:
- Matches Rust's `fs::write` (industry best practice)
- 12 chars: `file.write()`
- Clear intent: "write to file"
- Consistent with `file.read`

---

### Operation: append_file
**ID**: `file.append`
**Description**: Append string to file

**Cross-Language Analysis**:
- **Python**: `open(path, 'a').write(content)` ← requires mode flag
- **Rust**: `OpenOptions::new().append(true).open(path)?.write_all(...)` ← verbose
- **Go**: `os.OpenFile(path, os.O_APPEND|os.O_WRONLY, 0644)` ← requires flags
- **JavaScript**: `fs.appendFileSync(path, content)` ← dedicated function
- **C++**: `ofstream f(path, ios::app);` ← append mode

**Common Patterns**:
- Two arguments: path, content
- No universal short form (all require mode/flags)
- JavaScript's dedicated `appendFile` is clearest

**PW Syntax (RECOMMENDED)**:
```pw
file.append(path, content) -> void
```

**Rationale**:
- Dedicated verb `append` is clearest intent
- 13 chars: `file.append()`
- Follows JS pattern (most explicit)
- Parallel to `file.write`

---

### Operation: file_exists
**ID**: `file.exists`
**Description**: Check if file exists

**Cross-Language Analysis**:
- **Python**: `Path(path).exists()` ← pathlib method
- **Rust**: `Path::new(path).exists()` ← idiomatic
- **Go**: `_, err := os.Stat(path); err == nil` ← verbose
- **JavaScript**: `fs.existsSync(path)` ← sync version
- **C++**: `filesystem::exists(path)` ← C++17

**Common Patterns**:
- Single argument: path
- Return: boolean
- `exists` is universal verb (Python, Rust, C++)

**PW Syntax (RECOMMENDED)**:
```pw
file.exists(path) -> bool
```

**Rationale**:
- `exists` is universal across Rust, Python, C++
- 13 chars: `file.exists()`
- Clear boolean intent
- Natural reading: "does file exist at path?"

---

### Operation: delete_file
**ID**: `file.delete`
**Description**: Delete file

**Cross-Language Analysis**:
- **Python**: `Path(path).unlink()` ← pathlib (historical Unix term)
- **Rust**: `fs::remove_file(path)` ← explicit "remove"
- **Go**: `os.Remove(path)` ← simple
- **JavaScript**: `fs.unlinkSync(path)` ← follows Unix tradition
- **C++**: `filesystem::remove(path)` ← C++17

**Common Patterns**:
- Two naming camps: `remove` (Rust, Go, C++) vs `unlink` (Python, JS - Unix tradition)
- Single argument: path
- `remove` is more intuitive for non-Unix users

**PW Syntax (RECOMMENDED)**:
```pw
file.delete(path) -> void
```

**Rationale**:
- `delete` is most universal/intuitive (clearer than `remove` or `unlink`)
- 13 chars: `file.delete()`
- Matches user intent (not implementation detail)
- Consistent with common UI terminology

---

### Operation: read_lines
**ID**: `file.read_lines`
**Description**: Read file as array of lines

**Cross-Language Analysis**:
- **Python**: `Path(path).read_text().splitlines()` ← two-step modern approach
- **Rust**: `BufReader::new(File::open(path)?).lines().collect()` ← explicit buffering
- **Go**: `strings.Split(string(os.ReadFile(path)), "\n")` ← manual split
- **JavaScript**: `fs.readFileSync(path, 'utf8').split('\n')` ← manual split
- **C++**: Requires loop with `getline()`

**Common Patterns**:
- Most languages: read + split by newline
- No universal dedicated function
- Rust has `lines()` iterator method

**PW Syntax (RECOMMENDED)**:
```pw
file.read_lines(path) -> List<str>
```

**Rationale**:
- Compound verb `read_lines` makes operation explicit
- 16 chars: `file.read_lines()`
- Clearer than separate read + split operations
- Matches high-level intent (not low-level implementation)

---

### Operation: write_lines
**ID**: `file.write_lines`
**Description**: Write array of strings as lines

**Cross-Language Analysis**:
- **Python**: `open(path, 'w').writelines(line + '\n' for line in lines)` ← requires newline addition
- **Rust**: `fs::write(path, lines.join("\n"))` ← join then write
- **Go**: `os.WriteFile(path, []byte(strings.Join(lines, "\n")), 0644)` ← join then write
- **JavaScript**: `fs.writeFileSync(path, lines.join('\n'))` ← join then write
- **C++**: Requires loop

**Common Patterns**:
- Two-step: join with newline + write
- No dedicated "write lines" function in most languages
- Python's `writelines()` is misleading (doesn't add newlines)

**PW Syntax (RECOMMENDED)**:
```pw
file.write_lines(path, lines) -> void
```

**Rationale**:
- Compound verb `write_lines` is explicit
- 17 chars: `file.write_lines()`
- High-level intent (abstracts join + write)
- Parallel to `file.read_lines`

---

### Operation: list_directory
**ID**: `file.list_dir`
**Description**: List files/directories in path

**Cross-Language Analysis**:
- **Python**: `os.listdir(path)` ← classic | `[f.name for f in Path(path).iterdir()]` ← modern
- **Rust**: `fs::read_dir(path)?` ← returns iterator
- **Go**: `os.ReadDir(path)` ← returns entries
- **JavaScript**: `fs.readdirSync(path)` ← "readdir" is Unix tradition
- **C++**: `filesystem::directory_iterator(path)` ← C++17

**Common Patterns**:
- Two naming camps: `listdir` (Python) vs `readdir` (Unix, JS)
- Single argument: path
- Return: array of names

**PW Syntax (RECOMMENDED)**:
```pw
file.list_dir(path) -> List<str>
```

**Rationale**:
- `list_dir` is clearer than `readdir` (not "reading" directory)
- 14 chars: `file.list_dir()`
- Matches Python's `listdir` (widely understood)
- Abbreviated `dir` keeps it short

---

### Operation: create_directory
**ID**: `file.mkdir`
**Description**: Create directory (and parents if needed)

**Cross-Language Analysis**:
- **Python**: `Path(path).mkdir(parents=True, exist_ok=True)` ← modern
- **Rust**: `fs::create_dir_all(path)` ← explicit "all parents"
- **Go**: `os.MkdirAll(path, 0755)` ← Unix tradition
- **JavaScript**: `fs.mkdirSync(path, {recursive: true})` ← recursive option
- **C++**: `filesystem::create_directories(path)` ← C++17

**Common Patterns**:
- Universal: `mkdir` (Unix tradition)
- Modern versions create parents by default
- "All" or "recursive" variants common

**PW Syntax (RECOMMENDED)**:
```pw
file.mkdir(path) -> void
```

**Rationale**:
- `mkdir` is universal Unix term (all languages use it)
- 12 chars: `file.mkdir()`
- Implicit parent creation (modern behavior)
- Shortest, most recognized form

---

### Operation: delete_directory
**ID**: `file.rmdir`
**Description**: Delete directory recursively

**Cross-Language Analysis**:
- **Python**: `shutil.rmtree(path)` ← "tree" implies recursive
- **Rust**: `fs::remove_dir_all(path)` ← explicit "all"
- **Go**: `os.RemoveAll(path)` ← explicit "all"
- **JavaScript**: `fs.rmSync(path, {recursive: true, force: true})` ← options-based
- **C++**: `filesystem::remove_all(path)` ← C++17

**Common Patterns**:
- Unix tradition: `rmdir` + variants
- Recursive deletion requires explicit flag/suffix
- "tree" (Python) or "all" (Rust, Go, C++) for recursive

**PW Syntax (RECOMMENDED)**:
```pw
file.rmdir(path) -> void
```

**Rationale**:
- `rmdir` is universal Unix term
- 12 chars: `file.rmdir()`
- Implicit recursive (modern behavior, matches `mkdir`)
- Parallel to `file.mkdir`

---

### Operation: get_file_size
**ID**: `file.size`
**Description**: Get file size in bytes

**Cross-Language Analysis**:
- **Python**: `Path(path).stat().st_size` ← requires stat
- **Rust**: `fs::metadata(path)?.len()` ← metadata + len
- **Go**: `info, _ := os.Stat(path); info.Size()` ← stat + size
- **JavaScript**: `fs.statSync(path).size` ← stat + size
- **C++**: `filesystem::file_size(path)` ← direct function (C++17)

**Common Patterns**:
- Most require two steps: stat + extract size
- C++ has dedicated `file_size` function (clearest)
- Property/method name is `size` or `Size()`

**PW Syntax (RECOMMENDED)**:
```pw
file.size(path) -> int
```

**Rationale**:
- `size` is universal property name
- 11 chars: `file.size()`
- Matches C++'s direct function (best practice)
- Clear intent: "get file size"

---

### Operation: copy_file
**ID**: `file.copy`
**Description**: Copy file from src to dest

**Cross-Language Analysis**:
- **Python**: `shutil.copy2(src, dest)` ← preserves metadata
- **Rust**: `fs::copy(src, dest)` ← simple, idiomatic
- **Go**: Manual read + write (no built-in)
- **JavaScript**: `fs.copyFileSync(src, dest)` ← explicit "file"
- **C++**: `filesystem::copy_file(src, dest)` ← C++17

**Common Patterns**:
- Two arguments: src, dest
- Rust has simplest API: `fs::copy`
- C++ and JS are explicit: `copy_file`

**PW Syntax (RECOMMENDED)**:
```pw
file.copy(src, dest) -> void
```

**Rationale**:
- `copy` is universal verb
- 11 chars: `file.copy()`
- Matches Rust's concise API
- Context (file namespace) makes intent clear

---

## CATEGORY 2: STRING OPERATIONS (15 operations)

### Operation: str_length
**ID**: `str.len`
**Description**: Get string length

**Cross-Language Analysis**:
- **Python**: `len(s)` ← built-in function
- **Rust**: `s.len()` ← method
- **Go**: `len(s)` ← built-in function
- **JavaScript**: `s.length` ← property
- **C++**: `s.length()` | `s.size()` ← methods

**Common Patterns**:
- Split between function (`len()`) and method (`.len()` or `.length`)
- `len` vs `length`: both common
- Python's built-in `len()` is simplest

**PW Syntax (RECOMMENDED)**:
```pw
str.len(s) -> int
```

**Rationale**:
- `len` is shorter than `length` (3 chars vs 6)
- Follows Rust/Go convention
- 8 chars: `str.len()`
- Note: Could also use built-in `len(s)` like Python, but namespacing keeps consistency

**Alternative considered**: Built-in `len(s)` (Python-style) - May be better for universality

---

### Operation: str_concat
**ID**: `+` operator
**Description**: Concatenate two strings

**Cross-Language Analysis**:
- **Python**: `s1 + s2` ← operator overload
- **Rust**: `format!("{}{}", s1, s2)` or `s1.to_owned() + &s2` ← ownership complexity
- **Go**: `s1 + s2` ← operator
- **JavaScript**: `s1 + s2` or `` `${s1}${s2}` `` ← operator + template literals
- **C++**: `s1 + s2` ← operator overload

**Common Patterns**:
- Universal: `+` operator for string concatenation
- Only Rust is complex (due to ownership)

**PW Syntax (RECOMMENDED)**:
```pw
s1 + s2  // operator syntax
```

**Rationale**:
- `+` is universal across Python, Go, JS, C++
- Built-in operator (not function call)
- Most concise possible (1 char)
- Matches developer expectations

**Note**: No `str.concat()` function needed - operator is sufficient

---

### Operation: str_substring
**ID**: Slice operator `[start:end]`
**Description**: Extract substring from start to end index

**Cross-Language Analysis**:
- **Python**: `s[start:end]` ← slice syntax
- **Rust**: `&s[start..end]` ← slice syntax (different notation)
- **Go**: `s[start:end]` ← slice syntax
- **JavaScript**: `s.substring(start, end)` or `s.slice(start, end)` ← methods
- **C++**: `s.substr(start, end-start)` ← method (length parameter, not end)

**Common Patterns**:
- Python/Go: slice notation `[start:end]`
- Rust: slice notation `[start..end]`
- JS/C++: method calls
- Slice notation is more concise

**PW Syntax (RECOMMENDED)**:
```pw
s[start:end]  // slice syntax
```

**Rationale**:
- Matches Python/Go slice syntax (widely adopted)
- Most concise: `[:]` notation
- Operator syntax (not function call)
- Universal understanding in modern languages

**Note**: No `str.substring()` function needed - slice operator is sufficient

---

### Operation: str_contains
**ID**: `in` operator | `str.contains`
**Description**: Check if string contains substring

**Cross-Language Analysis**:
- **Python**: `substring in s` ← operator (most readable)
- **Rust**: `s.contains(substring)` ← method
- **Go**: `strings.Contains(s, substring)` ← function
- **JavaScript**: `s.includes(substring)` ← method
- **C++**: `s.find(substring) != string::npos` ← complex

**Common Patterns**:
- Split between operator (`in`) and method (`.contains()` or `.includes()`)
- Python's `in` is most readable
- Rust's `.contains()` is explicit

**PW Syntax (RECOMMENDED)**:
```pw
substring in s  // operator syntax (primary)
str.contains(s, substring)  // function syntax (alternative)
```

**Rationale**:
- Python's `in` operator is most natural ("is X in Y?")
- But also provide `str.contains()` for consistency with other operations
- Support both: operator for brevity, function for discoverability

---

### Operation: str_starts_with
**ID**: `str.starts_with`
**Description**: Check if string starts with prefix

**Cross-Language Analysis**:
- **Python**: `s.startswith(prefix)` ← method (lowercase, no underscore)
- **Rust**: `s.starts_with(prefix)` ← method (underscore)
- **Go**: `strings.HasPrefix(s, prefix)` ← function (different naming)
- **JavaScript**: `s.startsWith(prefix)` ← method (camelCase)
- **C++**: `s.rfind(prefix, 0) == 0` ← manual check

**Common Patterns**:
- Most have dedicated method
- Naming: `startswith` (Python) vs `starts_with` (Rust) vs `startsWith` (JS) vs `HasPrefix` (Go)
- Rust's snake_case `starts_with` is clearest

**PW Syntax (RECOMMENDED)**:
```pw
str.starts_with(s, prefix) -> bool
```

**Rationale**:
- Follows Rust convention (snake_case, underscore)
- 16 chars: `str.starts_with()`
- Most explicit naming
- Consistent with PW naming conventions

---

### Operation: str_ends_with
**ID**: `str.ends_with`
**Description**: Check if string ends with suffix

**Cross-Language Analysis**:
- **Python**: `s.endswith(suffix)` ← method (lowercase)
- **Rust**: `s.ends_with(suffix)` ← method (underscore)
- **Go**: `strings.HasSuffix(s, suffix)` ← function
- **JavaScript**: `s.endsWith(suffix)` ← method (camelCase)
- **C++**: Manual comparison

**Common Patterns**:
- Similar to `starts_with` naming patterns
- Rust's `ends_with` is clearest

**PW Syntax (RECOMMENDED)**:
```pw
str.ends_with(s, suffix) -> bool
```

**Rationale**:
- Parallel to `str.starts_with`
- Follows Rust convention
- 14 chars: `str.ends_with()`

---

### Operation: str_split
**ID**: `str.split`
**Description**: Split string by delimiter

**Cross-Language Analysis**:
- **Python**: `s.split(delimiter)` ← method (most common)
- **Rust**: `s.split(delimiter).collect()` ← returns iterator
- **Go**: `strings.Split(s, delimiter)` ← function
- **JavaScript**: `s.split(delimiter)` ← method
- **C++**: No built-in (requires manual tokenization)

**Common Patterns**:
- Universal method name: `split`
- Single argument: delimiter
- Return: array/list of strings

**PW Syntax (RECOMMENDED)**:
```pw
str.split(s, delimiter) -> List<str>
```

**Rationale**:
- `split` is universal across all languages
- 10 chars: `str.split()`
- Clear intent
- Standard behavior (split by delimiter)

---

### Operation: str_join
**ID**: `str.join`
**Description**: Join array of strings with separator

**Cross-Language Analysis**:
- **Python**: `separator.join(strings)` ← method on separator (unusual but elegant)
- **Rust**: `strings.join(separator)` ← method on array
- **Go**: `strings.Join(strings, separator)` ← function
- **JavaScript**: `strings.join(separator)` ← method on array
- **C++**: No built-in

**Common Patterns**:
- Most: method on array/list
- Python: method on separator (reversed)
- `join` is universal name

**PW Syntax (RECOMMENDED)**:
```pw
str.join(strings, separator) -> str
```

**Rationale**:
- Follow Rust/JS/Go convention (strings first, separator second)
- 9 chars: `str.join()`
- More intuitive than Python's reversed order
- Consistent parameter order: data first, option second

---

### Operation: str_trim
**ID**: `str.trim`
**Description**: Remove whitespace from both ends

**Cross-Language Analysis**:
- **Python**: `s.strip()` ← different name ("strip")
- **Rust**: `s.trim()` ← method
- **Go**: `strings.TrimSpace(s)` ← function (explicit "space")
- **JavaScript**: `s.trim()` ← method
- **C++**: No built-in

**Common Patterns**:
- Most: `trim()` method
- Python: `strip()` (different terminology)
- `trim` is more universal

**PW Syntax (RECOMMENDED)**:
```pw
str.trim(s) -> str
```

**Rationale**:
- `trim` is more common than Python's `strip`
- Matches Rust, JS, Go
- 9 chars: `str.trim()`
- Clear intent: trim whitespace

---

### Operation: str_to_upper
**ID**: `str.upper`
**Description**: Convert string to uppercase

**Cross-Language Analysis**:
- **Python**: `s.upper()` ← method
- **Rust**: `s.to_uppercase()` ← explicit "to_"
- **Go**: `strings.ToUpper(s)` ← function
- **JavaScript**: `s.toUpperCase()` ← method (camelCase)
- **C++**: `transform(..., ::toupper)` ← manual

**Common Patterns**:
- Split: `upper()` (Python, short) vs `toUpperCase()` (JS, explicit)
- Rust uses `to_uppercase` (conversion prefix)

**PW Syntax (RECOMMENDED)**:
```pw
str.upper(s) -> str
```

**Rationale**:
- `upper` is shortest, clearest
- Matches Python (widely used)
- 10 chars: `str.upper()`
- No need for `to_` prefix (context is clear)

---

### Operation: str_to_lower
**ID**: `str.lower`
**Description**: Convert string to lowercase

**Cross-Language Analysis**:
- **Python**: `s.lower()` ← method
- **Rust**: `s.to_lowercase()` ← explicit "to_"
- **Go**: `strings.ToLower(s)` ← function
- **JavaScript**: `s.toLowerCase()` ← method (camelCase)
- **C++**: `transform(..., ::tolower)` ← manual

**Common Patterns**:
- Parallel to `upper` naming
- Python's `lower()` is shortest

**PW Syntax (RECOMMENDED)**:
```pw
str.lower(s) -> str
```

**Rationale**:
- Parallel to `str.upper`
- 10 chars: `str.lower()`
- Shortest, clearest form

---

### Operation: str_replace
**ID**: `str.replace`
**Description**: Replace all occurrences of old with new

**Cross-Language Analysis**:
- **Python**: `s.replace(old, new)` ← method (replaces all by default)
- **Rust**: `s.replace(old, new)` ← method
- **Go**: `strings.ReplaceAll(s, old, new)` ← explicit "All"
- **JavaScript**: `s.replaceAll(old, new)` ← explicit "All" (newer method)
- **C++**: No built-in

**Common Patterns**:
- Universal name: `replace`
- Python/Rust: implicit "replace all"
- Go/JS: explicit `ReplaceAll` or `replaceAll`

**PW Syntax (RECOMMENDED)**:
```pw
str.replace(s, old, new) -> str
```

**Rationale**:
- `replace` is universal
- 12 chars: `str.replace()`
- Follow Python/Rust: implicit "all" (most common use case)
- If need single replacement, can add `str.replace_first` later

---

### Operation: str_index_of
**ID**: `str.index_of`
**Description**: Find first index of substring (-1 if not found)

**Cross-Language Analysis**:
- **Python**: `s.find(substring)` ← returns -1 if not found
- **Rust**: `s.find(substring)` ← returns Option (requires unwrap)
- **Go**: `strings.Index(s, substring)` ← returns -1 if not found
- **JavaScript**: `s.indexOf(substring)` ← returns -1 if not found
- **C++**: `s.find(substring)` ← returns npos if not found

**Common Patterns**:
- Split: `find` (Python, Rust, C++) vs `indexOf` (JS) vs `Index` (Go)
- Return -1 or special value if not found
- `indexOf` is most explicit

**PW Syntax (RECOMMENDED)**:
```pw
str.index_of(s, substring) -> int
```

**Rationale**:
- `index_of` is clearer than `find` (specific about returning index)
- Matches JS convention (widely understood)
- 13 chars: `str.index_of()`
- Return -1 if not found (universal pattern)

---

### Operation: str_reverse
**ID**: `str.reverse`
**Description**: Reverse string

**Cross-Language Analysis**:
- **Python**: `s[::-1]` ← slice trick (concise but obscure)
- **Rust**: `s.chars().rev().collect()` ← char-aware reversal
- **Go**: Manual rune manipulation
- **JavaScript**: `s.split('').reverse().join('')` ← array conversion
- **C++**: `reverse(s.begin(), s.end())` ← in-place

**Common Patterns**:
- No universal method name
- Most require multi-step process
- `reverse` is clear verb

**PW Syntax (RECOMMENDED)**:
```pw
str.reverse(s) -> str
```

**Rationale**:
- `reverse` is universal verb
- 12 chars: `str.reverse()`
- Clearer than Python's slice trick
- Single operation (not multi-step)

---

### Operation: str_is_empty
**ID**: `str.is_empty`
**Description**: Check if string is empty

**Cross-Language Analysis**:
- **Python**: `len(s) == 0` or `not s` ← comparison or truthiness
- **Rust**: `s.is_empty()` ← dedicated method
- **Go**: `len(s) == 0` ← comparison
- **JavaScript**: `s.length === 0` or `!s` ← comparison or truthiness
- **C++**: `s.empty()` ← method

**Common Patterns**:
- Rust/C++ have dedicated methods
- Python/Go/JS use length comparison
- `is_empty` or `empty` for methods

**PW Syntax (RECOMMENDED)**:
```pw
str.is_empty(s) -> bool
```

**Rationale**:
- `is_empty` follows Rust convention (explicit predicate naming)
- 13 chars: `str.is_empty()`
- More readable than `len(s) == 0`
- Consistent with other boolean predicates

---

## CATEGORY 3: HTTP/NETWORK (8 operations)

### Operation: http_get
**ID**: `http.get`
**Description**: Make HTTP GET request, return body as string

**Cross-Language Analysis**:
- **Python**: `requests.get(url).text` ← requires requests library
- **Rust**: `reqwest::blocking::get(url)?.text()?` ← reqwest is standard
- **Go**: `http.Get(url)` + body read ← stdlib
- **JavaScript**: `(await fetch(url)).text()` ← fetch API
- **C++**: Requires external library (libcurl)

**Common Patterns**:
- Namespace: `http` or module prefix
- Method: `get` is universal
- Rust reqwest is most ergonomic

**PW Syntax (RECOMMENDED)**:
```pw
http.get(url) -> str
```

**Rationale**:
- `http.get` is simplest, clearest
- Matches Rust reqwest, Go stdlib naming
- 9 chars: `http.get()`
- Natural reading: "HTTP get URL"

---

### Operation: http_post
**ID**: `http.post`
**Description**: Make HTTP POST request with body

**Cross-Language Analysis**:
- **Python**: `requests.post(url, data=body).text` ← requests library
- **Rust**: `reqwest::blocking::Client::new().post(url).body(body).send()?.text()?` ← builder pattern
- **Go**: `http.Post(url, "text/plain", body)` ← requires content type
- **JavaScript**: `(await fetch(url, {method: 'POST', body})).text()` ← fetch API
- **C++**: Requires external library

**Common Patterns**:
- Method: `post` is universal
- Arguments: url + body (content type often implicit)

**PW Syntax (RECOMMENDED)**:
```pw
http.post(url, body) -> str
```

**Rationale**:
- Parallel to `http.get`
- 10 chars: `http.post()`
- Implicit content-type (text/plain or auto-detect)
- Matches Python requests simplicity

---

### Operation: http_get_json
**ID**: `http.get_json`
**Description**: Make HTTP GET, parse JSON response

**Cross-Language Analysis**:
- **Python**: `requests.get(url).json()` ← one-liner
- **Rust**: `reqwest::blocking::get(url)?.json()` ← one-liner
- **Go**: Manual: GET + unmarshal
- **JavaScript**: `(await fetch(url)).json()` ← one-liner
- **C++**: Manual: HTTP + JSON parse

**Common Patterns**:
- High-level libraries combine HTTP + JSON
- Method name: `json()` suffix

**PW Syntax (RECOMMENDED)**:
```pw
http.get_json(url) -> Map<str, any>
```

**Rationale**:
- Compound name `get_json` is explicit
- 14 chars: `http.get_json()`
- Common pattern (avoid manual parse)
- Convenience wrapper over `json.parse(http.get(url))`

---

### Operation: http_post_json
**ID**: `http.post_json`
**Description**: POST JSON data, return JSON response

**Cross-Language Analysis**:
- **Python**: `requests.post(url, json=data).json()` ← dual JSON handling
- **Rust**: `reqwest::blocking::Client::new().post(url).json(&data).send()?.json()?` ← builder
- **Go**: Manual: marshal + POST + unmarshal
- **JavaScript**: `(await fetch(url, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data)})).json()` ← verbose
- **C++**: Manual

**Common Patterns**:
- High-level: accept JSON, return JSON
- Python requests is simplest API

**PW Syntax (RECOMMENDED)**:
```pw
http.post_json(url, data) -> Map<str, any>
```

**Rationale**:
- Parallel to `http.get_json`
- 15 chars: `http.post_json()`
- Handles JSON serialization + content-type automatically
- Matches Python requests ergonomics

---

### Operation: http_download_file
**ID**: `http.download`
**Description**: Download file from URL to local path

**Cross-Language Analysis**:
- **Python**: `urllib.request.urlretrieve(url, path)` ← dedicated function
- **Rust**: `fs::write(path, reqwest::blocking::get(url)?.bytes()?)` ← compose HTTP + file
- **Go**: Manual: GET + write to file
- **JavaScript**: `fs.writeFileSync(path, await (await fetch(url)).arrayBuffer())` ← compose
- **C++**: Manual

**Common Patterns**:
- Dedicated function in Python
- Most languages: compose HTTP + file write
- Operation is "download to file"

**PW Syntax (RECOMMENDED)**:
```pw
http.download(url, path) -> void
```

**Rationale**:
- `download` is clearer than `download_file` (context is clear)
- 14 chars: `http.download()`
- High-level convenience (common operation)
- Natural reading: "HTTP download URL to path"

---

### Operation: url_encode
**ID**: `url.encode`
**Description**: URL-encode string (percent encoding)

**Cross-Language Analysis**:
- **Python**: `urllib.parse.quote(s)` ← "quote" is historical term
- **Rust**: `urlencoding::encode(s)` ← dedicated crate
- **Go**: `url.QueryEscape(s)` ← stdlib
- **JavaScript**: `encodeURIComponent(s)` ← verbose name
- **C++**: Manual

**Common Patterns**:
- Names vary: `quote` (Python), `encode` (Rust), `escape` (Go), `encodeURIComponent` (JS)
- `encode` is most intuitive

**PW Syntax (RECOMMENDED)**:
```pw
url.encode(s) -> str
```

**Rationale**:
- `encode` is clearest (what it does, not how)
- Matches Rust convention
- 11 chars: `url.encode()`
- Natural namespace: URL operations

---

### Operation: url_decode
**ID**: `url.decode`
**Description**: Decode URL-encoded string

**Cross-Language Analysis**:
- **Python**: `urllib.parse.unquote(s)` ← "unquote"
- **Rust**: `urlencoding::decode(s)` ← dedicated crate
- **Go**: `url.QueryUnescape(s)` ← stdlib
- **JavaScript**: `decodeURIComponent(s)` ← verbose
- **C++**: Manual

**Common Patterns**:
- Parallel to encode naming
- `decode` is most intuitive

**PW Syntax (RECOMMENDED)**:
```pw
url.decode(s) -> str
```

**Rationale**:
- Parallel to `url.encode`
- 11 chars: `url.decode()`
- Clearest naming

---

### Operation: parse_url
**ID**: `url.parse`
**Description**: Parse URL into components (scheme, host, path, query)

**Cross-Language Analysis**:
- **Python**: `urllib.parse.urlparse(url)` ← returns namedtuple
- **Rust**: `Url::parse(url)?` ← url crate, returns struct
- **Go**: `url.Parse(url)` ← returns struct
- **JavaScript**: `new URL(url)` ← constructor, returns object
- **C++**: External library

**Common Patterns**:
- Function/method name: `parse` is universal
- Returns structured data (tuple/struct/object)

**PW Syntax (RECOMMENDED)**:
```pw
url.parse(url) -> Map<str, str>
```

**Rationale**:
- `parse` is universal
- 10 chars: `url.parse()`
- Return map for easy property access: `{scheme, host, path, query}`
- Matches modern API design

---

## CATEGORY 4: JSON OPERATIONS (4 operations)

### Operation: parse_json
**ID**: `json.parse`
**Description**: Parse JSON string to data structure

**Cross-Language Analysis**:
- **Python**: `json.loads(s)` ← "loads" = "load string" (historical)
- **Rust**: `serde_json::from_str(s)?` ← explicit "from string"
- **Go**: `json.Unmarshal(...)` ← "unmarshal" (different terminology)
- **JavaScript**: `JSON.parse(s)` ← standard, universal
- **C++**: `json::parse(s)` ← nlohmann/json

**Common Patterns**:
- JS/C++: `parse` is standard
- Python: `loads` (historical)
- `parse` is most intuitive

**PW Syntax (RECOMMENDED)**:
```pw
json.parse(s) -> any
```

**Rationale**:
- `parse` matches JS (most widely used)
- 11 chars: `json.parse()`
- Clearer than Python's `loads`
- Universal understanding

---

### Operation: stringify_json
**ID**: `json.stringify`
**Description**: Convert data structure to JSON string

**Cross-Language Analysis**:
- **Python**: `json.dumps(data)` ← "dumps" = "dump string" (historical)
- **Rust**: `serde_json::to_string(&data)?` ← explicit "to string"
- **Go**: `json.Marshal(data)` ← "marshal" (different terminology)
- **JavaScript**: `JSON.stringify(data)` ← standard
- **C++**: `data.dump()` ← nlohmann/json

**Common Patterns**:
- JS: `stringify` (most widely used)
- Python: `dumps` (historical)
- `stringify` is most explicit

**PW Syntax (RECOMMENDED)**:
```pw
json.stringify(data) -> str
```

**Rationale**:
- `stringify` matches JS convention (widely adopted)
- 15 chars: `json.stringify()`
- More explicit than `dumps` or `dump`
- Parallel to `json.parse`

---

### Operation: stringify_json_pretty
**ID**: `json.stringify_pretty`
**Description**: Convert to pretty-printed JSON

**Cross-Language Analysis**:
- **Python**: `json.dumps(data, indent=2)` ← parameter-based
- **Rust**: `serde_json::to_string_pretty(&data)?` ← dedicated function
- **Go**: `json.MarshalIndent(data, "", "  ")` ← dedicated function
- **JavaScript**: `JSON.stringify(data, null, 2)` ← parameter-based
- **C++**: `data.dump(2)` ← parameter-based

**Common Patterns**:
- Two approaches: parameter (Python, JS) or dedicated function (Rust, Go)
- Rust's `to_string_pretty` is most explicit

**PW Syntax (RECOMMENDED)**:
```pw
json.stringify_pretty(data) -> str
```

**Rationale**:
- Dedicated function is more discoverable than parameter
- Follows Rust convention
- 22 chars: `json.stringify_pretty()`
- Explicit name (no magic parameters)

---

### Operation: json_validate
**ID**: `json.validate`
**Description**: Check if string is valid JSON

**Cross-Language Analysis**:
- **Python**: Try/catch `json.loads(s)`
- **Rust**: `serde_json::from_str::<Value>(s).is_ok()` ← result checking
- **Go**: Try unmarshal, check error
- **JavaScript**: Try/catch `JSON.parse(s)`
- **C++**: Try/catch parse

**Common Patterns**:
- No universal dedicated function
- All use try/catch or error checking
- Rust's `is_ok()` is cleanest API

**PW Syntax (RECOMMENDED)**:
```pw
json.validate(s) -> bool
```

**Rationale**:
- Dedicated function is clearer than try/catch in user code
- 14 chars: `json.validate()`
- Common use case deserves dedicated API
- Returns boolean (simple interface)

---

## CATEGORY 5: MATH OPERATIONS (10 operations)

### Operation: math_abs
**ID**: `abs` (built-in) | `math.abs`
**Description**: Absolute value

**Cross-Language Analysis**:
- **Python**: `abs(n)` ← built-in function
- **Rust**: `n.abs()` ← method on numeric types
- **Go**: `math.Abs(n)` ← math package
- **JavaScript**: `Math.abs(n)` ← Math object
- **C++**: `abs(n)` or `fabs(n)` ← built-in functions

**Common Patterns**:
- Split: built-in function (Python, C++) vs Math namespace (JS, Go) vs method (Rust)
- `abs` is universal name

**PW Syntax (RECOMMENDED)**:
```pw
abs(n) -> number
```

**Rationale**:
- Built-in function (matches Python, C++)
- 3 chars: `abs()`
- Universal name
- Common enough to be built-in (not namespaced)

---

### Operation: math_min
**ID**: `min` (built-in)
**Description**: Minimum of two numbers

**Cross-Language Analysis**:
- **Python**: `min(a, b)` ← built-in (variadic)
- **Rust**: `a.min(b)` ← method
- **Go**: `math.Min(a, b)` ← math package
- **JavaScript**: `Math.min(a, b)` ← Math object (variadic)
- **C++**: `min(a, b)` or `std::min(a, b)` ← built-in

**Common Patterns**:
- Universal name: `min`
- Python/C++ have built-ins

**PW Syntax (RECOMMENDED)**:
```pw
min(a, b) -> number
```

**Rationale**:
- Built-in function (matches Python)
- 3 chars: `min()`
- Universal, fundamental operation
- Can be variadic: `min(a, b, c, ...)`

---

### Operation: math_max
**ID**: `max` (built-in)
**Description**: Maximum of two numbers

**Cross-Language Analysis**:
- **Python**: `max(a, b)` ← built-in (variadic)
- **Rust**: `a.max(b)` ← method
- **Go**: `math.Max(a, b)` ← math package
- **JavaScript**: `Math.max(a, b)` ← Math object (variadic)
- **C++**: `max(a, b)` or `std::max(a, b)` ← built-in

**Common Patterns**:
- Universal name: `max`
- Python/C++ have built-ins

**PW Syntax (RECOMMENDED)**:
```pw
max(a, b) -> number
```

**Rationale**:
- Built-in function (matches Python)
- Parallel to `min`
- 3 chars: `max()`
- Can be variadic

---

### Operation: math_pow
**ID**: `**` operator | `pow` (built-in)
**Description**: Raise base to exponent

**Cross-Language Analysis**:
- **Python**: `base ** exp` ← operator (also `pow(base, exp)`)
- **Rust**: `base.powf(exp)` ← method (for floats)
- **Go**: `math.Pow(base, exp)` ← function
- **JavaScript**: `Math.pow(base, exp)` or `base ** exp` ← function + operator
- **C++**: `pow(base, exp)` ← function

**Common Patterns**:
- Python/JS support `**` operator (most concise)
- Others: `pow` function

**PW Syntax (RECOMMENDED)**:
```pw
base ** exp  // operator syntax (primary)
pow(base, exp)  // function syntax (alternative)
```

**Rationale**:
- `**` operator matches Python/JS (widely adopted)
- 2 chars: `**`
- Also provide `pow()` for discoverability
- Operator is more natural for math expressions

---

### Operation: math_sqrt
**ID**: `sqrt` (built-in)
**Description**: Square root

**Cross-Language Analysis**:
- **Python**: `math.sqrt(n)` or `n ** 0.5` ← math module or operator
- **Rust**: `n.sqrt()` ← method
- **Go**: `math.Sqrt(n)` ← math package
- **JavaScript**: `Math.sqrt(n)` ← Math object
- **C++**: `sqrt(n)` ← built-in function

**Common Patterns**:
- Universal name: `sqrt`
- C++ has built-in, others need namespace/method

**PW Syntax (RECOMMENDED)**:
```pw
sqrt(n) -> float
```

**Rationale**:
- Built-in function (matches C++)
- 4 chars: `sqrt()`
- Common enough for built-in status
- Universal abbreviation

---

### Operation: math_floor
**ID**: `floor` (built-in)
**Description**: Round down to integer

**Cross-Language Analysis**:
- **Python**: `math.floor(n)` ← math module
- **Rust**: `n.floor() as i32` ← method + cast
- **Go**: `math.Floor(n)` ← math package
- **JavaScript**: `Math.floor(n)` ← Math object
- **C++**: `floor(n)` ← built-in function

**Common Patterns**:
- Universal name: `floor`
- C++ has built-in

**PW Syntax (RECOMMENDED)**:
```pw
floor(n) -> int
```

**Rationale**:
- Built-in function
- 5 chars: `floor()`
- Common operation
- Returns integer (unlike some languages that return float)

---

### Operation: math_ceil
**ID**: `ceil` (built-in)
**Description**: Round up to integer

**Cross-Language Analysis**:
- **Python**: `math.ceil(n)` ← math module
- **Rust**: `n.ceil() as i32` ← method + cast
- **Go**: `math.Ceil(n)` ← math package
- **JavaScript**: `Math.ceil(n)` ← Math object
- **C++**: `ceil(n)` ← built-in function

**Common Patterns**:
- Universal name: `ceil`
- Parallel to `floor`

**PW Syntax (RECOMMENDED)**:
```pw
ceil(n) -> int
```

**Rationale**:
- Built-in function
- Parallel to `floor`
- 4 chars: `ceil()`

---

### Operation: math_round
**ID**: `round` (built-in)
**Description**: Round to nearest integer

**Cross-Language Analysis**:
- **Python**: `round(n)` ← built-in
- **Rust**: `n.round() as i32` ← method + cast
- **Go**: `math.Round(n)` ← math package
- **JavaScript**: `Math.round(n)` ← Math object
- **C++**: `round(n)` ← built-in function

**Common Patterns**:
- Universal name: `round`
- Python/C++ have built-ins

**PW Syntax (RECOMMENDED)**:
```pw
round(n) -> int
```

**Rationale**:
- Built-in function (matches Python)
- 5 chars: `round()`
- Common operation

---

### Operation: math_random
**ID**: `random` (built-in)
**Description**: Random float between 0 and 1

**Cross-Language Analysis**:
- **Python**: `random.random()` ← random module
- **Rust**: `rand::random::<f64>()` ← rand crate
- **Go**: `rand.Float64()` ← rand package
- **JavaScript**: `Math.random()` ← Math object
- **C++**: `(double)rand() / RAND_MAX` ← manual

**Common Patterns**:
- Universal name: `random`
- Most: namespace/module prefix

**PW Syntax (RECOMMENDED)**:
```pw
random() -> float
```

**Rationale**:
- Built-in function (simple API)
- 6 chars: `random()`
- Common operation
- Returns float in [0, 1)

---

### Operation: math_random_int
**ID**: `random_int` (built-in)
**Description**: Random integer between min and max (inclusive)

**Cross-Language Analysis**:
- **Python**: `random.randint(min, max)` ← inclusive range
- **Rust**: `rand::thread_rng().gen_range(min..=max)` ← inclusive range
- **Go**: `rand.Intn(max-min+1) + min` ← manual calculation
- **JavaScript**: `Math.floor(Math.random() * (max - min + 1)) + min` ← manual
- **C++**: `rand() % (max - min + 1) + min` ← manual

**Common Patterns**:
- Python has dedicated `randint` function
- Others require manual calculation
- Inclusive range is most intuitive

**PW Syntax (RECOMMENDED)**:
```pw
random_int(min, max) -> int
```

**Rationale**:
- `random_int` is explicit
- 10 chars: `random_int()`
- Inclusive range (matches user expectations)
- Convenience over manual calculation

---

## CATEGORY 6: TIME/DATE (8 operations)

### Operation: time_now
**ID**: `time.now`
**Description**: Current Unix timestamp (seconds since epoch)

**Cross-Language Analysis**:
- **Python**: `int(time.time())` ← time module
- **Rust**: `SystemTime::now().duration_since(UNIX_EPOCH)?.as_secs()` ← verbose
- **Go**: `time.Now().Unix()` ← time package
- **JavaScript**: `Math.floor(Date.now() / 1000)` ← Date.now() returns ms
- **C++**: `chrono::system_clock::now()...` ← verbose

**Common Patterns**:
- Most have `now()` function/method
- Return: seconds since epoch (Unix timestamp)

**PW Syntax (RECOMMENDED)**:
```pw
time.now() -> int
```

**Rationale**:
- `time.now()` is simplest, clearest
- 9 chars: `time.now()`
- Matches Go's API (cleanest)
- Natural namespace: time operations

---

### Operation: time_now_ms
**ID**: `time.now_ms`
**Description**: Current timestamp in milliseconds

**Cross-Language Analysis**:
- **Python**: `int(time.time() * 1000)` ← manual calculation
- **Rust**: `SystemTime::now().duration_since(UNIX_EPOCH)?.as_millis()` ← explicit method
- **Go**: `time.Now().UnixMilli()` ← dedicated method
- **JavaScript**: `Date.now()` ← returns milliseconds by default
- **C++**: Verbose chrono calculation

**Common Patterns**:
- JS: `Date.now()` returns ms (most common)
- Go: `UnixMilli()` dedicated method
- Others: calculation from seconds

**PW Syntax (RECOMMENDED)**:
```pw
time.now_ms() -> int
```

**Rationale**:
- Parallel to `time.now()`
- 12 chars: `time.now_ms()`
- `_ms` suffix is clear (milliseconds)
- Matches Go naming convention

---

### Operation: sleep
**ID**: `sleep` (built-in)
**Description**: Sleep for N seconds

**Cross-Language Analysis**:
- **Python**: `time.sleep(seconds)` ← time module
- **Rust**: `thread::sleep(Duration::from_secs(seconds))` ← explicit duration
- **Go**: `time.Sleep(time.Duration(seconds) * time.Second)` ← explicit duration
- **JavaScript**: `await new Promise(resolve => setTimeout(resolve, seconds * 1000))` ← verbose
- **C++**: `this_thread::sleep_for(chrono::seconds(seconds))` ← verbose

**Common Patterns**:
- Universal name: `sleep`
- Most: namespace prefix
- Python's API is simplest

**PW Syntax (RECOMMENDED)**:
```pw
sleep(seconds) -> void
```

**Rationale**:
- Built-in function (common operation)
- 5 chars: `sleep()`
- Matches Python (simplest API)
- Seconds parameter (most intuitive unit)

---

### Operation: sleep_ms
**ID**: `sleep_ms` (built-in)
**Description**: Sleep for N milliseconds

**Cross-Language Analysis**:
- **Python**: `time.sleep(milliseconds / 1000)` ← calculation
- **Rust**: `thread::sleep(Duration::from_millis(milliseconds))` ← explicit
- **Go**: `time.Sleep(time.Duration(milliseconds) * time.Millisecond)` ← explicit
- **JavaScript**: `await new Promise(resolve => setTimeout(resolve, milliseconds))` ← native unit
- **C++**: `this_thread::sleep_for(chrono::milliseconds(milliseconds))` ← explicit

**Common Patterns**:
- Dedicated millisecond functions in Rust, Go
- JS uses milliseconds natively
- Parallel to `sleep`

**PW Syntax (RECOMMENDED)**:
```pw
sleep_ms(milliseconds) -> void
```

**Rationale**:
- Parallel to `sleep`
- 8 chars: `sleep_ms()`
- `_ms` suffix is clear
- Common need (avoid float math)

---

### Operation: format_timestamp
**ID**: `time.format`
**Description**: Format Unix timestamp to string

**Cross-Language Analysis**:
- **Python**: `datetime.fromtimestamp(timestamp).strftime(format)` ← datetime module
- **Rust**: Requires chrono crate (not stdlib)
- **Go**: `time.Unix(timestamp, 0).Format(format)` ← time package
- **JavaScript**: `new Date(timestamp * 1000).toISOString()` ← Date object (format handling varies)
- **C++**: Complex (no stdlib)

**Common Patterns**:
- Python: `strftime` (C tradition)
- Go: `Format` with layout string
- Most: convert timestamp → date object → format

**PW Syntax (RECOMMENDED)**:
```pw
time.format(timestamp, format) -> str
```

**Rationale**:
- `format` is clearer than `strftime`
- 12 chars: `time.format()`
- Two arguments: timestamp, format string
- High-level abstraction (hide date object conversion)

---

### Operation: parse_timestamp
**ID**: `time.parse`
**Description**: Parse date string to Unix timestamp

**Cross-Language Analysis**:
- **Python**: `int(datetime.strptime(date_string, format).timestamp())` ← strptime
- **Rust**: Requires chrono crate
- **Go**: `t, _ := time.Parse(format, date_string); t.Unix()` ← time package
- **JavaScript**: `Math.floor(new Date(date_string).getTime() / 1000)` ← Date constructor
- **C++**: Complex

**Common Patterns**:
- Python: `strptime` (C tradition - "parse time")
- Go: `Parse` (clearer)
- Operation: string + format → timestamp

**PW Syntax (RECOMMENDED)**:
```pw
time.parse(date_string, format) -> int
```

**Rationale**:
- `parse` is clearer than `strptime`
- 11 chars: `time.parse()`
- Parallel to `time.format` (inverse operation)
- Two arguments: date string, format string

---

### Operation: date_now_iso
**ID**: `time.now_iso`
**Description**: Current date/time in ISO 8601 format

**Cross-Language Analysis**:
- **Python**: `datetime.now().isoformat()` ← datetime method
- **Rust**: `Utc::now().to_rfc3339()` ← chrono (RFC 3339 is ISO 8601 profile)
- **Go**: `time.Now().Format(time.RFC3339)` ← RFC 3339 format
- **JavaScript**: `new Date().toISOString()` ← Date method
- **C++**: Requires library

**Common Patterns**:
- Most: method on date/time object
- ISO 8601 / RFC 3339 (same for practical purposes)
- `toISOString` (JS) or `isoformat` (Python)

**PW Syntax (RECOMMENDED)**:
```pw
time.now_iso() -> str
```

**Rationale**:
- Compound name combines `now` + `iso` format
- 13 chars: `time.now_iso()`
- Convenience function (common use case)
- ISO 8601 is universal standard

---

### Operation: date_add_days
**ID**: `time.add_days`
**Description**: Add days to timestamp

**Cross-Language Analysis**:
- **Python**: `timestamp + (days * 86400)` ← simple math (86400 = seconds per day)
- **Rust**: Manual calculation or chrono
- **Go**: `time.Unix(timestamp, 0).AddDate(0, 0, days).Unix()` ← AddDate method
- **JavaScript**: `timestamp + (days * 86400)` ← simple math
- **C++**: Manual calculation

**Common Patterns**:
- Simple: manual math (86400 seconds per day)
- Go: `AddDate` method (more complex but handles edge cases)
- Most: simple addition

**PW Syntax (RECOMMENDED)**:
```pw
time.add_days(timestamp, days) -> int
```

**Rationale**:
- `add_days` is explicit operation
- 14 chars: `time.add_days()`
- Abstracts calculation (86400 * days)
- Handles edge cases (DST, leap seconds) internally
- Could extend to `add_hours`, `add_minutes`, etc.

---

## CATEGORY 7: PROCESS/SYSTEM (6 operations)

### Operation: run_command
**ID**: `process.run`
**Description**: Execute shell command, return output

**Cross-Language Analysis**:
- **Python**: `subprocess.check_output(cmd, shell=True).decode()` ← subprocess module
- **Rust**: `String::from_utf8(Command::new("sh").arg("-c").arg(cmd).output()?.stdout)?` ← Command API
- **Go**: `out, _ := exec.Command("sh", "-c", cmd).Output(); string(out)` ← exec package
- **JavaScript**: `require('child_process').execSync(cmd).toString()` ← child_process module
- **C++**: `popen(cmd)` ← C API

**Common Patterns**:
- Most: shell execution via subprocess/exec
- Return: stdout as string
- Python: `subprocess.check_output` is standard

**PW Syntax (RECOMMENDED)**:
```pw
process.run(cmd) -> str
```

**Rationale**:
- `run` is simple, clear verb
- 12 chars: `process.run()`
- Returns stdout (most common use case)
- Namespace: `process` for process operations

---

### Operation: get_env
**ID**: `env.get`
**Description**: Get environment variable

**Cross-Language Analysis**:
- **Python**: `os.environ.get(key, "")` ← dict access
- **Rust**: `env::var(key).unwrap_or_default()` ← env module
- **Go**: `os.Getenv(key)` ← returns empty string if not found
- **JavaScript**: `process.env[key] || ""` ← object access
- **C++**: `getenv(key.c_str())` ← C API

**Common Patterns**:
- Universal: `env` namespace
- Method: `get` or `var`
- Return: empty string if not found (not error)

**PW Syntax (RECOMMENDED)**:
```pw
env.get(key) -> str
```

**Rationale**:
- `get` is standard for optional retrieval
- 8 chars: `env.get()`
- Returns empty string if not found (safe default)
- Short namespace: `env`

---

### Operation: set_env
**ID**: `env.set`
**Description**: Set environment variable

**Cross-Language Analysis**:
- **Python**: `os.environ[key] = value` ← dict assignment
- **Rust**: `env::set_var(key, value)` ← env module
- **Go**: `os.Setenv(key, value)` ← function
- **JavaScript**: `process.env[key] = value` ← object assignment
- **C++**: `setenv(key, value, 1)` ← C API

**Common Patterns**:
- Parallel to `get_env`
- `set` or `setenv`

**PW Syntax (RECOMMENDED)**:
```pw
env.set(key, value) -> void
```

**Rationale**:
- `set` is standard setter verb
- 8 chars: `env.set()`
- Parallel to `env.get`

---

### Operation: exit_program
**ID**: `exit` (built-in)
**Description**: Exit program with code

**Cross-Language Analysis**:
- **Python**: `sys.exit(code)` ← sys module
- **Rust**: `std::process::exit(code)` ← process module
- **Go**: `os.Exit(code)` ← os package
- **JavaScript**: `process.exit(code)` ← process object
- **C++**: `exit(code)` ← built-in

**Common Patterns**:
- Universal name: `exit`
- C++ has built-in

**PW Syntax (RECOMMENDED)**:
```pw
exit(code) -> void
```

**Rationale**:
- Built-in function (matches C++)
- 4 chars: `exit()`
- Universal, fundamental operation
- No namespace needed (universally understood)

---

### Operation: get_cwd
**ID**: `process.cwd`
**Description**: Get current working directory

**Cross-Language Analysis**:
- **Python**: `os.getcwd()` ← os module
- **Rust**: `env::current_dir()?.to_str()?` ← env module
- **Go**: `os.Getwd()` ← "get working directory"
- **JavaScript**: `process.cwd()` ← process object (most concise)
- **C++**: `filesystem::current_path()` ← C++17

**Common Patterns**:
- Split: `getcwd` (Python, Go) vs `cwd` (JS) vs `current_dir` (Rust)
- `cwd` is most concise (universally understood abbreviation)

**PW Syntax (RECOMMENDED)**:
```pw
process.cwd() -> str
```

**Rationale**:
- `cwd` is universal abbreviation (current working directory)
- 12 chars: `process.cwd()`
- Matches JS (simplest API)
- No verb needed (`get` is implicit)

---

### Operation: change_dir
**ID**: `process.chdir`
**Description**: Change working directory

**Cross-Language Analysis**:
- **Python**: `os.chdir(path)` ← os module
- **Rust**: `env::set_current_dir(path)?` ← env module
- **Go**: `os.Chdir(path)` ← os package
- **JavaScript**: `process.chdir(path)` ← process object
- **C++**: `filesystem::current_path(path)` ← C++17

**Common Patterns**:
- Universal: `chdir` (Unix tradition)
- Most: namespace prefix

**PW Syntax (RECOMMENDED)**:
```pw
process.chdir(path) -> void
```

**Rationale**:
- `chdir` is universal Unix term
- 14 chars: `process.chdir()`
- Parallel to `process.cwd`
- Matches Python, Go, JS naming

---

## CATEGORY 8: ARRAY OPERATIONS (10 operations)

### Operation: array_length
**ID**: `len` (built-in) | `arr.len()`
**Description**: Get array length

**Cross-Language Analysis**:
- **Python**: `len(arr)` ← built-in function
- **Rust**: `arr.len()` ← method
- **Go**: `len(arr)` ← built-in function
- **JavaScript**: `arr.length` ← property
- **C++**: `arr.size()` ← method

**Common Patterns**:
- Python/Go: built-in `len()` function
- Others: method/property
- `len` vs `length` vs `size`

**PW Syntax (RECOMMENDED)**:
```pw
len(arr) -> int  // built-in (works for strings, arrays, maps, etc.)
```

**Rationale**:
- Built-in `len()` is universal (works on all collections)
- Matches Python/Go (simplest API)
- 3 chars: `len()`
- Single function for all collections (arrays, strings, maps, sets)

---

### Operation: array_push
**ID**: `arr.push`
**Description**: Add item to end of array

**Cross-Language Analysis**:
- **Python**: `arr.append(item)` ← "append" terminology
- **Rust**: `arr.push(item)` ← "push" terminology
- **Go**: `arr = append(arr, item)` ← "append" (returns new slice)
- **JavaScript**: `arr.push(item)` ← "push" terminology
- **C++**: `arr.push_back(item)` ← "push" terminology

**Common Patterns**:
- Split: `append` (Python, Go) vs `push` (Rust, JS, C++)
- `push` is more common in modern languages

**PW Syntax (RECOMMENDED)**:
```pw
arr.push(item) -> void  // method syntax
```

**Rationale**:
- `push` is more common (Rust, JS, C++)
- Method syntax (operates on array in-place)
- Stack terminology (universally understood)
- 4 chars: `push()`

---

### Operation: array_pop
**ID**: `arr.pop`
**Description**: Remove and return last item

**Cross-Language Analysis**:
- **Python**: `arr.pop()` ← returns item
- **Rust**: `arr.pop()` ← returns Option<T>
- **Go**: Manual: `item := arr[len(arr)-1]; arr = arr[:len(arr)-1]`
- **JavaScript**: `arr.pop()` ← returns item
- **C++**: `arr.pop_back()` ← returns void (must use `back()` first)

**Common Patterns**:
- Universal: `pop` (stack terminology)
- Most return the item (except C++)

**PW Syntax (RECOMMENDED)**:
```pw
arr.pop() -> T  // method syntax, returns last item
```

**Rationale**:
- `pop` is universal (Python, Rust, JS)
- Method syntax
- Returns item (most common behavior)
- Parallel to `arr.push`

---

### Operation: array_get
**ID**: `arr[index]` operator
**Description**: Get item at index

**Cross-Language Analysis**:
- **Python**: `arr[index]` ← operator
- **Rust**: `arr[index]` ← operator
- **Go**: `arr[index]` ← operator
- **JavaScript**: `arr[index]` ← operator
- **C++**: `arr[index]` ← operator

**Common Patterns**:
- Universal: `[]` indexing operator

**PW Syntax (RECOMMENDED)**:
```pw
arr[index]  // operator syntax
```

**Rationale**:
- Universal `[]` operator across all languages
- No function needed (built-in syntax)

---

### Operation: array_set
**ID**: `arr[index] = value` operator
**Description**: Set item at index

**Cross-Language Analysis**:
- **Python**: `arr[index] = value` ← operator
- **Rust**: `arr[index] = value` ← operator
- **Go**: `arr[index] = value` ← operator
- **JavaScript**: `arr[index] = value` ← operator
- **C++**: `arr[index] = value` ← operator

**Common Patterns**:
- Universal: `[]=` assignment operator

**PW Syntax (RECOMMENDED)**:
```pw
arr[index] = value  // operator syntax
```

**Rationale**:
- Universal assignment operator
- No function needed (built-in syntax)

---

### Operation: array_contains
**ID**: `item in arr` operator
**Description**: Check if array contains item

**Cross-Language Analysis**:
- **Python**: `item in arr` ← operator (most readable)
- **Rust**: `arr.contains(&item)` ← method
- **Go**: Requires manual loop (no built-in)
- **JavaScript**: `arr.includes(item)` ← method
- **C++**: `find(arr.begin(), arr.end(), item) != arr.end()` ← algorithm

**Common Patterns**:
- Python: `in` operator (clearest)
- Rust/JS: method (`.contains()` or `.includes()`)

**PW Syntax (RECOMMENDED)**:
```pw
item in arr  // operator syntax (primary)
arr.contains(item)  // method syntax (alternative)
```

**Rationale**:
- Python's `in` is most natural
- Also provide method for consistency
- Support both styles

---

### Operation: array_index_of
**ID**: `arr.index_of`
**Description**: Find index of item (-1 if not found)

**Cross-Language Analysis**:
- **Python**: `arr.index(item)` ← raises exception if not found (different!)
- **Rust**: `arr.iter().position(|x| x == &item)` ← returns Option
- **Go**: Requires manual loop
- **JavaScript**: `arr.indexOf(item)` ← returns -1 if not found
- **C++**: `find(arr.begin(), arr.end(), item) - arr.begin()` ← returns index

**Common Patterns**:
- JS: `indexOf` returns -1 (safest)
- Python: `index` throws (different semantics)
- `indexOf` is more explicit

**PW Syntax (RECOMMENDED)**:
```pw
arr.index_of(item) -> int  // returns -1 if not found
```

**Rationale**:
- `index_of` is explicit (returns index)
- Matches JS convention
- Returns -1 if not found (safe, no exceptions)
- 8 chars: `index_of()`

---

### Operation: array_slice
**ID**: `arr[start:end]` operator
**Description**: Extract subarray from start to end

**Cross-Language Analysis**:
- **Python**: `arr[start:end]` ← slice operator
- **Rust**: `&arr[start..end]` ← slice operator (returns reference)
- **Go**: `arr[start:end]` ← slice operator
- **JavaScript**: `arr.slice(start, end)` ← method
- **C++**: Manual: `vector<T>(arr.begin()+start, arr.begin()+end)`

**Common Patterns**:
- Python/Go: slice notation `[start:end]`
- Rust: slice notation `[start..end]`
- JS: method `.slice()`

**PW Syntax (RECOMMENDED)**:
```pw
arr[start:end]  // slice operator
```

**Rationale**:
- Slice operator is concise (matches string slicing)
- Consistent with `str[start:end]`
- Python/Go syntax (widely understood)

---

### Operation: array_reverse
**ID**: `arr.reverse`
**Description**: Reverse array

**Cross-Language Analysis**:
- **Python**: `arr[::-1]` or `list(reversed(arr))` ← slice trick or function
- **Rust**: `arr.iter().rev().collect()` ← iterator
- **Go**: Requires manual loop (no built-in)
- **JavaScript**: `[...arr].reverse()` ← method (creates copy)
- **C++**: `reverse(arr.begin(), arr.end())` ← algorithm (in-place)

**Common Patterns**:
- Most have dedicated method/function
- Some in-place (C++), some return new (JS)

**PW Syntax (RECOMMENDED)**:
```pw
arr.reverse() -> List<T>  // returns new reversed array
```

**Rationale**:
- `reverse` is universal verb
- Returns new array (immutable/functional style)
- 7 chars: `reverse()`
- Clear intent

---

### Operation: array_sort
**ID**: `arr.sort`
**Description**: Sort array (ascending)

**Cross-Language Analysis**:
- **Python**: `sorted(arr)` ← returns new list (or `arr.sort()` in-place)
- **Rust**: `arr.sort()` ← in-place (or `.sorted()` on iterator)
- **Go**: `sort.Ints(arr)` ← in-place
- **JavaScript**: `[...arr].sort((a,b) => a-b)` ← method (requires comparator for numbers)
- **C++**: `sort(arr.begin(), arr.end())` ← algorithm (in-place)

**Common Patterns**:
- Universal verb: `sort`
- Split: in-place vs returns new
- Most require explicit ascending order for numbers

**PW Syntax (RECOMMENDED)**:
```pw
arr.sort() -> List<T>  // returns new sorted array (ascending)
```

**Rationale**:
- `sort` is universal
- Returns new array (functional style)
- 4 chars: `sort()`
- Ascending order by default (most common)

---

## CATEGORY 9: ENCODING/DECODING (6 operations)

### Operation: base64_encode
**ID**: `base64.encode`
**Description**: Encode bytes/string to base64

**Cross-Language Analysis**:
- **Python**: `base64.b64encode(data.encode()).decode()` ← base64 module
- **Rust**: `base64::encode(data)` ← base64 crate
- **Go**: `base64.StdEncoding.EncodeToString([]byte(data))` ← encoding/base64
- **JavaScript**: `Buffer.from(data).toString('base64')` ← Buffer API
- **C++**: Requires external library

**Common Patterns**:
- Namespace: `base64`
- Method: `encode`
- Rust has simplest API

**PW Syntax (RECOMMENDED)**:
```pw
base64.encode(data) -> str
```

**Rationale**:
- Matches Rust's simple API
- 14 chars: `base64.encode()`
- Clear namespace + verb
- Handles string/bytes automatically

---

### Operation: base64_decode
**ID**: `base64.decode`
**Description**: Decode base64 to string

**Cross-Language Analysis**:
- **Python**: `base64.b64decode(encoded).decode()` ← base64 module
- **Rust**: `String::from_utf8(base64::decode(encoded)?)` ← base64 crate
- **Go**: `decoded, _ := base64.StdEncoding.DecodeString(encoded); string(decoded)` ← base64 package
- **JavaScript**: `Buffer.from(encoded, 'base64').toString()` ← Buffer API
- **C++**: Requires library

**Common Patterns**:
- Parallel to `encode`
- Method: `decode`

**PW Syntax (RECOMMENDED)**:
```pw
base64.decode(encoded) -> str
```

**Rationale**:
- Parallel to `base64.encode`
- 14 chars: `base64.decode()`
- Returns string (most common use case)

---

### Operation: hex_encode
**ID**: `hex.encode`
**Description**: Encode bytes to hex string

**Cross-Language Analysis**:
- **Python**: `data.encode().hex()` ← bytes method
- **Rust**: `hex::encode(data)` ← hex crate
- **Go**: `hex.EncodeToString([]byte(data))` ← encoding/hex
- **JavaScript**: `Buffer.from(data).toString('hex')` ← Buffer API
- **C++**: Manual implementation

**Common Patterns**:
- Namespace: `hex`
- Method: `encode`
- Similar to base64 patterns

**PW Syntax (RECOMMENDED)**:
```pw
hex.encode(data) -> str
```

**Rationale**:
- Parallel to `base64.encode`
- 11 chars: `hex.encode()`
- Consistent encoding namespace pattern

---

### Operation: hex_decode
**ID**: `hex.decode`
**Description**: Decode hex string to bytes

**Cross-Language Analysis**:
- **Python**: `bytes.fromhex(encoded).decode()` ← bytes class method
- **Rust**: `String::from_utf8(hex::decode(encoded)?)` ← hex crate
- **Go**: `decoded, _ := hex.DecodeString(encoded); string(decoded)` ← hex package
- **JavaScript**: `Buffer.from(encoded, 'hex').toString()` ← Buffer API
- **C++**: Manual implementation

**Common Patterns**:
- Parallel to `hex_encode`

**PW Syntax (RECOMMENDED)**:
```pw
hex.decode(encoded) -> str
```

**Rationale**:
- Parallel to `hex.encode`
- 11 chars: `hex.decode()`

---

### Operation: md5_hash
**ID**: `hash.md5`
**Description**: Compute MD5 hash

**Cross-Language Analysis**:
- **Python**: `hashlib.md5(data.encode()).hexdigest()` ← hashlib module
- **Rust**: `format!("{:x}", md5::compute(data))` ← md5 crate
- **Go**: `fmt.Sprintf("%x", md5.Sum([]byte(data)))` ← crypto/md5
- **JavaScript**: `require('crypto').createHash('md5').update(data).digest('hex')` ← crypto module
- **C++**: Requires OpenSSL or similar

**Common Patterns**:
- Namespace: `hash` or `crypto`
- Algorithm as method/parameter: `md5`
- Return: hex string

**PW Syntax (RECOMMENDED)**:
```pw
hash.md5(data) -> str
```

**Rationale**:
- `hash` namespace groups all hash algorithms
- `md5` is algorithm name
- 9 chars: `hash.md5()`
- Returns hex string (standard format)

---

### Operation: sha256_hash
**ID**: `hash.sha256`
**Description**: Compute SHA-256 hash

**Cross-Language Analysis**:
- **Python**: `hashlib.sha256(data.encode()).hexdigest()` ← hashlib module
- **Rust**: `format!("{:x}", sha2::Sha256::digest(data))` ← sha2 crate
- **Go**: `fmt.Sprintf("%x", sha256.Sum256([]byte(data)))` ← crypto/sha256
- **JavaScript**: `require('crypto').createHash('sha256').update(data).digest('hex')` ← crypto module
- **C++**: Requires OpenSSL

**Common Patterns**:
- Parallel to MD5
- Algorithm name: `sha256`

**PW Syntax (RECOMMENDED)**:
```pw
hash.sha256(data) -> str
```

**Rationale**:
- Parallel to `hash.md5`
- 12 chars: `hash.sha256()`
- Algorithm name matches universal convention

---

## CATEGORY 10: TYPE CONVERSIONS (8 operations)

### Operation: to_string
**ID**: `str` (built-in) | `to_string`
**Description**: Convert any value to string

**Cross-Language Analysis**:
- **Python**: `str(value)` ← built-in function
- **Rust**: `value.to_string()` or `format!("{}", value)` ← trait method
- **Go**: `fmt.Sprint(value)` or `strconv.Itoa(value)` ← functions
- **JavaScript**: `String(value)` or `value.toString()` ← function/method
- **C++**: `to_string(value)` or `std::to_string(value)` ← function

**Common Patterns**:
- Python: built-in `str()`
- C++: function `to_string()`
- Rust: method `.to_string()`
- `str` or `to_string` are standard

**PW Syntax (RECOMMENDED)**:
```pw
str(value) -> str  // built-in function
```

**Rationale**:
- Built-in `str()` matches Python (simplest)
- 3 chars: `str()`
- Universal conversion function
- Consistent with type name

---

### Operation: to_int
**ID**: `int` (built-in)
**Description**: Convert string to integer

**Cross-Language Analysis**:
- **Python**: `int(s)` ← built-in function
- **Rust**: `s.parse::<i32>()?` ← parse method with type annotation
- **Go**: `strconv.Atoi(s)` ← "ASCII to integer"
- **JavaScript**: `parseInt(s, 10)` or `Number(s)` ← function
- **C++**: `stoi(s)` or `atoi(s)` ← functions

**Common Patterns**:
- Python: built-in `int()`
- Others: parse/convert functions
- `int` is universal type name

**PW Syntax (RECOMMENDED)**:
```pw
int(s) -> int  // built-in function
```

**Rationale**:
- Built-in `int()` matches Python
- 3 chars: `int()`
- Type name as conversion function (clear intent)

---

### Operation: to_float
**ID**: `float` (built-in)
**Description**: Convert string to float

**Cross-Language Analysis**:
- **Python**: `float(s)` ← built-in function
- **Rust**: `s.parse::<f64>()?` ← parse method
- **Go**: `strconv.ParseFloat(s, 64)` ← function
- **JavaScript**: `parseFloat(s)` or `Number(s)` ← function
- **C++**: `stod(s)` or `atof(s)` ← functions

**Common Patterns**:
- Python: built-in `float()`
- Parallel to `int()` conversion

**PW Syntax (RECOMMENDED)**:
```pw
float(s) -> float  // built-in function
```

**Rationale**:
- Built-in `float()` matches Python
- 5 chars: `float()`
- Parallel to `int()`

---

### Operation: to_bool
**ID**: `bool` (built-in)
**Description**: Convert string to boolean

**Cross-Language Analysis**:
- **Python**: `s.lower() in ('true', '1', 'yes')` ← manual check (no standard)
- **Rust**: `s.parse::<bool>()?` ← only accepts "true"/"false"
- **Go**: `strconv.ParseBool(s)` ← accepts "true"/"false", "1"/"0", etc.
- **JavaScript**: `s.toLowerCase() === 'true'` ← manual check
- **C++**: `s == "true" || s == "1"` ← manual check

**Common Patterns**:
- No universal standard for string → bool
- Most: case-insensitive "true" check
- Go's `ParseBool` is most flexible (accepts multiple formats)

**PW Syntax (RECOMMENDED)**:
```pw
bool(s) -> bool  // built-in function, accepts "true"/"false" (case-insensitive)
```

**Rationale**:
- Built-in `bool()` is consistent with `int()`, `float()`, `str()`
- 4 chars: `bool()`
- Accept "true"/"false" (case-insensitive), "1"/"0"
- Follows Go's flexible approach

---

### Operation: is_string
**ID**: `typeof(value) == "string"`
**Description**: Check if value is string type

**Cross-Language Analysis**:
- **Python**: `isinstance(value, str)` ← type checking
- **Rust**: Compile-time type checking (no runtime check)
- **Go**: Compile-time type checking
- **JavaScript**: `typeof value === 'string'` ← typeof operator
- **C++**: Compile-time type checking

**Common Patterns**:
- Dynamic languages: runtime type checking
- Static languages: compile-time only
- Python: `isinstance()`
- JS: `typeof` operator

**PW Syntax (RECOMMENDED)**:
```pw
typeof(value) == "string"  // operator + comparison
// OR provide: is_string(value) -> bool
```

**Rationale**:
- `typeof` operator matches JS (widely understood)
- Can compare to type string: `typeof(x) == "string"`
- Alternative: dedicated `is_string()` function for convenience
- Support both styles

**Note**: May also want dedicated type predicates: `is_string()`, `is_int()`, etc.

---

### Operation: is_int
**ID**: `typeof(value) == "int"`
**Description**: Check if value is integer type

**Cross-Language Analysis**:
- **Python**: `isinstance(value, int)` ← type checking
- **Rust**: Compile-time
- **Go**: Compile-time
- **JavaScript**: `Number.isInteger(value)` ← dedicated function
- **C++**: Compile-time

**Common Patterns**:
- Similar to `is_string`
- JS has dedicated `Number.isInteger()`

**PW Syntax (RECOMMENDED)**:
```pw
typeof(value) == "int"  // operator + comparison
// OR: is_int(value) -> bool
```

**Rationale**:
- Consistent with `is_string`
- JS's `Number.isInteger()` is useful pattern for dedicated function

---

### Operation: is_float
**ID**: `typeof(value) == "float"`
**Description**: Check if value is float type

**Cross-Language Analysis**:
- **Python**: `isinstance(value, float)` ← type checking
- **Rust**: Compile-time
- **Go**: Compile-time
- **JavaScript**: `typeof value === 'number' && !Number.isInteger(value)` ← complex check
- **C++**: Compile-time

**Common Patterns**:
- Similar to `is_int`
- No simple check in most languages

**PW Syntax (RECOMMENDED)**:
```pw
typeof(value) == "float"  // operator + comparison
// OR: is_float(value) -> bool
```

**Rationale**:
- Consistent with other type checks

---

### Operation: is_bool
**ID**: `typeof(value) == "bool"`
**Description**: Check if value is boolean type

**Cross-Language Analysis**:
- **Python**: `isinstance(value, bool)` ← type checking
- **Rust**: Compile-time
- **Go**: Compile-time
- **JavaScript**: `typeof value === 'boolean'` ← typeof operator
- **C++**: Compile-time

**Common Patterns**:
- Similar to other type checks

**PW Syntax (RECOMMENDED)**:
```pw
typeof(value) == "bool"  // operator + comparison
// OR: is_bool(value) -> bool
```

**Rationale**:
- Consistent with other type checks

---

## SUMMARY TABLE

| Category | Operations | Primary Namespace | Example Operations |
|----------|-----------|-------------------|-------------------|
| **File I/O** | 12 | `file.*` | `file.read(path)`, `file.write(path, content)`, `file.exists(path)` |
| **String** | 15 | `str.*` + operators | `str.split(s, delim)`, `str.trim(s)`, `s[start:end]`, `+` |
| **HTTP/Network** | 8 | `http.*`, `url.*` | `http.get(url)`, `http.post_json(url, data)`, `url.encode(s)` |
| **JSON** | 4 | `json.*` | `json.parse(s)`, `json.stringify(data)` |
| **Math** | 10 | built-ins | `abs(n)`, `min(a,b)`, `sqrt(n)`, `random()`, `**` |
| **Time/Date** | 8 | `time.*` | `time.now()`, `time.now_ms()`, `sleep(seconds)`, `time.format(ts, fmt)` |
| **Process/System** | 6 | `process.*`, `env.*` | `process.run(cmd)`, `env.get(key)`, `exit(code)` |
| **Array** | 10 | methods + operators | `arr.push(item)`, `arr.pop()`, `arr[index]`, `len(arr)` |
| **Encoding** | 6 | `base64.*`, `hex.*`, `hash.*` | `base64.encode(data)`, `hex.decode(s)`, `hash.sha256(data)` |
| **Type Conversions** | 8 | built-ins + `typeof` | `str(value)`, `int(s)`, `typeof(value)` |
| **TOTAL** | **107** | **9 namespaces** + **built-ins/operators** | — |

---

## KEY DESIGN DECISIONS

### 1. Namespace Strategy
- **Consistent namespaces**: `file.*`, `str.*`, `http.*`, `json.*`, `url.*`, `time.*`, `process.*`, `env.*`, `base64.*`, `hex.*`, `hash.*`
- **Built-in functions**: Common operations like `len()`, `abs()`, `min()`, `max()`, `sqrt()`, `floor()`, `ceil()`, `round()`, `random()`, `sleep()`, `exit()`, `str()`, `int()`, `float()`, `bool()`
- **Operators**: `+` (concat), `**` (power), `[]` (index/slice), `[]=` (assignment), `in` (contains), `[:]` (slice)

### 2. Naming Conventions
- **Verbs**: Use clear action verbs (`read`, `write`, `append`, `delete` vs obscure terms)
- **Snake_case**: Follow Python/Rust convention (`starts_with`, `ends_with`, `index_of`)
- **Brevity**: Abbreviate where universal (`len`, `cwd`, `mkdir`, `rmdir`)
- **Explicitness**: Be explicit when needed (`get_json`, `post_json`, `stringify_pretty`)

### 3. API Style
- **Functions vs Methods**: Namespaced functions for operations, methods for object-specific operations
- **Return values**: Return useful values (not void where possible), return -1 for not-found (not exceptions)
- **Immutability preference**: Return new values rather than mutating (e.g., `arr.reverse()` returns new array)

### 4. Cross-Language Influence
- **Python**: Built-in functions (`len`, `str`, `int`), slice syntax, `in` operator
- **Rust**: Explicit naming (`starts_with`, `ends_with`), namespace organization
- **JavaScript**: JSON API (`parse`, `stringify`), HTTP fetch patterns
- **Go**: Simple stdlib functions (`time.now()`), clear package organization
- **C++**: Math built-ins (`abs`, `sqrt`, `floor`)

### 5. Consistency Patterns
- **Pairs**: `encode`/`decode`, `parse`/`stringify`, `read`/`write`, `get`/`set`, `push`/`pop`
- **Symmetry**: Operations in same category follow similar patterns
- **Discoverability**: Clear namespace grouping makes operations easy to find
- **Natural language**: Operations read like English sentences

---

## AMBIGUOUS CASES REQUIRING INPUT

### 1. String Operations - Function vs Operator
**Question**: Should `str.len(s)` be namespaced or use built-in `len(s)` (which works on all collections)?

**Current decision**: Built-in `len()` for universality (works on strings, arrays, maps, sets)

**Alternative**: Namespaced `str.len()` for consistency with other `str.*` operations

---

### 2. Array Contains - Operator vs Method
**Question**: Should `item in arr` be the primary syntax, or `arr.contains(item)`?

**Current decision**: Support both (operator for brevity, method for discoverability)

**Alternative**: Choose one for consistency

---

### 3. Type Checking - Operator vs Functions
**Question**: Should type checking use `typeof(value) == "string"` or dedicated functions like `is_string(value)`?

**Current decision**: Support both (operator for flexibility, functions for convenience)

**Alternative**: Choose one approach

---

### 4. Math Operations - Built-in vs Namespace
**Question**: Should math operations be built-in functions (`abs`, `sqrt`, etc.) or namespaced (`math.abs`, `math.sqrt`)?

**Current decision**: Built-ins for common operations (matches Python, C++)

**Alternative**: Namespace all math under `math.*` (like JS, Go)

---

### 5. Immutability - In-place vs New Return
**Question**: Should operations like `arr.sort()` mutate in-place or return new values?

**Current decision**: Return new values (functional style, safer)

**Alternative**: Mutate in-place (matches Python's `list.sort()`, more efficient)

---

## NEXT STEPS

1. **Validation**: Review all 107 operations for consistency and completeness
2. **Parser Implementation**: Implement PW syntax parsing for all operations
3. **Stdlib Implementation**: Implement runtime functions for all 107 operations
4. **Code Generation**: Update Python/Rust generators to emit correct code for each operation
5. **CharCNN Dataset**: Generate 10-20 examples per operation per language (1,070+ examples total)
6. **Testing**: Create comprehensive tests for each operation
7. **Documentation**: Write API reference documentation with examples

---

## FILE STATISTICS

- **Total operations designed**: 107
- **Namespaces defined**: 11 (`file`, `str`, `http`, `url`, `json`, `time`, `process`, `env`, `base64`, `hex`, `hash`)
- **Built-in functions**: 18 (`len`, `abs`, `min`, `max`, `pow`, `sqrt`, `floor`, `ceil`, `round`, `random`, `random_int`, `sleep`, `sleep_ms`, `exit`, `str`, `int`, `float`, `bool`)
- **Operators**: 7 (`+`, `**`, `[]`, `[]=`, `in`, `[:]`, `typeof`)
- **Lines**: ~2,500+
- **Cross-language references**: Python, Rust, Go, JavaScript, C++
- **Design rationale entries**: 107 (one per operation)

---

**END OF DOCUMENT**
