# symtable 정의

### defer symtable

```h
typedef enum _block_type {
    // 수정
    FunctionBlock, ClassBlock, ModuleBlock, DeferBlock,
    ...
}
```
DeferBlock이라는 새로운 블록 정의


```c
case Defer_kind:
    // 정의한 DeferBlcok에 진입
    if (!symtable_enter_block(st, &_Py_ID(defer),
                                DeferBlock, (void *)s, 
                                s->lineno, s->col_offset, 
                                s->end_lineno, s->end_col_offset))
        VISIT_QUIT(st, 0);

    // ast 노드에 있는 arguments와 body 탐색
    VISIT(st, arguments, s->v.Defer.args);
    VISIT_SEQ(st, stmt, s->v.Defer.body);

    PyObject *key, *value;
    Py_ssize_t pos = 0;

    Py_ssize_t stack_size = PyList_GET_SIZE(st->st_stack);
    PySTEntryObject *outer = NULL;
    PyObject *outer_symbols = NULL;

    // defer 문이 function, class 등 다른 스코프 안에 선언된 경우
    if (stack_size >= 2) {
        outer = (PySTEntryObject *)PyList_GET_ITEM(st->st_stack, stack_size - 2);
        outer_symbols = outer->ste_symbols;
    }
    
    // defer symbol table 순회
    while (PyDict_Next(st->st_cur->ste_symbols, &pos, &key, &value)) {
        long flags = symtable_lookup(st, key);
        if (flags < 0) {
            VISIT_QUIT(st, 0);
        }

        if (!(flags & DEF_PARAM)) {
            continue;
        }

        if (outer_symbols) {
            // 상위 테이블에서 key값(변수, 함수 등의 이름)이 존재하는지 확인
            long outer_flags = symtable_lookup_entry(st, outer, key);
            //실제로 존재하는지 확인 및 타입 확인
            if (!outer_flags) {
                PyObject *error_msg = PyUnicode_FromFormat("no binding for defer '%U' found", key);
                Py_DECREF(error_msg);
            }
        }
    }

    if (!symtable_exit_block(st))
        VISIT_QUIT(st, 0);
    break;
```

defer문을 해석하여 defer symtable을 만들 수 있도록 함

## 예시
```py
import tabulate # 설치 필요
import symtable

code ="""
a = 1
b = 2

defer:
    a += 2
"""

_st = symtable.symtable(code, "example.py", "exec")

def show(table):
    print("Symtable {0}".format(table.get_name()))
    
    print(
        tabulate.tabulate(
            [
                (
                    symbol.get_name(),
                    symbol.is_global(),
                    symbol.is_local(),
                    symbol.get_namespaces(),
                )
                for symbol in table.get_symbols()
            ],
            headers=["name", "global", "local", "namespaces"],
            tablefmt="grid",
        )
    )
    if table.has_children():
        [show(child) for child in table.get_children()]


show(_st)
```

결과
```
Symtable top
+--------+----------+---------+--------------+
| name   | global   | local   | namespaces   |
+========+==========+=========+==============+
| a      | True     | True    | ()           |
+--------+----------+---------+--------------+
| b      | True     | True    | ()           |
+--------+----------+---------+--------------+
Symtable defer
+--------+----------+---------+--------------+
| name   | global   | local   | namespaces   |
+========+==========+=========+==============+
| a      | False    | True    | ()           |
+--------+----------+---------+--------------+
```
defer symtable이 만들어짐