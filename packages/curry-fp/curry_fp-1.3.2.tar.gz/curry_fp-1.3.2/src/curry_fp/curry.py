from collections.abc import Callable
from functools import partial
from inspect import BoundArguments, signature
from types import CodeType
from typing import Any, Union

from pipe_fp import pipe


def curry(f: Union[Callable, partial]):
    """
    ## Description
    Creates a new and curryable function from a Callable.

    ## Example
    .. code-block:: python
        @curry
        def sum_all(a: int, b: int=2, c: int=3) -> int:
            return a + b + c

    **Without using default values**
    >>> sum_all(1)(2)(3)
    6

    **Using default values**
    >>> sum_all(1)(...)
    6
    """

    def count_partial_args(f: partial):
        return len(f.args) + len(f.keywords)

    def count_co_args_kwargs(co: CodeType):
        return co.co_argcount + co.co_kwonlyargcount

    def apply_defaults(f: partial):
        def filter_args(f: partial):
            return filter(lambda x: x != ..., f.args)

        def bind_args(f: partial):
            return signature(f.func).bind_partial(*filter_args(f), **f.keywords)

        def partial_with_defaults(f: partial, ba: BoundArguments):
            return ba.apply_defaults() or partial(f.func, *ba.args, **ba.kwargs)

        return partial_with_defaults(f, bind_args(f))

    def wrapper(*args, **kwargs) -> Union[Any, Callable]:
        def is_base_case(f: partial):
            return count_co_args_kwargs(f.func.__code__) == count_partial_args(f)

        return pipe[Callable](
            lambda f: partial(f, *args, **kwargs),
            lambda f: apply_defaults(f) if ... in args else f,
            lambda f: f() if is_base_case(f) else curry(f),
        )(f)

    return wrapper
