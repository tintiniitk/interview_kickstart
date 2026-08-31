from ast import List

from utils.collections.LinkedList import ListNode


def node2str(n: ListNode | None) -> str:
    return n.__str__() if n else "None"


class Solution:
    def reverseKGroup(self, head: ListNode | None, k: int) -> ListNode | None:
        if not head or not head.next or k == 1:
            return head

        # print(f"head={node2str(head)}, k={k}")

        # guaranteed: k > 1, n > 1
        def reverseGroup(
            pre_head: ListNode | None,
            head: ListNode | None,
            tail: ListNode | None,
            post_tail: ListNode | None,
        ) -> tuple[ListNode, ListNode]:
            # it's assumed that prev->head->.next.(total k-1 times)->tail->next. prev.next = head. tail.next = next .
            # prev can be None
            # next can be None
            assert head and (not pre_head or pre_head.next == head)
            assert tail and tail.next == post_tail
            cur_head = head
            assert cur_head is not None
            cur_tail = post_tail
            while cur_head != tail:
                old_cur_head_next = cur_head.next
                cur_head.next = cur_tail
                cur_tail = cur_head
                cur_head = old_cur_head_next
                assert cur_head is not None
            assert cur_head == tail
            if pre_head:
                pre_head.next = cur_head
            assert cur_head is not None
            cur_head.next = cur_tail
            return (tail, head)

        pre_head = None
        cur_head = head
        cur_tail, post_tail = head, head.next

        def advance_to_first_group() -> int:
            nonlocal cur_tail
            nonlocal post_tail
            i = 0
            while i < k - 1 and post_tail is not None:
                assert cur_tail is not None
                cur_tail, post_tail = cur_tail.next, post_tail.next
                i += 1
            return i

        # get cur_tail, cur_post_tail by moving k-1 times from
        i = advance_to_first_group()
        # print(
        #     f"After advancing to first group, pre_head={node2str(pre_head)}, cur_head={node2str(cur_head)}, cur_tail={node2str(cur_tail)}, post_tail={node2str(post_tail)}"
        # )
        # reverse first group:
        if i == k - 1:
            cur_head, cur_tail = reverseGroup(None, cur_head, cur_tail, post_tail)
            # print(
            #     f"After reversing first group, pre_head={node2str(pre_head)}, cur_head={node2str(cur_head)}, cur_tail={node2str(cur_tail)}, post_tail={node2str(post_tail)}"
            # )
            head = cur_head  # return the eventual list head.
        else:
            return head  # not even k members.

        # now move everything forward by k repeatedly:
        def advance_to_next_group(num_steps: int) -> int:
            nonlocal pre_head
            nonlocal cur_head
            nonlocal cur_tail
            nonlocal post_tail
            i = 0
            assert pre_head is not None
            assert cur_head is not None
            assert cur_tail is not None
            while i < num_steps and post_tail is not None:
                pre_head, cur_head, cur_tail, post_tail = (
                    pre_head.next,
                    cur_head.next,
                    cur_tail.next,
                    post_tail.next,
                )
                assert pre_head is not None
                assert cur_head is not None
                assert cur_tail is not None
                i += 1
            return i

        pre_head, cur_head, cur_tail, post_tail = (
            cur_head,
            cur_head.next,
            cur_tail.next,
            post_tail.next if post_tail else None,
        )
        # print(
        #     f"After moving 1 step for 2nd group, pre_head={node2str(pre_head)}, cur_head={node2str(cur_head)}, cur_tail={node2str(cur_tail)}, post_tail={node2str(post_tail)}"
        # )
        if not cur_tail:
            return head
        i = advance_to_next_group(k - 1)
        if i == k - 1:
            # print(f"After advancing to 2nd group, pre_head={node2str(pre_head)}, cur_head={node2str(cur_head)}, cur_tail={node2str(cur_tail)}, post_tail={node2str(post_tail)}")
            cur_head, cur_tail = reverseGroup(pre_head, cur_head, cur_tail, post_tail)
            # print(f"After reversing second group, pre_head={node2str(pre_head)}, cur_head={node2str(cur_head)}, cur_tail={node2str(cur_tail)}, post_tail={node2str(post_tail)}")
        else:
            # print(f"failed to advance to 2nd group")
            pass
        g = 3
        while True:
            i = advance_to_next_group(k)
            if i == k:
                # print(f"After advancing to group#{g}, pre_head={node2str(pre_head)}, cur_head={node2str(cur_head)}, cur_tail={node2str(cur_tail)}, post_tail={node2str(post_tail)}")
                cur_head, cur_tail = reverseGroup(
                    pre_head, cur_head, cur_tail, post_tail
                )
                # print(f"After reversing group#{g}, pre_head={node2str(pre_head)}, cur_head={node2str(cur_head)}, cur_tail={node2str(cur_tail)}, post_tail={node2str(post_tail)}")
                g += 1
            else:
                # print(f"failed to advance to group#{g}")
                break
        return head


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(head: ListNode | None, k: int, expected: ListNode | None) -> tuple[bool, str]:
    actual = Solution().reverseKGroup(head, k)
    if not actual:
        return False, f"got=None, wanted={expected}"
    if not actual.eq(expected):
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5))))),
                k=2,
                expected=ListNode(
                    2, ListNode(1, ListNode(4, ListNode(3, ListNode(5))))
                ),
            )
            Test(
                ListNode(
                    1,
                    ListNode(
                        2,
                        ListNode(
                            3,
                            ListNode(
                                4,
                                ListNode(
                                    5,
                                    ListNode(
                                        6,
                                        ListNode(
                                            7,
                                            ListNode(
                                                8,
                                                ListNode(
                                                    9,
                                                    ListNode(10, ListNode(11)),
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
                k=3,
                expected=ListNode(
                    3,
                    ListNode(
                        2,
                        ListNode(
                            1,
                            ListNode(
                                6,
                                ListNode(
                                    5,
                                    ListNode(
                                        4,
                                        ListNode(
                                            9,
                                            ListNode(
                                                8,
                                                ListNode(
                                                    7,
                                                    ListNode(
                                                        10,
                                                        ListNode(11),
                                                    ),
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            )
            Test(
                ListNode(
                    1,
                    ListNode(2),
                ),
                k=2,
                expected=ListNode(2, ListNode(1)),
            )
            Test(
                ListNode(
                    1,
                    ListNode(2, ListNode(3)),
                ),
                k=2,
                expected=ListNode(2, ListNode(1, ListNode(3))),
            )
            Test(
                ListNode(
                    1,
                    ListNode(
                        2,
                        ListNode(
                            3,
                            ListNode(
                                4,
                                ListNode(
                                    5,
                                    ListNode(6),
                                ),
                            ),
                        ),
                    ),
                ),
                k=4,
                expected=ListNode(
                    4,
                    ListNode(
                        3,
                        ListNode(
                            2,
                            ListNode(
                                1,
                                ListNode(
                                    5,
                                    ListNode(6),
                                ),
                            ),
                        ),
                    ),
                ),
            )
            Test(
                ListNode(
                    1,
                    ListNode(
                        2,
                        ListNode(
                            3,
                            ListNode(
                                4,
                                ListNode(
                                    5,
                                    ListNode(6, ListNode(7)),
                                ),
                            ),
                        ),
                    ),
                ),
                k=7,
                expected=ListNode(
                    7,
                    ListNode(
                        6,
                        ListNode(
                            5,
                            ListNode(
                                4,
                                ListNode(
                                    3,
                                    ListNode(2, ListNode(1)),
                                ),
                            ),
                        ),
                    ),
                ),
            )
            Test(
                ListNode(
                    1,
                    ListNode(
                        2,
                        ListNode(
                            3,
                            ListNode(
                                4,
                                ListNode(
                                    5,
                                    ListNode(6),
                                ),
                            ),
                        ),
                    ),
                ),
                k=5,
                expected=ListNode(
                    5,
                    ListNode(
                        4,
                        ListNode(
                            3,
                            ListNode(
                                2,
                                ListNode(
                                    1,
                                    ListNode(6),
                                ),
                            ),
                        ),
                    ),
                ),
            )
            Test(
                ListNode(
                    1,
                    ListNode(
                        2,
                        ListNode(
                            3,
                            ListNode(
                                4,
                                ListNode(
                                    5,
                                    ListNode(
                                        6,
                                        ListNode(
                                            7,
                                            ListNode(
                                                8,
                                                ListNode(
                                                    9,
                                                    ListNode(
                                                        10, ListNode(11, ListNode(12))
                                                    ),
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
                k=6,
                expected=ListNode(
                    6,
                    ListNode(
                        5,
                        ListNode(
                            4,
                            ListNode(
                                3,
                                ListNode(
                                    2,
                                    ListNode(
                                        1,
                                        ListNode(
                                            12,
                                            ListNode(
                                                11,
                                                ListNode(
                                                    10,
                                                    ListNode(
                                                        9,
                                                        ListNode(8, ListNode(7)),
                                                    ),
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
