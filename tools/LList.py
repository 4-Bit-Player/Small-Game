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


    def __next__(self) -> _T:
        if self._current_node is None:
            raise StopIteration
        val = self._current_node.val
        self._current_node = self._current_node.right_node
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
    def size(self):
        return self._size

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        new_ll:LinkedList[_T] = LinkedList()
        new_ll._init_via_llist(self)
        return new_ll

    def __str__(self):
        out = ""
        node = self._head
        for i in range(self._size):
            out +=str(node.val) + ", "
            node = node.right_node
        return out

    def _init_via_llist(self, llist):
        if llist._size == 0:
            return
        self._size = llist._size

        previous_node = self._head = self._end = _Node(llist._head.val)

        for other_node in llist:
            next_node = _Node(other_node, left_node=previous_node)
            previous_node.right_node = next_node
            previous_node = next_node
        self._end = previous_node






