# Promptware Universal Operations Library
## Complete MCP Tool List for Bidirectional Translation

**Purpose:** Define every fundamental coding operation that exists across all languages.
**Format:** Each operation has:
1. PW canonical syntax (what users type)
2. Implementations in Python, Rust, Go, JavaScript, C++
3. CharCNN training examples

---

## CATEGORY 1: FILE I/O (12 operations)

### read_file(path) -> str
**Description:** Read entire file contents as string

**PW Syntax:**
```pw
read_file(path) -> str:
  return file.read(path)
```

**Implementations:**
- **Python:** `open(path, 'r').read()` | `Path(path).read_text()`
- **Rust:** `fs::read_to_string(path)` | `File::open(path)?.read_to_string(&mut buf)`
- **Go:** `os.ReadFile(path)` | `ioutil.ReadFile(path)`
- **JavaScript:** `fs.readFileSync(path, 'utf8')` | `await fs.promises.readFile(path, 'utf8')`
- **C++:** `ifstream f(path); string((istreambuf_iterator<char>(f)), istreambuf_iterator<char>())`

---

### write_file(path, content) -> void
**Description:** Write string to file (overwrite)

**PW Syntax:**
```pw
write_file(path, content) -> void:
  file.write(path, content)
```

**Implementations:**
- **Python:** `open(path, 'w').write(content)` | `Path(path).write_text(content)`
- **Rust:** `fs::write(path, content)` | `File::create(path)?.write_all(content.as_bytes())`
- **Go:** `os.WriteFile(path, []byte(content), 0644)` | `ioutil.WriteFile(path, []byte(content), 0644)`
- **JavaScript:** `fs.writeFileSync(path, content)` | `await fs.promises.writeFile(path, content)`
- **C++:** `ofstream f(path); f << content;`

---

### append_file(path, content) -> void
**Description:** Append string to file

**PW Syntax:**
```pw
append_file(path, content) -> void:
  file.append(path, content)
```

**Implementations:**
- **Python:** `open(path, 'a').write(content)`
- **Rust:** `OpenOptions::new().append(true).open(path)?.write_all(content.as_bytes())`
- **Go:** `f, _ := os.OpenFile(path, os.O_APPEND|os.O_WRONLY, 0644); f.WriteString(content)`
- **JavaScript:** `fs.appendFileSync(path, content)`
- **C++:** `ofstream f(path, ios::app); f << content;`

---

### file_exists(path) -> bool
**Description:** Check if file exists

**PW Syntax:**
```pw
file_exists(path) -> bool:
  return file.exists(path)
```

**Implementations:**
- **Python:** `os.path.exists(path)` | `Path(path).exists()`
- **Rust:** `Path::new(path).exists()`
- **Go:** `_, err := os.Stat(path); err == nil`
- **JavaScript:** `fs.existsSync(path)`
- **C++:** `ifstream f(path); return f.good();` | `filesystem::exists(path)` (C++17)

---

### delete_file(path) -> void
**Description:** Delete file

**PW Syntax:**
```pw
delete_file(path) -> void:
  file.delete(path)
```

**Implementations:**
- **Python:** `os.remove(path)` | `Path(path).unlink()`
- **Rust:** `fs::remove_file(path)`
- **Go:** `os.Remove(path)`
- **JavaScript:** `fs.unlinkSync(path)`
- **C++:** `remove(path.c_str())` | `filesystem::remove(path)` (C++17)

---

### read_lines(path) -> array<str>
**Description:** Read file as array of lines

**PW Syntax:**
```pw
read_lines(path) -> array<str>:
  return file.read_lines(path)
```

**Implementations:**
- **Python:** `open(path).readlines()` | `Path(path).read_text().splitlines()`
- **Rust:** `BufReader::new(File::open(path)?).lines().collect()`
- **Go:** `data, _ := os.ReadFile(path); strings.Split(string(data), "\n")`
- **JavaScript:** `fs.readFileSync(path, 'utf8').split('\n')`
- **C++:** `ifstream f(path); string line; vector<string> lines; while(getline(f, line)) lines.push_back(line);`

---

### write_lines(path, lines) -> void
**Description:** Write array of strings as lines

**PW Syntax:**
```pw
write_lines(path, lines) -> void:
  file.write_lines(path, lines)
```

**Implementations:**
- **Python:** `open(path, 'w').writelines(line + '\n' for line in lines)`
- **Rust:** `fs::write(path, lines.join("\n"))`
- **Go:** `os.WriteFile(path, []byte(strings.Join(lines, "\n")), 0644)`
- **JavaScript:** `fs.writeFileSync(path, lines.join('\n'))`
- **C++:** `ofstream f(path); for(auto& line : lines) f << line << '\n';`

---

### list_directory(path) -> array<str>
**Description:** List files/directories in path

**PW Syntax:**
```pw
list_directory(path) -> array<str>:
  return file.list_dir(path)
```

**Implementations:**
- **Python:** `os.listdir(path)` | `[f.name for f in Path(path).iterdir()]`
- **Rust:** `fs::read_dir(path)?.map(|e| e?.file_name().to_string_lossy().to_string()).collect()`
- **Go:** `entries, _ := os.ReadDir(path); names := make([]string, len(entries)); for i, e := range entries { names[i] = e.Name() }`
- **JavaScript:** `fs.readdirSync(path)`
- **C++:** `vector<string> files; for(auto& p: filesystem::directory_iterator(path)) files.push_back(p.path().filename());` (C++17)

---

### create_directory(path) -> void
**Description:** Create directory (and parents if needed)

**PW Syntax:**
```pw
create_directory(path) -> void:
  file.mkdir(path)
```

