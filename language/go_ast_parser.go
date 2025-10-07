package main

import (
	"encoding/json"
	"fmt"
	"go/ast"
	"go/parser"
	"go/token"
	"os"
)

// Simplified AST structures for JSON serialization
type FileAST struct {
	Package   string      `json:"package"`
	Imports   []Import    `json:"imports"`
	Types     []TypeDecl  `json:"types"`
	Functions []Function  `json:"functions"`
}

type Import struct {
	Path  string `json:"path"`
	Alias string `json:"alias,omitempty"`
}

type TypeDecl struct {
	Name   string   `json:"name"`
	Kind   string   `json:"kind"` // "struct", "interface"
	Fields []Field  `json:"fields,omitempty"`
}

type Field struct {
	Name string `json:"name"`
	Type string `json:"type"`
}

type Function struct {
	Name       string      `json:"name"`
	Receiver   *Receiver   `json:"receiver,omitempty"`
	Params     []Parameter `json:"params"`
	Results    []Parameter `json:"results"`
	Body       []Statement `json:"body"` // Parsed statement AST
}

type Receiver struct {
	Name string `json:"name"`
	Type string `json:"type"`
}

type Parameter struct {
	Name string `json:"name"`
	Type string `json:"type"`
}

// Statement types
type Statement struct {
	Type   string       `json:"type"` // "assignment", "if", "for", "return", etc.
	Target string       `json:"target,omitempty"`
	Value  *Expression  `json:"value,omitempty"`
	Expr   *Expression  `json:"expr,omitempty"`
	Init   *Statement   `json:"init,omitempty"`
	Cond   *Expression  `json:"cond,omitempty"`
	Post   *Statement   `json:"post,omitempty"`
	Body   []Statement  `json:"body,omitempty"`
	Else   []Statement  `json:"else,omitempty"`
}

type Expression struct {
	Type     string       `json:"type"` // "binary", "ident", "literal", "call"
	Operator string       `json:"operator,omitempty"`
	Left     *Expression  `json:"left,omitempty"`
	Right    *Expression  `json:"right,omitempty"`
	Name     string       `json:"name,omitempty"`
	Value    interface{}  `json:"value,omitempty"`
	Function string       `json:"function,omitempty"`
	Args     []Expression `json:"args,omitempty"`
}

func main() {
	if len(os.Args) < 2 {
		fmt.Fprintf(os.Stderr, "Usage: go_ast_parser <file.go>\n")
		os.Exit(1)
	}

	filename := os.Args[1]

	// Parse Go source file
	fset := token.NewFileSet()
	file, err := parser.ParseFile(fset, filename, nil, parser.ParseComments)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Parse error: %v\n", err)
		os.Exit(1)
	}

	// Convert to simplified AST
	fileAST := convertFile(file, fset)

	// Output JSON
	encoder := json.NewEncoder(os.Stdout)
	encoder.SetIndent("", "  ")
	if err := encoder.Encode(fileAST); err != nil {
		fmt.Fprintf(os.Stderr, "JSON encode error: %v\n", err)
		os.Exit(1)
	}
}

func convertFile(file *ast.File, fset *token.FileSet) *FileAST {
	result := &FileAST{
		Package: file.Name.Name,
	}

	// Extract imports
	for _, imp := range file.Imports {
		importDecl := Import{
			Path: imp.Path.Value,
		}
		if imp.Name != nil {
			importDecl.Alias = imp.Name.Name
		}
		result.Imports = append(result.Imports, importDecl)
	}

	// Extract declarations
	for _, decl := range file.Decls {
		switch d := decl.(type) {
		case *ast.GenDecl:
			// Type declarations
			if d.Tok == token.TYPE {
				for _, spec := range d.Specs {
					if ts, ok := spec.(*ast.TypeSpec); ok {
						result.Types = append(result.Types, convertTypeSpec(ts))
					}
				}
			}
		case *ast.FuncDecl:
			// Function declarations
			result.Functions = append(result.Functions, convertFunction(d, fset))
		}
	}

	return result
}

func convertTypeSpec(ts *ast.TypeSpec) TypeDecl {
	typeDecl := TypeDecl{
		Name: ts.Name.Name,
	}

	switch t := ts.Type.(type) {
	case *ast.StructType:
		typeDecl.Kind = "struct"
		if t.Fields != nil {
			for _, field := range t.Fields.List {
				fieldType := exprToString(field.Type)
				for _, name := range field.Names {
					typeDecl.Fields = append(typeDecl.Fields, Field{
						Name: name.Name,
						Type: fieldType,
					})
				}
			}
		}
	case *ast.InterfaceType:
		typeDecl.Kind = "interface"
	}

	return typeDecl
}

func convertFunction(fn *ast.FuncDecl, fset *token.FileSet) Function {
	function := Function{
		Name: fn.Name.Name,
	}

	// Receiver (for methods)
	if fn.Recv != nil && len(fn.Recv.List) > 0 {
		recv := fn.Recv.List[0]
		recvName := ""
		if len(recv.Names) > 0 {
			recvName = recv.Names[0].Name
		}
		function.Receiver = &Receiver{
			Name: recvName,
			Type: exprToString(recv.Type),
		}
	}

	// Parameters
	if fn.Type.Params != nil {
		for _, param := range fn.Type.Params.List {
			paramType := exprToString(param.Type)
			for _, name := range param.Names {
				function.Params = append(function.Params, Parameter{
					Name: name.Name,
					Type: paramType,
				})
			}
		}
	}

	// Results
	if fn.Type.Results != nil {
		for _, result := range fn.Type.Results.List {
			resultType := exprToString(result.Type)
			resultName := ""
			if len(result.Names) > 0 {
				resultName = result.Names[0].Name
			}
			function.Results = append(function.Results, Parameter{
				Name: resultName,
				Type: resultType,
			})
		}
	}

	// Body (parse statements)
	if fn.Body != nil {
		for _, stmt := range fn.Body.List {
			function.Body = append(function.Body, convertStatement(stmt))
		}
	}

	return function
}

