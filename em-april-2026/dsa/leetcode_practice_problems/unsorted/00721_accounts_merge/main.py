import logging

from utils.logger import create_logger

logger = create_logger(logging.ERROR)


class Solution:
    def accountsMerge(self, accounts: list[list[str]]) -> list[list[str]]:
        n = len(accounts)
        if n == 1:
            return accounts
        logger.debug(f"accounts = {accounts}")
        e2a = {}
        a2a = {i: i for i in range(n)}  # account to mapped account

        def find_ultimate_mapped_account(account: int) -> int:
            while account in a2a and a2a[account] != account:
                account = a2a[account]
            return account

        for i, account in enumerate(accounts):
            # logger.debug(f"processing account #{i:04} {account}")
            name = account[0]
            mapped_accounts = {i}
            for email in account[1:]:
                if email in e2a and accounts[e2a[email]][0] == name:
                    mapped_accounts.add(find_ultimate_mapped_account(e2a[email]))
            # logger.debug(f"  found mapped_accounts = {mapped_accounts}")
            ultimate_mapped_account = min(mapped_accounts)
            # logger.debug(f"  found ultimate_mapped_account = {ultimate_mapped_account}")
            if i != ultimate_mapped_account:
                a2a[i] = ultimate_mapped_account
                # logger.debug(f"  updated a2a[{i}] = {ultimate_mapped_account}")
            e2a.update({email: ultimate_mapped_account for email in account[1:]})
            # logger.debug(f"  updated e2a -> {e2a}")
            for other_same_account in [
                account
                for account in mapped_accounts
                if account not in {ultimate_mapped_account, i}
            ]:
                a2a[other_same_account] = ultimate_mapped_account
                # logger.debug(
                # f"  updated a2a[{other_same_account}] = {ultimate_mapped_account}"
                # )
                for email in accounts[other_same_account][1:]:
                    e2a[email] = ultimate_mapped_account
                    # logger.debug(f"  updated e2a -> {e2a}")
            # logger.debug(f"  so far a2a = {a2a}")
        for account, mapped_account in a2a.items():
            if account != mapped_account:
                a2a[account] = find_ultimate_mapped_account(mapped_account)
        # logger.debug(f"e2a={e2a}")
        logger.debug(f"a2a={a2a}")
        unique_accounts = set(a2a.values())
        num_unique_accounts = len(unique_accounts)
        index = 0
        account_to_index = {}
        ret = [[] for _ in range(num_unique_accounts)]
        for unique_account in unique_accounts:
            if unique_account not in account_to_index:
                account_to_index[unique_account] = index
                ret[index].append(accounts[unique_account][0])
                index += 1
        # logger.debug(f"account_to_index = {account_to_index}")
        logger.debug(f"initialized ret = {ret}")
        for account in range(n):
            for email in accounts[account][1:]:
                ret[account_to_index[a2a[account]]].append(email)
        logger.debug(f"unsorted ret = {ret}")
        for account_row in ret:
            account_row[1:] = sorted(set(account_row[1:]))
        logger.debug(f"Sorted ret = {ret}")
        return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(accounts: list[list[str]], expected: list[list[str]]) -> tuple[bool, str]:
    actual = Solution().accountsMerge(accounts)
    if sorted(actual) != sorted(expected):
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        logger.info("Running tests ...")
        with time_limit(5):
            Test(
                accounts=[
                    ["John", "johnsmith@mail.com", "john_newyork@mail.com"],
                    ["John", "johnsmith@mail.com", "john00@mail.com"],
                    ["Mary", "mary@mail.com"],
                    ["John", "johnnybravo@mail.com"],
                ],
                expected=[
                    [
                        "John",
                        "john00@mail.com",
                        "john_newyork@mail.com",
                        "johnsmith@mail.com",
                    ],
                    ["Mary", "mary@mail.com"],
                    ["John", "johnnybravo@mail.com"],
                ],
            )
            Test(
                accounts=[
                    ["Gabe", "Gabe0@m.co", "Gabe3@m.co", "Gabe1@m.co"],
                    ["Kevin", "Kevin3@m.co", "Kevin5@m.co", "Kevin0@m.co"],
                    ["Ethan", "Ethan5@m.co", "Ethan4@m.co", "Ethan0@m.co"],
                    ["Hanzo", "Hanzo3@m.co", "Hanzo1@m.co", "Hanzo0@m.co"],
                    ["Fern", "Fern5@m.co", "Fern1@m.co", "Fern0@m.co"],
                ],
                expected=[
                    ["Ethan", "Ethan0@m.co", "Ethan4@m.co", "Ethan5@m.co"],
                    ["Gabe", "Gabe0@m.co", "Gabe1@m.co", "Gabe3@m.co"],
                    ["Hanzo", "Hanzo0@m.co", "Hanzo1@m.co", "Hanzo3@m.co"],
                    ["Kevin", "Kevin0@m.co", "Kevin3@m.co", "Kevin5@m.co"],
                    ["Fern", "Fern0@m.co", "Fern1@m.co", "Fern5@m.co"],
                ],
            )
            Test(
                accounts=[
                    ["nameA", "email1@a.com", "email2@a.com"],
                    ["nameB", "email3@a.com", "email4@a.com"],
                    ["nameA", "email5@a.com", "email6@a.com", "email7@a.com"],
                    ["nameA", "email1@a.com", "email5@a.com"],
                    ["nameC", "email8@a.com", "email9@a.com"],
                    ["nameB", "email4@a.com", "email10@a.com"],
                ],
                expected=[
                    ["nameC", "email8@a.com", "email9@a.com"],
                    ["nameB", "email10@a.com", "email3@a.com", "email4@a.com"],
                    [
                        "nameA",
                        "email1@a.com",
                        "email2@a.com",
                        "email5@a.com",
                        "email6@a.com",
                        "email7@a.com",
                    ],
                ],
            )
            Test(
                accounts=[
                    ["David", "David0@m.co", "David1@m.co"],
                    ["David", "David3@m.co", "David4@m.co"],
                    ["David", "David4@m.co", "David5@m.co"],
                    ["David", "David2@m.co", "David3@m.co"],
                    ["David", "David1@m.co", "David2@m.co"],
                ],
                expected=[
                    [
                        "David",
                        "David0@m.co",
                        "David1@m.co",
                        "David2@m.co",
                        "David3@m.co",
                        "David4@m.co",
                        "David5@m.co",
                    ]
                ],
            )

    except TimeoutException as te:
        logger.error(f"Tests got timed out: {te}")
        sys.exit(1)
    finally:
        logger.info("Tests completed!")


if __name__ == "__main__":
    main()