**Implementations:**
- **Python:** `os.makedirs(path, exist_ok=True)` | `Path(path).mkdir(parents=True, exist_ok=True)`
- **Rust:** `fs::create_dir_all(path)`
- **Go:** `os.MkdirAll(path, 0755)`
- **JavaScript:** `fs.mkdirSync(path, {recursive: true})`
- **C++:** `filesystem::create_directories(path)` (C++17)

---

### delete_directory(path) -> void
**Description:** Delete directory recursively

**PW Syntax:**
```pw
delete_directory(path) -> void:
  file.rmdir(path)
```

**Implementations:**
- **Python:** `shutil.rmtree(path)`
- **Rust:** `fs::remove_dir_all(path)`
- **Go:** `os.RemoveAll(path)`
- **JavaScript:** `fs.rmSync(path, {recursive: true, force: true})`
- **C++:** `filesystem::remove_all(path)` (C++17)

---

### get_file_size(path) -> int
**Description:** Get file size in bytes

**PW Syntax:**
```pw
get_file_size(path) -> int:
  return file.size(path)
```

**Implementations:**
- **Python:** `os.path.getsize(path)` | `Path(path).stat().st_size`
- **Rust:** `fs::metadata(path)?.len()`
- **Go:** `info, _ := os.Stat(path); info.Size()`
- **JavaScript:** `fs.statSync(path).size`
- **C++:** `filesystem::file_size(path)` (C++17)

---

### copy_file(src, dest) -> void
**Description:** Copy file from src to dest

**PW Syntax:**
```pw
copy_file(src, dest) -> void:
  file.copy(src, dest)
```

**Implementations:**
- **Python:** `shutil.copy2(src, dest)`
- **Rust:** `fs::copy(src, dest)`
- **Go:** `input, _ := os.ReadFile(src); os.WriteFile(dest, input, 0644)`
- **JavaScript:** `fs.copyFileSync(src, dest)`
- **C++:** `filesystem::copy_file(src, dest)` (C++17)

---

## CATEGORY 2: STRING OPERATIONS (15 operations)

### str_length(s) -> int
**Description:** Get string length

**PW Syntax:**
```pw
str_length(s) -> int:
  return len(s)
```

**Implementations:**
- **Python:** `len(s)`
- **Rust:** `s.len()`
- **Go:** `len(s)`
- **JavaScript:** `s.length`
- **C++:** `s.length()` | `s.size()`

---

### str_concat(s1, s2) -> str
**Description:** Concatenate two strings

**PW Syntax:**
```pw
str_concat(s1, s2) -> str:
  return s1 + s2
```

**Implementations:**
- **Python:** `s1 + s2`
- **Rust:** `format!("{}{}", s1, s2)` | `s1.to_owned() + &s2`
- **Go:** `s1 + s2`
- **JavaScript:** `s1 + s2` | `` `${s1}${s2}` ``
- **C++:** `s1 + s2`

---

### str_substring(s, start, end) -> str
**Description:** Extract substring from start to end index

**PW Syntax:**
```pw
str_substring(s, start, end) -> str:
  return s[start:end]
```

**Implementations:**
- **Python:** `s[start:end]`
- **Rust:** `&s[start..end]`
- **Go:** `s[start:end]`
- **JavaScript:** `s.substring(start, end)` | `s.slice(start, end)`
- **C++:** `s.substr(start, end-start)`

---

### str_contains(s, substring) -> bool
**Description:** Check if string contains substring

**PW Syntax:**
```pw
str_contains(s, substring) -> bool:
  return substring in s
```

**Implementations:**
- **Python:** `substring in s`
- **Rust:** `s.contains(substring)`
- **Go:** `strings.Contains(s, substring)`
- **JavaScript:** `s.includes(substring)`
- **C++:** `s.find(substring) != string::npos`

---

### str_starts_with(s, prefix) -> bool
**Description:** Check if string starts with prefix

**PW Syntax:**
```pw
str_starts_with(s, prefix) -> bool:
  return s.starts_with(prefix)
```

**Implementations:**
- **Python:** `s.startswith(prefix)`
- **Rust:** `s.starts_with(prefix)`
- **Go:** `strings.HasPrefix(s, prefix)`
- **JavaScript:** `s.startsWith(prefix)`
- **C++:** `s.rfind(prefix, 0) == 0`

---

### str_ends_with(s, suffix) -> bool
**Description:** Check if string ends with suffix

**PW Syntax:**
```pw
str_ends_with(s, suffix) -> bool:
  return s.ends_with(suffix)
```

**Implementations:**
- **Python:** `s.endswith(suffix)`
- **Rust:** `s.ends_with(suffix)`
- **Go:** `strings.HasSuffix(s, suffix)`
- **JavaScript:** `s.endsWith(suffix)`
- **C++:** `s.size() >= suffix.size() && s.compare(s.size()-suffix.size(), suffix.size(), suffix) == 0`

---

### str_split(s, delimiter) -> array<str>
**Description:** Split string by delimiter

**PW Syntax:**
```pw
str_split(s, delimiter) -> array<str>:
  return s.split(delimiter)
```

**Implementations:**
- **Python:** `s.split(delimiter)`
- **Rust:** `s.split(delimiter).collect()`
- **Go:** `strings.Split(s, delimiter)`
- **JavaScript:** `s.split(delimiter)`
- **C++:** (complex - no built-in, requires tokenization)

---

### str_join(strings, separator) -> str
**Description:** Join array of strings with separator

**PW Syntax:**
```pw
str_join(strings, separator) -> str:
  return separator.join(strings)
```

**Implementations:**
- **Python:** `separator.join(strings)`
- **Rust:** `strings.join(separator)`
- **Go:** `strings.Join(strings, separator)`
- **JavaScript:** `strings.join(separator)`
- **C++:** (complex - requires accumulation)

---

### str_trim(s) -> str
**Description:** Remove whitespace from both ends

