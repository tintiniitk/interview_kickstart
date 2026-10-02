# Design And Implement Skip List
Skip List is a probabilistic data structure that allows O (log(n)) search complexity as well as O (log(n)) insertion complexity within an ordered sequence of n elements.

Implement it using only linked lists.

Skip list has three operations:

insert(value) inserts a value in a skip list, does not return anything.
is_present(value) returns true if given value is present in the skip list and false otherwise.
remove(value) removes a value from a skip list, does not return anything.
Execute the given sequence of operations and return values returned by is_present operations.

Each operation will be given as two numbers:
- [0, value] means insert(value),
- [1, value] means is_present(value), and
- [2, value] means remove(value).

## Example
{
"operations": [
[0, 5],
[0, 10],
[0, 1],
[1, 0],
[2, 0],
[1, 1],
[2, 1],
[2, 10],
[0, 10],
[1, 10]
]
}
Output:

[0, 1, 1]
First 3 operations are to insert 5, 10 and 1 in the skip list. So the skip list contains values [1, 5, 10].

4th operation is to search for 0. As 0 is not present in the skip list, the return value will be false.

5th operation is to remove value 0. Now skip list contains [1, 5, 10].

6th operation is to search for 1. As 1 is present in the skip list, the return value will be true.

7th operation is to remove value 1. Now skip list contains [5, 10].

8th operation is to remove value 10. Now skip list contains [5].

9th operation is to insert value 10. Now skip list contains [5, 10].

10th operation is to search for 10. As 10 is present in the skip list, the return value will be true.

## Notes
- There can be duplicate instructions in the input.
- In case of the remove operation, if given value is not present in the skip list, ignore it.
- It is a good idea to implement skip list as a class (or object or struct - depending on the language you use). In function implement_skip_list you would then create an instance of that class/object/struct and call its methods/functions to execute the operations.
- Structure of the class may look like this:
    ```java
    class SkipList {
        SkipList() {
            // This is a constructor.
            // Initialize required data structures.
        }

        void insert(int value) {
            // ...
        }

        bool is_present(int value) {
            // ...
        }

        void remove(int value) {
            // ...
        }
    }
    ```

## Constraints:
- 1 <= number of operations <= 100000
- -10<sup>9</sup> <= value in an operation <= 10<sup>9</sup>