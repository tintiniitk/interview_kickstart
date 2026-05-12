# 1. Generate the grid: 999,999 rows of ["O"], followed by one row of ["G"]
grid = [["O"] for _ in range(999999)] + [["G"]]

# 2. Generate the expected output: counting down from 999,999 to 0
expected_output = [[i] for i in range(999999, -1, -1)]