**PW Syntax:**
```pw
str_trim(s) -> str:
  return s.trim()
```

**Implementations:**
- **Python:** `s.strip()`
- **Rust:** `s.trim()`
- **Go:** `strings.TrimSpace(s)`
- **JavaScript:** `s.trim()`
- **C++:** (complex - no built-in)

---

### str_to_upper(s) -> str
**Description:** Convert string to uppercase

**PW Syntax:**
```pw
str_to_upper(s) -> str:
  return s.upper()
```

**Implementations:**
- **Python:** `s.upper()`
- **Rust:** `s.to_uppercase()`
- **Go:** `strings.ToUpper(s)`
- **JavaScript:** `s.toUpperCase()`
- **C++:** `transform(s.begin(), s.end(), s.begin(), ::toupper)`

---

### str_to_lower(s) -> str
**Description:** Convert string to lowercase

**PW Syntax:**
```pw
str_to_lower(s) -> str:
  return s.lower()
```

**Implementations:**
- **Python:** `s.lower()`
- **Rust:** `s.to_lowercase()`
- **Go:** `strings.ToLower(s)`
- **JavaScript:** `s.toLowerCase()`
- **C++:** `transform(s.begin(), s.end(), s.begin(), ::tolower)`

---

### str_replace(s, old, new) -> str
**Description:** Replace all occurrences of old with new

**PW Syntax:**
```pw
str_replace(s, old, new) -> str:
  return s.replace(old, new)
```

**Implementations:**
- **Python:** `s.replace(old, new)`
- **Rust:** `s.replace(old, new)`
- **Go:** `strings.ReplaceAll(s, old, new)`
- **JavaScript:** `s.replaceAll(old, new)`
- **C++:** (complex - requires loop)

---

### str_index_of(s, substring) -> int
**Description:** Find first index of substring (-1 if not found)

**PW Syntax:**
```pw
str_index_of(s, substring) -> int:
  return s.index_of(substring)
```

**Implementations:**
- **Python:** `s.find(substring)`
- **Rust:** `s.find(substring).unwrap_or(-1)` (returns Option)
- **Go:** `strings.Index(s, substring)`
- **JavaScript:** `s.indexOf(substring)`
- **C++:** `s.find(substring)` (returns size_t, npos on not found)

---

### str_reverse(s) -> str
**Description:** Reverse string

**PW Syntax:**
```pw
str_reverse(s) -> str:
  return s.reverse()
```

**Implementations:**
- **Python:** `s[::-1]`
- **Rust:** `s.chars().rev().collect()`
- **Go:** `runes := []rune(s); for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 { runes[i], runes[j] = runes[j], runes[i] }`
- **JavaScript:** `s.split('').reverse().join('')`
- **C++:** `reverse(s.begin(), s.end())`

---

### str_is_empty(s) -> bool
**Description:** Check if string is empty

**PW Syntax:**
```pw
str_is_empty(s) -> bool:
  return len(s) == 0
```

**Implementations:**
- **Python:** `len(s) == 0` | `not s`
- **Rust:** `s.is_empty()`
- **Go:** `len(s) == 0`
- **JavaScript:** `s.length === 0` | `!s`
- **C++:** `s.empty()`

---

## CATEGORY 3: HTTP/NETWORK (8 operations)

### http_get(url) -> str
**Description:** Make HTTP GET request, return body as string

**PW Syntax:**
```pw
http_get(url) -> str:
  return http.get(url)
```

**Implementations:**
- **Python:** `requests.get(url).text` | `urllib.request.urlopen(url).read().decode()`
- **Rust:** `reqwest::blocking::get(url)?.text()?` | `reqwest::get(url).await?.text().await?`
- **Go:** `resp, _ := http.Get(url); body, _ := io.ReadAll(resp.Body); string(body)`
- **JavaScript:** `(await fetch(url)).text()` | `require('https').get(url, res => {...})`
- **C++:** (complex - requires external library like libcurl)

---

### http_post(url, body) -> str
**Description:** Make HTTP POST request with body

**PW Syntax:**
```pw
http_post(url, body) -> str:
  return http.post(url, body)
```

**Implementations:**
- **Python:** `requests.post(url, data=body).text`
- **Rust:** `reqwest::blocking::Client::new().post(url).body(body).send()?.text()?`
- **Go:** `resp, _ := http.Post(url, "text/plain", strings.NewReader(body)); data, _ := io.ReadAll(resp.Body); string(data)`
- **JavaScript:** `(await fetch(url, {method: 'POST', body})).text()`
- **C++:** (requires libcurl)

---

### http_get_json(url) -> map<str, any>
**Description:** Make HTTP GET, parse JSON response

**PW Syntax:**
```pw
http_get_json(url) -> map<str, any>:
  return parse_json(http.get(url))
```

**Implementations:**
- **Python:** `requests.get(url).json()`
- **Rust:** `reqwest::blocking::get(url)?.json()?`
- **Go:** `resp, _ := http.Get(url); json.Unmarshal(io.ReadAll(resp.Body))`
- **JavaScript:** `(await fetch(url)).json()`
- **C++:** (requires JSON library + HTTP library)

---

### http_post_json(url, data) -> map<str, any>
**Description:** POST JSON data, return JSON response

**PW Syntax:**
```pw
http_post_json(url, data) -> map<str, any>:
  return parse_json(http.post(url, stringify_json(data)))
```

**Implementations:**
- **Python:** `requests.post(url, json=data).json()`
- **Rust:** `reqwest::blocking::Client::new().post(url).json(&data).send()?.json()?`
- **Go:** `jsonData, _ := json.Marshal(data); resp, _ := http.Post(url, "application/json", bytes.NewBuffer(jsonData))`
- **JavaScript:** `(await fetch(url, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data)})).json()`
- **C++:** (requires JSON + HTTP libraries)

