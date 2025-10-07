// Rust AST Parser: Official syn crate → JSON
//
// This parser uses Rust's syn crate for 100% accurate Rust parsing.
// Outputs JSON AST that can be consumed by Python.
//
// Usage: rust_ast_parser <file.rs>

use serde::{Deserialize, Serialize};
use std::env;
use std::fs;
use syn::{
    visit::Visit, Expr, File, Item, ItemFn, ItemImpl, ItemStruct, Stmt, Type,
};

// JSON output structures
#[derive(Serialize, Deserialize, Debug)]
struct FileAST {
    items: Vec<ItemDecl>,
}

#[derive(Serialize, Deserialize, Debug)]
#[serde(tag = "type")]
enum ItemDecl {
    #[serde(rename = "struct")]
    Struct {
        name: String,
        fields: Vec<Field>,
    },
    #[serde(rename = "impl")]
    Impl {
        target: String,
        methods: Vec<Function>,
    },
    #[serde(rename = "function")]
    Function(Function),
}

#[derive(Serialize, Deserialize, Debug, Clone)]
struct Field {
    name: String,
    #[serde(rename = "type")]
    field_type: String,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
struct Function {
    name: String,
    params: Vec<Parameter>,
    return_type: String,
    body: Vec<Statement>,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
struct Parameter {
    name: String,
    #[serde(rename = "type")]
    param_type: String,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
#[serde(tag = "type")]
enum Statement {
    #[serde(rename = "let")]
    Let {
        name: String,
        value: Option<Expression>,
    },
    #[serde(rename = "assign")]
    Assign {
        target: String,
        value: Expression,
    },
    #[serde(rename = "if")]
    If {
        condition: Expression,
        then_body: Vec<Statement>,
        else_body: Option<Vec<Statement>>,
    },
    #[serde(rename = "for")]
    For {
        iterator: String,
        iterable: Expression,
        body: Vec<Statement>,
    },
    #[serde(rename = "while")]
    While {
        condition: Expression,
        body: Vec<Statement>,
    },
    #[serde(rename = "return")]
    Return { value: Option<Expression> },
    #[serde(rename = "expr")]
    Expr { expr: Expression },
}

#[derive(Serialize, Deserialize, Debug, Clone)]
#[serde(tag = "type")]
enum Expression {
    #[serde(rename = "binary")]
    Binary {
        op: String,
        left: Box<Expression>,
        right: Box<Expression>,
    },
    #[serde(rename = "ident")]
    Ident { name: String },
    #[serde(rename = "literal")]
    Literal { value: String },
    #[serde(rename = "call")]
    Call {
        function: String,
        args: Vec<Expression>,
    },
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: rust_ast_parser <file.rs>");
        std::process::exit(1);
    }

    let filename = &args[1];
    let content = fs::read_to_string(filename)
        .unwrap_or_else(|e| {
            eprintln!("Failed to read file: {}", e);
            std::process::exit(1);
        });

    // Parse Rust source
    let syntax = syn::parse_file(&content)
        .unwrap_or_else(|e| {
            eprintln!("Parse error: {}", e);
            std::process::exit(1);
        });

    // Convert to our JSON format
    let file_ast = convert_file(&syntax);

    // Output JSON
    let json = serde_json::to_string_pretty(&file_ast)
        .unwrap_or_else(|e| {
            eprintln!("JSON encode error: {}", e);
            std::process::exit(1);
        });

