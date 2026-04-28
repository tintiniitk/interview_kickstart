/**

Generate All Possible Expressions That Evaluate To The Given Target Value
Given a string s that consists of digits ("0".."9") and target, a non-negative
integer, find all expressions that can be built from string s that evaluate to
the target.

When building expressions, you have to insert one of the following operators
between each pair of consecutive characters in s: join or * or +. For example,
by inserting different operators between the two characters of string "12" we
can get either 12 (1 joined with 2 or "12") or 2 ("1*2") or 3 ("1+2").

Other operators such as - or ÷ are NOT supported.

Expressions that evaluate to the target but only utilize a part of s do not
count: entire s has to be consumed.

Precedence of the operators is conventional: join has the highest precedence, *
– medium and + has the lowest precedence. For example, 1 + 2 * 34 = (1 + (2 *
(34))) = 1 + 68 = 69.

You have to return ALL expressions that can be built from string s and evaluate
to the target.

Example
{
\"s\": "202",
\"target\": 4
}
Output:

[\"2+0+2\", \"2+02\", \"2*02\"]
Same three strings in any other order are also a correct output.

Notes
Order of strings in the output does not matter.
If there are no expressions that evaluate to target, return an empty list.
Returned strings must not contain spaces or any characters other than "0",...,
"9", "*", "+". All returned strings must start and end with a digit.
Constraints:

1 <= length of s <= 13
1 <= target <= 1013

Worst-case inputs:
1. s="0000000000000", target=0

**/

#include <cctype>
#include <iostream>
#include <stdexcept>
#include <string>
#include <variant>
#include <vector>

using namespace std;

template <typename T>
ostream& operator<<(ostream& o, const vector<T>& v) {
    o << "[";
    for (const auto& e : v) {
        o << e << ", ";
    }
    return o << "]";
}

enum class NodeType { DIGIT, OP };
enum class OpType { PLUS, MULTIPLY };

struct Node {
    NodeType oftype;
    variant<int, OpType> value;
};

