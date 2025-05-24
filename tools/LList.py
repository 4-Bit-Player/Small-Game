from typing import TypeVar, Iterable
_T = TypeVar("_T")


class _Node:
    def __init__(self, val, left_node = None, right_node = None):
        self.right_node:_Node|None = right_node
        self.left_node:_Node|None = left_node
        self.val = val

class _LLiterator:
    def __init__(self, node:_Node):
        """
        The iterator for the Linked List class.
        :param node: The starting Node
        """
        self._current_node:_Node = node

    def __iter__(self):
        return self

    def __next__(self) -> _T:
        if self._current_node is None:
            raise StopIteration
        val = self._current_node.val
        self._current_node = self._current_node.right_node
        return val


class _ReversedLLiterator(_LLiterator):
    def __iter__(self):
        return self
    def __next__(self):
        if self._current_node is None:
            raise StopIteration
        val = self._current_node.val
        self._current_node = self._current_node.left_node
        return val


class LinkedList(Iterable[_T]):
    def __init__(self, iterable_sequence:Iterable=None):
        """
        A linked list made in pure python. :>
        :param iterable_sequence: An optional iterable sequence. It will add the items of it to itself.
        """
        self._head:None|_Node = None
        self._end:None|_Node = None
        self._size = 0
        self._reversed = False
        if iterable_sequence is not None:
            last_node = None
            self._size = len(iterable_sequence)
            for item in iterable_sequence:
                node = _Node(item)
                if self._head is None:
                    self._head = node
                    last_node = node
                    continue
                last_node.right_node = node
                node.left_node = last_node
                last_node = node
            self._end = last_node


    def appendleft(self, val):
        node = _Node(val, right_node=self._head)
        self._size += 1
        if self._head is not None:
            self._head.left_node = node
            self._head = node
            return
        self._end = node
        self._head = node

    def append(self, val):
        node = _Node(val, left_node=self._end)
        self._size += 1
        if self._end is not None:
            self._end.right_node = node
            self._end = node
            return
        self._end = node
        self._head = node

    def pop(self) -> _T:
        if self._end is None:
            raise IndexError("pop from an empty linked list")
        if self._size == 1:
            val = self._head.val
            self._head = None
            self._end = None
            self._size = 0
            return val
        self._size -= 1
        val = self._end.val
        left_node:_Node = self._end.left_node
        left_node.right_node = None
        self._end = left_node
        return val

    def popleft(self) -> _T:
        if self._head is None:
            raise IndexError("pop from an empty linked list")
        if self._size == 1:
            val = self._head.val
            self._head = None
            self._end = None
            self._size = 0
            return val
        self._size -= 1
        val = self._head.val
        right_node:_Node = self._head.right_node
        right_node.left_node = None
        self._head = right_node
        return val

    def __len__(self) -> int:
        return self._size

    def __getitem__(self, index:int) -> _T:
        if self._reversed:
            index = -index-1
        if index > self._size:
            raise IndexError("list index out of range")
        if index < 0:
            index = -index
            if index > self._size:
                raise IndexError("list index out of range")
            if index + index > self._size:
                return self._search_left(self._size - index)
            return self._search_right(index-1)
        if index + index > self._size:
            return self._search_right(self._size -1 - index)
        return self._search_left(index)

    def __iter__(self):
        if self._reversed:
            return _ReversedLLiterator(self._end)
        return _LLiterator(self._head)


    def __contains__(self, item) -> bool:
        if self._head is None:
            return False
        current_node = self._head
        while current_node is not None:
            if current_node.val == item:
                return True
            current_node = current_node.right_node
        return False


    def _search_left(self, index):
        node:_Node = self._head
        for _ in range(index):
            node = node.right_node
        return node.val

    def _search_right(self, index):
        node: _Node = self._end
        for _ in range(index):
            node = node.left_node
        return node.val

    @property
    def size(self) -> int:
        return self._size

    def copy(self):
        """
        :return: Returns a new Linked List with the same values
        """
        return self.__copy__()

    def __copy__(self):
        revrsd = self._reversed
        if revrsd:
            self.reverse()
        new_list = LinkedList(self)
        if revrsd:
            new_list.reverse()
            self.reverse()
        return new_list

    def __str__(self):
        node = self._head
        val_strs = []
        for _ in range(self._size):
            val_strs.append(str(node.val))
            node = node.right_node
        if self._reversed:
            val_strs.reverse()
        out = "[" + ", ".join(val_strs) + "]"
        return out

    def __reversed__(self):
        if self._reversed:
            return _LLiterator(self._head)
        return _ReversedLLiterator(self._end)

    def __bool__(self):
        return self._size != 0

    def __iadd__(self, other:Iterable[_T]):
        if type(other) in [list, tuple, LinkedList]:
            for val in other:
                self.append(val)
            return self

        raise NotImplementedError(f"Can't add {type(other)} to a linked list")

    def index(self, val, start=0, stop=-1) -> int:
        """
        :param val: The value to search
        :param start:(optional) where it should start searching
        :param stop: (optional) where it should stop searching
        :return: The index of the first occurrence, if it contains it, else -1
        """
        current_node = self._head
        for _ in range(start):
            current_node = current_node.right_node

        end = min(self._size, stop) if stop != -1 else self._size

        for i in range(start, end, 1):
            if current_node is None:
                return -1
            if current_node.val == val:
                return i
            current_node = current_node.right_node

        return -1

    def reverse(self) -> None:
        """
        Reverses the linked list in place.
        """
        self._reversed = not self._reversed
        self.pop, self.popleft = self.popleft, self.pop
        self.append, self.appendleft = self.appendleft, self.append