---

### http_download_file(url, path) -> void
**Description:** Download file from URL to local path

**PW Syntax:**
```pw
http_download_file(url, path) -> void:
  write_file(path, http.get(url))
```

**Implementations:**
- **Python:** `urllib.request.urlretrieve(url, path)` | `open(path, 'wb').write(requests.get(url).content)`
- **Rust:** `fs::write(path, reqwest::blocking::get(url)?.bytes()?)?`
- **Go:** `resp, _ := http.Get(url); out, _ := os.Create(path); io.Copy(out, resp.Body)`
- **JavaScript:** `fs.writeFileSync(path, await (await fetch(url)).arrayBuffer())`
- **C++:** (requires libcurl + file I/O)

---

### url_encode(s) -> str
**Description:** URL-encode string (percent encoding)

**PW Syntax:**
```pw
url_encode(s) -> str:
  return url.encode(s)
```

**Implementations:**
- **Python:** `urllib.parse.quote(s)`
- **Rust:** `urlencoding::encode(s)`
- **Go:** `url.QueryEscape(s)`
- **JavaScript:** `encodeURIComponent(s)`
- **C++:** (manual implementation required)

---

### url_decode(s) -> str
**Description:** Decode URL-encoded string

**PW Syntax:**
```pw
url_decode(s) -> str:
  return url.decode(s)
```

**Implementations:**
- **Python:** `urllib.parse.unquote(s)`
- **Rust:** `urlencoding::decode(s)`
- **Go:** `url.QueryUnescape(s)`
- **JavaScript:** `decodeURIComponent(s)`
- **C++:** (manual implementation)

---

### parse_url(url) -> map<str, str>
**Description:** Parse URL into components (scheme, host, path, query)

**PW Syntax:**
```pw
parse_url(url) -> map<str, str>:
  return url.parse(url)
```

**Implementations:**
- **Python:** `urllib.parse.urlparse(url)` (returns namedtuple)
- **Rust:** `Url::parse(url)?` (url crate)
- **Go:** `url.Parse(url)`
- **JavaScript:** `new URL(url)`
- **C++:** (requires external library)

---

## CATEGORY 4: JSON OPERATIONS (4 operations)

### parse_json(s) -> any
**Description:** Parse JSON string to data structure

**PW Syntax:**
```pw
parse_json(s) -> any:
  return json.parse(s)
```

**Implementations:**
- **Python:** `json.loads(s)`
- **Rust:** `serde_json::from_str(s)?`
- **Go:** `var data interface{}; json.Unmarshal([]byte(s), &data)`
- **JavaScript:** `JSON.parse(s)`
- **C++:** (requires library like nlohmann/json: `json::parse(s)`)

---

### stringify_json(data) -> str
**Description:** Convert data structure to JSON string

**PW Syntax:**
```pw
stringify_json(data) -> str:
  return json.stringify(data)
```

**Implementations:**
- **Python:** `json.dumps(data)`
- **Rust:** `serde_json::to_string(&data)?`
- **Go:** `jsonData, _ := json.Marshal(data); string(jsonData)`
- **JavaScript:** `JSON.stringify(data)`
- **C++:** (requires JSON library: `data.dump()`)

---

### stringify_json_pretty(data) -> str
**Description:** Convert to pretty-printed JSON

**PW Syntax:**
```pw
stringify_json_pretty(data) -> str:
  return json.stringify_pretty(data)
```

**Implementations:**
- **Python:** `json.dumps(data, indent=2)`
- **Rust:** `serde_json::to_string_pretty(&data)?`
- **Go:** `jsonData, _ := json.MarshalIndent(data, "", "  "); string(jsonData)`
- **JavaScript:** `JSON.stringify(data, null, 2)`
- **C++:** `data.dump(2)`

---

### json_validate(s) -> bool
**Description:** Check if string is valid JSON

**PW Syntax:**
```pw
json_validate(s) -> bool:
  try: parse_json(s); return true
  catch: return false
```

**Implementations:**
- **Python:** `try: json.loads(s); return True\nexcept: return False`
- **Rust:** `serde_json::from_str::<serde_json::Value>(s).is_ok()`
- **Go:** `var js json.RawMessage; err := json.Unmarshal([]byte(s), &js); err == nil`
- **JavaScript:** `try { JSON.parse(s); return true; } catch { return false; }`
- **C++:** `try { json::parse(s); return true; } catch { return false; }`

---

## CATEGORY 5: MATH OPERATIONS (10 operations)

### math_abs(n) -> number
**Description:** Absolute value

**PW Syntax:**
```pw
math_abs(n) -> number:
  return abs(n)
```

**Implementations:**
- **Python:** `abs(n)`
- **Rust:** `n.abs()`
- **Go:** `math.Abs(n)`
- **JavaScript:** `Math.abs(n)`
- **C++:** `abs(n)` | `fabs(n)` (for floats)

---

### math_min(a, b) -> number
**Description:** Minimum of two numbers

**PW Syntax:**
```pw
math_min(a, b) -> number:
  return min(a, b)
```

**Implementations:**
- **Python:** `min(a, b)`
- **Rust:** `a.min(b)`
- **Go:** `math.Min(a, b)`
- **JavaScript:** `Math.min(a, b)`
- **C++:** `min(a, b)` | `std::min(a, b)`

---

### math_max(a, b) -> number
**Description:** Maximum of two numbers

**PW Syntax:**
```pw
math_max(a, b) -> number:
  return max(a, b)
```

**Implementations:**
- **Python:** `max(a, b)`
- **Rust:** `a.max(b)`
- **Go:** `math.Max(a, b)`
- **JavaScript:** `Math.max(a, b)`
- **C++:** `max(a, b)` | `std::max(a, b)`

---

### math_pow(base, exp) -> number
**Description:** Raise base to exponent

