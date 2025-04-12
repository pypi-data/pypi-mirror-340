from os import path
from typing import Any, Callable, Tuple


def _list2str(lst: list, prefix="") -> str:
    """
    将 list 内的元素转化为字符串，使得打印时能够按行输出并在前面加上序号(从1开始)
    e.g.
    [a,b,c] -> 1. a\n2. b\n3. c
    """
    i = 1
    res_list = []
    for x in lst:
        res_list.append(prefix + str(i) + ". " + str(x))
        i += 1
    res_str = "\n".join(res_list)
    return res_str


def _islegal_int(s: str, low=1, high=100) -> Tuple[bool, Any]:
    try:
        s = int(s)
        assert low <= s <= high
        return True, s
    except ValueError and AssertionError:
        return False, None


def _islegal_path(s: str) -> Tuple[bool, Any]:
    try:
        if s == "":
            s = "list.txt"
        s = path.abspath(s)
        return True, s
    except ValueError:
        return False, None


def _get_input_until_success(
    prompt: str, islegal: Callable[[str], Tuple[bool, Any]] = _islegal_int
):
    while True:
        a, b = islegal(input(prompt))
        if a:
            return b
        else:
            print("输入不合法, 请重新输入.")


def _handle_num(keyword):
    keyword = keyword.upper().strip()
    if keyword.endswith("-C"):
        keyword = keyword[:-2]
    return keyword
