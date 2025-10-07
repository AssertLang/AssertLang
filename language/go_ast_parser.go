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
	Body       string      `json:"body"` // Raw source code
}

type Receiver struct {
	Name string `json:"name"`
	Type string `json:"type"`
}

type Parameter struct {
	Name string `json:"name"`
	Type string `json:"type"`
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

	// Body (as raw source)
	if fn.Body != nil {
		// Would need original source file to extract body text
		// For now, just mark that body exists
		function.Body = "<parsed_body>"
	}

	return function
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
