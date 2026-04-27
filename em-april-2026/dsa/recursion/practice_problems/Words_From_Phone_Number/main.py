import sys

"""

Words From Phone Number
Given a seven-digit phone number, return all the character combinations that can be generated according to the following mapping:

Graph

Return the combinations in the lexicographical order.

Example One
{
"phone_number": "1234567"
}
Output:

[
"adgjmp",
"adgjmq",
"adgjmr",
"adgjms",
"adgjnp",
...
"cfilns",
"cfilop",
"cfiloq",
"cfilor",
"cfilos"
]
First string \"adgjmp\" in the first line comes from the first characters mapped to digits 2, 3, 4, 5, 6 and 7 respectively. Since digit 1 maps to nothing, nothing is appended before 'a'. Similarly, the fifth string \"adgjnp\" generated from first characters of 2, 3, 4, 5 second character of 6 and first character of 7. All combinations generated in such a way must be returned in the lexicographical order.

Example Two
{
\"phone_number\": "1010101"
}
Output:

[""]
Notes
Return an array of the generated string combinations in the lexicographical order. If nothing can be generated, return a list with an empty string "".
Digits 0 and 1 map to nothing. Other digits map to either three or four different characters each.
Constraints:

Input string is 7 characters long; each character is a digit.


"""


def helper(
    mappings: dict[int, str],
    remaining_numbers: list[int],
    slate: list[str],
    done: int,
    filled: int,
    ret: list[str],
):
    if done == len(slate):
        ret.append("".join(slate[:filled]))
        return
    next_num = remaining_numbers[0]
    if next_num in mappings:
        for next_char in mappings[next_num]:
            slate[filled] = next_char
            helper(mappings, remaining_numbers[1:], slate, done + 1, filled + 1, ret)
    else:
        helper(mappings, remaining_numbers[1:], slate, done + 1, filled, ret)


def get_words_from_phone_number(phone_number):
    """
    Args:
     phone_number(str)
    Returns:
     list_str
    """
    # Write your code here.
    mappings = {
        2: "abc",
        3: "def",
        4: "ghi",
        5: "jkl",
        6: "mno",
        7: "pqrs",
        8: "tuv",
        9: "wxyz",
    }
    ret = []
    helper(
        mappings,
        [int(phone_number_digit_char) for phone_number_digit_char in phone_number],
        ["."] * len(phone_number),
        0,
        0,
        ret,
    )
    return ret


if __name__ == "__main__":
    phone_number = "1234567"
    if len(sys.argv) > 1:
        phone_number = sys.argv[1]
    words = get_words_from_phone_number(phone_number)
    print(f"phone_number={phone_number}, words={words}")
