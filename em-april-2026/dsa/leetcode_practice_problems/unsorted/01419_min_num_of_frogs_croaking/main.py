class Solution:
    def minNumberOfFrogs(self, croakOfFrogs) -> int:
        c = 0
        r = 0
        o = 0
        a = 0
        k = 0
        current_frogs = 0
        max_frogs = 0

        for ch in croakOfFrogs:
            # 1. Increment the specific letter we just saw
            if ch == "c":
                c = c + 1
                current_frogs = current_frogs + 1
                max_frogs = max(max_frogs, current_frogs)
            elif ch == "r":
                r = r + 1
            elif ch == "o":
                o = o + 1
            elif ch == "a":
                a = a + 1
            elif ch == "k":
                k = k + 1
                current_frogs = current_frogs - 1
            else:
                return -1  # Invalid character

            # 2. The Golden Rule of Croaking:
            # A letter can never be counted more times than the letter before
            # it.
            if (c < r or r < o or o < a or a < k):
                return -1
        # 3. Ensure no frogs are left mid-croak
        if current_frogs == 0:
            return max_frogs
        return -1


def main():
    s = Solution()
    input = "crcoakroak"
    # input = "croakcroak"
    output = s.minNumberOfFrogs(input)
    print(f"input = {input}, output = {output}")


if __name__ == "__main__":
    main()
