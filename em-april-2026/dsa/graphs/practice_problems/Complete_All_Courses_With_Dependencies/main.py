import sys


def can_be_completed(n, a, b):
    """
    Args:
     n(int32)
     a(list_int32)
     b(list_int32)
    Returns:
     bool
    """
    # Write your code here.
    # assuming n > 1
    k = len(a)
    if k == 0:
        return True
    if k != len(b):
        return ValueError(f"len(a)={k} != len(b)={len(b)}")
    dependency_lists = [
        set() for _ in range(n)
    ]  # dependency_lists[i] is the list of all the courses {j} which are prerequisites for {i}.
    for i in range(k):
        dependency_lists[b[i]].add(a[i])

    courses_done = [False for _ in range(n)]

    # iterative DFS
    def trace_dependencies(start: int) -> bool:
        visiting = []
        stack = [(start, False)]
        print(f"Added starting course {start} to stack => stack={stack}")
        while stack:
            course, backtracking = stack.pop()
            print(
                f"Popped course={course},backtracking={backtracking} from stack, with visiting={visiting}"
            )
            if backtracking:
                visiting.remove(course)
                print(
                    f"Removed backtracked course={course} from stack => visiting={visiting}"
                )
                continue
            if course in visiting:
                print(
                    f"found cycle at {course} which is dependent on itself through path {visiting}"
                )
                return False
            if courses_done[course]:
                print(f"found {course} has already been visited")
                continue
            visiting.append(course)
            print(f"Added course={course} to visiting => visiting={visiting}")
            stack.append((course, True))
            print(f"Added course={course} to stack for backtracking => stack={stack}")
            courses_done[course] = True
            print(f"Marked course={course} as visited => visited={courses_done}")
            for depencency_course in dependency_lists[course]:
                if depencency_course not in visiting:
                    stack.append((depencency_course, False))
                    print(
                        f"Added dependency course={depencency_course} to stack for checking => stack={stack}"
                    )
                else:
                    return False
        return True

    for course in range(n):
        if not courses_done[course]:
            print(f"Started new DFS with {course}")
            if not trace_dependencies(course):
                print(f"DFS with {course} failed => return False")
                return False
    return True


def main():
    n = 4
    a = [1, 1, 3, 0]
    b = [0, 2, 1, 3]
    expected_output = False
    output = can_be_completed(n, a, b)
    print(f"n={n}")
    if n < 100:
        print(f"a={a}")
        print(f"b={b}")
    print(f"expected_output={expected_output},output={output}")
    pass


if __name__ == "__main__":
    main()
