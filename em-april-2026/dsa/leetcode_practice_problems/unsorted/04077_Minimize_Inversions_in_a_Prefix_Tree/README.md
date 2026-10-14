# 4077. Minimize Inversions in a Prefix Tree

You are given an array words of n unique strings containing only lowercase English letters from 'a' to 'j'. You are also given an integer array target containing each index from 0 to n - 1 exactly once.

Build a prefix tree from words:

The root represents the empty string "".
Each other node represents a different non-empty prefix of a word. The parent of a node is the prefix obtained by removing its last character.
The node representing the complete word words[i] is marked with index i. A marked node may also have children.
You may choose the order of the children of each node independently. You cannot change which node is a child's parent.

Traverse the tree starting at the root. When visiting a node, first record its index if it is marked. Then visit its children in the chosen order, completing the traversal of each child before moving to the next. This is a pre-order traversal.

The recorded indices form an array traversal of length n. Let pos[i] be the position of index i in target.

An inversion is a pair of positions (a, b) such that 0 <= a < b < n and pos[traversal[a]] > pos[traversal[b]].

Return the minimum possible number of inversions over all choices of child orderings.

## Example 1:
- ​​​​​​​​​​​​​​Input: words = ["bad","bag","fig","fed"], target = [3,1,0,2]
- Output: 2
- Explanation:
  - Visit the root's "f" child before its "b" child. Within the "f" branch, visit "fed" before "fig". Within the "b" branch, visit "bag" before "bad".
  - This produces traversal = [3,2,1,0]:
  - Traversal position	Word index	Word	Position in target
    ```
    0	3	"fed"	0
    1	2	"fig"	3
    2	1	"bag"	1
    3	0	"bad"	2
    ```
  - The positions in target are [0,3,1,2]. The inversions are the pairs of traversal positions (1,2) and (1,3), since 3 > 1 and 3 > 2.
  - No child ordering produces fewer than 2 inversions.

## Example 2:
- Input: words = ["ab","ac","ba","bc"], target = [0,3,1,2]
- Output: 1
- Explanation:
 - Visit the root's "a" child before its "b" child. Within these branches, visit "ab" before "ac", and "bc" before "ba".
 - This produces traversal = [0,1,3,2]:
 - Traversal position	Word index	Word	Position in target
   ```md
   0	0	"ab"	0
   1	1	"ac"	2
   2	3	"bc"	1
   3	2	"ba"	3
   ```
 - The positions in target are [0,2,1,3]. The only inversion is the pair of traversal positions (1,2), since 2 > 1.
 - No child ordering produces zero inversions.

## Constraints:
- 1 <= n == words.length <= 10<sup>4</sup>
- 1 <= words[i].length <= 20
- words[i] contains only lowercase English letters from 'a' to 'j'​​​​​​​
- All words[i] are unique
- 0 <= target[i] <= n - 1
- target is a permutation of integers from 0 to n - 1