func convertStatement(stmt ast.Stmt) Statement {
	switch s := stmt.(type) {
	case *ast.AssignStmt:
		// Handle assignment: x := 5, x = y, etc.
		result := Statement{Type: "assignment"}

		// Get target (left side)
		if len(s.Lhs) > 0 {
			result.Target = exprToIdentifier(s.Lhs[0])
		}

		// Get value (right side)
		if len(s.Rhs) > 0 {
			result.Value = convertExpression(s.Rhs[0])
		}

		return result

	case *ast.IfStmt:
		// Handle if statement
		result := Statement{Type: "if"}

		// Condition
		result.Cond = convertExpression(s.Cond)

		// Body
		if s.Body != nil {
			for _, bodyStmt := range s.Body.List {
				result.Body = append(result.Body, convertStatement(bodyStmt))
			}
		}

		// Else clause
		if s.Else != nil {
			switch elseStmt := s.Else.(type) {
			case *ast.BlockStmt:
				for _, stmt := range elseStmt.List {
					result.Else = append(result.Else, convertStatement(stmt))
				}
			case *ast.IfStmt:
				// else if
				result.Else = append(result.Else, convertStatement(elseStmt))
			}
		}

		return result

	case *ast.ForStmt:
		// Handle for loop
		result := Statement{Type: "for"}

		// Init statement (e.g., i := 0)
		if s.Init != nil {
			initStmt := convertStatement(s.Init)
			result.Init = &initStmt
		}

		// Condition (e.g., i < 10)
		if s.Cond != nil {
			result.Cond = convertExpression(s.Cond)
		}

		// Post statement (e.g., i++)
		if s.Post != nil {
			postStmt := convertStatement(s.Post)
			result.Post = &postStmt
		}

		// Body
		if s.Body != nil {
			for _, bodyStmt := range s.Body.List {
				result.Body = append(result.Body, convertStatement(bodyStmt))
			}
		}

		return result

	case *ast.ReturnStmt:
		// Handle return statement
		result := Statement{Type: "return"}

		if len(s.Results) > 0 {
			result.Value = convertExpression(s.Results[0])
		}

		return result

	case *ast.ExprStmt:
		// Expression as statement (e.g., function call)
		result := Statement{Type: "expr"}
		result.Expr = convertExpression(s.X)
		return result

	case *ast.IncDecStmt:
		// Handle i++ or i--
		result := Statement{Type: "incdec"}
		result.Target = exprToIdentifier(s.X)
		result.Value = &Expression{
			Type:  "literal",
			Value: s.Tok.String(), // "++" or "--"
		}
		return result

	default:
		// Unknown statement type
		return Statement{Type: "unknown"}
	}
}

func convertExpression(expr ast.Expr) *Expression {
	switch e := expr.(type) {
	case *ast.BinaryExpr:
		// Binary operation: x + y, x > y, etc.
		return &Expression{
			Type:     "binary",
			Operator: e.Op.String(),
			Left:     convertExpression(e.X),
			Right:    convertExpression(e.Y),
		}

	case *ast.Ident:
		// Identifier: variable name
		return &Expression{
			Type: "ident",
			Name: e.Name,
		}

	case *ast.BasicLit:
		// Literal: 123, "hello", true
		return &Expression{
			Type:  "literal",
			Value: e.Value,
		}

	case *ast.CallExpr:
		// Function call: foo(a, b)
		result := &Expression{
			Type:     "call",
			Function: exprToIdentifier(e.Fun),
		}

		for _, arg := range e.Args {
			result.Args = append(result.Args, *convertExpression(arg))
		}

		return result

	case *ast.UnaryExpr:
		// Unary operation: -x, !flag
		return &Expression{
			Type:     "unary",
			Operator: e.Op.String(),
			Right:    convertExpression(e.X),
		}

	default:
		// Unknown expression
		return &Expression{
			Type: "unknown",
		}
	}
}

func exprToIdentifier(expr ast.Expr) string {
	switch e := expr.(type) {
	case *ast.Ident:
		return e.Name
	case *ast.SelectorExpr:
		return exprToIdentifier(e.X) + "." + e.Sel.Name
	default:
		return "unknown"
	}
}

func exprToString(expr ast.Expr) string {
	switch e := expr.(type) {
	case *ast.Ident:
		return e.Name
	case *ast.StarExpr:
		return "*" + exprToString(e.X)
	case *ast.SelectorExpr:
		return exprToString(e.X) + "." + e.Sel.Name
	case *ast.ArrayType:
		return "[]" + exprToString(e.Elt)
	case *ast.MapType:
		return "map[" + exprToString(e.Key) + "]" + exprToString(e.Value)
	default:
		return "unknown"
	}
}
