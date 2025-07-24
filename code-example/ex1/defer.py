import ast
import inspect
import textwrap
from typing import Callable

class DeferTransformer(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        # 함수 내부에 defer 객체 생성 및 try-finally 삽입
        setup ="defer = Defer()"
        setup_nodes = ast.parse(textwrap.dedent(setup)).body

        clean = "defer.clean()"
        clean_nodes = ast.parse(textwrap.dedent(clean)).body

        try_node = ast.Try(
            body=node.body,
            handlers=[],
            orelse=[],
            finalbody=clean_nodes
        )

        node.body = [
            *setup_nodes,
            try_node
        ]

        return node

class Defer:
    # defer
    def __init__(self):
        self._stack = []

    def __call__(self, func):
        self._stack.append(func)

    def clean(self):
        while self._stack:
            self._stack.pop()()

def defer(func:Callable):
    # code(str) 가져오기
    source = textwrap.dedent(inspect.getsource(func))
    
    # ast로 parsing
    tree = ast.parse(source)

    # decorate 제거(안하면 무한 제귀)
    node = tree.body[0]
    node.decorator_list = [
        d for d in node.decorator_list
        if not (isinstance(d, ast.Name) and d.id == 'defer')
    ]

    # tree 변경
    tree = DeferTransformer().visit(tree)
    ast.fix_missing_locations(tree)

    # globals 전달
    globals_dict = func.__globals__.copy()
    globals_dict['Defer'] = Defer


    # ast compile
    filename = f"{func.__name__}_defer"
    code = compile(tree, filename=filename, mode="exec")

    # code 실행 
    exec(code, globals_dict)

    # 변경된 ast로 생성된 function 반환
    return globals_dict[func.__name__]
