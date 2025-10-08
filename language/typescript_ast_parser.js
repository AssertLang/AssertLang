"use strict";
/**
 * TypeScript AST Parser: Official TypeScript Compiler API → JSON
 *
 * This parser uses TypeScript's official compiler API for 100% accurate parsing.
 * Outputs JSON AST that can be consumed by Python.
 *
 * Usage: node typescript_ast_parser.js <file.ts>
 */
Object.defineProperty(exports, "__esModule", { value: true });
const ts = require("typescript");
const fs = require("fs");
function main() {
    const args = process.argv.slice(2);
    if (args.length < 1) {
        console.error('Usage: node typescript_ast_parser.js <file.ts>');
        process.exit(1);
    }
    const filename = args[0];
    const sourceCode = fs.readFileSync(filename, 'utf8');
    // Parse TypeScript source
    const sourceFile = ts.createSourceFile(filename, sourceCode, ts.ScriptTarget.Latest, true);
    // Convert to our JSON format
    const fileAST = convertFile(sourceFile);
    // Output JSON
    console.log(JSON.stringify(fileAST, null, 2));
}
function convertFile(sourceFile) {
    const items = [];
    ts.forEachChild(sourceFile, (node) => {
        if (ts.isClassDeclaration(node)) {
            items.push(convertClass(node));
        }
        else if (ts.isInterfaceDeclaration(node)) {
            items.push(convertInterface(node));
        }
        else if (ts.isFunctionDeclaration(node)) {
            items.push(convertFunction(node));
        }
    });
    return { items };
}
function convertClass(node) {
    const name = node.name ? node.name.text : 'anonymous';
    const properties = [];
    const methods = [];
    let constructor;
    node.members.forEach((member) => {
        if (ts.isPropertyDeclaration(member)) {
            properties.push(convertProperty(member));
        }
        else if (ts.isMethodDeclaration(member)) {
            methods.push(convertMethod(member));
        }
        else if (ts.isConstructorDeclaration(member)) {
            constructor = convertConstructor(member);
        }
    });
    return {
        type: 'class',
        name,
        properties,
        methods,
        constructor,
    };
}
function convertInterface(node) {
    const name = node.name.text;
    const properties = [];
    node.members.forEach((member) => {
        if (ts.isPropertySignature(member)) {
            const propName = member.name && ts.isIdentifier(member.name) ? member.name.text : 'unknown';
            const propType = member.type ? typeToString(member.type) : 'any';
            const isOptional = member.questionToken !== undefined;
            properties.push({
                name: propName,
                type: propType,
                isOptional,
            });
        }
    });
    return {
        type: 'interface',
        name,
        properties,
    };
}
function convertFunction(node) {
    const name = node.name ? node.name.text : 'anonymous';
    const params = convertParameters(node.parameters);
    const returnType = node.type ? typeToString(node.type) : 'void';
    const body = node.body ? convertBlock(node.body) : [];
    const isAsync = node.modifiers?.some(m => m.kind === ts.SyntaxKind.AsyncKeyword) ?? false;
    return {
        type: 'function',
        name,
        params,
        returnType,
        body,
        isAsync,
    };
}
function convertProperty(node) {
    const name = node.name && ts.isIdentifier(node.name) ? node.name.text : 'unknown';
    const type = node.type ? typeToString(node.type) : 'any';
    const isOptional = node.questionToken !== undefined;
    return { name, type, isOptional };
}
function convertMethod(node) {
    const name = node.name && ts.isIdentifier(node.name) ? node.name.text : 'unknown';
    const params = convertParameters(node.parameters);
    const returnType = node.type ? typeToString(node.type) : 'void';
    const body = node.body ? convertBlock(node.body) : [];
    const isAsync = node.modifiers?.some(m => m.kind === ts.SyntaxKind.AsyncKeyword) ?? false;
    const isStatic = node.modifiers?.some(m => m.kind === ts.SyntaxKind.StaticKeyword) ?? false;
    return {
        name,
        params,
        returnType,
        body,
        isAsync,
        isStatic,
    };
}
function convertConstructor(node) {
    const params = convertParameters(node.parameters);
    const body = node.body ? convertBlock(node.body) : [];
    return {
        name: 'constructor',
        params,
        returnType: 'void',
        body,
        isAsync: false,
        isStatic: false,
    };
}
function convertParameters(params) {
    return params.map((param) => {
        const name = param.name && ts.isIdentifier(param.name) ? param.name.text : 'unknown';
        const type = param.type ? typeToString(param.type) : 'any';
        const isOptional = param.questionToken !== undefined;
        return { name, type, isOptional };
    });
}
function convertBlock(block) {
    const statements = [];
    block.statements.forEach((stmt) => {
        const converted = convertStatement(stmt);
        if (converted) {
            statements.push(converted);
        }
    });
    return statements;
}
function convertStatement(node) {
    if (ts.isVariableStatement(node)) {
        // Handle variable declarations
        const decl = node.declarationList.declarations[0];
        if (decl && ts.isIdentifier(decl.name)) {
            const isConst = (node.declarationList.flags & ts.NodeFlags.Const) !== 0;
            const name = decl.name.text;
            const value = decl.initializer ? convertExpression(decl.initializer) : undefined;
            return isConst
                ? { type: 'const', name, value }
                : { type: 'variable', name, value };
        }
    }
    else if (ts.isExpressionStatement(node)) {
        // Check if it's an assignment
        if (ts.isBinaryExpression(node.expression) && node.expression.operatorToken.kind === ts.SyntaxKind.EqualsToken) {
            const target = node.expression.left.getText();
            const value = convertExpression(node.expression.right);
            return { type: 'assign', target, value };
        }
        // Regular expression statement
        return { type: 'expr', expr: convertExpression(node.expression) };
    }
    else if (ts.isIfStatement(node)) {
        const condition = convertExpression(node.expression);
        const thenBody = ts.isBlock(node.thenStatement)
            ? convertBlock(node.thenStatement)
            : [convertStatement(node.thenStatement)].filter(Boolean);
        const elseBody = node.elseStatement
            ? ts.isBlock(node.elseStatement)
                ? convertBlock(node.elseStatement)
                : [convertStatement(node.elseStatement)].filter(Boolean)
            : undefined;
        return { type: 'if', condition, thenBody, elseBody };
    }
    else if (ts.isForStatement(node)) {
        // C-style for loop: for (let i = 0; i < n; i++)
        const iterator = node.initializer ? node.initializer.getText() : 'i';
        const iterable = node.condition ? convertExpression(node.condition) : { type: 'ident', name: 'unknown' };
        const body = ts.isBlock(node.statement)
            ? convertBlock(node.statement)
            : [convertStatement(node.statement)].filter(Boolean);
        return { type: 'for', iterator, iterable, body };
    }
    else if (ts.isForOfStatement(node)) {
        // for...of loop: for (const item of array)
        const iterator = node.initializer.getText();
        const iterable = convertExpression(node.expression);
        const body = ts.isBlock(node.statement)
            ? convertBlock(node.statement)
            : [convertStatement(node.statement)].filter(Boolean);
        return { type: 'for', iterator, iterable, body };
    }
    else if (ts.isWhileStatement(node)) {
        const condition = convertExpression(node.expression);
        const body = ts.isBlock(node.statement)
            ? convertBlock(node.statement)
            : [convertStatement(node.statement)].filter(Boolean);
        return { type: 'while', condition, body };
    }
    else if (ts.isSwitchStatement(node)) {
        const value = convertExpression(node.expression);
        const cases = [];
        node.caseBlock.clauses.forEach((clause) => {
            if (ts.isCaseClause(clause)) {
                const caseValue = convertExpression(clause.expression);
                const caseBody = [];
                clause.statements.forEach((stmt) => {
                    const converted = convertStatement(stmt);
                    if (converted)
                        caseBody.push(converted);
                });
                cases.push({ isDefault: false, values: [caseValue], body: caseBody });
            }
            else if (ts.isDefaultClause(clause)) {
                const defaultBody = [];
                clause.statements.forEach((stmt) => {
                    const converted = convertStatement(stmt);
                    if (converted)
                        defaultBody.push(converted);
                });
                cases.push({ isDefault: true, body: defaultBody });
            }
        });
        return { type: 'switch', value, cases };
    }
    else if (ts.isTryStatement(node)) {
        const tryBody = convertBlock(node.tryBlock);
        let catchVar;
        let catchBody;
        let finallyBody;
        if (node.catchClause) {
            catchVar = node.catchClause.variableDeclaration?.name.getText();
            catchBody = convertBlock(node.catchClause.block);
        }
        if (node.finallyBlock) {
            finallyBody = convertBlock(node.finallyBlock);
        }
        return { type: 'try', tryBody, catchVar, catchBody, finallyBody };
    }
    else if (ts.isReturnStatement(node)) {
        const value = node.expression ? convertExpression(node.expression) : undefined;
        return { type: 'return', value };
    }
    else if (ts.isThrowStatement(node)) {
        const value = convertExpression(node.expression);
        return { type: 'throw', value };
    }
    else if (ts.isBreakStatement(node)) {
        return { type: 'break' };
    }
    else if (ts.isContinueStatement(node)) {
        return { type: 'continue' };
    }
    return null;
}
function convertExpression(node) {
    if (ts.isBinaryExpression(node)) {
        const op = node.operatorToken.getText();
        const left = convertExpression(node.left);
        const right = convertExpression(node.right);
        return { type: 'binary', op, left, right };
    }
    else if (ts.isIdentifier(node)) {
        return { type: 'ident', name: node.text };
    }
    else if (ts.isNumericLiteral(node) || ts.isStringLiteral(node)) {
        return { type: 'literal', value: node.text };
    }
    else if (node.kind === ts.SyntaxKind.TrueKeyword || node.kind === ts.SyntaxKind.FalseKeyword) {
        return { type: 'literal', value: node.kind === ts.SyntaxKind.TrueKeyword };
    }
    else if (ts.isCallExpression(node)) {
        const functionName = node.expression.getText();
        const args = node.arguments.map(convertExpression);
        return { type: 'call', function: functionName, args };
    }
    else if (ts.isNewExpression(node)) {
        const className = node.expression.getText();
        const args = node.arguments ? node.arguments.map(convertExpression) : [];
        return { type: 'new', class: className, args };
    }
    else if (ts.isArrayLiteralExpression(node)) {
        const elements = node.elements.map(convertExpression);
        return { type: 'array', elements };
    }
    else if (ts.isObjectLiteralExpression(node)) {
        const properties = node.properties.map((prop) => {
            if (ts.isPropertyAssignment(prop)) {
                const key = prop.name.getText();
                const value = convertExpression(prop.initializer);
                return { key, value };
            }
            return { key: 'unknown', value: { type: 'literal', value: null } };
        });
        return { type: 'object', properties };
    }
    else if (ts.isArrowFunction(node)) {
        const params = node.parameters.map(p => p.name.getText());
        const body = ts.isBlock(node.body)
            ? convertBlock(node.body)
            : convertExpression(node.body);
        return { type: 'arrow', params, body: body };
    }
    // Default: return as identifier
    return { type: 'ident', name: node.getText() };
}
function typeToString(type) {
    return type.getText();
}
main();
