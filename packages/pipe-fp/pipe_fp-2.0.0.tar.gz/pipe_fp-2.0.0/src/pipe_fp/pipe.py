from collections.abc import Callable
from functools import reduce
from typing import Any, Generic, overload

from .type import T0, T1, T2, T3, T4, T5, T6, T7, T8, T9


class pipe(Generic[T0]):
    """
    ## Description
    Functionally streamlines a series of function calls.

    ## Example
    .. code-block:: python
        def title_case(msg: str) -> list[str]:
            return pipe[str](
                lambda msg: msg.lower(),
                lambda msg: msg.title(),
                lambda msg: msg.split()
            )(msg)

    **Returns**
    >>> title_case('WHY, HELLO THERE! 😊')
    ['Why,', 'Hello', 'There!', '😊']
    """

    @overload
    def __new__(
        cls,
        f1: Callable[[T0], T1],
    ) -> Callable[[T0], T0]: ...

    @overload
    def __new__(
        cls,
        f1: Callable[[T0], T1],
        f2: Callable[[T1], T2],
    ) -> Callable[[T0], T2]: ...

    @overload
    def __new__(
        cls,
        f1: Callable[[T0], T1],
        f2: Callable[[T1], T2],
        f3: Callable[[T2], T3],
    ) -> Callable[[T0], T3]: ...

    @overload
    def __new__(
        cls,
        f1: Callable[[T0], T1],
        f2: Callable[[T1], T2],
        f3: Callable[[T2], T3],
        f4: Callable[[T3], T4],
    ) -> Callable[[T0], T9]: ...

    @overload
    def __new__(
        cls,
        f1: Callable[[T0], T1],
        f2: Callable[[T1], T2],
        f3: Callable[[T2], T3],
        f4: Callable[[T3], T4],
        f5: Callable[[T4], T5],
    ) -> Callable[[T0], T9]: ...

    @overload
    def __new__(
        cls,
        f1: Callable[[T0], T1],
        f2: Callable[[T1], T2],
        f3: Callable[[T2], T3],
        f4: Callable[[T3], T4],
        f5: Callable[[T4], T5],
        f6: Callable[[T5], T6],
    ) -> Callable[[T0], T9]: ...

    @overload
    def __new__(
        cls,
        f1: Callable[[T0], T1],
        f2: Callable[[T1], T2],
        f3: Callable[[T2], T3],
        f4: Callable[[T3], T4],
        f5: Callable[[T4], T5],
        f6: Callable[[T5], T6],
        f7: Callable[[T6], T7],
    ) -> Callable[[T0], T9]: ...

    @overload
    def __new__(
        cls,
        f1: Callable[[T0], T1],
        f2: Callable[[T1], T2],
        f3: Callable[[T2], T3],
        f4: Callable[[T3], T4],
        f5: Callable[[T4], T5],
        f6: Callable[[T5], T6],
        f7: Callable[[T6], T7],
        f8: Callable[[T7], T8],
    ) -> Callable[[T0], T9]: ...

    @overload
    def __new__(
        cls,
        f1: Callable[[T0], T1],
        f2: Callable[[T1], T2],
        f3: Callable[[T2], T3],
        f4: Callable[[T3], T4],
        f5: Callable[[T4], T5],
        f6: Callable[[T5], T6],
        f7: Callable[[T6], T7],
        f8: Callable[[T7], T8],
        f9: Callable[[T8], T9],
    ) -> Callable[[T0], T9]: ...

    def __new__(cls, *f: Callable[..., Any]) -> Callable[..., Any]:
        return lambda x: reduce(lambda a, c: c(a), f, x)
