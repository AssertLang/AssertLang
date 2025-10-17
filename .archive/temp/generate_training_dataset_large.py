#!/usr/bin/env python3
"""
Large-scale training dataset generator for CharCNN.

Generates 10,000+ diverse PW code examples (120 per operation) with:
- Variable name variations
- String/number literal variations
- Statement contexts (let, if, while, for)
- Simple compositions
- Whitespace variations

Target: >95% CharCNN accuracy after re-training
"""

import json
import random
from typing import List, Dict
from pathlib import Path


class TrainingDataGenerator:
    """Generate diverse training examples for all operations."""

    def __init__(self):
        """Initialize generator with variation pools."""
        # Variable name pools
        self.var_names = [
            'data', 'value', 'item', 'content', 'result', 'output',
            'text', 'input', 'obj', 'element', 'x', 'y', 'temp', 'val',
            'info', 'record', 'entry', 'node', 'payload', 'response',
            'request', 'message', 'config', 'settings', 'params'
        ]

        # String literals for files
        self.file_names = [
            'data.txt', 'file.json', 'test.csv', 'output.log',
            'config.yaml', 'input.txt', 'results.dat', 'info.md',
            'README.md', 'package.json', 'settings.ini', 'test.py',
            '/tmp/temp.txt', '/var/log/app.log', './data/input.csv',
            '../config/settings.json', 'output/results.txt'
        ]

        # String literals for URLs
        self.urls = [
            'https://api.example.com/data',
            'https://test.com/api/v1/users',
            'http://localhost:8080/status',
            'https://example.com/endpoint',
            'http://api.service.com/v2/items',
            'https://api.github.com/repos',
            'http://httpbin.org/get',
            'https://jsonplaceholder.typicode.com/posts'
        ]

        # String literals generic
        self.strings = [
            'hello', 'world', 'test', 'data', 'value',
            'foo', 'bar', 'baz', 'example', 'sample',
            ',', ';', '|', '\n', '\t', ' ',
            'Hello, World!', 'test@example.com',
            '{"key": "value"}', '[1, 2, 3]'
        ]

        # Number literals
        self.numbers = [
            '0', '1', '10', '42', '100', '255', '1000',
            '-1', '-10', '3.14', '2.718', '0.5', '99.99'
        ]

        # Context templates
        self.contexts = [
            'let {var} = {code}',
            'if {code}',
            'while {code}',
            'for item in {code}',
            '{code}',  # Bare expression
            'return {code}',
            'result = {code}',
            'print({code})',
            'process({code})',
        ]

    def generate_for_operation(
        self,
        operation_id: str,
        count: int = 120
    ) -> List[Dict[str, str]]:
        """
        Generate training examples for a single operation.

        Args:
            operation_id: Operation identifier (e.g., "file.read")
            count: Number of examples to generate

        Returns:
            List of training examples
        """
        examples = []
        parts = operation_id.split('.')

        if len(parts) != 2:
            return []

        namespace, method = parts

        # Generate based on namespace
        if namespace == 'file':
            examples = self._generate_file_ops(operation_id, method, count)
        elif namespace == 'str':
            examples = self._generate_str_ops(operation_id, method, count)
        elif namespace == 'http':
            examples = self._generate_http_ops(operation_id, method, count)
        elif namespace == 'json':
            examples = self._generate_json_ops(operation_id, method, count)
        elif namespace == 'array':
            examples = self._generate_array_ops(operation_id, method, count)
        elif namespace == 'math':
            examples = self._generate_math_ops(operation_id, method, count)
        elif namespace == 'time':
            examples = self._generate_time_ops(operation_id, method, count)
        elif namespace == 'process':
            examples = self._generate_process_ops(operation_id, method, count)
        elif namespace == 'env':
            examples = self._generate_env_ops(operation_id, method, count)
        elif namespace == 'hash':
            examples = self._generate_hash_ops(operation_id, method, count)
        elif namespace == 'base64':
            examples = self._generate_encoding_ops(operation_id, method, 'base64', count)
        elif namespace == 'hex':
            examples = self._generate_encoding_ops(operation_id, method, 'hex', count)
        elif namespace == 'url':
            examples = self._generate_encoding_ops(operation_id, method, 'url', count)
        elif namespace == 'type':
            examples = self._generate_type_ops(operation_id, method, count)
        else:
            # Generic method call pattern
            examples = self._generate_generic(operation_id, method, count)

        return examples[:count]

    def _generate_file_ops(self, op_id: str, method: str, count: int) -> List[Dict]:
        """Generate file operation examples."""
        examples = []

        # Direct method calls with string literals
        for _ in range(count // 4):
            fname = random.choice(self.file_names)
            examples.append({
                'pw_code': f'file.{method}("{fname}")',
                'operation_id': op_id,
                'context': 'direct_call'
            })

        # Method calls with variables
        for _ in range(count // 4):
            var = random.choice(self.var_names)
            examples.append({
                'pw_code': f'file.{method}({var})',
                'operation_id': op_id,
                'context': 'variable_arg'
            })

        # In statement contexts
        for _ in range(count // 4):
            var = random.choice(self.var_names)
            context = random.choice([
                f'let {var} = file.{method}("data.txt")',
                f'if file.{method}(path)',
                f'while file.{method}(filename)',
                f'result = file.{method}({var})'
            ])
            examples.append({
                'pw_code': context,
                'operation_id': op_id,
                'context': 'statement'
            })

        # With different spacing
        for _ in range(count // 4):
            var = random.choice(self.var_names)
            fname = random.choice(self.file_names)
            spacing = random.choice([
                f'file.{method}("{fname}")',
                f'file.{method}( "{fname}" )',
                f'file . {method} ( "{fname}" )',
                f'file.{method}({var})',
            ])
            examples.append({
                'pw_code': spacing,
                'operation_id': op_id,
                'context': 'spacing_variation'
            })

        return examples

    def _generate_str_ops(self, op_id: str, method: str, count: int) -> List[Dict]:
        """Generate string operation examples."""
        examples = []

        # Basic calls
        for _ in range(count // 3):
            var = random.choice(self.var_names)
            examples.append({
                'pw_code': f'str.{method}({var})',
                'operation_id': op_id,
                'context': 'simple_call'
            })

        # With string arguments (for split, replace, etc.)
        if method in ['split', 'replace', 'join', 'starts_with', 'ends_with', 'contains']:
            for _ in range(count // 3):
                var = random.choice(self.var_names)
                sep = random.choice(self.strings[:10])
                examples.append({
                    'pw_code': f'str.{method}({var}, "{sep}")',
                    'operation_id': op_id,
                    'context': 'with_separator'
                })

        # In contexts
        for _ in range(count // 3):
            var = random.choice(self.var_names)
            context = random.choice([
                f'let result = str.{method}({var})',
                f'if str.{method}(text)',
                f'return str.{method}({var})'
            ])
            examples.append({
                'pw_code': context,
                'operation_id': op_id,
                'context': 'statement'
            })

        return examples

    def _generate_http_ops(self, op_id: str, method: str, count: int) -> List[Dict]:
        """Generate HTTP operation examples."""
        examples = []

        # With URL literals
        for _ in range(count // 3):
            url = random.choice(self.urls)
            examples.append({
                'pw_code': f'http.{method}("{url}")',
                'operation_id': op_id,
                'context': 'url_literal'
            })

        # With variables
        for _ in range(count // 3):
            var = random.choice(['url', 'endpoint', 'api_url', 'path', 'uri'])
            examples.append({
                'pw_code': f'http.{method}({var})',
                'operation_id': op_id,
                'context': 'url_variable'
            })

        # In contexts
        for _ in range(count // 3):
            var = random.choice(self.var_names)
            context = random.choice([
                f'let {var} = http.{method}("https://api.example.com")',
                f'response = http.{method}(url)',
                f'return http.{method}(endpoint)'
            ])
            examples.append({
                'pw_code': context,
                'operation_id': op_id,
                'context': 'statement'
            })

        return examples

    def _generate_json_ops(self, op_id: str, method: str, count: int) -> List[Dict]:
        """Generate JSON operation examples."""
        examples = []

        for _ in range(count):
            var = random.choice(self.var_names)
            context = random.choice([
                f'json.{method}({var})',
                f'let parsed = json.{method}({var})',
                f'result = json.{method}(text)',
                f'return json.{method}({var})',
                f'if json.{method}({var})'
            ])
            examples.append({
                'pw_code': context,
                'operation_id': op_id,
                'context': random.choice(['simple', 'statement'])
            })

        return examples

    def _generate_array_ops(self, op_id: str, method: str, count: int) -> List[Dict]:
        """Generate array operation examples."""
        examples = []

        # NOTE: Some array operations use special syntax
        # array.contains → "item in array" (operator)
        # array.sort → "sorted(array)" (function)

        # For now, generate method call syntax
        # TODO: Add operator/function syntax variants

        for _ in range(count):
            var = random.choice(['items', 'arr', 'array', 'list', 'data'])
            item_var = random.choice(['item', 'element', 'value', 'x'])

            context = random.choice([
                f'array.{method}({var})',
                f'array.{method}({var}, {item_var})',
                f'let result = array.{method}({var})',
                f'if array.{method}({var}, {item_var})',
                f'return array.{method}({var})'
            ])
            examples.append({
                'pw_code': context,
                'operation_id': op_id,
                'context': random.choice(['simple', 'statement'])
            })

        return examples

    def _generate_math_ops(self, op_id: str, method: str, count: int) -> List[Dict]:
        """Generate math operation examples."""
        examples = []

        # NOTE: Many math operations use built-in syntax
        # math.abs → abs(x)
        # For now, generate both styles

        for i in range(count):
            var = random.choice(['x', 'y', 'num', 'value', 'n'])
            num = random.choice(self.numbers)

            # Half with namespace.method(), half with built-in style
            if i % 2 == 0:
                context = random.choice([
                    f'math.{method}({var})',
                    f'math.{method}({num})',
                    f'let result = math.{method}({var})',
                    f'return math.{method}({var})'
                ])
            else:
                # Built-in style (no namespace)
                context = random.choice([
                    f'{method}({var})',
                    f'{method}({num})',
                    f'let result = {method}({var})',
                    f'return {method}({num})'
                ])

            examples.append({
                'pw_code': context,
                'operation_id': op_id,
                'context': random.choice(['namespaced', 'builtin'])
            })

        return examples

    def _generate_time_ops(self, op_id: str, method: str, count: int) -> List[Dict]:
        """Generate time operation examples."""
        examples = []

        for _ in range(count):
            var = random.choice(self.var_names)
            num = random.choice(self.numbers)

            context = random.choice([
                f'time.{method}()',
                f'time.{method}({var})',
                f'time.{method}({num})',
                f'let timestamp = time.{method}()',
                f'return time.{method}({var})'
            ])
            examples.append({
                'pw_code': context,
                'operation_id': op_id,
                'context': random.choice(['simple', 'statement'])
            })

        return examples

    def _generate_process_ops(self, op_id: str, method: str, count: int) -> List[Dict]:
        """Generate process operation examples."""
        examples = []

        for _ in range(count):
            var = random.choice(self.var_names)
            context = random.choice([
                f'process.{method}()',
                f'process.{method}({var})',
                f'let result = process.{method}()',
                f'return process.{method}({var})'
            ])
            examples.append({
                'pw_code': context,
                'operation_id': op_id,
                'context': random.choice(['simple', 'statement'])
            })

        return examples

    def _generate_env_ops(self, op_id: str, method: str, count: int) -> List[Dict]:
        """Generate environment operation examples."""
        examples = []

        env_vars = ['PATH', 'HOME', 'USER', 'API_KEY', 'DB_URL', 'PORT']

        for _ in range(count):
            var = random.choice(self.var_names)
            env_var = random.choice(env_vars)

            context = random.choice([
                f'env.{method}("{env_var}")',
                f'env.{method}({var})',
                f'let value = env.{method}("API_KEY")',
                f'return env.{method}({var})'
            ])
            examples.append({
                'pw_code': context,
                'operation_id': op_id,
                'context': random.choice(['simple', 'statement'])
            })

        return examples

    def _generate_hash_ops(self, op_id: str, method: str, count: int) -> List[Dict]:
        """Generate hash operation examples."""
        examples = []

        for _ in range(count):
            var = random.choice(self.var_names)
            context = random.choice([
                f'hash.{method}({var})',
                f'let digest = hash.{method}({var})',
                f'let checksum = hash.{method}(data)',
                f'return hash.{method}({var})'
            ])
            examples.append({
                'pw_code': context,
                'operation_id': op_id,
                'context': random.choice(['simple', 'statement'])
            })

        return examples

    def _generate_encoding_ops(self, op_id: str, method: str, namespace: str, count: int) -> List[Dict]:
        """Generate encoding operation examples (base64, hex, url)."""
        examples = []

        for _ in range(count):
            var = random.choice(self.var_names)
            context = random.choice([
                f'{namespace}.{method}({var})',
                f'let encoded = {namespace}.{method}({var})',
                f'let decoded = {namespace}.{method}(data)',
                f'return {namespace}.{method}({var})'
            ])
            examples.append({
                'pw_code': context,
                'operation_id': op_id,
                'context': random.choice(['simple', 'statement'])
            })

        return examples

    def _generate_type_ops(self, op_id: str, method: str, count: int) -> List[Dict]:
        """Generate type operation examples."""
        examples = []

        for _ in range(count):
            var = random.choice(self.var_names)
            num = random.choice(self.numbers)

            context = random.choice([
                f'type.{method}({var})',
                f'type.{method}({num})',
                f'let converted = type.{method}({var})',
                f'if type.{method}({var})',
                f'return type.{method}({var})'
            ])
            examples.append({
                'pw_code': context,
                'operation_id': op_id,
                'context': random.choice(['simple', 'statement'])
            })

        return examples

    def _generate_generic(self, op_id: str, method: str, count: int) -> List[Dict]:
        """Generic generation for unknown operations."""
        examples = []
        namespace = op_id.split('.')[0]

        for _ in range(count):
            var = random.choice(self.var_names)
            context = random.choice([
                f'{namespace}.{method}({var})',
                f'let result = {namespace}.{method}({var})',
                f'return {namespace}.{method}({var})'
            ])
            examples.append({
                'pw_code': context,
                'operation_id': op_id,
                'context': 'generic'
            })

        return examples

    def generate_full_dataset(
        self,
        operation_ids: List[str],
        examples_per_operation: int = 120
    ) -> List[Dict[str, str]]:
        """
        Generate complete training dataset.

        Args:
            operation_ids: List of all operations
            examples_per_operation: Target examples per operation

        Returns:
            Complete dataset
        """
        print("=" * 80)
        print("Generating Large-Scale Training Dataset")
        print("=" * 80)
        print()
        print(f"Operations: {len(operation_ids)}")
        print(f"Target per operation: {examples_per_operation}")
        print(f"Total target: {len(operation_ids) * examples_per_operation}")
        print()

        all_examples = []

        for i, op_id in enumerate(operation_ids, 1):
            examples = self.generate_for_operation(op_id, examples_per_operation)
            all_examples.extend(examples)

            if i % 10 == 0:
                print(f"Generated {len(all_examples):,} examples ({i}/{len(operation_ids)} operations)")

        print()
        print(f"✅ Generated {len(all_examples):,} total examples")
        print()

        return all_examples


def main():
    """Generate and save large training dataset."""
    # Load existing small dataset to get operation list
    with open('training_dataset_full.json') as f:
        small_dataset = json.load(f)

    operation_ids = sorted(set(ex['operation_id'] for ex in small_dataset))

    print(f"Found {len(operation_ids)} operations from existing dataset")
    print()

    # Generate large dataset
    generator = TrainingDataGenerator()
    large_dataset = generator.generate_full_dataset(operation_ids, examples_per_operation=120)

    # Save
    output_path = Path('training_dataset_large.json')
    with open(output_path, 'w') as f:
        json.dump(large_dataset, f, indent=2)

    print("=" * 80)
    print("Dataset saved")
    print("=" * 80)
    print()
    print(f"File: {output_path}")
    print(f"Size: {output_path.stat().st_size / 1024 / 1024:.1f} MB")
    print(f"Examples: {len(large_dataset):,}")
    print(f"Operations: {len(operation_ids)}")
    print(f"Avg per operation: {len(large_dataset) / len(operation_ids):.1f}")
    print()

    # Statistics
    from collections import Counter
    contexts = Counter(ex['context'] for ex in large_dataset)
    print("Context distribution:")
    for ctx, count in contexts.most_common():
        pct = count / len(large_dataset) * 100
        print(f"  {ctx:20s} {count:5d} ({pct:.1f}%)")

    print()
    print("✅ Ready to re-train CharCNN")
    print()


if __name__ == "__main__":
    main()
