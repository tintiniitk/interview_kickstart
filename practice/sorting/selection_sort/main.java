import java.util.Arrays;

public class SelectionSort {

    // Efficiently print the array using Java's built-in utility
    public static void printV(int[] v) {
        System.out.print(Arrays.toString(v));
    }

    public static boolean selectionSort(int[] input) {
        if (input.length < 2) {
            return true;
        }

        int end = input.length;
        for (int start = 0; start < end - 1; ++start) {
            int minVal = input[start];
            int minIndex = start;

            for (int i = start + 1; i < end; ++i) {
                if (input[i] < minVal) {
                    minIndex = i;
                    minVal = input[i];
                }
            }

            // Swap using a temporary variable
            if (minIndex != start) {
                int temp = input[start];
                input[start] = input[minIndex];
                input[minIndex] = temp;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        // Primitive array (equivalent to C++ int array or vector)
        int[] input = {5, 3, 2, 4, 9, 6, 7, 1, 0, 8};

        System.out.print("Before sorting: \t\t\t\t");
        printV(input);
        System.out.println();

        selectionSort(input);

        System.out.print("After sorting: \t\t\t\t\t");
        printV(input);
        System.out.println();
    }
}