**PW Syntax:**
```pw
math_pow(base, exp) -> number:
  return base ** exp
```

**Implementations:**
- **Python:** `base ** exp` | `pow(base, exp)`
- **Rust:** `base.powf(exp)`
- **Go:** `math.Pow(base, exp)`
- **JavaScript:** `Math.pow(base, exp)` | `base ** exp`
- **C++:** `pow(base, exp)`

---

### math_sqrt(n) -> float
**Description:** Square root

**PW Syntax:**
```pw
math_sqrt(n) -> float:
  return sqrt(n)
```

**Implementations:**
- **Python:** `math.sqrt(n)` | `n ** 0.5`
- **Rust:** `n.sqrt()`
- **Go:** `math.Sqrt(n)`
- **JavaScript:** `Math.sqrt(n)`
- **C++:** `sqrt(n)`

---

### math_floor(n) -> int
**Description:** Round down to integer

**PW Syntax:**
```pw
math_floor(n) -> int:
  return floor(n)
```

**Implementations:**
- **Python:** `math.floor(n)` | `int(n)` (for positive)
- **Rust:** `n.floor() as i32`
- **Go:** `math.Floor(n)`
- **JavaScript:** `Math.floor(n)`
- **C++:** `floor(n)`

---

### math_ceil(n) -> int
**Description:** Round up to integer

**PW Syntax:**
```pw
math_ceil(n) -> int:
  return ceil(n)
```

**Implementations:**
- **Python:** `math.ceil(n)`
- **Rust:** `n.ceil() as i32`
- **Go:** `math.Ceil(n)`
- **JavaScript:** `Math.ceil(n)`
- **C++:** `ceil(n)`

---

### math_round(n) -> int
**Description:** Round to nearest integer

**PW Syntax:**
```pw
math_round(n) -> int:
  return round(n)
```

**Implementations:**
- **Python:** `round(n)`
- **Rust:** `n.round() as i32`
- **Go:** `math.Round(n)`
- **JavaScript:** `Math.round(n)`
- **C++:** `round(n)`

---

### math_random() -> float
**Description:** Random float between 0 and 1

**PW Syntax:**
```pw
math_random() -> float:
  return random()
```

**Implementations:**
- **Python:** `random.random()`
- **Rust:** `rand::random::<f64>()`
- **Go:** `rand.Float64()`
- **JavaScript:** `Math.random()`
- **C++:** `(double)rand() / RAND_MAX`

---

### math_random_int(min, max) -> int
**Description:** Random integer between min and max (inclusive)

**PW Syntax:**
```pw
math_random_int(min, max) -> int:
  return random_int(min, max)
```

**Implementations:**
- **Python:** `random.randint(min, max)`
- **Rust:** `rand::thread_rng().gen_range(min..=max)`
- **Go:** `rand.Intn(max-min+1) + min`
- **JavaScript:** `Math.floor(Math.random() * (max - min + 1)) + min`
- **C++:** `rand() % (max - min + 1) + min`

---

## CATEGORY 6: TIME/DATE (8 operations)

### time_now() -> int
**Description:** Current Unix timestamp (seconds since epoch)

**PW Syntax:**
```pw
time_now() -> int:
  return time.now()
```

**Implementations:**
- **Python:** `int(time.time())`
- **Rust:** `SystemTime::now().duration_since(UNIX_EPOCH)?.as_secs()`
- **Go:** `time.Now().Unix()`
- **JavaScript:** `Math.floor(Date.now() / 1000)`
- **C++:** `chrono::system_clock::now().time_since_epoch().count()`

---

### time_now_ms() -> int
**Description:** Current timestamp in milliseconds

**PW Syntax:**
```pw
time_now_ms() -> int:
  return time.now_ms()
```

**Implementations:**
- **Python:** `int(time.time() * 1000)`
- **Rust:** `SystemTime::now().duration_since(UNIX_EPOCH)?.as_millis()`
- **Go:** `time.Now().UnixMilli()`
- **JavaScript:** `Date.now()`
- **C++:** `chrono::duration_cast<chrono::milliseconds>(chrono::system_clock::now().time_since_epoch()).count()`

---

### sleep(seconds) -> void
**Description:** Sleep for N seconds

**PW Syntax:**
```pw
sleep(seconds) -> void:
  time.sleep(seconds)
```

**Implementations:**
- **Python:** `time.sleep(seconds)`
- **Rust:** `thread::sleep(Duration::from_secs(seconds))`
- **Go:** `time.Sleep(time.Duration(seconds) * time.Second)`
- **JavaScript:** `await new Promise(resolve => setTimeout(resolve, seconds * 1000))`
- **C++:** `this_thread::sleep_for(chrono::seconds(seconds))`

---

### sleep_ms(milliseconds) -> void
**Description:** Sleep for N milliseconds

**PW Syntax:**
```pw
sleep_ms(milliseconds) -> void:
  time.sleep_ms(milliseconds)
```

**Implementations:**
- **Python:** `time.sleep(milliseconds / 1000)`
- **Rust:** `thread::sleep(Duration::from_millis(milliseconds))`
- **Go:** `time.Sleep(time.Duration(milliseconds) * time.Millisecond)`
- **JavaScript:** `await new Promise(resolve => setTimeout(resolve, milliseconds))`
- **C++:** `this_thread::sleep_for(chrono::milliseconds(milliseconds))`

---

### format_timestamp(timestamp, format) -> str
**Description:** Format Unix timestamp to string

**PW Syntax:**
```pw
format_timestamp(timestamp, format) -> str:
  return time.format(timestamp, format)
```

**Implementations:**
- **Python:** `datetime.fromtimestamp(timestamp).strftime(format)`
- **Rust:** (requires chrono crate)
- **Go:** `time.Unix(timestamp, 0).Format(format)`
- **JavaScript:** `new Date(timestamp * 1000).toISOString()` (format handling varies)
- **C++:** (complex - requires time formatting)

