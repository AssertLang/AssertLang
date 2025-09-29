from tools.conditional.adapters import adapter_py as conditional
from tools.loop.adapters import adapter_py as loop
from tools.branch.adapters import adapter_py as branch


def test_conditional_eq():
    res = conditional.handle({'left': 'a', 'op': '==', 'right': 'a'})
    assert res['ok'] is True
    assert res['data']['pass'] is True


def test_loop_iterations():
    res = loop.handle({'items': [1, 2, 3], 'body': []})
    assert res['ok'] is True
    assert res['data']['iterations'] == 3


def test_branch_select():
    res = branch.handle({'key': 'x', 'value': 'A', 'cases': {'A': [], 'B': []}})
    assert res['ok'] is True
    assert res['data']['selected'] == 'A'


