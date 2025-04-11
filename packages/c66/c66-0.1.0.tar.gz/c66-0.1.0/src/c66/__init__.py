# src/c66/__init__.py
from inspect import currentframe, getframeinfo
from ast import parse, unparse

def pp(*args):
    # 抓呼叫這個函數的那一行程式碼
    frame = currentframe().f_back
    code_context = getframeinfo(frame).code_context
    if not code_context:
        for arg in args:
            print(arg)
        return

    code_line = code_context[0].strip()
    
    try:
        # 解析 AST 拿到呼叫 pp 裡面的參數原始碼
        tree = parse(code_line)
        call = tree.body[0].value  # 假設這行是一個 expression
        arg_sources = [unparse(arg) for arg in call.args]
    except Exception:
        # fallback
        arg_sources = [f'arg{i}' for i in range(len(args))]

    for name, value in zip(arg_sources, args):
        print(f"{name}: {value}")