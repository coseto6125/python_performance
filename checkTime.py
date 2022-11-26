import asyncio
from time import perf_counter


def checkTimer(func):
    """
    非 async 效能檢測
    """

    def clocked(*args, **params):
        t0 = perf_counter()
        result = func(*args, **params)
        elapsed = perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print(f'[{elapsed:0.8f}s] {name}({arg_str}) -> {result}')
        return result

    return clocked


def checkTimer_aio(func):
    """
    async 效能檢測
    """

    async def process(func, *args, **params):
        if asyncio.iscoroutinefunction(func):
            print(f'this function is a coroutine: {func.__name__}')
            return await func(*args, **params)
        else:
            print('this is not a coroutine')
            return func(*args, **params)

    async def clocked(*args, **params):
        t0 = perf_counter()
        result = await process(func, *args, **params)
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        elapsed = perf_counter() - t0
        print(f'[{elapsed:0.8f}s] {name}({arg_str}) -> {result}')
        return result

    return clocked
