# ast를 활용한 defer 구현

### 설계

stack을 가지는 defer 객체를 생성 후  try-finally를 사용해 defer_stack에 저장된 function을 실행

이는 function의 ast 변경으로 수행가능

### 예시
다음과 같은 function 작성
```py
from defer import defer

@defer
def example():
    defer(lambda: print("Hello,"))
    defer(lambda: print("Python!"))
    print("yeah!!")
```

다음과 같이 변경됨
```py
def example():
    defer = Defer()
    try:
        defer(lambda: print("Hello,"))
        defer(lambda: print("Python!"))
        print("yeah!!")
    finally:
        defer.clean()
```

결과
```
yeah!!
Python!
Hello,
```