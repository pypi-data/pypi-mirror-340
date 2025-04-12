# 🥘 Curry fp

### Functional currying for Python.
Simple ⬦ Clear ⬦ Concise

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/A-4S/curry-fp/python-app.yml?logo=github&label=unit%20test&style=for-the-badge)](https://github.com/A-4S/curry-fp/actions/workflows/python-app.yml) [![PyPI - Version](https://img.shields.io/pypi/v/curry-fp?style=for-the-badge)](https://pypi.org/project/curry-fp/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/curry-fp?style=for-the-badge)](https://pypi.org/project/curry-fp/)

---
## Background
Currying is a technique targeting strategic code composition, breaking apart a function into a series of functions, allowing arguments to be applied piece-by-piece until all parameters are fulfilled.

## Usage
Curry fp is a powerful tool that can be used as a decorator on Callable objects for the purpose of currying.

## Features
- Allows for 1 or more arguments to be passed to the curried function at a time, including all at once.
- Default values can be specified using ```... (Ellipsis)``` as an argument, at any point.
- Keyword arguments can be used, allowing for arguments to be passed in whenever available.

### Example
```python
from curry_fp import curry

@curry
def sum_all(a: int, b: int=2, c: int=3) -> int:
    return a + b + c
```
**Without using default values**
```python
sum_all(1)(2)(3)
>>> 6
```

**Using default values**
```python
sum_all(1)(...)
>>> 6
```

**All arguments at once**
```python
sum_all(1, 2, 3)
>>> 6
```

**All arguments at once (with defaults)**
```python
sum_all(1, 2, ...)
>>> 6
```

**Using keyword arguments in any order**
```python
sum_all(b=2)(c=3)(a=1)
>>> 6
```

See ```test/test_curry.py``` for more examples. ✨