int evaluate(const string& s) {
    if (s.empty()) {
        return 0;
    }

    auto parse = [](const string& str) -> vector<Node> {
        vector<Node> nodes;
        if (!isdigit(str.front())) {
            throw invalid_argument("first character of expression " + str +
                                   " is not a digit");
        }
        if (!isdigit(str.back())) {
            throw invalid_argument("last character of expression " + str +
                                   " is not a digit");
        }

        nodes.push_back({NodeType::DIGIT, static_cast<int>(str[0] - '0')});

        for (size_t i = 1; i < str.length(); ++i) {
            char c = str[i];
            if (isdigit(c)) {
                int next_digit = c - '0';
                if (nodes.back().oftype == NodeType::DIGIT) {
                    int& prev_val = get<int>(nodes.back().value);
                    prev_val = (10 * prev_val) + next_digit;
                } else {
                    nodes.push_back({NodeType::DIGIT, next_digit});
                }
            } else if (c == '+') {
                if (nodes.back().oftype == NodeType::DIGIT) {
                    nodes.push_back({NodeType::OP, OpType::PLUS});
                } else {
                    throw invalid_argument(
                        "'+' character of expression preceded by a non-digit "
                        "character");
                }
            } else if (c == '*') {
                if (nodes.back().oftype == NodeType::DIGIT) {
                    nodes.push_back({NodeType::OP, OpType::MULTIPLY});
                } else {
                    throw invalid_argument(
                        "'*' character of expression preceded by a non-digit "
                        "character");
                }
            } else {
                throw invalid_argument(string("Unexpected character: ") + c);
            }
        }
        return nodes;
    };

    auto multiply_parse = [](vector<Node>& nodes) -> vector<Node>& {
        if (nodes.front().oftype != NodeType::DIGIT) {
            throw invalid_argument("first node is not a digit");
        }
        if (nodes.back().oftype != NodeType::DIGIT) {
            throw invalid_argument("last node is not a digit");
        }
        if (nodes.size() % 2 == 0) {
            throw invalid_argument("nodes is of even length, should be odd!");
        }

        size_t i = 1;
        while (i < nodes.size() - 1) {
            Node& op_node = nodes[i];
            Node& next_digit_node = nodes[i + 1];

            if (op_node.oftype != NodeType::OP ||
                next_digit_node.oftype != NodeType::DIGIT) {
                throw invalid_argument(
                    "Failed check op_node.oftype != NodeType::OP OR "
                    "next_digit_node.oftype != NodeType::DIGIT");
            }

            if (holds_alternative<OpType>(op_node.value) &&
                get<OpType>(op_node.value) == OpType::MULTIPLY) {
                int& prev_val = get<int>(nodes[i - 1].value);
                int next_val = get<int>(next_digit_node.value);

                prev_val *= next_val;

                nodes.erase(nodes.begin() + i, nodes.begin() + i + 2);
            } else {
                i += 2;
            }
        }
        return nodes;
    };

    auto add_parse = [](vector<Node>& nodes) -> vector<Node>& {
        if (nodes.front().oftype != NodeType::DIGIT) {
            throw invalid_argument("first node is not a digit");
        }
        if (nodes.back().oftype != NodeType::DIGIT) {
            throw invalid_argument("last node is not a digit");
        }
        if (nodes.size() % 2 == 0) {
            throw invalid_argument("nodes is of even length, should be odd!");
        }

        size_t i = 1;
        while (i < nodes.size() - 1) {
            Node& op_node = nodes[i];
            Node& next_digit_node = nodes[i + 1];

            if (op_node.oftype != NodeType::OP ||
                get<OpType>(op_node.value) != OpType::PLUS ||
                next_digit_node.oftype != NodeType::DIGIT) {
                throw invalid_argument("Failed check for PLUS operation");
            }

            int& prev_val = get<int>(nodes[i - 1].value);
            int next_val = get<int>(next_digit_node.value);

            prev_val += next_val;
            nodes.erase(nodes.begin() + i, nodes.begin() + i + 2);
        }
        return nodes;
    };

    vector<Node> nodes = parse(s);
    multiply_parse(nodes);
    add_parse(nodes);

    return get<int>(nodes[0].value);
}

void helper(const string& s, size_t s_index, int target, vector<char>& slate,
            int filled, vector<string>& ret) {
    if (s_index >= s.length()) {
        string joined(slate.begin(), slate.begin() + filled);
        if (evaluate(joined) == target) {
            ret.push_back(joined);
        }
        return;
    }

    // try joining
    slate[filled] = s[s_index];
    helper(s, s_index + 1, target, slate, filled + 1, ret);

    // try adding
    slate[filled] = '+';
    slate[filled + 1] = s[s_index];
    helper(s, s_index + 1, target, slate, filled + 2, ret);

    // try multiplying
    slate[filled] = '*';
    slate[filled + 1] = s[s_index];
    helper(s, s_index + 1, target, slate, filled + 2, ret);
}

vector<string> generate_all_expressions(const string& s, int target) {
    if (s.empty()) {
        return {};
    }
    vector<string> ret;

    // Initialize slate with enough capacity, mirroring [" "] * (2 * len(s) - 2)
    vector<char> slate(2 * s.length() - 1, ' ');
    slate[0] = s[0];

    helper(s, 1, target, slate, 1, ret);
    return ret;
}

int main(int argc, char* argv[]) {
    // //string s = "12+3*41+5";
    // //s = "1+2*2*2+11";
    // s = "2+0*2";
    // auto evaluated = evaluate(s);
    // print(f "s={s}, evaluated={evaluated}")
    string s = "202";
    int target = 4;
    if (argc > 2) {
        s = argv[1];
        target = stoi(argv[2]);
    }
    auto expressions = generate_all_expressions(s, target);
    if (expressions.size() > 100) {
        cout << "s=" << s << ", num=" << expressions.size() << endl;
    } else {
        cout << "s=" << s << ", num=" << expressions.size()
             << ", expressions=" << expressions << endl;
    }
}