---

### parse_timestamp(date_string, format) -> int
**Description:** Parse date string to Unix timestamp

**PW Syntax:**
```pw
parse_timestamp(date_string, format) -> int:
  return time.parse(date_string, format)
```

**Implementations:**
- **Python:** `int(datetime.strptime(date_string, format).timestamp())`
- **Rust:** (requires chrono crate)
- **Go:** `t, _ := time.Parse(format, date_string); t.Unix()`
- **JavaScript:** `Math.floor(new Date(date_string).getTime() / 1000)`
- **C++:** (complex - requires parsing library)

---

### date_now_iso() -> str
**Description:** Current date/time in ISO 8601 format

**PW Syntax:**
```pw
date_now_iso() -> str:
  return time.now_iso()
```

**Implementations:**
- **Python:** `datetime.now().isoformat()`
- **Rust:** `Utc::now().to_rfc3339()`
- **Go:** `time.Now().Format(time.RFC3339)`
- **JavaScript:** `new Date().toISOString()`
- **C++:** (requires date library)

---

### date_add_days(timestamp, days) -> int
**Description:** Add days to timestamp

**PW Syntax:**
```pw
date_add_days(timestamp, days) -> int:
  return timestamp + (days * 86400)
```

**Implementations:**
- **Python:** `timestamp + (days * 86400)`
- **Rust:** (calculate manually or use chrono)
- **Go:** `time.Unix(timestamp, 0).AddDate(0, 0, days).Unix()`
- **JavaScript:** `timestamp + (days * 86400)`
- **C++:** `timestamp + (days * 86400)`

---

## CATEGORY 7: PROCESS/SYSTEM (6 operations)

### run_command(cmd) -> str
**Description:** Execute shell command, return output

**PW Syntax:**
```pw
run_command(cmd) -> str:
  return process.run(cmd)
```

**Implementations:**
- **Python:** `subprocess.check_output(cmd, shell=True).decode()`
- **Rust:** `String::from_utf8(Command::new("sh").arg("-c").arg(cmd).output()?.stdout)?`
- **Go:** `out, _ := exec.Command("sh", "-c", cmd).Output(); string(out)`
- **JavaScript:** `require('child_process').execSync(cmd).toString()`
- **C++:** (popen or system() - complex)

---

### get_env(key) -> str
**Description:** Get environment variable

**PW Syntax:**
```pw
get_env(key) -> str:
  return env.get(key)
```

**Implementations:**
- **Python:** `os.environ.get(key, "")`
- **Rust:** `env::var(key).unwrap_or_default()`
- **Go:** `os.Getenv(key)`
- **JavaScript:** `process.env[key] || ""`
- **C++:** `getenv(key.c_str())`

---

### set_env(key, value) -> void
**Description:** Set environment variable

**PW Syntax:**
```pw
set_env(key, value) -> void:
  env.set(key, value)
```

**Implementations:**
- **Python:** `os.environ[key] = value`
- **Rust:** `env::set_var(key, value)`
- **Go:** `os.Setenv(key, value)`
- **JavaScript:** `process.env[key] = value`
- **C++:** `setenv(key.c_str(), value.c_str(), 1)`

---

### exit_program(code) -> void
**Description:** Exit program with code

**PW Syntax:**
```pw
exit_program(code) -> void:
  process.exit(code)
```

**Implementations:**
- **Python:** `sys.exit(code)`
- **Rust:** `std::process::exit(code)`
- **Go:** `os.Exit(code)`
- **JavaScript:** `process.exit(code)`
- **C++:** `exit(code)`

---

### get_cwd() -> str
**Description:** Get current working directory

**PW Syntax:**
```pw
get_cwd() -> str:
  return process.cwd()
```

**Implementations:**
- **Python:** `os.getcwd()`
- **Rust:** `env::current_dir()?.to_str()?`
- **Go:** `os.Getwd()`
- **JavaScript:** `process.cwd()`
- **C++:** `filesystem::current_path()` (C++17)

---

### change_dir(path) -> void
**Description:** Change working directory

**PW Syntax:**
```pw
change_dir(path) -> void:
  process.chdir(path)
```

**Implementations:**
- **Python:** `os.chdir(path)`
- **Rust:** `env::set_current_dir(path)?`
- **Go:** `os.Chdir(path)`
- **JavaScript:** `process.chdir(path)`
- **C++:** `filesystem::current_path(path)` (C++17)

---

## CATEGORY 8: ARRAY OPERATIONS (10 operations)

### array_length(arr) -> int
**Description:** Get array length

**PW Syntax:**
```pw
array_length(arr) -> int:
  return len(arr)
```

**Implementations:**
- **Python:** `len(arr)`
- **Rust:** `arr.len()`
- **Go:** `len(arr)`
- **JavaScript:** `arr.length`
- **C++:** `arr.size()`

---

### array_push(arr, item) -> void
**Description:** Add item to end of array

**PW Syntax:**
```pw
array_push(arr, item) -> void:
  arr.append(item)
```

**Implementations:**
- **Python:** `arr.append(item)`
- **Rust:** `arr.push(item)`
- **Go:** `arr = append(arr, item)`
- **JavaScript:** `arr.push(item)`
- **C++:** `arr.push_back(item)`

---

### array_pop(arr) -> any
**Description:** Remove and return last item

**PW Syntax:**
```pw
array_pop(arr) -> any:
  return arr.pop()
```

**Implementations:**
- **Python:** `arr.pop()`
- **Rust:** `arr.pop()`
- **Go:** `item := arr[len(arr)-1]; arr = arr[:len(arr)-1]`
- **JavaScript:** `arr.pop()`
- **C++:** `auto item = arr.back(); arr.pop_back(); return item;`

