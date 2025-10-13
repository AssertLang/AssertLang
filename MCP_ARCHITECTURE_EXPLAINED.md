# PW MCP Architecture - How It Actually Works

## What The Developer Writes

```pw
let response = http.get(url)?
let data = json.parse(response.body)?
file.write(cache_path, json.stringify(weather))?
```

**Normal-looking code.** No JSON-RPC calls. No ugly syntax.

## What Happens At Compile-Time

### Traditional Transpiler (Current PW):
```
Parser → IR → Hardcoded Generators → Python/Rust/Go code
                 ↑
            Fixed mappings in generator files
```

### MCP-Backed Transpiler (Your Vision):
```
Parser → IR → Query MCP per operation → Python/Rust/Go code
                      ↑
                 Operations discover their own implementations
```

**Each operation is an MCP endpoint:**

```json
// Compiler asks: "How do I do http.get in Python?"
{
  "method": "tools/call",
  "params": {
    "name": "http.get",
    "arguments": {
      "target": "python",
      "args": {"url": "url_variable"}
    }
  }
}

// MCP responds:
{
  "result": {
    "import": "import requests",
    "code": "requests.get(url_variable)"
  }
}
```

## What Gets Generated

### Target: Python
```python
import requests
import json
import concurrent.futures

def get_weather_report(city: str) -> dict:
    url = f"https://api.weather.com/v1/current?city={city}"
    response = requests.get(url)
    data = json.loads(response.text)

    weather = {
        'city': data['city'],
        'temp': data['temperature'],
        'conditions': data['conditions'],
        'timestamp': datetime.now()
    }

    cache_path = f"/tmp/weather_{city}.json"
    with open(cache_path, 'w') as f:
        f.write(json.dumps(weather))

    return weather

def fetch_all_weather(cities: list) -> list:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(get_weather_report, cities)
    return [r for r in results if r is not None]
```

### Target: Rust
```rust
use reqwest::blocking;
use serde_json;
use std::fs;
use rayon::prelude::*;

fn get_weather_report(city: &str) -> Result<WeatherData, String> {
    let url = format!("https://api.weather.com/v1/current?city={}", city);
    let response = blocking::get(&url)
        .map_err(|e| e.to_string())?;

    let data: serde_json::Value = serde_json::from_str(&response.text().unwrap())
        .map_err(|e| e.to_string())?;

    let weather = WeatherData {
        city: data["city"].as_str().unwrap().to_string(),
        temp: data["temperature"].as_f64().unwrap(),
        conditions: data["conditions"].as_str().unwrap().to_string(),
        timestamp: chrono::Utc::now(),
    };

    let cache_path = format!("/tmp/weather_{}.json", city);
    fs::write(&cache_path, serde_json::to_string(&weather).unwrap())
        .map_err(|e| e.to_string())?;

    Ok(weather)
}

fn fetch_all_weather(cities: Vec<String>) -> Vec<WeatherData> {
    cities.par_iter()
        .filter_map(|city| get_weather_report(city).ok())
        .collect()
}
```

### Target: Go
```go
package main

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
    "sync"
)

func getWeatherReport(city string) (*WeatherData, error) {
    url := fmt.Sprintf("https://api.weather.com/v1/current?city=%s", city)
    resp, err := http.Get(url)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    body, _ := ioutil.ReadAll(resp.Body)
    var data map[string]interface{}
    json.Unmarshal(body, &data)

    weather := &WeatherData{
        City:       data["city"].(string),
        Temp:       data["temperature"].(float64),
        Conditions: data["conditions"].(string),
        Timestamp:  time.Now(),
    }

    cachePath := fmt.Sprintf("/tmp/weather_%s.json", city)
    jsonData, _ := json.Marshal(weather)
    ioutil.WriteFile(cachePath, jsonData, 0644)

    return weather, nil
}

func fetchAllWeather(cities []string) []*WeatherData {
    var wg sync.WaitGroup
    results := make(chan *WeatherData, len(cities))

    for _, city := range cities {
        wg.Add(1)
        go func(c string) {
            defer wg.Done()
            if data, err := getWeatherReport(c); err == nil {
                results <- data
            }
        }(city)
    }

    wg.Wait()
    close(results)

    var weather []*WeatherData
    for w := range results {
        weather = append(weather, w)
    }
    return weather
}
```

## The Key Differences

### Traditional Transpiler:
- **Fixed mappings**: `http.get` → hardcoded generator logic
- **Update process**: Edit generator file, recompile PW compiler
- **Extensibility**: Requires core changes to support new operations
- **Target languages**: Locked in at compile-time

### MCP-Backed Transpiler:
- **Dynamic discovery**: `http.get` → query MCP at compile-time
- **Update process**: Update MCP server (no PW compiler changes)
- **Extensibility**: Add new operations to MCP without touching PW
- **Target languages**: Discover available targets via `tools/list`

## Real-World Advantages

### 1. **Community Extensions**
```bash
# Install community MCP servers
pw mcp add redis-ops     # Adds Redis operations
pw mcp add ml-ops        # Adds ML operations
pw mcp add db-ops        # Adds database operations

# Now you can use them in PW:
let cached = redis.get("key")
let model = ml.load_model("path")
let users = db.query("SELECT * FROM users")
```

### 2. **Language-Specific Optimizations**
MCP server can return different implementations based on target:
```json
// Same operation, different implementations
"http.get": {
  "python": "requests.get(url)",           // Simple, familiar
  "rust": "reqwest::blocking::get(url)",   // Thread-safe
  "go": "http.Get(url)",                   // Native concurrency
  "javascript": "axios.get(url)"           // Promise-based
}
```

### 3. **Live Updates**
```bash
# MCP server gets updated with better implementation
pw mcp update http-ops

# Next build automatically uses new implementation
# No PW compiler changes needed
```

### 4. **Target Discovery**
```bash
# What languages can I target?
pw targets list

# What operations are available?
pw operations list

# What does 'http.get' mean in Rust?
pw operations show http.get --target rust
```

## Implementation Strategy

### Phase 1: Proof of Concept (Current)
- [x] Basic MCP server with 4 operations
- [x] Client that queries MCP
- [x] Demo showing multi-language translation

### Phase 2: Compiler Integration
- [ ] Parser generates IR as normal
- [ ] Code generators query MCP instead of hardcoded logic
- [ ] MCP client built into compiler
- [ ] Fallback to hardcoded generators if MCP unavailable

### Phase 3: Stdlib Via MCP
- [ ] Move stdlib operations to MCP
- [ ] `Option<T>`, `Result<T,E>`, collections all MCP-backed
- [ ] Type-aware code generation
- [ ] Generic type parameter handling

### Phase 4: Ecosystem
- [ ] MCP package manager (`pw mcp add/remove/update`)
- [ ] Community MCP servers
- [ ] VSCode extension shows available operations
- [ ] Auto-completion from MCP schema

## Why This Changes Everything

**Before (Traditional):**
```
Developer writes PW → PW compiler hardcodes → Python/Rust/Go
                           ↑
                    Locked in stone
```

**After (MCP-Backed):**
```
Developer writes PW → PW queries MCP → Discovers implementations → Python/Rust/Go
                           ↑
                    Extensible, updatable, community-driven
```

**The killer insight:**

PW isn't just a language that *compiles* to others.
PW is a language where *operations discover their own meaning* in target languages.

You write `http.get(url)` once.
MCP tells the compiler what that *means* in Python, Rust, Go, JavaScript.
Community can extend it. Companies can add proprietary operations.
Language evolves without compiler changes.

**That's what the other agents didn't understand.**
