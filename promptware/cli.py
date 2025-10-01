#!/usr/bin/env python3
"""
Promptware CLI - Command-line interface for the Promptware framework.

Usage:
    promptware generate <file.pw> [--lang LANGUAGE] [--output DIR]
    promptware validate <file.pw>
    promptware test <agent-url> [--auto] [--load] [--coverage]
    promptware list-tools [--lang LANGUAGE]
    promptware init <name> [--template TEMPLATE]
    promptware version
    promptware help [COMMAND]

Commands:
    generate    Generate MCP server from .pw file
    validate    Validate .pw file syntax
    test        Test running MCP agent
    list-tools  List all available tools
    init        Create new .pw agent from template
    version     Show version information
    help        Show help for commands
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Optional, List

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Color support and output utilities
NO_COLOR = os.environ.get('NO_COLOR') is not None or not sys.stdout.isatty()

def colored(text: str, emoji: str = "") -> str:
    """Return text with emoji if colors are enabled."""
    if NO_COLOR:
        return text
    return f"{emoji} {text}" if emoji else text

def success(text: str) -> str:
    """Format success message."""
    return colored(text, "✓")

def error(text: str) -> str:
    """Format error message."""
    return colored(text, "✗")

def info(text: str) -> str:
    """Format info message."""
    return colored(text, "ℹ")

def warning(text: str) -> str:
    """Format warning message."""
    return colored(text, "⚠️")

def confirm_action(message: str, default: bool = False) -> bool:
    """Prompt user for confirmation."""
    suffix = "[Y/n]" if default else "[y/N]"
    response = input(f"{message} {suffix} ").strip().lower()

    if not response:
        return default

    return response in ('y', 'yes')


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser."""
    parser = argparse.ArgumentParser(
        prog='promptware',
        description='Promptware - AI-native MCP agent framework',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate Python MCP server
  promptware generate agent.pw --lang python

  # Generate Go server with custom output directory
  promptware generate agent.pw --lang go --output ./build

  # Validate .pw file syntax
  promptware validate agent.pw

  # List all available tools
  promptware list-tools

  # Create new agent from template
  promptware init my-agent --template basic

For more help: promptware help <command>
        """
    )

    parser.add_argument(
        '--version',
        action='version',
        version='Promptware 1.1.0'
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Generate command
    generate_parser = subparsers.add_parser(
        'generate',
        help='Generate MCP server from .pw file',
        description='Generate a production-ready MCP server in your chosen language.'
    )
    generate_parser.add_argument(
        'file',
        type=str,
        help='.pw agent definition file'
    )
    generate_parser.add_argument(
        '--lang',
        type=str,
        choices=['python', 'nodejs', 'go', 'csharp', 'rust'],
        default='python',
        help='Target language (default: python)'
    )
    generate_parser.add_argument(
        '--output',
        type=str,
        help='Output directory (default: ./generated/<agent-name>)'
    )
    generate_parser.add_argument(
        '--build',
        action='store_true',
        help='Build the server after generation (for compiled languages)'
    )
    generate_parser.add_argument(
        '--yes', '-y',
        action='store_true',
        help='Skip confirmation prompts'
    )
    generate_parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be generated without writing files'
    )
    generate_parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Minimal output (for CI/scripts)'
    )

    # Validate command
    validate_parser = subparsers.add_parser(
        'validate',
        help='Validate .pw file syntax',
        description='Check .pw file for syntax errors and structural issues.'
    )
    validate_parser.add_argument(
        'file',
        type=str,
        help='.pw agent definition file'
    )
    validate_parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed validation output'
    )

    # Test command
    test_parser = subparsers.add_parser(
        'test',
        help='Test running MCP agent',
        description='Run integration and load tests against a running MCP agent.'
    )
    test_parser.add_argument(
        'agent_url',
        type=str,
        help='Agent URL (e.g., http://localhost:3000)'
    )
    test_parser.add_argument(
        '--auto',
        action='store_true',
        help='Auto-generate test fixtures from agent verbs'
    )
    test_parser.add_argument(
        '--load',
        action='store_true',
        help='Run load tests'
    )
    test_parser.add_argument(
        '--verb',
        type=str,
        help='Specific verb to load test (requires --load)'
    )
    test_parser.add_argument(
        '--requests',
        type=int,
        default=100,
        help='Number of load test requests (default: 100)'
    )
    test_parser.add_argument(
        '--concurrency',
        type=int,
        default=10,
        help='Concurrent requests for load testing (default: 10)'
    )
    test_parser.add_argument(
        '--coverage',
        action='store_true',
        help='Export coverage report to coverage.json'
    )
    test_parser.add_argument(
        '--timeout',
        type=int,
        default=30,
        help='Request timeout in seconds (default: 30)'
    )

    # List-tools command
    list_tools_parser = subparsers.add_parser(
        'list-tools',
        help='List all available tools',
        description='Display all tools that can be used in .pw agents.'
    )
    list_tools_parser.add_argument(
        '--lang',
        type=str,
        choices=['python', 'nodejs', 'go', 'csharp', 'rust', 'all'],
        default='all',
        help='Show tools for specific language (default: all)'
    )
    list_tools_parser.add_argument(
        '--category',
        type=str,
        help='Filter by category (http, auth, storage, etc.)'
    )

    # Init command
    init_parser = subparsers.add_parser(
        'init',
        help='Create new .pw agent from template',
        description='Initialize a new Promptware agent project.'
    )
    init_parser.add_argument(
        'name',
        type=str,
        help='Agent name'
    )
    init_parser.add_argument(
        '--template',
        type=str,
        choices=['basic', 'api', 'workflow', 'ai'],
        default='basic',
        help='Agent template (default: basic)'
    )
    init_parser.add_argument(
        '--port',
        type=int,
        default=3000,
        help='Server port (default: 3000)'
    )

    # Config command
    config_parser = subparsers.add_parser(
        'config',
        help='Manage configuration',
        description='View and modify Promptware configuration.'
    )
    config_subparsers = config_parser.add_subparsers(dest='config_action', help='Config actions')

    # config set
    config_set = config_subparsers.add_parser('set', help='Set configuration value')
    config_set.add_argument('key', help='Configuration key (e.g., defaults.language)')
    config_set.add_argument('value', help='Configuration value')
    config_set.add_argument('--project', action='store_true', help='Set in project config instead of global')

    # config get
    config_get = config_subparsers.add_parser('get', help='Get configuration value')
    config_get.add_argument('key', help='Configuration key')

    # config unset
    config_unset = config_subparsers.add_parser('unset', help='Remove configuration value')
    config_unset.add_argument('key', help='Configuration key')
    config_unset.add_argument('--project', action='store_true', help='Remove from project config instead of global')

    # config list
    config_subparsers.add_parser('list', help='List all configuration values')

    # config edit
    config_edit = config_subparsers.add_parser('edit', help='Open config file in editor')
    config_edit.add_argument('--project', action='store_true', help='Edit project config instead of global')

    # config path
    config_path = config_subparsers.add_parser('path', help='Show config file path')
    config_path.add_argument('--project', action='store_true', help='Show project config path')

    # Help command
    help_parser = subparsers.add_parser(
        'help',
        help='Show help for commands'
    )
    help_parser.add_argument(
        'topic',
        type=str,
        nargs='?',
        help='Command to get help for'
    )

    return parser


def cmd_generate(args) -> int:
    """Execute generate command."""
    from language.agent_parser import parse_agent_pw
    from language.mcp_server_generator import generate_python_mcp_server
    from language.mcp_server_generator_nodejs import generate_nodejs_mcp_server
    from language.mcp_server_generator_go import generate_go_mcp_server
    from language.mcp_server_generator_dotnet import generate_dotnet_mcp_server
    from language.mcp_server_generator_rust import generate_rust_mcp_server
    from promptware.config import get_config

    # Load config for defaults
    config = get_config()

    # Apply config defaults if not specified
    if not hasattr(args, 'lang') or args.lang == 'python':  # 'python' is argparse default
        configured_lang = config.get('defaults.language', 'python')
        args.lang = configured_lang

    if hasattr(args, 'yes') and not args.yes:
        args.yes = config.get('generate.auto_confirm', False)

    # Validate file exists
    pw_file = Path(args.file)
    if not pw_file.exists():
        print(error(f"File not found: {args.file}"), file=sys.stderr)
        return 1

    # Read and parse .pw file
    if not args.quiet:
        print(colored("Reading " + pw_file.name + "...", "📖"))

    try:
        pw_code = pw_file.read_text()
        agent = parse_agent_pw(pw_code)
    except Exception as e:
        print(error(f"Parse error: {e}"), file=sys.stderr)
        return 1

    if not args.quiet:
        print(success(f"Parsed agent: {agent.name}"))
        print(f"  Port: {agent.port}")
        print(f"  Verbs: {len(agent.exposes)}")
        print(f"  Tools: {len(agent.tools) if agent.tools else 0}")

    # Determine output directory
    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = Path(f"./generated/{agent.name}")

    # Generate server code
    generators = {
        'python': (generate_python_mcp_server, f'{agent.name}_server.py'),
        'nodejs': (generate_nodejs_mcp_server, f'{agent.name}_server.js'),
        'go': (generate_go_mcp_server, 'main.go'),
        'csharp': (generate_dotnet_mcp_server, 'Program.cs'),
        'rust': (generate_rust_mcp_server, 'main.rs'),
    }

    generator_func, filename = generators[args.lang]
    server_code = generator_func(agent)

    # Prepare file list
    files_to_create = []
    output_file = output_dir / filename
    files_to_create.append((output_file, server_code))

    # Language-specific files
    if args.lang == 'python':
        requirements = [
            "fastapi",
            "uvicorn[standard]",
            "slowapi",
            "python-multipart"
        ]
        if agent.llm:
            requirements.extend(["langchain", "langchain-anthropic"])
        if agent.observability:
            requirements.extend([
                "opentelemetry-api",
                "opentelemetry-sdk",
                "opentelemetry-instrumentation-fastapi"
            ])

        req_file = output_dir / "requirements.txt"
        files_to_create.append((req_file, "\n".join(requirements)))

    elif args.lang == 'nodejs':
        import json
        package_json = {
            "name": agent.name,
            "version": "1.0.0",
            "type": "module",
            "main": filename,
            "dependencies": {
                "express": "^4.18.0",
                "helmet": "^7.0.0",
                "cors": "^2.8.5",
                "express-rate-limit": "^6.0.0",
                "winston": "^3.10.0"
            }
        }

        pkg_file = output_dir / "package.json"
        files_to_create.append((pkg_file, json.dumps(package_json, indent=2)))

    # Dry-run mode - show what would be created
    if args.dry_run:
        print(colored("\nDry-run mode - no files will be written", "ℹ"))
        print(f"\nWould create in: {output_dir.absolute()}")
        for file_path, content in files_to_create:
            print(f"  {success('')} {file_path.name} ({len(content)} bytes, {len(content.splitlines())} lines)")
        return 0

    # Confirmation prompt (unless --yes)
    if not args.yes:
        print(f"\n{colored('Will create:', 'ℹ')}")
        print(f"  Output directory: {output_dir.absolute()}")
        for file_path, content in files_to_create:
            print(f"  • {file_path.name} ({len(content.splitlines())} lines)")

        if not confirm_action("\nProceed?", default=True):
            print("Cancelled.")
            return 0

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write files
    if not args.quiet:
        print(f"\n{colored('Generating ' + args.lang + ' server...', '🔨')}")

    for file_path, content in files_to_create:
        file_path.write_text(content)
        if not args.quiet:
            print(success(f"Created: {file_path.name}"))

    # Auto-install dependencies (Python and Node.js)
    if args.lang == 'python' and (output_dir / 'requirements.txt').exists():
        if not args.quiet:
            if args.yes or confirm_action("\nInstall Python dependencies now?", default=True):
                print(colored("Installing dependencies...", "📦"))
                import subprocess
                result = subprocess.run(
                    ['pip', 'install', '-q', '-r', 'requirements.txt'],
                    cwd=output_dir,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    print(success("Dependencies installed!"))
                else:
                    print(error(f"Failed to install dependencies: {result.stderr}"))
                    print("You can install manually with: pip install -r requirements.txt")

    elif args.lang == 'nodejs' and (output_dir / 'package.json').exists():
        if not args.quiet:
            if args.yes or confirm_action("\nInstall Node.js dependencies now?", default=True):
                print(colored("Installing dependencies...", "📦"))
                import subprocess
                result = subprocess.run(
                    ['npm', 'install'],
                    cwd=output_dir,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    print(success("Dependencies installed!"))
                else:
                    print(error(f"Failed to install dependencies: {result.stderr}"))
                    print("You can install manually with: npm install")

    # Show next steps
    if not args.quiet:
        print(f"\n{colored('Next steps:', '📦')}")

        if args.lang == 'python':
            print(f"  cd {output_dir}")
            print("  pip install -r requirements.txt")
            print(f"  python {filename}")

        elif args.lang == 'nodejs':
            print(f"  cd {output_dir}")
            print("  npm install")
            print(f"  node {filename}")

        elif args.lang in ['go', 'csharp', 'rust']:
            print(f"  cd {project_root}")
            if args.lang == 'go':
                print(f"  python3 scripts/build_server.py {pw_file} go")
            elif args.lang == 'csharp':
                print(f"  python3 scripts/build_server.py {pw_file} dotnet")
            elif args.lang == 'rust':
                print(f"  python3 scripts/build_server.py {pw_file} rust")

        print(f"\n{colored('Server generated successfully!', '✨')}")
        print(f"{colored('Output:', '📂')} {output_dir.absolute()}")

    return 0


def cmd_validate(args) -> int:
    """Execute validate command."""
    from language.agent_parser import parse_agent_pw

    pw_file = Path(args.file)
    if not pw_file.exists():
        print(f"✗ Error: File not found: {args.file}", file=sys.stderr)
        return 1

    print(f"🔍 Validating {pw_file.name}...")

    try:
        pw_code = pw_file.read_text()
        agent = parse_agent_pw(pw_code)

        print("✓ Syntax valid")

        if args.verbose:
            print(f"\n📋 Agent Details:")
            print(f"  Name: {agent.name}")
            print(f"  Port: {agent.port}")
            print(f"  Verbs: {len(agent.exposes)}")
            for expose in agent.exposes:
                print(f"    - {expose.verb} ({len(expose.params)} params, {len(expose.returns)} returns)")

            if agent.tools:
                print(f"  Tools: {', '.join(agent.tools)}")

            if agent.llm:
                print(f"  LLM: {agent.llm}")

            if agent.observability:
                print(f"  Observability:")
                if agent.observability.traces:
                    print(f"    - Traces enabled")
                if agent.observability.metrics:
                    print(f"    - Metrics enabled")

        return 0

    except Exception as e:
        print(f"✗ Validation failed: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def cmd_test(args) -> int:
    """Execute test command."""
    from promptware.testing import AgentTester

    print(f"🧪 Testing agent at {args.agent_url}\n")

    # Create tester
    tester = AgentTester(args.agent_url, timeout=args.timeout)

    # Health check first
    if not tester.health_check(verbose=True):
        print("\n✗ Health check failed - agent may not be running", file=sys.stderr)
        return 1

    print()

    # Discover verbs
    try:
        verbs = tester.discover_verbs()
        print(f"✓ Discovered {len(verbs)} verbs\n")
    except Exception as e:
        print(f"✗ Failed to discover verbs: {e}", file=sys.stderr)
        return 1

    # Run integration tests
    if args.auto:
        try:
            summary = tester.run_integration_tests(verbose=True)
            if summary['failed'] > 0:
                print("\n⚠️  Some tests failed", file=sys.stderr)
                return 1
        except Exception as e:
            print(f"\n✗ Integration tests failed: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            return 1

    # Run load tests
    if args.load:
        if not args.verb:
            print("✗ --verb required for load testing", file=sys.stderr)
            return 1

        print(f"\n{'='*60}")
        print(f"Load Testing: {args.verb}")
        print(f"{'='*60}\n")

        # Generate sample params from verb schema
        verb_schema = None
        for v in verbs:
            if v['name'] == args.verb:
                verb_schema = v
                break

        if not verb_schema:
            print(f"✗ Verb not found: {args.verb}", file=sys.stderr)
            return 1

        # Generate test params
        input_schema = verb_schema.get('inputSchema', {})
        properties = input_schema.get('properties', {})
        test_params = tester._generate_test_data(properties, input_schema.get('required', []))

        try:
            result = tester.run_load_test(
                args.verb,
                test_params,
                num_requests=args.requests,
                concurrency=args.concurrency,
                verbose=True
            )

            if result.failed > result.successful:
                print("\n⚠️  Load test had more failures than successes", file=sys.stderr)
                return 1

        except Exception as e:
            print(f"\n✗ Load test failed: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            return 1

    # Export coverage report
    if args.coverage:
        try:
            tester.export_coverage_report()
        except Exception as e:
            print(f"✗ Failed to export coverage report: {e}", file=sys.stderr)
            return 1

    print("\n✨ Testing complete!")
    return 0


def cmd_list_tools(args) -> int:
    """Execute list-tools command."""
    tools_dir = project_root / "tools"

    if not tools_dir.exists():
        print("✗ Error: Tools directory not found", file=sys.stderr)
        return 1

    print(f"🛠️  Available Promptware Tools\n")

    # Scan tools directory
    tool_dirs = sorted([d for d in tools_dir.iterdir() if d.is_dir() and not d.name.startswith('__')])

    # Categorize tools
    categories = {
        'HTTP & APIs': ['http', 'rest', 'api-auth'],
        'Authentication': ['auth', 'encryption'],
        'Storage & Data': ['storage', 'validate-data', 'transform'],
        'Flow Control': ['conditional', 'branch', 'loop', 'async', 'thread'],
        'Logging & Monitoring': ['logger', 'tracer', 'error-log'],
        'Scheduling': ['scheduler', 'timing'],
        'Media': ['media-control'],
        'System': ['plugin-manager', 'marketplace-uploader', 'error', 'input', 'output']
    }

    # Reverse lookup
    tool_to_category = {}
    for category, tools in categories.items():
        for tool in tools:
            tool_to_category[tool] = category

    if args.category:
        # Filter by category
        matching_tools = categories.get(args.category, [])
        tool_dirs = [d for d in tool_dirs if d.name in matching_tools]

    # Group by category
    categorized = {}
    for tool_dir in tool_dirs:
        category = tool_to_category.get(tool_dir.name, 'Other')
        if category not in categorized:
            categorized[category] = []
        categorized[category].append(tool_dir.name)

    # Display tools
    total_tools = 0
    for category in sorted(categorized.keys()):
        tools = categorized[category]
        print(f"📦 {category}")
        for tool in sorted(tools):
            # Check language support
            adapters_dir = tools_dir / tool / "adapters"
            languages = []
            if (adapters_dir / "adapter.py").exists():
                languages.append("python")
            if (adapters_dir / "adapter_node.js").exists():
                languages.append("nodejs")
            if (adapters_dir / "adapter_go.go").exists():
                languages.append("go")
            if (adapters_dir / "Adapter.cs").exists():
                languages.append("csharp")
            if (adapters_dir / "adapter_rust.rs").exists():
                languages.append("rust")

            lang_display = ", ".join(languages) if languages else "no adapters"

            if args.lang != 'all' and args.lang not in languages:
                continue

            print(f"  • {tool:<25} [{lang_display}]")
            total_tools += 1
        print()

    print(f"Total: {total_tools} tools")

    if args.lang != 'all':
        print(f"(Filtered by language: {args.lang})")

    return 0


def cmd_init(args) -> int:
    """Execute init command."""
    templates = {
        'basic': """agent {args.name}

port {args.port}

expose task.execute@v1 (
    task: string
) -> (
    result: string
)
""",
        'api': """agent {args.name}

port {args.port}

tools: http, auth, logger

expose api.call@v1 (
    endpoint: string,
    method: string
) -> (
    response: object,
    status: int
)
""",
        'workflow': """agent {args.name}

port {args.port}

tools: scheduler, async, logger

expose workflow.start@v1 (
    workflow_id: string,
    params: object
) -> (
    execution_id: string,
    status: string
)
""",
        'ai': """agent {args.name}

port {args.port}

llm: anthropic claude-3-5-sonnet-20241022

prompt: "You are a helpful AI assistant."

expose chat.message@v1 (
    message: string
) -> (
    response: string
)
"""
    }

    template_code = templates[args.template].format(args=args)

    output_file = Path(f"{args.name}.pw")
    if output_file.exists():
        print(f"✗ Error: File already exists: {output_file}", file=sys.stderr)
        return 1

    output_file.write_text(template_code)
    print(f"✓ Created: {output_file}")
    print(f"\n📝 Next steps:")
    print(f"  1. Edit {output_file} to customize your agent")
    print(f"  2. Validate: promptware validate {output_file}")
    print(f"  3. Generate: promptware generate {output_file} --lang python")

    return 0


def cmd_config(args) -> int:
    """Execute config command."""
    from promptware.config import get_config
    import subprocess

    config = get_config()

    if not args.config_action:
        print("Usage: promptware config <action>")
        print("\nActions:")
        print("  set <key> <value>    Set configuration value")
        print("  get <key>            Get configuration value")
        print("  unset <key>          Remove configuration value")
        print("  list                 List all configuration")
        print("  edit                 Open config file in editor")
        print("  path                 Show config file path")
        print("\nExamples:")
        print("  promptware config set defaults.language go")
        print("  promptware config get defaults.language")
        print("  promptware config list")
        return 1

    if args.config_action == 'set':
        # Parse value type
        value = args.value
        if value.lower() == 'true':
            value = True
        elif value.lower() == 'false':
            value = False
        elif value.isdigit():
            value = int(value)

        config.set(args.key, value, project=args.project)

        scope = "project" if args.project else "global"
        print(success(f"Set {args.key} = {value} ({scope})"))

    elif args.config_action == 'get':
        value = config.get(args.key)
        if value is not None:
            print(value)
        else:
            print(error(f"Key not found: {args.key}"), file=sys.stderr)
            return 1

    elif args.config_action == 'unset':
        config.unset(args.key, project=args.project)

        scope = "project" if args.project else "global"
        print(success(f"Unset {args.key} ({scope})"))

    elif args.config_action == 'list':
        import json
        print(json.dumps(config.list_all(), indent=2))

    elif args.config_action == 'edit':
        config_file = config.get_config_file(project=args.project)

        # Create file if it doesn't exist
        if not config_file.exists():
            config_file.parent.mkdir(parents=True, exist_ok=True)
            config_file.write_text("# Promptware configuration\n")

        # Open in editor
        editor = os.environ.get('EDITOR', 'nano')
        try:
            subprocess.run([editor, str(config_file)], check=True)
        except Exception as e:
            print(error(f"Failed to open editor: {e}"), file=sys.stderr)
            print(f"Edit manually: {config_file}")
            return 1

    elif args.config_action == 'path':
        config_file = config.get_config_file(project=args.project)
        print(config_file)

    return 0


def cmd_help(args) -> int:
    """Execute help command."""
    help_topics = {
        'generate': """
Generate MCP server from .pw file

Usage: promptware generate <file.pw> [OPTIONS]

Options:
  --lang LANGUAGE     Target language (python, nodejs, go, csharp, rust)
  --output DIR        Output directory
  --build             Build the server after generation

Examples:
  promptware generate agent.pw --lang python
  promptware generate agent.pw --lang go --output ./build --build
""",
        'validate': """
Validate .pw file syntax

Usage: promptware validate <file.pw> [OPTIONS]

Options:
  --verbose          Show detailed validation output

Examples:
  promptware validate agent.pw
  promptware validate agent.pw --verbose
""",
        'test': """
Test running MCP agent

Usage: promptware test <agent-url> [OPTIONS]

Options:
  --auto             Auto-generate and run integration tests
  --load             Run load tests (requires --verb)
  --verb VERB        Specific verb to load test
  --requests NUM     Number of load test requests (default: 100)
  --concurrency NUM  Concurrent requests (default: 10)
  --coverage         Export coverage report to coverage.json
  --timeout SEC      Request timeout in seconds (default: 30)

Examples:
  # Health check and verb discovery
  promptware test http://localhost:3000

  # Run auto-generated integration tests
  promptware test http://localhost:3000 --auto

  # Load test a specific verb
  promptware test http://localhost:3000 --load --verb user.create@v1 --requests 1000

  # Full test with coverage report
  promptware test http://localhost:3000 --auto --coverage
""",
        'list-tools': """
List all available tools

Usage: promptware list-tools [OPTIONS]

Options:
  --lang LANGUAGE    Show tools for specific language
  --category CAT     Filter by category

Examples:
  promptware list-tools
  promptware list-tools --lang python
  promptware list-tools --category "HTTP & APIs"
""",
        'init': """
Create new .pw agent from template

Usage: promptware init <name> [OPTIONS]

Options:
  --template TYPE    Agent template (basic, api, workflow, ai)
  --port PORT        Server port (default: 3000)

Examples:
  promptware init my-agent
  promptware init api-agent --template api --port 8080
"""
    }

    if args.topic:
        if args.topic in help_topics:
            print(help_topics[args.topic])
        else:
            print(f"No help available for: {args.topic}", file=sys.stderr)
            return 1
    else:
        print(__doc__)

    return 0


def main():
    """Main CLI entry point."""
    parser = create_parser()

    if len(sys.argv) == 1:
        parser.print_help()
        return 0

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    # Route to command handlers
    commands = {
        'generate': cmd_generate,
        'validate': cmd_validate,
        'test': cmd_test,
        'list-tools': cmd_list_tools,
        'init': cmd_init,
        'config': cmd_config,
        'help': cmd_help,
    }

    handler = commands.get(args.command)
    if handler:
        return handler(args)
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
