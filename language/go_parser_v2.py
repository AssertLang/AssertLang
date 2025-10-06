"""
Go Parser V2 - Arbitrary Go Code → IR

This parser converts arbitrary Go code into Promptware's Intermediate Representation (IR).
Unlike V1 which only handled MCP servers, V2 parses any Go code including:
- Functions and methods
- Structs and interfaces
- Goroutines (abstracted as async)
- Channels (abstracted as message passing)
- Error handling patterns (val, err := ...)
- Control flow (if/for/while/switch)
- Type definitions

Strategy:
- Use regex-based parsing for Go syntax (no external dependencies)
- Extract functions, types, control flow, expressions
- Map Go types to IR types via type_system
- Abstract Go-specific features (goroutines → async, channels → messaging)
"""

import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Set

from dsl.ir import (
    IRModule,
    IRImport,
    IRFunction,
    IRParameter,
    IRClass,
    IRProperty,
    IRTypeDefinition,
    IRType,
    IRStatement,
    IRExpression,
    IRAssignment,
    IRReturn,
    IRIf,
    IRFor,
    IRWhile,
    IRCall,
    IRIdentifier,
    IRLiteral,
    IRBinaryOp,
    IRPropertyAccess,
    IRArray,
    IRMap,
    IRComprehension,
    IRLambda,
    IRTernary,
    BinaryOperator,
    LiteralType,
    SourceLocation,
)
from dsl.type_system import TypeSystem


