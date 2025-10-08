/**
 * C# AST Parser: Roslyn Compiler API → JSON
 *
 * This parser uses C#'s official Roslyn compiler API for 100% accurate parsing.
 * Outputs JSON AST that can be consumed by Python.
 *
 * Usage: dotnet run csharp_ast_parser.cs <file.cs>
 */

using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;
using System.Text.Json;

namespace CSharpASTParser
{
    // JSON output structures
    public class FileAST
    {
        public List<ItemDecl> Items { get; set; } = new List<ItemDecl>();
    }

    public class ItemDecl
    {
        public string Type { get; set; }
        public string Name { get; set; }
        public List<Property> Properties { get; set; } = new List<Property>();
        public List<Method> Methods { get; set; } = new List<Method>();
        public Method Constructor { get; set; }
        public List<Parameter> Params { get; set; } = new List<Parameter>();
        public string ReturnType { get; set; }
        public List<Statement> Body { get; set; } = new List<Statement>();
        public bool IsAsync { get; set; }
    }

    public class Property
    {
        public string Name { get; set; }
        public string Type { get; set; }
        public bool IsOptional { get; set; }
    }

    public class Method
    {
        public string Name { get; set; }
        public List<Parameter> Params { get; set; } = new List<Parameter>();
        public string ReturnType { get; set; }
        public List<Statement> Body { get; set; } = new List<Statement>();
        public bool IsAsync { get; set; }
        public bool IsStatic { get; set; }
    }

    public class Parameter
    {
        public string Name { get; set; }
        public string Type { get; set; }
        public bool IsOptional { get; set; }
    }

    public class CaseClause
    {
        public bool IsDefault { get; set; }
        public List<Expression> Values { get; set; }
        public List<Statement> Body { get; set; }
    }

    public class Statement
    {
        public string Type { get; set; }
        public string Name { get; set; }
        public string Target { get; set; }
        public Expression Value { get; set; }
        public Expression Condition { get; set; }
        public List<Statement> ThenBody { get; set; }
        public List<Statement> ElseBody { get; set; }
        public string Iterator { get; set; }
        public Expression Iterable { get; set; }
        public List<Statement> Body { get; set; }
        public Expression Expr { get; set; }
        // Switch statement
        public List<CaseClause> Cases { get; set; }
        // Try/catch statement
        public List<Statement> TryBody { get; set; }
        public string CatchVar { get; set; }
        public List<Statement> CatchBody { get; set; }
        public List<Statement> FinallyBody { get; set; }
    }

