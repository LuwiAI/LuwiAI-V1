"""Minimal guarded tool runtime for agent experiments.

The model must emit one JSON object such as
{"tool":"calculator","arguments":{"expression":"(12 + 7) * 2"}}.
Only the explicitly registered tools can be called. This is not a complete
agent, sandbox, or security boundary for untrusted applications.
"""
import ast
import json
import operator


_BINARY = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
           ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod}
_UNARY = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def safe_arithmetic(expression: str) -> int:
    """Evaluate a bounded integer arithmetic expression using an AST allowlist."""
    if not isinstance(expression, str) or len(expression) > 200:
        raise ValueError("expression must be a string of at most 200 characters")
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError("invalid arithmetic expression") from exc

    def visit(node, depth=0):
        if depth > 20:
            raise ValueError("expression is too deeply nested")
        if isinstance(node, ast.Expression):
            return visit(node.body, depth + 1)
        if isinstance(node, ast.Constant) and type(node.value) is int:
            if abs(node.value) > 10**12:
                raise ValueError("integer literal exceeds limit")
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _BINARY:
            left, right = visit(node.left, depth + 1), visit(node.right, depth + 1)
            result = _BINARY[type(node.op)](left, right)
            if abs(result) > 10**12:
                raise ValueError("result exceeds limit")
            return result
        if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY:
            return _UNARY[type(node.op)](visit(node.operand, depth + 1))
        raise ValueError(f"unsupported expression element: {type(node).__name__}")

    return visit(tree)


class ToolRuntime:
    """Dispatch model requests only to the fixed built-in allowlist."""
    def __init__(self):
        self._tools = {"calculator": self._calculator}

    @staticmethod
    def _calculator(arguments):
        if not isinstance(arguments, dict) or set(arguments) != {"expression"}:
            raise ValueError("calculator expects only an expression argument")
        return {"result": safe_arithmetic(arguments["expression"])}

    def dispatch(self, request):
        if isinstance(request, str):
            try:
                request = json.loads(request)
            except json.JSONDecodeError as exc:
                raise ValueError("tool request must be valid JSON") from exc
        if not isinstance(request, dict) or set(request) != {"tool", "arguments"}:
            raise ValueError("request must contain exactly tool and arguments")
        name = request["tool"]
        if name not in self._tools:
            raise ValueError(f"tool is not allowed: {name}")
        return {"tool": name, "observation": self._tools[name](request["arguments"])}
