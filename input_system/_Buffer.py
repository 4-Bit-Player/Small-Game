from typing import TypeVar, Generic
T = TypeVar("T")

class Buffer(Generic[T]):
    def __init__(self, size:int=10):
        self.__buffer = ["" for _ in range(size)]
        self.__actual_size = size
        self.__offset:int = 0
        self.__size:int = 0

    def clear(self):
        self.__size = 0
        self.__offset = 0

    def pop_left(self) -> T:
        if self.__size <= 0:
            raise IndexError("Trying to pop from empty list.")
        self.__size -= 1
        val = self.__buffer[self.__offset]
        self.__offset = (self.__offset + 1) % self.__actual_size
        return val

    def pop_right(self) -> T:
        if self.__size <= 0:
            raise IndexError("Trying to pop from empty list.")
        self.__size -= 1
        return self.__buffer[(self.__offset + self.__size) % self.__actual_size]

    def append(self, val:T) -> None:
        self.__buffer[(self.__offset + self.__size) % self.__actual_size] = val
        if self.__size < self.__actual_size:
            self.__size += 1
            return
        self.__offset = (self.__offset + 1) % self.__actual_size

    def size(self) -> int:
        return self.__size

    def __len__(self) -> int:
        return self.__size

    def __getitem__(self, item:int) -> T:
        if not isinstance(item, int):
            raise ValueError(f"Indices must be integers, not {type(item)}")
        if item >= self.__size:
            raise IndexError(f"Index out of range")
        return self.__buffer[(self.__offset + item) % self.__actual_size]