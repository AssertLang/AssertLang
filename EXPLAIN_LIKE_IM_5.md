# Promptware Explained Simply

## The Big Idea

**You write `.pw` code describing what you want. It builds and runs it in any programming language you choose.**

That's it. That's the whole system.

---

## Real Example

**You write** (in a `.pw` file):
```pw
lang python
start python app.py

file app.py:
  from http.server import BaseHTTPRequestHandler, HTTPServer
  class Handler(BaseHTTPRequestHandler):
      def do_GET(self):
          self.send_response(200)
          self.wfile.write(b'Hello, World!')
  if __name__ == '__main__':
      server = HTTPServer(('127.0.0.1', 8000), Handler)
      server.serve_forever()
```

**Promptware does**:
1. Parses your `.pw` code
2. Creates the `app.py` file
3. Starts the Python server
4. Gives you a URL like `http://localhost:23456/apps/abc123/`
5. When you visit that URL, you see "Hello, World!"

**You did**: Wrote simple `.pw` code
**Promptware did**: Everything else

---

## How It Works (Step by Step)

### Step 1: You Write `.pw` Code

```pw
lang python
start python app.py

file app.py:
  <your Python code here>
```

Simple DSL syntax. No complex build systems needed.

---

### Step 2: Promptware Makes a Plan

The system says "Okay, to build a web service, I need to":
- Write a file called `app.py` with Python code
- Install Flask (a library that makes web servers easy)
- Run the command `python app.py`

This plan is like a recipe. It's the steps needed to make what you asked for.

---

### Step 3: Promptware Writes the Code

The system writes this file:

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(port=8080)
```

You didn't write this. **The system wrote it for you.**

---

### Step 4: Promptware Sets Everything Up

- Creates a folder for your project
- Writes the code file into that folder
- Runs `pip install flask` to get the Flask library
- Makes sure everything is ready to go

---

### Step 5: Promptware Starts Your Application

Runs: `python app.py`

Your web server is now running on port 8080.

---

### Step 6: You Use It

Visit `http://localhost:8080` in your browser.

You see: **Hello, World!**

Done.

---

## What Makes This Special?

### Traditional Way (Without Promptware)

1. You open an editor
2. You write Python code
3. You figure out what library to use
4. You install the library
5. You write more code
6. You test it
7. You fix bugs
8. You run it
9. You test it again
10. Finally it works

**Time**: 30 minutes to 2 hours (if you know Python)

### Promptware Way

1. You type: "Create a web service that responds 'Hello, World!'"
2. Wait 2 seconds
3. It's running

**Time**: 2 seconds

---

## But Wait, It Gets Better

### You Can Build Complex Things Too

**Example 1: API Integration**

You say:
```
"Fetch weather data for San Francisco from OpenWeather API
and save it to a file called weather.json"
```

Promptware:
- Figures out how to call the weather API
- Makes the HTTP request
- Saves the response to a file
- All done

---

**Example 2: Conditional Logic**

You say:
```
"Check if the GitHub repo 'anthropics/claude' has more than 1000 stars.
If yes, send me a notification.
If no, just log it."
```

Promptware:
- Calls GitHub API
- Checks the star count
- Makes a decision (if/else logic)
- Sends notification or logs it

---

**Example 3: Multiple Services Working Together**

You say:
```
"Create a web service that fetches user data from an API,
processes it, and displays a dashboard"
```

Promptware:
- Sets up the web server
- Writes code to call the API
- Writes code to process the data
- Writes code to display it
- Connects all the pieces
- Runs it

---

## The Magic: Multi-Language Support

Here's where it gets really cool.

### Same Task, Different Languages

You can tell Promptware: "Build this in Python"
OR: "Build this in Node.js"
OR: "Build this in Go"
OR: "Build this in Rust"
OR: "Build this in C#"

**Same request, different language, Promptware figures it out.**

Example:
- "Create a file reader tool in Python" → Python code
- "Create a file reader tool in Node" → JavaScript code
- "Create a file reader tool in Go" → Go code

All from the same specification.

---

## Under the Hood (Slightly Technical)

### The Components

