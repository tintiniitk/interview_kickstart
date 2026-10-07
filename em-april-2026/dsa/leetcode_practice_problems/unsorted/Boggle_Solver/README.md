# Boggle Solver
You are given a dictionary set dictionary that contains dictionaryCount distinct words and a matrix mat of size n * m.
Your task is to find all possible words that can be formed by a sequence of adjacent characters in the matrix mat.
Note that we can move to any of 8 adjacent characters, but a word should not have multiple instances of the same cell of the matrix.

## Example
```json
{
"dictionary": ["bst", "heap", "tree"],
"mat": ["bsh", "tee", "arh"]
}
```
Output:
```json
["bst", "tree"]
```
The input matrix is represented below:

bsh
tee
arh

Assume here top left-most corner is at (0,0) and bottom right-most corner is (2,2).
Presence of "bst" is marked bold in the below representation:
(0,0) -> (0,1) -> (1,0)

bsh
tee
arh

Presence of "tree" is marked bold in the below representation:
(1,0) -> (2,1) -> (1,1) -> (1,2)

bsh
tee
arh

Notes
Same dictionary word can be found in the matrix multiple times. We only need to check the existence of the dictionary word in the matrix. Hence, for multiple existences for the same word only add it once in the list of all found words.
Constraints:

1 <= dictionaryCount <= 1000
1 <= n * m <= 100000
1 <= length of words in dictionary <= 100
All the characters in mat and in the dictionary words are lower case English letters