    println!("{}", json);
}

fn convert_file(file: &File) -> FileAST {
    let mut items = Vec::new();

    for item in &file.items {
        match item {
            Item::Struct(item_struct) => {
                items.push(convert_struct(item_struct));
            }
            Item::Impl(item_impl) => {
                if let Some(impl_decl) = convert_impl(item_impl) {
                    items.push(impl_decl);
                }
            }
            Item::Fn(item_fn) => {
                items.push(ItemDecl::Function(convert_function(item_fn)));
            }
            _ => {}
        }
    }

    FileAST { items }
}

fn convert_struct(item: &ItemStruct) -> ItemDecl {
    let mut fields = Vec::new();

    if let syn::Fields::Named(named_fields) = &item.fields {
        for field in &named_fields.named {
            if let Some(ident) = &field.ident {
                fields.push(Field {
                    name: ident.to_string(),
                    field_type: type_to_string(&field.ty),
                });
            }
        }
    }

    ItemDecl::Struct {
        name: item.ident.to_string(),
        fields,
    }
}

fn convert_impl(item: &ItemImpl) -> Option<ItemDecl> {
    // Get the type being implemented
    let target = type_to_string(&item.self_ty);

    let mut methods = Vec::new();
    for impl_item in &item.items {
        if let syn::ImplItem::Fn(method) = impl_item {
            methods.push(convert_method(method));
        }
    }

    if methods.is_empty() {
        return None;
    }

    Some(ItemDecl::Impl { target, methods })
}

fn convert_function(item: &ItemFn) -> Function {
    let name = item.sig.ident.to_string();
    let params = convert_params(&item.sig.inputs);
    let return_type = convert_return_type(&item.sig.output);
    let body = convert_block(&item.block);

    Function {
        name,
        params,
        return_type,
        body,
    }
}

fn convert_method(item: &syn::ImplItemFn) -> Function {
    let name = item.sig.ident.to_string();
    let params = convert_params(&item.sig.inputs);
    let return_type = convert_return_type(&item.sig.output);
    let body = convert_block(&item.block);

    Function {
        name,
        params,
        return_type,
        body,
    }
}

fn convert_params(inputs: &syn::punctuated::Punctuated<syn::FnArg, syn::token::Comma>) -> Vec<Parameter> {
    let mut params = Vec::new();

    for input in inputs {
        match input {
            syn::FnArg::Typed(pat_type) => {
                if let syn::Pat::Ident(pat_ident) = &*pat_type.pat {
                    params.push(Parameter {
                        name: pat_ident.ident.to_string(),
                        param_type: type_to_string(&pat_type.ty),
                    });
                }
            }
            syn::FnArg::Receiver(_) => {
                // Skip 'self' parameter
            }
        }
    }

    params
}

fn convert_return_type(output: &syn::ReturnType) -> String {
    match output {
        syn::ReturnType::Default => "()".to_string(),
        syn::ReturnType::Type(_, ty) => type_to_string(ty),
    }
}

fn convert_block(block: &syn::Block) -> Vec<Statement> {
    let mut statements = Vec::new();

    for stmt in &block.stmts {
        if let Some(converted) = convert_statement(stmt) {
            statements.push(converted);
        }
    }

    statements
}

fn convert_statement(stmt: &Stmt) -> Option<Statement> {
    match stmt {
        Stmt::Local(local) => {
            // let x = 5;
            let name = if let syn::Pat::Ident(pat_ident) = &local.pat {
                pat_ident.ident.to_string()
            } else {
                "unknown".to_string()
            };

            let value = if let Some(init) = &local.init {
                Some(convert_expr(&init.expr))
            } else {
                None
            };

            Some(Statement::Let { name, value })
        }
        Stmt::Expr(expr, _) => {
            // Handle different expression types
            match expr {
                Expr::If(expr_if) => Some(convert_if(expr_if)),
                Expr::ForLoop(expr_for) => Some(convert_for(expr_for)),
                Expr::While(expr_while) => Some(convert_while(expr_while)),
                Expr::Return(expr_return) => Some(Statement::Return {
                    value: expr_return.expr.as_ref().map(|e| convert_expr(e)),
                }),
                Expr::Assign(expr_assign) => {
                    let target = expr_to_string(&expr_assign.left);
                    let value = convert_expr(&expr_assign.right);
                    Some(Statement::Assign { target, value })
                }
                _ => Some(Statement::Expr {
                    expr: convert_expr(expr),
                }),
            }
        }
        _ => None,
    }
}

fn convert_if(expr_if: &syn::ExprIf) -> Statement {
    let condition = convert_expr(&expr_if.cond);
    let then_body = convert_block(&expr_if.then_branch);
    let else_body = expr_if.else_branch.as_ref().and_then(|(_, else_expr)| {
        if let Expr::Block(block_expr) = &**else_expr {
            Some(convert_block(&block_expr.block))
        } else {
            None
        }
    });

    Statement::If {
        condition,
        then_body,
        else_body,
    }
}

fn convert_for(expr_for: &syn::ExprForLoop) -> Statement {
    let iterator = if let syn::Pat::Ident(pat_ident) = &*expr_for.pat {
        pat_ident.ident.to_string()
    } else {
        "it".to_string()
    };

    let iterable = convert_expr(&expr_for.expr);
    let body = convert_block(&expr_for.body);

    Statement::For {
        iterator,
        iterable,
        body,
    }
}

fn convert_while(expr_while: &syn::ExprWhile) -> Statement {
    let condition = convert_expr(&expr_while.cond);
    let body = convert_block(&expr_while.body);

    Statement::While { condition, body }
}

fn convert_expr(expr: &Expr) -> Expression {
    match expr {
        Expr::Binary(binary) => {
            let op = match binary.op {
                syn::BinOp::Add(_) => "+",
                syn::BinOp::Sub(_) => "-",
                syn::BinOp::Mul(_) => "*",
                syn::BinOp::Div(_) => "/",
                syn::BinOp::Eq(_) => "==",
                syn::BinOp::Ne(_) => "!=",
                syn::BinOp::Lt(_) => "<",
                syn::BinOp::Gt(_) => ">",
                syn::BinOp::Le(_) => "<=",
                syn::BinOp::Ge(_) => ">=",
                syn::BinOp::And(_) => "&&",
                syn::BinOp::Or(_) => "||",
                _ => "unknown",
            };

            Expression::Binary {
                op: op.to_string(),
                left: Box::new(convert_expr(&binary.left)),
                right: Box::new(convert_expr(&binary.right)),
            }
        }
        Expr::Path(path) => Expression::Ident {
            name: path
                .path
                .segments
                .iter()
                .map(|s| s.ident.to_string())
                .collect::<Vec<_>>()
                .join("::"),
        },
        Expr::Lit(lit) => Expression::Literal {
            value: quote::quote!(#lit).to_string(),
        },
        Expr::Call(call) => {
            let function = expr_to_string(&call.func);
            let args = call.args.iter().map(convert_expr).collect();

            Expression::Call { function, args }
        }
        _ => Expression::Ident {
            name: "unknown".to_string(),
        },
    }
}

fn type_to_string(ty: &Type) -> String {
    quote::quote!(#ty).to_string()
}

fn expr_to_string(expr: &Expr) -> String {
    quote::quote!(#expr).to_string()
}