**1. Parser**
- Reads your instructions
- Understands what you want
- Creates a structured plan

**2. Interpreter**
- Takes the plan
- Executes each step in order
- Keeps track of what's happening

**3. Runners**
- Handle the actual execution
- Write files to disk
- Install dependencies
- Start processes
- Check if things are running

**4. Tool Adapters**
- Pre-built components for common tasks
- HTTP requests, file operations, data validation, etc.
- Work across multiple programming languages

**5. Timeline Events**
- Like a flight tracker for your code
- Shows you what's happening at each step
- "Started", "Running", "Finished", "Failed"

---

## Real Working Example

Here's what ACTUALLY runs and works today:

```bash
# You run this command
promptware run "Create a web service that responds 'Hello, World!'"

# System output:
Creating plan...
Writing files...
Installing dependencies...
Starting service...
Service ready at http://127.0.0.1:23456/apps/a384d6/

# You visit the URL
# Browser shows: Hello, World!
```

**This actually works. We tested it. It passes.**

---

## What Can You Build With This?

### Easy Things
- Simple web servers
- API clients
- File processors
- Data validators
- Log parsers

### Medium Things
- REST APIs with multiple endpoints
- Data pipelines (fetch → transform → save)
- Monitoring services (check APIs every 5 minutes)
- Webhook receivers

### Complex Things (Future)
- Multi-service applications
- Microservices architectures
- Complex workflows with branching logic
- Systems that adapt based on conditions

---

## The Vision (What We're Building Toward)

### Today (Wave 1-2) ✅
You give simple instructions → Promptware builds and runs it

### Tomorrow (Wave 3-4) 🚧
- More intelligent planning
- Better error handling
- Marketplace of pre-built components
- Even more languages supported

### Future
- "Build me a todo app with user authentication"
  - Promptware builds the entire thing
  - Frontend, backend, database
  - Deploys it
  - Gives you a working URL

- "Add a feature to my app that sends daily email summaries"
  - Promptware modifies your existing app
  - Adds the new feature
  - Redeploys it

---

## Why This Matters

### For Humans
- **Non-programmers** can build software by describing what they want
- **Programmers** can build things 100x faster
- **Everyone** spends less time on boring setup, more time on creative work

### For AI Agents
- Agents can build tools for themselves
- Agents can create complete applications
- Agents can modify and extend existing systems
- Agents become more capable and autonomous

---

## The Name "Promptware"

**Prompt** = Instructions you give (in plain language or DSL)
**Ware** = Software/middleware/firmware (something that runs)

**Promptware** = Turn prompts into runnable software

---

## Current Status

**What works today**:
- ✅ Simple web services (tested, passing)
- ✅ File operations
- ✅ HTTP requests
- ✅ Conditional logic
- ✅ Multi-language support (5 languages)
- ✅ Timeline tracking (see what's happening)

**What's coming soon**:
- 🚧 Natural language understanding (better parsing)
- 🚧 More pre-built components
- 🚧 Security policies (control what code can do)
- 🚧 Component marketplace (share and reuse)

---

## Bottom Line

**Old way**: You write code, you debug code, you deploy code
**New way**: You describe what you want, Promptware does the rest

**Question**: "What do you want to build?"
**Answer**: Just tell Promptware. It'll figure it out.

---

## Try It Yourself

```bash
# Install
git clone https://github.com/promptware/promptware
cd promptware
pip install -e .

# Run
promptware run "Create a web service that responds 'Hello, World!'"

# Visit the URL it gives you
# See "Hello, World!"

# That's it. You just built and deployed a web service.
```

---

**Promptware: Write `.pw` once, run anywhere. From idea to running code in seconds, not hours.**

---

## Note: Natural Language (Future Enhancement)

**Current (Wave 1-2)**: You write `.pw` DSL code with syntax like `lang`, `start`, `file`

**Future (Wave 4+)**: Optional natural language → `.pw` compiler
- You say: "Create a web service that says Hello"
- AI generates the `.pw` code for you
- Promptware runs the `.pw` code

The `.pw` language is the core. Natural language is an optional enhancement.