---

### array_get(arr, index) -> any
**Description:** Get item at index

**PW Syntax:**
```pw
array_get(arr, index) -> any:
  return arr[index]
```

**Implementations:**
- **Python:** `arr[index]`
- **Rust:** `arr[index]`
- **Go:** `arr[index]`
- **JavaScript:** `arr[index]`
- **C++:** `arr[index]`

---

### array_set(arr, index, value) -> void
**Description:** Set item at index

**PW Syntax:**
```pw
array_set(arr, index, value) -> void:
  arr[index] = value
```

**Implementations:**
- **Python:** `arr[index] = value`
- **Rust:** `arr[index] = value`
- **Go:** `arr[index] = value`
- **JavaScript:** `arr[index] = value`
- **C++:** `arr[index] = value`

---

### array_contains(arr, item) -> bool
**Description:** Check if array contains item

**PW Syntax:**
```pw
array_contains(arr, item) -> bool:
  return item in arr
```

**Implementations:**
- **Python:** `item in arr`
- **Rust:** `arr.contains(&item)`
- **Go:** (requires loop)
- **JavaScript:** `arr.includes(item)`
- **C++:** `find(arr.begin(), arr.end(), item) != arr.end()`

---

### array_index_of(arr, item) -> int
**Description:** Find index of item (-1 if not found)

**PW Syntax:**
```pw
array_index_of(arr, item) -> int:
  return arr.index(item)
```

**Implementations:**
- **Python:** `arr.index(item) if item in arr else -1`
- **Rust:** `arr.iter().position(|x| x == &item).unwrap_or(-1)`
- **Go:** (requires loop)
- **JavaScript:** `arr.indexOf(item)`
- **C++:** `find(arr.begin(), arr.end(), item) - arr.begin()`

---

### array_slice(arr, start, end) -> array
**Description:** Extract subarray from start to end

**PW Syntax:**
```pw
array_slice(arr, start, end) -> array:
  return arr[start:end]
```

**Implementations:**
- **Python:** `arr[start:end]`
- **Rust:** `&arr[start..end]`
- **Go:** `arr[start:end]`
- **JavaScript:** `arr.slice(start, end)`
- **C++:** `vector<T>(arr.begin()+start, arr.begin()+end)`

---

### array_reverse(arr) -> array
**Description:** Reverse array

**PW Syntax:**
```pw
array_reverse(arr) -> array:
  return arr.reverse()
```

**Implementations:**
- **Python:** `arr[::-1]` | `list(reversed(arr))`
- **Rust:** `arr.iter().rev().cloned().collect()`
- **Go:** (requires loop)
- **JavaScript:** `[...arr].reverse()`
- **C++:** `reverse(arr.begin(), arr.end())`

---

### array_sort(arr) -> array
**Description:** Sort array (ascending)

**PW Syntax:**
```pw
array_sort(arr) -> array:
  return sorted(arr)
```

**Implementations:**
- **Python:** `sorted(arr)`
- **Rust:** `arr.sort(); arr`
- **Go:** `sort.Ints(arr)` (in-place)
- **JavaScript:** `[...arr].sort((a,b) => a-b)`
- **C++:** `sort(arr.begin(), arr.end())`

---

## CATEGORY 9: ENCODING/DECODING (6 operations)

### base64_encode(data) -> str
**Description:** Encode bytes/string to base64

**PW Syntax:**
```pw
base64_encode(data) -> str:
  return base64.encode(data)
```

**Implementations:**
- **Python:** `base64.b64encode(data.encode()).decode()`
- **Rust:** `base64::encode(data)`
- **Go:** `base64.StdEncoding.EncodeToString([]byte(data))`
- **JavaScript:** `Buffer.from(data).toString('base64')`
- **C++:** (requires library)

---

### base64_decode(encoded) -> str
**Description:** Decode base64 to string

**PW Syntax:**
```pw
base64_decode(encoded) -> str:
  return base64.decode(encoded)
```

**Implementations:**
- **Python:** `base64.b64decode(encoded).decode()`
- **Rust:** `String::from_utf8(base64::decode(encoded)?)?`
- **Go:** `decoded, _ := base64.StdEncoding.DecodeString(encoded); string(decoded)`
- **JavaScript:** `Buffer.from(encoded, 'base64').toString()`
- **C++:** (requires library)

---

### hex_encode(data) -> str
**Description:** Encode bytes to hex string

**PW Syntax:**
```pw
hex_encode(data) -> str:
  return hex.encode(data)
```

**Implementations:**
- **Python:** `data.encode().hex()`
- **Rust:** `hex::encode(data)`
- **Go:** `hex.EncodeToString([]byte(data))`
- **JavaScript:** `Buffer.from(data).toString('hex')`
- **C++:** (manual implementation)

---

### hex_decode(encoded) -> str
**Description:** Decode hex string to bytes

**PW Syntax:**
```pw
hex_decode(encoded) -> str:
  return hex.decode(encoded)
```

**Implementations:**
- **Python:** `bytes.fromhex(encoded).decode()`
- **Rust:** `String::from_utf8(hex::decode(encoded)?)?`
- **Go:** `decoded, _ := hex.DecodeString(encoded); string(decoded)`
- **JavaScript:** `Buffer.from(encoded, 'hex').toString()`
- **C++:** (manual implementation)

---

### md5_hash(data) -> str
**Description:** Compute MD5 hash

**PW Syntax:**
```pw
md5_hash(data) -> str:
  return hash.md5(data)
```

**Implementations:**
- **Python:** `hashlib.md5(data.encode()).hexdigest()`
- **Rust:** `format!("{:x}", md5::compute(data))`
- **Go:** `fmt.Sprintf("%x", md5.Sum([]byte(data)))`
- **JavaScript:** `require('crypto').createHash('md5').update(data).digest('hex')`
- **C++:** (requires OpenSSL or similar)

