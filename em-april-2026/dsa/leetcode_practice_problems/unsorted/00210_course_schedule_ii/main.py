from collections import deque


class Solution:
    def findOrder(self, numCourses: int, prerequisites: list[list[int]]) -> list[int]:
        n = numCourses
        if n < 2:
            return [0]
        if not prerequisites:
            return [i for i in range(n)]
        # e = len(prerequisites)
        dependencies = [set() for _ in range(n)]
        dependents = [set() for _ in range(n)]
        for prerequisite in prerequisites:
            dependent, dependency = prerequisite[0], prerequisite[1]
            if dependent == dependency:
                print(f"Found self-dependency for course {dependent}")
                return []
            dependencies[dependent].add(dependency)
            dependents[dependency].add(dependent)
        # print(f"dependents={ ({i: dependent for i, dependent in enumerate(dependents)}) }")
        # print(f"dependencies={ ({i: dependency for i, dependency in enumerate(dependencies)}) }")
        independent_courses = [
            course for course in range(n) if not dependencies[course]
        ]
        if not independent_courses:
            print("Found no independent courses")
            return []

        # print(f"independent_courses={independent_courses}")
        # assign ranks i.e. topological sorting
        def assign_ranks() -> tuple[bool, list[int]]:
            ranks = [0] * n
            for independent_course in independent_courses:
                ranks[independent_course] = 1
            q = deque(independent_courses)
            # print(f"Pushed {independent_courses} to q")
            while q:
                course = q.popleft()
                # print(f"While processing {course:<3}, Popped {course:>3} from q; at this point with rank={ranks[course]} => q={q}")
                if ranks[course] > n:
                    print(
                        f"There is a cycle in courses, q={q}, ranks={ranks}, independent_courses={independent_courses}, dependents={dependents}"
                    )
                    return False, ranks
                dependent_course_rank = ranks[course] + 1
                for dependent_course in dependents[course]:
                    # graph is known to have no cycles:
                    old_rank = ranks[dependent_course]
                    if dependent_course_rank > old_rank:
                        ranks[dependent_course] = dependent_course_rank
                        q.append(dependent_course)
                    # print(f"While processing {course:<3}, Pushed {dependent_course:>3} to q with rank={ranks[dependent_course]} => q={q}")
            return True, ranks

        def populate_courses_to_take_in_order(ranks):
            # it's assumed that by now every course has a rank in [1, n] range.
            courses_to_take_in_order = []
            for rank in range(1, n + 1):
                courses_to_take_in_order += list(
                    filter(lambda i: ranks[i] == rank, range(n))
                )
            return courses_to_take_in_order

        success, ranks = assign_ranks()
        if not success:
            return []
        # print(f"Assigned ranks in the graph: {ranks}")
        if any(rank < 1 or rank > n for rank in ranks):
            print(
                f"Something went wrong while assigning ranks ({ranks}): some course has a rank <0 or >n"
            )
            return []
        return populate_courses_to_take_in_order(ranks)


import sys

from tc_x import tc as tc_x_tc
from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(
    numCourses: int, prerequisites: list[list[int]], expected: list[int]
) -> tuple[bool, str]:
    actual = Solution().findOrder(numCourses, prerequisites)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(numCourses=3, prerequisites=[[1, 0], [1, 2], [0, 1]], expected=[])
            Test(**tc_x_tc)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
