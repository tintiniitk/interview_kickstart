from collections.abc import Callable
from heapq import heappop, heappush

DEBUGGING = False


def log(log_factory: Callable[[], object]) -> None:
    if DEBUGGING:
        print(log_factory())


class Solution:
    def topStudents(
        self,
        positive_feedback: list[str],
        negative_feedback: list[str],
        report: list[str],
        student_id: list[int],
        k: int,
    ) -> list[int]:
        positive_words = set(positive_feedback)
        negative_words = set(negative_feedback)
        log(lambda: f"positive_words={positive_words}, negative_words={negative_words}")
        n = len(report)
        assert n == len(student_id)
        pq = []
        for id, report_words in zip(student_id, report):
            log(
                lambda id=id, report_words=report_words: (
                    f"evaluating id={id}, report_words={report_words}, score=0"
                )
            )
            score = 0
            for report_word in report_words.split(" "):
                # log(lambda: f"  evaluating report_word={report_word}")
                if report_word in positive_words:
                    score += 3
                    # log(lambda: f"  report_word={report_word}, score => {score}")
                elif report_word in negative_words:
                    score -= 1
                    # log(lambda: f"  report_word={report_word}, score => {score}")
            log(lambda score=score: f"  score => {score}")
            if not pq or len(pq) < k:
                heappush(pq, (score, -id))
                log(lambda: f"  Inserted into pq => {pq}")
            else:  # size = k, may be evict one if needed.
                cur_min_top_k_student_score, cur_min_top_k_student_id = pq[0]
                cur_min_top_k_student_id = -cur_min_top_k_student_id
                if cur_min_top_k_student_score < score or (
                    cur_min_top_k_student_score == score
                    and id < cur_min_top_k_student_id
                ):
                    heappop(pq)
                    heappush(pq, (score, -id))
                    log(lambda: f"  Inserted into pq => {pq}")
        log(lambda: f"pq after all iterations = {pq}")
        ret = []
        while pq:
            score, id = heappop(pq)
            ret.append(-id)
        return ret[::-1]


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(
    positive_feedback: list[str],
    negative_feedback: list[str],
    report: list[str],
    student_id: list[int],
    k: int,
    expected: list[int],
) -> tuple[bool, str]:
    actual = Solution().topStudents(
        positive_feedback, negative_feedback, report, student_id, k
    )
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                positive_feedback=["smart", "brilliant", "studious"],
                negative_feedback=["not"],
                report=["this student is studious", "the student is smart"],
                student_id=[1, 2],
                k=2,
                expected=[1, 2],
            )
            Test(
                positive_feedback=["smart", "brilliant", "studious"],
                negative_feedback=["not"],
                report=["this student is not studious", "the student is smart"],
                student_id=[1, 2],
                k=2,
                expected=[2, 1],
            )
            Test(
                positive_feedback=["fkeofjpc", "qq", "iio"],
                negative_feedback=[
                    "jdh",
                    "khj",
                    "eget",
                    "rjstbhe",
                    "yzyoatfyx",
                    "wlinrrgcm",
                ],
                report=[
                    "rjstbhe eget kctxcoub urrmkhlmi yniqafy fkeofjpc iio yzyoatfyx khj iio",
                    "gpnhgabl qq qq fkeofjpc dflidshdb qq iio khj qq yzyoatfyx",
                    "tizpzhlbyb eget z rjstbhe iio jdh jdh iptxh qq rjstbhe",
                    "jtlghe wlinrrgcm jnkdbd k iio et rjstbhe iio qq jdh",
                    "yp fkeofjpc lkhypcebox rjstbhe ewwykishv egzhne jdh y qq qq",
                    "fu ql iio fkeofjpc jdh luspuy yzyoatfyx li qq v",
                    "wlinrrgcm iio qq omnc sgkt tzgev iio iio qq qq",
                    "d vhg qlj khj wlinrrgcm qq f jp zsmhkjokmb rjstbhe",
                ],
                student_id=[
                    96537918,
                    589204657,
                    765963609,
                    613766496,
                    43871615,
                    189209587,
                    239084671,
                    908938263,
                ],
                k=3,
                expected=[239084671, 589204657, 43871615],
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
