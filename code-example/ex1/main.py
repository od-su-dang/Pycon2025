from defer import defer

@defer
def example():
    defer(lambda: print("Hello,"))
    defer(lambda: print("Python!"))
    print("yeah!!")

    # ->
    # def example():
    #     defer = Defer()
    #     try:
    #         defer(lambda: print("Hello,"))
    #         defer(lambda: print("Python!"))
    #         print("yeah!!")
    #     finally:
    #         defer.clean()

# 실행
example()