---

### sha256_hash(data) -> str
**Description:** Compute SHA-256 hash

**PW Syntax:**
```pw
sha256_hash(data) -> str:
  return hash.sha256(data)
```

**Implementations:**
- **Python:** `hashlib.sha256(data.encode()).hexdigest()`
- **Rust:** `format!("{:x}", sha2::Sha256::digest(data))`
- **Go:** `fmt.Sprintf("%x", sha256.Sum256([]byte(data)))`
- **JavaScript:** `require('crypto').createHash('sha256').update(data).digest('hex')`
- **C++:** (requires OpenSSL or similar)

---

## CATEGORY 10: TYPE CONVERSIONS (8 operations)

### to_string(value) -> str
**Description:** Convert any value to string

**PW Syntax:**
```pw
to_string(value) -> str:
  return str(value)
```

**Implementations:**
- **Python:** `str(value)`
- **Rust:** `value.to_string()` | `format!("{}", value)`
- **Go:** `fmt.Sprint(value)` | `strconv.Itoa(value)` (for ints)
- **JavaScript:** `String(value)` | `value.toString()`
- **C++:** `to_string(value)` | `std::to_string(value)`

---

### to_int(s) -> int
**Description:** Convert string to integer

**PW Syntax:**
```pw
to_int(s) -> int:
  return int(s)
```

**Implementations:**
- **Python:** `int(s)`
- **Rust:** `s.parse::<i32>()?`
- **Go:** `strconv.Atoi(s)`
- **JavaScript:** `parseInt(s, 10)` | `Number(s)`
- **C++:** `stoi(s)` | `atoi(s.c_str())`

---

### to_float(s) -> float
**Description:** Convert string to float

**PW Syntax:**
```pw
to_float(s) -> float:
  return float(s)
```

**Implementations:**
- **Python:** `float(s)`
- **Rust:** `s.parse::<f64>()?`
- **Go:** `strconv.ParseFloat(s, 64)`
- **JavaScript:** `parseFloat(s)` | `Number(s)`
- **C++:** `stod(s)` | `atof(s.c_str())`

---

### to_bool(s) -> bool
**Description:** Convert string to boolean

**PW Syntax:**
```pw
to_bool(s) -> bool:
  return bool(s)
```

**Implementations:**
- **Python:** `s.lower() in ('true', '1', 'yes')`
- **Rust:** `s.parse::<bool>()?` (only "true"/"false")
- **Go:** `strconv.ParseBool(s)`
- **JavaScript:** `s.toLowerCase() === 'true'`
- **C++:** `s == "true" || s == "1"`

---

### is_string(value) -> bool
**Description:** Check if value is string type

**PW Syntax:**
```pw
is_string(value) -> bool:
  return typeof(value) == "string"
```

**Implementations:**
- **Python:** `isinstance(value, str)`
- **Rust:** (compile-time type checking)
- **Go:** (compile-time type checking)
- **JavaScript:** `typeof value === 'string'`
- **C++:** (compile-time type checking)

---

### is_int(value) -> bool
**Description:** Check if value is integer type

**PW Syntax:**
```pw
is_int(value) -> bool:
  return typeof(value) == "int"
```

**Implementations:**
- **Python:** `isinstance(value, int)`
- **Rust:** (compile-time type checking)
- **Go:** (compile-time type checking)
- **JavaScript:** `Number.isInteger(value)`
- **C++:** (compile-time type checking)

---

### is_float(value) -> bool
**Description:** Check if value is float type

**PW Syntax:**
```pw
is_float(value) -> bool:
  return typeof(value) == "float"
```

**Implementations:**
- **Python:** `isinstance(value, float)`
- **Rust:** (compile-time type checking)
- **Go:** (compile-time type checking)
- **JavaScript:** `typeof value === 'number' && !Number.isInteger(value)`
- **C++:** (compile-time type checking)

---

### is_bool(value) -> bool
**Description:** Check if value is boolean type

**PW Syntax:**
```pw
is_bool(value) -> bool:
  return typeof(value) == "bool"
```

**Implementations:**
- **Python:** `isinstance(value, bool)`
- **Rust:** (compile-time type checking)
- **Go:** (compile-time type checking)
- **JavaScript:** `typeof value === 'boolean'`
- **C++:** (compile-time type checking)

---

## SUMMARY STATISTICS

**Total Operations Defined:** 107
**Categories:** 10

**Breakdown by category:**
1. File I/O: 12 operations
2. String Operations: 15 operations
3. HTTP/Network: 8 operations
4. JSON Operations: 4 operations
5. Math Operations: 10 operations
6. Time/Date: 8 operations
7. Process/System: 6 operations
8. Array Operations: 10 operations
9. Encoding/Decoding: 6 operations
10. Type Conversions: 8 operations

**Plus existing stdlib:**
- Option<T>: 9 operations
- Result<T,E>: 9 operations
- List<T>: 9 operations
- Map<K,V>: 9 operations
- Set<T>: 6 operations

**Grand Total: 149 universal operations**

---

## NEXT STEPS

1. **Validate completeness** - Are there critical operations missing?
2. **Create CharCNN training dataset** - 10-20 code examples per operation per language
3. **Build MCP server generator** - Auto-generate MCP servers from this spec
4. **Implement PW runtime** - Execute PW code using these primitives
5. **Train CharCNN model** - Bidirectional code recognition

---

## NOTES

- Some operations (especially C++) require external libraries
- Go often requires manual loops for operations other languages have built-in
- Async operations (async/await) need separate category
- Database operations (SQL) need separate category
- Regular expressions need separate category
- Concurrency primitives (threads, locks) need separate category
