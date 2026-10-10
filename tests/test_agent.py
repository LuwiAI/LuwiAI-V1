import pytest
from luwiai.agent import ToolRuntime, safe_arithmetic


def test_calculator_tool():
    runtime = ToolRuntime()
    assert runtime.dispatch('{"tool":"calculator","arguments":{"expression":"(12 + 7) * 2"}}') == {
        "tool": "calculator", "observation": {"result": 38}
    }


@pytest.mark.parametrize("expression", ["__import__('os').system('id')", "2 ** 100", "open('/etc/passwd')", "1 / 2"])
def test_calculator_rejects_unsupported_operations(expression):
    with pytest.raises(ValueError):
        safe_arithmetic(expression)


def test_unknown_tool_is_rejected():
    with pytest.raises(ValueError, match="not allowed"):
        ToolRuntime().dispatch({"tool": "shell", "arguments": {"command": "id"}})
