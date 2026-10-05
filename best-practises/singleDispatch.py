# Problem
# In the first approach, the describe() function handles every data type using
# if/elif conditions. Whenever we need to support a new data type, we have to
# modify the existing describe() function, which can make it larger and harder
# to maintain. In the second approach, singledispatch allows us to define a
# separate implementation for each data type. This means we can add support
# for a new type without modifying the main describe() function. It keeps
# type-specific logic separated and makes the code easier to extend and maintain.

# Instead of below code:
'''
def describe(value):
    if isinstance(value, int):
        parity = "even" if value % 2 == 0 else "odd"
        return f"int: {value} ({parity})"
    elif isinstance(value, str):
        return f"str: '{value}' ({len(value)} chars)"
    elif isinstance(value, list):
        return f"list: {len(value)} items, sum={sum(value)}"
    else:
        return f"{type(value).__name__}: {value!r}"

print(describe(5))
print(describe("hello"))
print(describe([1, 3, 5]))
'''

# Use this code.
from functools import singledispatch

@singledispatch
def describe(value) -> str:
    return f"{type(value).__name__}: {value!r}"

@describe.register
def _(value: int) -> str:
    parity = "even" if value % 2 == 0 else "odd"
    return f"int: {value} ({parity})"

@describe.register
def _(value: str) -> str:
    return f"str: '{value}' ({len(value)} chars)"

@describe.register
def _(value: list) -> str:
    return f"list: {len(value)} items, sum={sum(value)}"

@describe.register
def _(value: dict) -> str:
    return f"dict: {len(value)} keys -> {list(value.keys())}"

print(describe(5))
print(describe("hello"))
print(describe([1, 3, 5]))
print(describe({"name": "rahi", "age": "infinity"}))