"""Closures

Abstractions for callback-heavy control flows.
"""
from collections.abc import Callable
from functools import wraps


class _Closure:
    """A callable decorator factory that supports chaining callbacks.

    Usage:
        ```
        @closure(
            lambda result, *_: do_something_else_with(result)
        )
        def foo(bar):
            result = do_something_with(bar)
            return result
        ```

    Chaining:
        ```
        def cb1(result, *_):
            return some_transforming_callable(result)

        def cb2(result, *_):
            return another_transforming_callable(result)

        def cb3(result *_):
            return yet_another_transforming_callable(result)

        @closure(
            cb1
            ).cc(cb2
            ).cc(cb3
        )
        def foo(bar):
            result = do_something_with(bar)
            return result
        ```
    """
    def __init__(self, fn: Callable):
        """Instantiates a new closure.

        Args:
          fn:
            The function whose return value will be passed as the first
            argument to any callbacks included in the closure.
        """
        self._callbacks = [fn]

    def __call__(self, target):
        """Makes the `_Closure` class callable.

        Instantiate the `_Closure` class by calling `closure`, which is
        the class's preferred alias and comprises the only publicly
        exposed object in Pristine's closure API. See class
        documentation for detailed discussion regarding usage.
        """
        @wraps(target)
        def wrapped(*args, **kwargs):
            result = target(*args, **kwargs)
            for fn in self._callbacks:
                result = fn(result, *args, **kwargs)
            return result
        return wrapped

    def cc(self, fn) -> "_Closure":
        """Add a callback function to the (c)losure (c)hain.

        Each callback receives (result, *args, **kwargs) and may return
        a transformed result. The final return value is passed to the
        caller.
        """
        self._callbacks.append(fn)
        return self


# Public API
closure = _Closure
