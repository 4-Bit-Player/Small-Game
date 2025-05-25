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
    """
    The reversed iterator for the Linked List class.
    """
    def __next__(self) -> _T:
        if self._current_node is None:
            raise StopIteration
        val = self._current_node.val
        self._current_node = self._current_node.left_node
        return val


class LinkedList(Iterable[_T]):
    def __init__(self, iterable_sequence:Iterable[_T]=None):
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


    def appendleft(self, val:_T) -> None:
        """
        Adds the value to its beginning.
        """
        node = _Node(val, right_node=self._head)
        self._size += 1
        if self._head is not None:
            self._head.left_node = node
            self._head = node
            return
        self._end = node
        self._head = node

    def append(self, val:_T) -> None:
        """
        Adds the value to its end.
        """
        node = _Node(val, left_node=self._end)
        self._size += 1
        if self._end is not None:
            self._end.right_node = node
            self._end = node
            return
        self._end = node
        self._head = node

    def pop(self) -> _T:
        """
        Removes and returns the rightmost value.
        """
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
        """
        Removes and returns the leftmost value.
        """
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
            index = - index - 1
            if index < 0:
                index -= 1

        if index < 0:
            index = self._size + index + 1
            if index < 0:
                raise IndexError("Index out of range!")

        if index > self._size:
            raise IndexError("list index out of range")

        if index * 2 > self._size:
            return self._search_from_right(self._size - 1 - index).val
        return self._search_from_left(index).val

    def __iter__(self):
        if self._reversed:
            return _ReversedLLiterator(self._end)
        return _LLiterator(self._head)


    def __contains__(self, item:_T) -> bool:
        if self._head is None:
            return False
        current_node = self._head
        while current_node is not None:
            if current_node.val == item:
                return True
            current_node = current_node.right_node
        return False


    def _search_from_left(self, index) -> _Node:
        node:_Node = self._head
        for _ in range(index):
            node = node.right_node
        return node

    def _search_from_right(self, index) -> _Node:
        node: _Node = self._end
        for _ in range(index):
            node = node.left_node
        return node

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

    def __bool__(self) -> bool:
        return self._size != 0

    def __iadd__(self, other:Iterable[_T]):
        if type(other) in [list, tuple, LinkedList]:
            raise NotImplementedError(f"Can't add {type(other)} to a linked list")
        for val in other:
            self.append(val)
        return self

    def __add__(self, other:Iterable[_T]):
        if type(other) not in [list, tuple, LinkedList]:
            raise NotImplementedError(f"Can't add {type(other)} to a linked list")
        new_llist = LinkedList(self)
        new_llist += other
        return new_llist


    def clear(self) -> None:
        """
        Clears itself and sets its size to 0.
        """
        self._head = self._end = None
        self._size = 0


    def insert(self, index:int, val:_T) -> None:
        """
        Insert a value at the given index.
        """

        if index < 0:
            index = self._size + index + 1
            if index < 0:
                raise IndexError("Index out of range!")

        if index > self._size:
            raise IndexError("Index out of range!")

        if self._reversed:
            index = self._size-index

        if index == self._size:
            self.append(val) if not self._reversed else self.appendleft(val)
            return

        if index == 0:
            self.appendleft(val) if not self._reversed else self.append(val)
            return

        self._size += 1
        if self._size == 1:
            self._head = self._end = _Node(val)
            return

        if index*2 > self._size:
            right_node:_Node = self._search_from_right(self._size - 2 - index)
        else:
            right_node:_Node = self._search_from_left(index)

        new_node = _Node(val,left_node=right_node.left_node, right_node=right_node)
        left_node = right_node.left_node
        right_node.left_node = new_node
        left_node.right_node = new_node
        return


    def index(self, val:_T, start:int=0, stop:int=-1) -> int:
        """
        Returns the index of the first occurrence of the value.
        Returns -1 if it doesn't exist.

        :param val: The value to search
        :param start:(optional) where it should start searching
        :param stop: (optional) where it should stop searching
        :return: The index of the first occurrence, if it contains it, else -1
        """
        if start >= self._size:
            return -1
        if start < 0:
            start = 0

        end = min(self._size, stop) if stop != -1 else self._size

        if self._reversed:
            current_node = self._search_from_right(start)
            for i in range(start, end, 1):
                if current_node is None:
                    return -1
                if current_node.val == val:
                    return i
                current_node = current_node.left_node
            return -1

        current_node = self._search_from_left(start)

        for i in range(start, end, 1):
            if current_node is None:
                return -1
            if current_node.val == val:
                return i
            current_node = current_node.right_node

        return -1

    def count(self, val:_T) -> int:
        """
        Returns the occurrences count of the given value.
        """
        current_node = self._head
        found = 0
        while current_node is not None:
            if current_node.val == val:
                found += 1
            current_node = current_node.right_node
        return found

    def rotate(self, n:int) -> None:
        """
        Rotate the list n steps in place to the right.
        Use negative numbers to rotate it to the left.
        """
        n = n % self._size
        if n == 0:
            return
        if n*2 < self._size:
            new_start_node = self._search_from_right(n-1)
        else:
            new_start_node = self._search_from_left(self._size - n)
        new_end = new_start_node.left_node

        self._head.left_node = self._end
        self._end.right_node = self._head

        new_start_node.left_node = None
        self._end = new_end
        self._head = new_start_node
        return


    def reverse(self) -> None:
        """
        Reverses the linked list in place.
        """
        self._reversed = not self._reversed
        self.pop, self.popleft = self.popleft, self.pop
        self.append, self.appendleft = self.appendleft, self.append