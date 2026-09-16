"""
implement a stack using an array. Implement, push, pop, and peek.
"""


class myStack:
    arr: list[int]
    n: int
    end: int = 0

    def __init__(self, capacity: int = 10):
        print(f"init({capacity})")
        self.n = capacity
        self.arr = [-1] * self.n
        self.end = 0

    def isEmpty(self):
        return self.end == 0

    def isFull(self):
        return self.end == self.n

    def peek(self) -> int:
        print("peek()")
        if self.end == 0:
            raise ValueError("No entry in the stack")
            # return -1
        else:
            return self.arr[self.end - 1]

    def pop(self):
        print("pop()")
        if self.end == 0:
            raise ValueError("No entry in the stack to pop")
        else:
            self.end -= 1

    def push(self, value: int):
        print(f"push({value})")
        if self.end == self.n:
            print("  resizing underlying array ...")
            # need to resize, double in size.
            new_arr = self.arr + [-1] * self.n
            self.arr = new_arr
            self.end = self.n
            self.n *= 2
        self.arr[self.end] = value
        self.end += 1

    def __str__(self) -> str:
        return f"MyStack : {{ {' -> '.join(map(str, self.arr[: self.end]))} }}"

    def __repr__(self) -> str:
        return self.__str__()


# def Test(i: int):
#     print(f"[RUN]")
#     assert i % 2, f"i = {i}\n[FAILED]"
#     print(f"[PASSED]")
# Test(1)
# Test(2)


def Test():
    s = myStack(1)
    print(s)
    s.push(10)
    print(s)
    s.push(8)
    print(s)
    print(s.peek())
    s.pop()
    print(s)
    print(s.peek())
    s.pop()
    print(s)
    s.pop()
    print(s)


Test()
