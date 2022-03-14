from typing import Callable, Set, Generic, TypeVar


T = TypeVar("T")
noop = lambda _: _


class Writable(Generic[T]):
    __slots__ = "__value__", "__subscribers__", "__start__", "__ready__"

    def __init__(self, value: T = None, start: Callable = noop) -> None:
        self.__value__: T = value
        self.__subscribers__: Set[Callable] = set()
        self.__start__: Callable = start
        self.__ready__: Callable = False

    def __call__(self) -> T:
        return self.__value__

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} value={self.__value__} subscribers={len(self.__subscribers__)}>"

    def __set__(self, value: T) -> None:
        if self.__value__ == value:
            return

        self.__value__ = value
        if self.__ready__:
            self.notify()

    def notify(self) -> None:
        for subscriber in self.__subscribers__:
            subscriber(self.__value__)

    def set(self, value: T) -> None:
        self.__set__(value)

    def update(self, func: Callable) -> None:
        self.set(func(self.__value__))

    def subscribe(self, func: Callable) -> Callable:
        self.__subscribers__.add(func)

        if len(self.__subscribers__) == 1:
            self.__start__(self.__set__)
            self.__ready__ = True

        func(self.__value__)


class Readable(Writable):
    def set(self, value: T = None):
        raise Exception("Attempted to set value on Readable Store")

    def update(self, func: Callable = noop):
        raise Exception("Attempted to update value on Readable Store")