    public class Expression
    {
        public string Type { get; set; }
        public string Op { get; set; }
        public Expression Left { get; set; }
        public Expression Right { get; set; }
        public string Name { get; set; }
        public object Value { get; set; }
        public string Function { get; set; }
        public List<Expression> Args { get; set; }
        public string Class { get; set; }
        public List<Expression> Elements { get; set; }
        public Dictionary<string, Expression> Properties { get; set; }
    }

    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length < 1)
            {
                Console.Error.WriteLine("Usage: dotnet run csharp_ast_parser.cs <file.cs>");
                Environment.Exit(1);
            }

            string filename = args[0];
            string sourceCode = File.ReadAllText(filename);

            // Parse C# source
            SyntaxTree tree = CSharpSyntaxTree.ParseText(sourceCode);
            CompilationUnitSyntax root = tree.GetCompilationUnitRoot();

            // Convert to our JSON format
            FileAST fileAST = ConvertFile(root);

            // Output JSON
            var options = new JsonSerializerOptions
            {
                WriteIndented = true,
                DefaultIgnoreCondition = System.Text.Json.Serialization.JsonIgnoreCondition.WhenWritingNull
            };
            string json = JsonSerializer.Serialize(fileAST, options);
            Console.WriteLine(json);
        }

        static FileAST ConvertFile(CompilationUnitSyntax root)
        {
            var fileAST = new FileAST();

            foreach (var member in root.Members)
            {
                if (member is ClassDeclarationSyntax classDecl)
                {
                    fileAST.Items.Add(ConvertClass(classDecl));
                }
                else if (member is InterfaceDeclarationSyntax interfaceDecl)
                {
                    fileAST.Items.Add(ConvertInterface(interfaceDecl));
                }
                else if (member is NamespaceDeclarationSyntax namespaceDecl)
                {
                    // Handle classes inside namespace
                    foreach (var nsMember in namespaceDecl.Members)
                    {
                        if (nsMember is ClassDeclarationSyntax nsClassDecl)
                        {
                            fileAST.Items.Add(ConvertClass(nsClassDecl));
                        }
                        else if (nsMember is InterfaceDeclarationSyntax nsInterfaceDecl)
                        {
                            fileAST.Items.Add(ConvertInterface(nsInterfaceDecl));
                        }
                    }
                }
            }

            return fileAST;
        }

        static ItemDecl ConvertClass(ClassDeclarationSyntax classDecl)
        {
            var item = new ItemDecl
            {
                Type = "class",
                Name = classDecl.Identifier.Text
            };

            foreach (var member in classDecl.Members)
            {
                if (member is PropertyDeclarationSyntax propDecl)
                {
                    item.Properties.Add(new Property
                    {
                        Name = propDecl.Identifier.Text,
                        Type = propDecl.Type.ToString(),
                        IsOptional = propDecl.Type.ToString().EndsWith("?")
                    });
                }
                else if (member is FieldDeclarationSyntax fieldDecl)
                {
                    foreach (var variable in fieldDecl.Declaration.Variables)
                    {
                        item.Properties.Add(new Property
                        {
                            Name = variable.Identifier.Text,
                            Type = fieldDecl.Declaration.Type.ToString(),
                            IsOptional = false
                        });
                    }
                }
                else if (member is MethodDeclarationSyntax methodDecl)
                {
                    item.Methods.Add(ConvertMethod(methodDecl));
                }
                else if (member is ConstructorDeclarationSyntax ctorDecl)
                {
                    item.Constructor = ConvertConstructor(ctorDecl);
                }
            }

            return item;
        }

        static ItemDecl ConvertInterface(InterfaceDeclarationSyntax interfaceDecl)
        {
            var item = new ItemDecl
            {
                Type = "interface",
                Name = interfaceDecl.Identifier.Text
            };

            foreach (var member in interfaceDecl.Members)
            {
                if (member is PropertyDeclarationSyntax propDecl)
                {
                    item.Properties.Add(new Property
                    {
                        Name = propDecl.Identifier.Text,
                        Type = propDecl.Type.ToString(),
                        IsOptional = propDecl.Type.ToString().EndsWith("?")
                    });
                }
            }

            return item;
        }

        static Method ConvertMethod(MethodDeclarationSyntax methodDecl)
        {
            var method = new Method
            {
                Name = methodDecl.Identifier.Text,
                ReturnType = methodDecl.ReturnType.ToString(),
                IsAsync = methodDecl.Modifiers.Any(m => m.IsKind(SyntaxKind.AsyncKeyword)),
                IsStatic = methodDecl.Modifiers.Any(m => m.IsKind(SyntaxKind.StaticKeyword))
            };

            foreach (var param in methodDecl.ParameterList.Parameters)
            {
                method.Params.Add(new Parameter
                {
                    Name = param.Identifier.Text,
                    Type = param.Type?.ToString() ?? "object",
                    IsOptional = param.Default != null
                });
            }

            if (methodDecl.Body != null)
            {
                method.Body = ConvertBlock(methodDecl.Body);
            }

            return method;
        }

        static Method ConvertConstructor(ConstructorDeclarationSyntax ctorDecl)
        {
            var method = new Method
            {
                Name = "constructor",
                ReturnType = "void",
                IsAsync = false,
                IsStatic = false
            };

            foreach (var param in ctorDecl.ParameterList.Parameters)
            {
                method.Params.Add(new Parameter
                {
                    Name = param.Identifier.Text,
                    Type = param.Type?.ToString() ?? "object",
                    IsOptional = param.Default != null
                });
            }

            if (ctorDecl.Body != null)
            {
                method.Body = ConvertBlock(ctorDecl.Body);
            }

            return method;
        }

        static List<Statement> ConvertBlock(BlockSyntax block)
        {
            var statements = new List<Statement>();

            foreach (var stmt in block.Statements)
            {
                var converted = ConvertStatement(stmt);
                if (converted != null)
                {
                    statements.Add(converted);
                }
            }

            return statements;
        }

        static Statement ConvertStatement(StatementSyntax stmt)
        {
            if (stmt is LocalDeclarationStatementSyntax localDecl)
            {
                var variable = localDecl.Declaration.Variables.First();
                return new Statement
                {
                    Type = localDecl.IsConst ? "const" : "variable",
                    Name = variable.Identifier.Text,
                    Value = variable.Initializer != null ? ConvertExpression(variable.Initializer.Value) : null
                };
            }
            else if (stmt is ExpressionStatementSyntax exprStmt)
            {
                // Check if it's an assignment
                if (exprStmt.Expression is AssignmentExpressionSyntax assignment)
                {
                    return new Statement
                    {
                        Type = "assign",
                        Target = assignment.Left.ToString(),
                        Value = ConvertExpression(assignment.Right)
                    };
                }
                // Regular expression statement
                return new Statement
                {
                    Type = "expr",
                    Expr = ConvertExpression(exprStmt.Expression)
                };
            }
            else if (stmt is IfStatementSyntax ifStmt)
            {
                var statement = new Statement
                {
                    Type = "if",
                    Condition = ConvertExpression(ifStmt.Condition),
                    ThenBody = ifStmt.Statement is BlockSyntax thenBlock
                        ? ConvertBlock(thenBlock)
                        : new List<Statement> { ConvertStatement(ifStmt.Statement) }
                };

                if (ifStmt.Else != null)
                {
                    statement.ElseBody = ifStmt.Else.Statement is BlockSyntax elseBlock
                        ? ConvertBlock(elseBlock)
                        : new List<Statement> { ConvertStatement(ifStmt.Else.Statement) };
                }

                return statement;
            }
            else if (stmt is ForStatementSyntax forStmt)
            {
                return new Statement
                {
                    Type = "for",
                    Iterator = forStmt.Declaration?.ToString() ?? forStmt.Initializers.FirstOrDefault()?.ToString() ?? "i",
                    Iterable = forStmt.Condition != null ? ConvertExpression(forStmt.Condition) : null,
                    Body = forStmt.Statement is BlockSyntax forBlock
                        ? ConvertBlock(forBlock)
                        : new List<Statement> { ConvertStatement(forStmt.Statement) }
                };
            }
            else if (stmt is ForEachStatementSyntax foreachStmt)
            {
                return new Statement
                {
                    Type = "for",
                    Iterator = foreachStmt.Identifier.Text,
                    Iterable = ConvertExpression(foreachStmt.Expression),
                    Body = foreachStmt.Statement is BlockSyntax foreachBlock
                        ? ConvertBlock(foreachBlock)
                        : new List<Statement> { ConvertStatement(foreachStmt.Statement) }
                };
            }
            else if (stmt is WhileStatementSyntax whileStmt)
            {
                return new Statement
                {
                    Type = "while",
                    Condition = ConvertExpression(whileStmt.Condition),
                    Body = whileStmt.Statement is BlockSyntax whileBlock
                        ? ConvertBlock(whileBlock)
                        : new List<Statement> { ConvertStatement(whileStmt.Statement) }
                };
            }
            else if (stmt is SwitchStatementSyntax switchStmt)
            {
                var cases = new List<CaseClause>();

                foreach (var section in switchStmt.Sections)
                {
                    var caseBody = new List<Statement>();
                    foreach (var bodyStmt in section.Statements)
                    {
                        var converted = ConvertStatement(bodyStmt);
                        if (converted != null)
                        {
                            caseBody.Add(converted);
                        }
                    }

                    foreach (var label in section.Labels)
                    {
                        if (label is CaseSwitchLabelSyntax caseLabel)
                        {
                            cases.Add(new CaseClause
                            {
                                IsDefault = false,
                                Values = new List<Expression> { ConvertExpression(caseLabel.Value) },
                                Body = caseBody
                            });
                        }
                        else if (label is DefaultSwitchLabelSyntax)
                        {
                            cases.Add(new CaseClause
                            {
                                IsDefault = true,
                                Values = new List<Expression>(),
                                Body = caseBody
                            });
                        }
                    }
                }

                return new Statement
                {
                    Type = "switch",
                    Value = ConvertExpression(switchStmt.Expression),
                    Cases = cases
                };
            }
            else if (stmt is TryStatementSyntax tryStmt)
            {
                var tryBody = ConvertBlock(tryStmt.Block);
                List<Statement> catchBody = null;
                string catchVar = null;
                List<Statement> finallyBody = null;

                foreach (var catchClause in tryStmt.Catches)
                {
                    catchVar = catchClause.Declaration?.Identifier.Text;
                    catchBody = ConvertBlock(catchClause.Block);
                    break; // Take first catch for simplicity
                }

                if (tryStmt.Finally != null)
                {
                    finallyBody = ConvertBlock(tryStmt.Finally.Block);
                }

                return new Statement
                {
                    Type = "try",
                    TryBody = tryBody,
                    CatchVar = catchVar,
                    CatchBody = catchBody,
                    FinallyBody = finallyBody
                };
            }
            else if (stmt is ReturnStatementSyntax returnStmt)
            {
                return new Statement
                {
                    Type = "return",
                    Value = returnStmt.Expression != null ? ConvertExpression(returnStmt.Expression) : null
                };
            }
            else if (stmt is ThrowStatementSyntax throwStmt)
            {
                return new Statement
                {
                    Type = "throw",
                    Value = ConvertExpression(throwStmt.Expression)
                };
            }
            else if (stmt is BreakStatementSyntax)
            {
                return new Statement
                {
                    Type = "break"
                };
            }
            else if (stmt is ContinueStatementSyntax)
            {
                return new Statement
                {
                    Type = "continue"
                };
            }

            return null;
        }

        static Expression ConvertExpression(ExpressionSyntax expr)
        {
            if (expr is BinaryExpressionSyntax binaryExpr)
            {
                return new Expression
                {
                    Type = "binary",
                    Op = binaryExpr.OperatorToken.Text,
                    Left = ConvertExpression(binaryExpr.Left),
                    Right = ConvertExpression(binaryExpr.Right)
                };
            }
            else if (expr is IdentifierNameSyntax identExpr)
            {
                return new Expression
                {
                    Type = "ident",
                    Name = identExpr.Identifier.Text
                };
            }
            else if (expr is LiteralExpressionSyntax literalExpr)
            {
                return new Expression
                {
                    Type = "literal",
                    Value = literalExpr.Token.Value
                };
            }
            else if (expr is InvocationExpressionSyntax invocationExpr)
            {
                var args = new List<Expression>();
                foreach (var arg in invocationExpr.ArgumentList.Arguments)
                {
                    args.Add(ConvertExpression(arg.Expression));
                }

                return new Expression
                {
                    Type = "call",
                    Function = invocationExpr.Expression.ToString(),
                    Args = args
                };
            }
            else if (expr is ObjectCreationExpressionSyntax objectCreation)
            {
                var args = new List<Expression>();
                if (objectCreation.ArgumentList != null)
                {
                    foreach (var arg in objectCreation.ArgumentList.Arguments)
                    {
                        args.Add(ConvertExpression(arg.Expression));
                    }
                }

                return new Expression
                {
                    Type = "new",
                    Class = objectCreation.Type.ToString(),
                    Args = args
                };
            }
            else if (expr is ArrayCreationExpressionSyntax arrayCreation)
            {
                var elements = new List<Expression>();
                if (arrayCreation.Initializer != null)
                {
                    foreach (var element in arrayCreation.Initializer.Expressions)
                    {
                        elements.Add(ConvertExpression(element));
                    }
                }

                return new Expression
                {
                    Type = "array",
                    Elements = elements
                };
            }

            // Default: return as identifier
            return new Expression
            {
                Type = "ident",
                Name = expr.ToString()
            };
        }
    }
}