class GoParserV2:
    """Parse arbitrary Go code → IR."""

    def __init__(self):
        self.type_system = TypeSystem()
        self.current_file = None

    def parse_file(self, file_path: str) -> IRModule:
        """Parse Go file and return IR module."""
        self.current_file = file_path
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()

        return self.parse_source(source, file_path)

    def parse_source(self, source: str, file_path: str = "unknown") -> IRModule:
        """Parse Go source code into IR."""
        self.current_file = file_path

        # Extract components
        package_name = self._extract_package_name(source)
        imports = self._extract_imports(source)
        module_vars = self._extract_module_vars(source)
        type_defs = self._extract_type_definitions(source)
        functions = self._extract_functions(source)

        # Build module
        module = IRModule(
            name=package_name,
            version="1.0.0",
            imports=imports,
            module_vars=module_vars,
            types=type_defs,
            functions=functions,
        )

        # Add source location
        module.location = SourceLocation(file=file_path, line=1, column=1)

        return module

    def _extract_package_name(self, source: str) -> str:
        """Extract package name from Go source."""
        match = re.search(r'^\s*package\s+(\w+)', source, re.MULTILINE)
        if match:
            return match.group(1)
        return "main"

    def _extract_imports(self, source: str) -> List[IRImport]:
        """Extract import statements from Go source."""
        imports = []

        # Single import: import "fmt"
        single_pattern = r'^\s*import\s+"([^"]+)"'
        for match in re.finditer(single_pattern, source, re.MULTILINE):
            package = match.group(1)
            imports.append(IRImport(module=package))

        # Multi-line imports: import ( ... )
        multi_pattern = r'import\s*\(\s*([^)]+)\)'
        for match in re.finditer(multi_pattern, source, re.DOTALL):
            import_block = match.group(1)
            # Extract each import line
            for line in import_block.split('\n'):
                line = line.strip()
                if not line:
                    continue

                # Handle: "package/path"
                pkg_match = re.match(r'"([^"]+)"', line)
                if pkg_match:
                    package = pkg_match.group(1)
                    imports.append(IRImport(module=package))

                # Handle: alias "package/path"
                alias_match = re.match(r'(\w+)\s+"([^"]+)"', line)
                if alias_match:
                    alias = alias_match.group(1)
                    package = alias_match.group(2)
                    imports.append(IRImport(module=package, alias=alias))

        return imports

    def _extract_module_vars(self, source: str) -> List[IRAssignment]:
        """Extract module-level const and var declarations."""
        module_vars = []

        # Const declarations: const NAME TYPE = VALUE or const NAME = VALUE
        # Type can be: int, []int, string, etc.
        const_pattern = r'^\s*const\s+(\w+)(?:\s+(\S+))?\s*=\s*(.+?)(?:\n|$)'
        for match in re.finditer(const_pattern, source, re.MULTILINE):
            name = match.group(1)
            type_annotation = match.group(2)  # May be None
            value_str = match.group(3).strip()

            # Parse the value expression
            value = self._parse_expression(value_str)

            # Create assignment
            module_vars.append(IRAssignment(
                target=IRIdentifier(name=name),
                value=value,
                is_declaration=True
            ))

        # Var declarations: var NAME TYPE = VALUE or var NAME = VALUE
        # Type can be: int, []int, [][]int, map[string]int, etc.
        var_pattern = r'^\s*var\s+(\w+)(?:\s+(\S+))?\s*=\s*(.+?)(?:\n|$)'
        for match in re.finditer(var_pattern, source, re.MULTILINE):
            name = match.group(1)
            type_annotation = match.group(2)  # May be None
            value_str = match.group(3).strip()

            # Parse the value expression
            value = self._parse_expression(value_str)

            # Create assignment
            module_vars.append(IRAssignment(
                target=IRIdentifier(name=name),
                value=value,
                is_declaration=True
            ))

        return module_vars

    def _extract_type_definitions(self, source: str) -> List[IRTypeDefinition]:
        """Extract struct type definitions."""
        type_defs = []

        # Pattern: type Name struct { ... }
        struct_pattern = r'type\s+(\w+)\s+struct\s*\{([^}]*)\}'

        for match in re.finditer(struct_pattern, source, re.DOTALL):
            type_name = match.group(1)
            fields_block = match.group(2)

            fields = self._parse_struct_fields(fields_block)

            type_def = IRTypeDefinition(name=type_name, fields=fields)
            type_defs.append(type_def)

        return type_defs

    def _parse_struct_fields(self, fields_block: str) -> List[IRProperty]:
        """Parse struct fields from field block."""
        fields = []

        # Pattern: FieldName Type `json:"name"`
        field_pattern = r'(\w+)\s+(\S+)(?:\s+`[^`]*`)?'

        for line in fields_block.split('\n'):
            line = line.strip()
            if not line or line.startswith('//'):
                continue

            match = re.match(field_pattern, line)
            if match:
                field_name = match.group(1)
                go_type = match.group(2)

                # Map Go type to IR type
                ir_type = self._go_type_to_ir(go_type)

                field = IRProperty(
                    name=field_name,
                    prop_type=ir_type,
                )
                fields.append(field)

        return fields

    def _go_type_to_ir(self, go_type: str) -> IRType:
        """Convert Go type to IR type."""
        go_type = go_type.strip()

        # Handle pointers: *Type → Type? (optional)
        if go_type.startswith('*'):
            base_type = self._go_type_to_ir(go_type[1:])
            base_type.is_optional = True
            return base_type

        # Handle arrays/slices: []Type → array<Type>
        if go_type.startswith('[]'):
            elem_type = self._go_type_to_ir(go_type[2:])
            return IRType(name="array", generic_args=[elem_type])

        # Handle maps: map[K]V → map<K, V>
        map_match = re.match(r'map\[([^]]+)\](.+)', go_type)
        if map_match:
            key_type = self._go_type_to_ir(map_match.group(1))
            val_type = self._go_type_to_ir(map_match.group(2))
            return IRType(name="map", generic_args=[key_type, val_type])

        # Map Go primitive types to IR types
        type_map = {
            'string': 'string',
            'int': 'int',
            'int8': 'int',
            'int16': 'int',
            'int32': 'int',
            'int64': 'int',
            'uint': 'int',
            'uint8': 'int',
            'uint16': 'int',
            'uint32': 'int',
            'uint64': 'int',
            'float32': 'float',
            'float64': 'float',
            'bool': 'bool',
            'byte': 'int',
            'rune': 'int',
            'interface{}': 'any',
            'any': 'any',
            'error': 'string',  # Errors are strings in IR
        }

        if go_type in type_map:
            return IRType(name=type_map[go_type])

        # Custom type (User, Payment, etc.)
        return IRType(name=go_type)

    def _extract_functions(self, source: str) -> List[IRFunction]:
        """Extract function definitions from Go source."""
        functions = []

        # Pattern: func name(params) returnType { body }
        # Also handles: func (receiver) name(params) returnType { body }
        func_pattern = r'func\s+(?:\([^)]+\)\s+)?(\w+)\s*\(([^)]*)\)(?:\s+([^{]+))?\s*\{'

        for match in re.finditer(func_pattern, source):
            func_name = match.group(1)
            params_str = match.group(2)
            return_type_str = match.group(3)

            # Skip internal functions (but not Test* - those might be user functions)
            if func_name.startswith('_'):
                continue

            # Parse parameters
            params = self._parse_function_params(params_str)

            # Parse return type
            return_type = None
            if return_type_str:
                return_type = self._parse_return_type(return_type_str.strip())

            # Extract function body
            func_start = match.start()
            func_body_str = self._extract_function_body(source, func_start)

            # Parse function body into statements
            body_stmts = self._parse_function_body(func_body_str)

            # Check if function is async (uses goroutines)
            is_async = 'go ' in func_body_str

            # Build IR function
            ir_func = IRFunction(
                name=func_name,
                params=params,
                return_type=return_type,
                body=body_stmts,
                is_async=is_async,
            )

            # Add source location
            line_num = source[:func_start].count('\n') + 1
            ir_func.location = SourceLocation(
                file=self.current_file,
                line=line_num,
                column=1
            )

            functions.append(ir_func)

        return functions

    def _parse_function_params(self, params_str: str) -> List[IRParameter]:
        """Parse function parameters."""
        params = []

        if not params_str.strip():
            return params

        # Split by comma, but handle complex types
        param_parts = self._split_params(params_str)

        for part in param_parts:
            part = part.strip()
            if not part:
                continue

            # Pattern: name type or just type
            # Examples: "x int", "name string", "opts ...string"

            # Handle variadic: ...Type
            is_variadic = '...' in part
            if is_variadic:
                part = part.replace('...', '')

            # Split into name and type
            tokens = part.split()
            if len(tokens) >= 2:
                param_name = tokens[0]
                param_type_str = ' '.join(tokens[1:])
            else:
                # Just type, no name
                param_name = f"param_{len(params)}"
                param_type_str = tokens[0]

            param_type = self._go_type_to_ir(param_type_str)

            param = IRParameter(
                name=param_name,
                param_type=param_type,
                is_variadic=is_variadic,
            )
            params.append(param)

        return params

    def _split_params(self, params_str: str) -> List[str]:
        """Split parameters by comma, handling nested types."""
        parts = []
        current = []
        depth = 0

        for char in params_str:
            if char in '[]{}':
                depth += 1 if char in '[{' else -1
                current.append(char)
            elif char == ',' and depth == 0:
                parts.append(''.join(current).strip())
                current = []
            else:
                current.append(char)

        if current:
            parts.append(''.join(current).strip())

        return parts

    def _parse_return_type(self, return_str: str) -> Optional[IRType]:
        """Parse function return type."""
        return_str = return_str.strip()

        if not return_str:
            return None

        # Handle multiple return values: (Type1, Type2)
        if return_str.startswith('(') and return_str.endswith(')'):
            # For now, we'll return the first non-error type
            # TODO: Support multiple return values properly
            inner = return_str[1:-1]
            types = self._split_params(inner)

            # Find first non-error type
            for type_str in types:
                type_str = type_str.strip()
                if type_str != 'error':
                    return self._go_type_to_ir(type_str)

            # All errors? Return error type
            return IRType(name='string')

        # Single return type
        if return_str != 'error':
            return self._go_type_to_ir(return_str)

        return IRType(name='string')

    def _extract_function_body(self, source: str, func_start: int) -> str:
        """Extract function body from source."""
        # Find the LAST opening brace before any statement (handles []interface{} in return type)
        # Strategy: Find all { after func_start, the last one before a newline or statement is the function body

        # Find where function signature ends (look for { followed by newline or statement)
        i = func_start
        last_brace = -1

        while i < len(source):
            if source[i] == '{':
                # Check if this is followed by newline/whitespace (function body)
                # or by } (type parameter like interface{})
                next_char_index = i + 1
                while next_char_index < len(source) and source[next_char_index] in ' \t':
                    next_char_index += 1

                if next_char_index < len(source):
                    next_char = source[next_char_index]
                    if next_char == '\n' or next_char.isalpha() or next_char == '\t':
                        # This is the function body opening brace
                        last_brace = i
                        break
                    elif next_char == '}':
                        # This is a type parameter like interface{}, keep searching
                        last_brace = i

            # Stop at newline after opening paren (function body should start soon after)
            if source[i] == '\n' and last_brace != -1:
                break

            i += 1

            # Safety: don't search too far
            if i > func_start + 500:
                break

        if last_brace == -1:
            # Fallback to first {
            last_brace = source.find('{', func_start)
            if last_brace == -1:
                return ""

        brace_start = last_brace

        # Find matching closing brace
        depth = 0
        i = brace_start

        while i < len(source):
            if source[i] == '{':
                depth += 1
            elif source[i] == '}':
                depth -= 1
                if depth == 0:
                    return source[brace_start + 1:i]
            i += 1

        return source[brace_start + 1:]

    def _parse_function_body(self, body_str: str) -> List[IRStatement]:
        """Parse function body into IR statements."""
        statements = []

        # Remove leading/trailing whitespace
        body_str = body_str.strip()

        if not body_str:
            return statements

        # Split into lines for statement parsing
        lines = body_str.split('\n')

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Skip empty lines and comments
            if not line or line.startswith('//'):
                i += 1
                continue

            # Try to detect for-append comprehension pattern
            comprehension, lines_consumed = self._try_parse_comprehension_pattern(lines, i)
            if comprehension:
                statements.append(comprehension)
                i += lines_consumed
                continue

            # Parse statement
            stmt = self._parse_statement(line, lines, i)
            if stmt:
                statements.append(stmt)

            i += 1

        return statements

    def _parse_statement(self, line: str, lines: List[str], index: int) -> Optional[IRStatement]:
        """Parse a single statement."""

        # Return statement
        if line.startswith('return '):
            return self._parse_return_statement(line)

        # If statement
        if line.startswith('if '):
            return self._parse_if_statement(line, lines, index)

        # For loop
        if line.startswith('for '):
            return self._parse_for_statement(line, lines, index)

        # Variable assignment/declaration
        # Patterns: var x = ..., x := ..., x = ...
        if ':=' in line or '=' in line or line.startswith('var '):
            return self._parse_assignment(line)

        # Function call (expression statement)
        if '(' in line and ')' in line:
            expr = self._parse_expression(line)
            if isinstance(expr, IRCall):
                return expr

        return None

    def _parse_return_statement(self, line: str) -> IRReturn:
        """Parse return statement."""
        # Extract return value
        return_val = line[7:].strip()  # Remove 'return '

        if not return_val:
            return IRReturn(value=None)

        # Check for multiple return values (comma-separated)
        # Go allows: return val1, val2, val3
        # We need to detect this pattern outside of function calls/literals
        if ',' in return_val:
            # Split by comma, but be careful of commas inside function calls/literals
            # Simple heuristic: if no unbalanced parens/braces, split by comma
            depth = 0
            can_split = True
            for char in return_val:
                if char in '({[':
                    depth += 1
                elif char in ')}]':
                    depth -= 1

            # If balanced, we can safely split by comma
            if depth == 0:
                values = [v.strip() for v in return_val.split(',')]
                if len(values) > 1:
                    # Multiple return values - create IRArray
                    elements = [self._parse_expression(v) for v in values]
                    return IRReturn(value=IRArray(elements=elements))

        # Parse single return expression
        expr = self._parse_expression(return_val)
        return IRReturn(value=expr)

    def _parse_if_statement(self, line: str, lines: List[str], index: int) -> IRIf:
        """Parse if statement."""
        # Extract condition: if condition {
        condition_match = re.match(r'if\s+(.+?)\s*\{', line)
        if not condition_match:
            # Simple condition without body on same line
            condition_str = line[3:].strip()
            condition_expr = self._parse_expression(condition_str)
            return IRIf(condition=condition_expr, then_body=[], else_body=[])

        condition_str = condition_match.group(1)
        condition_expr = self._parse_expression(condition_str)

        # TODO: Extract body (multi-line parsing)
        # For now, return simple if
        return IRIf(condition=condition_expr, then_body=[], else_body=[])

    def _parse_for_statement(self, line: str, lines: List[str], index: int) -> IRFor:
        """Parse for loop."""
        # Handle: for _, item := range items {
        range_discard_match = re.match(r'for\s+_\s*,\s*(\w+)\s*:=\s*range\s+(.+?)\s*\{', line)
        if range_discard_match:
            iterator = range_discard_match.group(1)
            iterable_str = range_discard_match.group(2)
            iterable_expr = self._parse_expression(iterable_str)
            return IRFor(iterator=iterator, iterable=iterable_expr, body=[])

        # Handle: for item := range items {
        range_match = re.match(r'for\s+(\w+)\s*:=\s*range\s+(.+?)\s*\{', line)
        if range_match:
            iterator = range_match.group(1)
            iterable_str = range_match.group(2)
            iterable_expr = self._parse_expression(iterable_str)
            return IRFor(iterator=iterator, iterable=iterable_expr, body=[])

        # Handle: for range items {
        range_simple_match = re.match(r'for\s+range\s+(.+?)\s*\{', line)
        if range_simple_match:
            iterable_str = range_simple_match.group(1)
            iterable_expr = self._parse_expression(iterable_str)
            return IRFor(iterator='item', iterable=iterable_expr, body=[])

        # TODO: Handle C-style for loops
        return IRFor(iterator='i', iterable=IRIdentifier(name='range'), body=[])

    def _try_parse_comprehension_pattern(self, lines: List[str], start_index: int) -> Tuple[Optional[IRAssignment], int]:
        """
        Try to detect and parse the for-append comprehension pattern.

        Pattern:
            result := []interface{}{}
            for _, item := range items {
                if condition {
                    result = append(result, transform)
                }
            }

        Returns:
            (IRAssignment with IRComprehension value, lines_consumed) if detected
            (None, 0) if not detected
        """
        # Must have at least 3 lines: assignment, for, append
        if start_index + 2 >= len(lines):
            return None, 0

        line1 = lines[start_index].strip()
        line2 = lines[start_index + 1].strip() if start_index + 1 < len(lines) else ""

        # Line 1: result := []interface{}{}
        result_match = re.match(r'(\w+)\s*:=\s*\[\]interface\{\}\{\}', line1)
        if not result_match:
            return None, 0

        result_var = result_match.group(1)

        # Line 2: for _, item := range items {
        for_match = re.match(r'for\s+_\s*,\s*(\w+)\s*:=\s*range\s+(.+?)\s*\{', line2)
        if not for_match:
            return None, 0

        iterator = for_match.group(1)
        iterable_str = for_match.group(2)
        iterable_expr = self._parse_expression(iterable_str)

        # Find the append statement inside the for loop
        # Could be:
        #   result = append(result, transform)
        # or with condition:
        #   if condition {
        #       result = append(result, transform)
        #   }

        i = start_index + 2
        condition_expr = None
        target_expr = None
        lines_consumed = 0

        while i < len(lines):
            line = lines[i].strip()

            # Check for if statement
            if line.startswith('if ') and '{' in line:
                # Extract condition
                cond_match = re.match(r'if\s+(.+?)\s*\{', line)
                if cond_match:
                    condition_str = cond_match.group(1)
                    condition_expr = self._parse_expression(condition_str)
                i += 1
                continue

            # Check for append statement
            append_match = re.search(rf'{result_var}\s*=\s*append\({result_var},\s*(.+?)\)', line)
            if append_match:
                target_str = append_match.group(1)
                target_expr = self._parse_expression(target_str)
                i += 1
                break

            # Check for closing braces (end of for loop)
            if line == '}':
                i += 1
                # Check if this closes the if or the for
                if condition_expr and target_expr:
                    # This closes the if, next should close the for
                    if i < len(lines) and lines[i].strip() == '}':
                        i += 1
                break

            i += 1

        # If we found the pattern, create IRComprehension
        if target_expr:
            comprehension = IRComprehension(
                target=target_expr,
                iterator=iterator,
                iterable=iterable_expr,
                condition=condition_expr,
                comprehension_type='list'
            )

            # Create assignment: result := [comprehension]
            assignment = IRAssignment(
                target=result_var,
                value=comprehension,
                is_declaration=True
            )

            lines_consumed = i - start_index
            return assignment, lines_consumed

        return None, 0

    def _parse_assignment(self, line: str) -> IRAssignment:
        """Parse assignment statement."""
        # var x = value
        var_match = re.match(r'var\s+(\w+)\s*(?:(\S+)\s*)?=\s*(.+)', line)
        if var_match:
            var_name = var_match.group(1)
            var_type_str = var_match.group(2)
            value_str = var_match.group(3).rstrip(';')

            var_type = self._go_type_to_ir(var_type_str) if var_type_str else None
            value_expr = self._parse_expression(value_str)

            return IRAssignment(
                target=var_name,
                value=value_expr,
                is_declaration=True,
                var_type=var_type,
            )

        # x := value
        decl_match = re.match(r'(\w+)\s*:=\s*(.+)', line)
        if decl_match:
            var_name = decl_match.group(1)
            value_str = decl_match.group(2).rstrip(';')
            value_expr = self._parse_expression(value_str)

            return IRAssignment(
                target=var_name,
                value=value_expr,
                is_declaration=True,
            )

        # x = value
        assign_match = re.match(r'(\w+)\s*=\s*(.+)', line)
        if assign_match:
            var_name = assign_match.group(1)
            value_str = assign_match.group(2).rstrip(';')
            value_expr = self._parse_expression(value_str)

            return IRAssignment(
                target=var_name,
                value=value_expr,
                is_declaration=False,
            )

        # Fallback
        return IRAssignment(
            target='unknown',
            value=IRLiteral(value=None, literal_type=LiteralType.NULL),
            is_declaration=True,
        )

    def _parse_expression(self, expr_str: str) -> IRExpression:
        """Parse expression into IR."""
        expr_str = expr_str.strip().rstrip(';')

        if not expr_str:
            return IRLiteral(value=None, literal_type=LiteralType.NULL)

        # Function literals (closures): func(...) ReturnType { body }
        # Must check before other patterns since it starts with 'func'
        func_lit_match = re.match(r'^func\s*\(([^)]*)\)\s*([^\{]*?)\s*\{', expr_str)
        if func_lit_match:
            params_str = func_lit_match.group(1)
            return_type_str = func_lit_match.group(2).strip()

            # Extract function body (between { and matching })
            body_start = expr_str.index('{')
            body_end = self._find_matching_brace(expr_str, body_start)
            body_str = expr_str[body_start+1:body_end].strip()

            # Parse parameters
            params = self._parse_function_params(params_str)

            # Parse body statements
            body_stmts = self._parse_function_body(body_str)

            # Check if it's immediately invoked: func(){}()
            rest = expr_str[body_end+1:].strip()
            if rest.startswith('()'):
                # Immediately invoked function expression
                # Return as a Call to the lambda
                lambda_expr = IRLambda(params=params, body=body_stmts)
                return IRCall(function=lambda_expr, args=[])
            else:
                # Regular lambda
                return IRLambda(params=params, body=body_stmts)

        # Literals
        if expr_str.startswith('"') and expr_str.endswith('"'):
            # String literal
            value = expr_str[1:-1]
            return IRLiteral(value=value, literal_type=LiteralType.STRING)

        if expr_str.startswith('`') and expr_str.endswith('`'):
            # Raw string literal
            value = expr_str[1:-1]
            return IRLiteral(value=value, literal_type=LiteralType.STRING)

        if expr_str in ['true', 'false']:
            # Boolean literal
            value = expr_str == 'true'
            return IRLiteral(value=value, literal_type=LiteralType.BOOLEAN)

        if expr_str == 'nil':
            # Null literal
            return IRLiteral(value=None, literal_type=LiteralType.NULL)

        if re.match(r'^-?\d+$', expr_str):
            # Integer literal
            value = int(expr_str)
            return IRLiteral(value=value, literal_type=LiteralType.INTEGER)

        if re.match(r'^-?\d+\.\d+$', expr_str):
            # Float literal
            value = float(expr_str)
            return IRLiteral(value=value, literal_type=LiteralType.FLOAT)

        # Slice literal: []Type{elem1, elem2, ...}
        slice_match = re.match(r'\[\](\w+)\{([^}]*)\}', expr_str)
        if slice_match:
            elements = []
            elements_str = slice_match.group(2)
            if elements_str.strip():
                for elem in elements_str.split(','):
                    elements.append(self._parse_expression(elem.strip()))
            return IRArray(elements=elements)

        # Map literal: map[K]V{key: value, ...}
        map_match = re.match(r'map\[([^\]]+)\](\w+)\{([^}]*)\}', expr_str)
        if map_match:
            entries = {}
            entries_str = map_match.group(3)
            if entries_str.strip():
                # Parse key-value pairs
                for pair in entries_str.split(','):
                    if ':' in pair:
                        key_str, val_str = pair.split(':', 1)
                        key = self._parse_expression(key_str.strip())
                        value = self._parse_expression(val_str.strip())
                        # Store with key as string representation
                        entries[str(key)] = value
            return IRMap(entries=entries)

        # Struct literal: Type{Field: value, ...}
        struct_match = re.match(r'(\w+)\{([^}]*)\}', expr_str)
        if struct_match and not expr_str.startswith('map['):
            type_name = struct_match.group(1)
            fields_str = struct_match.group(2)

            kwargs = {}
            if fields_str.strip():
                # Parse field assignments
                for field_assign in fields_str.split(','):
                    if ':' in field_assign:
                        field_name, field_value = field_assign.split(':', 1)
                        field_name = field_name.strip()
                        field_value = field_value.strip()
                        kwargs[field_name] = self._parse_expression(field_value)

            return IRCall(
                function=IRIdentifier(name=type_name),
                args=[],
                kwargs=kwargs
            )

        # Function call: func(args)
        call_match = re.match(r'(\w+(?:\.\w+)*)\s*\(([^)]*)\)', expr_str)
        if call_match:
            func_name = call_match.group(1)
            args_str = call_match.group(2)

            # Parse function identifier (may have dots)
            if '.' in func_name:
                func_expr = self._parse_dotted_name(func_name)
            else:
                func_expr = IRIdentifier(name=func_name)

            # Parse arguments
            args = []
            if args_str.strip():
                arg_parts = self._split_params(args_str)
                for arg in arg_parts:
                    args.append(self._parse_expression(arg.strip()))

            return IRCall(function=func_expr, args=args)

        # Binary operations
        for op_str, op_enum in [
            ('==', BinaryOperator.EQUAL),
            ('!=', BinaryOperator.NOT_EQUAL),
            ('<=', BinaryOperator.LESS_EQUAL),
            ('>=', BinaryOperator.GREATER_EQUAL),
            ('<', BinaryOperator.LESS_THAN),
            ('>', BinaryOperator.GREATER_THAN),
            ('&&', BinaryOperator.AND),
            ('||', BinaryOperator.OR),
            ('+', BinaryOperator.ADD),
            ('-', BinaryOperator.SUBTRACT),
            ('*', BinaryOperator.MULTIPLY),
            ('/', BinaryOperator.DIVIDE),
        ]:
            if op_str in expr_str:
                parts = expr_str.split(op_str, 1)
                if len(parts) == 2:
                    left = self._parse_expression(parts[0].strip())
                    right = self._parse_expression(parts[1].strip())
                    return IRBinaryOp(op=op_enum, left=left, right=right)

        # Property access: obj.field
        if '.' in expr_str and '(' not in expr_str:
            return self._parse_dotted_name(expr_str)

        # Identifier
        if re.match(r'^\w+$', expr_str):
            return IRIdentifier(name=expr_str)

        # Fallback: treat as identifier
        return IRIdentifier(name=expr_str)

    def _parse_dotted_name(self, name: str) -> IRExpression:
        """Parse dotted name into property access chain."""
        parts = name.split('.')

        if len(parts) == 1:
            return IRIdentifier(name=parts[0])

        # Build nested property access
        expr = IRIdentifier(name=parts[0])
        for part in parts[1:]:
            expr = IRPropertyAccess(object=expr, property=part)

        return expr

    def _find_matching_brace(self, text: str, start_pos: int) -> int:
        """Find the position of the closing brace that matches the opening brace at start_pos."""
        if start_pos >= len(text) or text[start_pos] != '{':
            return -1

        depth = 0
        for i in range(start_pos, len(text)):
            if text[i] == '{':
                depth += 1
            elif text[i] == '}':
                depth -= 1
                if depth == 0:
                    return i

        return -1  # No matching brace found


def parse_go_file(file_path: str) -> IRModule:
    """Convenience function to parse a Go file."""
    parser = GoParserV2()
    return parser.parse_file(file_path)


def parse_go_source(source: str) -> IRModule:
    """Convenience function to parse Go source code."""
    parser = GoParserV2()
    return parser.parse_source(source)
