# defer 문법 정의

문법
```
# Grammar/python.gram

# Defer definitions
# -----------------
# defer 문법
defer_stmt[stmt_ty]:
    | 'defer' a=[defer_params] ':' b=block { 
        _PyAST_Defer((a) ? a : CHECK(arguments_ty, _PyPegen_empty_arguments(p)), b, EXTRA) }

# Defer parameters
# -------------------
# defer paramter 정의
defer_params[arguments_ty]:
    | defer_parameters
    # | invalid_defer_parameters 같은게 추가적으로 들어갈 수 있음

# arguments를 받는 정석적인 parameter 정의
defer_parameters[arguments_ty]:
    | a=defer_param_no_default+ { _PyPegen_make_arguments(p, NULL, NULL, a, NULL, NULL) }

# argument뒤 붙는 구별자 처리(',' 혹은 ':')
defer_param_no_default[arg_ty]:
    | a=defer_param ',' { a }
    | a=defer_param &':' { a }

# argument 인자 하나
defer_param[arg_ty]: a=NAME { _PyAST_arg(a->v.Name.id, NULL, NULL, EXTRA) }
```

## 예시
```py
defer: print("hi")
```
결과
``` 

```
errro 없이 해석됨