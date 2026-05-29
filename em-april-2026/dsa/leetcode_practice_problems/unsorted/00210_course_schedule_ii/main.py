from typing import List
from collections import deque


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        n = numCourses
        if n < 2:
            return [0]
        if not prerequisites:
            return [i for i in range(n)]
        e = len(prerequisites)
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
            print(f"Found no independent courses")
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


def main():
    numCourses, prerequisites = 3, [[1, 0], [1, 2], [0, 1]]
    numCourses, prerequisites = 100, [
        [1, 0],
        [2, 0],
        [2, 1],
        [3, 1],
        [3, 2],
        [4, 2],
        [4, 3],
        [5, 3],
        [5, 4],
        [6, 4],
        [6, 5],
        [7, 5],
        [7, 6],
        [8, 6],
        [8, 7],
        [9, 7],
        [9, 8],
        [10, 8],
        [10, 9],
        [11, 9],
        [11, 10],
        [12, 10],
        [12, 11],
        [13, 11],
        [13, 12],
        [14, 12],
        [14, 13],
        [15, 13],
        [15, 14],
        [16, 14],
        [16, 15],
        [17, 15],
        [17, 16],
        [18, 16],
        [18, 17],
        [19, 17],
        [19, 18],
        [20, 18],
        [20, 19],
        [21, 19],
        [21, 20],
        [22, 20],
        [22, 21],
        [23, 21],
        [23, 22],
        [24, 22],
        [24, 23],
        [25, 23],
        [25, 24],
        [26, 24],
        [26, 25],
        [27, 25],
        [27, 26],
        [28, 26],
        [28, 27],
        [29, 27],
        [29, 28],
        [30, 28],
        [30, 29],
        [31, 29],
        [31, 30],
        [32, 30],
        [32, 31],
        [33, 31],
        [33, 32],
        [34, 32],
        [34, 33],
        [35, 33],
        [35, 34],
        [36, 34],
        [36, 35],
        [37, 35],
        [37, 36],
        [38, 36],
        [38, 37],
        [39, 37],
        [39, 38],
        [40, 38],
        [40, 39],
        [41, 39],
        [41, 40],
        [42, 40],
        [42, 41],
        [43, 41],
        [43, 42],
        [44, 42],
        [44, 43],
        [45, 43],
        [45, 44],
        [46, 44],
        [46, 45],
        [47, 45],
        [47, 46],
        [48, 46],
        [48, 47],
        [49, 47],
        [49, 48],
        [50, 48],
        [50, 49],
        [51, 49],
        [51, 50],
        [52, 50],
        [52, 51],
        [53, 51],
        [53, 52],
        [54, 52],
        [54, 53],
        [55, 53],
        [55, 54],
        [56, 54],
        [56, 55],
        [57, 55],
        [57, 56],
        [58, 56],
        [58, 57],
        [59, 57],
        [59, 58],
        [60, 58],
        [60, 59],
        [61, 59],
        [61, 60],
        [62, 60],
        [62, 61],
        [63, 61],
        [63, 62],
        [64, 62],
        [64, 63],
        [65, 63],
        [65, 64],
        [66, 64],
        [66, 65],
        [67, 65],
        [67, 66],
        [68, 66],
        [68, 67],
        [69, 67],
        [69, 68],
        [70, 68],
        [70, 69],
        [71, 69],
        [71, 70],
        [72, 70],
        [72, 71],
        [73, 71],
        [73, 72],
        [74, 72],
        [74, 73],
        [75, 73],
        [75, 74],
        [76, 74],
        [76, 75],
        [77, 75],
        [77, 76],
        [78, 76],
        [78, 77],
        [79, 77],
        [79, 78],
        [80, 78],
        [80, 79],
        [81, 79],
        [81, 80],
        [82, 80],
        [82, 81],
        [83, 81],
        [83, 82],
        [84, 82],
        [84, 83],
        [85, 83],
        [85, 84],
        [86, 84],
        [86, 85],
        [87, 85],
        [87, 86],
        [88, 86],
        [88, 87],
        [89, 87],
        [89, 88],
        [90, 88],
        [90, 89],
        [91, 89],
        [91, 90],
        [92, 90],
        [92, 91],
        [93, 91],
        [93, 92],
        [94, 92],
        [94, 93],
        [95, 93],
        [95, 94],
        [96, 94],
        [96, 95],
        [97, 95],
        [97, 96],
        [98, 96],
        [98, 97],
        [99, 97],
    ]
    schedule = Solution().findOrder(numCourses, prerequisites)
    print(
        f"numCourses={numCourses}, "
        # f"prerequisites={prerequisites}, "
        f"schedule={schedule}"
    )


if __name__ == "__main__":
    main()
