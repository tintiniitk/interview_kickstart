# Skyline
Given n buildings on a two-dimensional plane, find the skyline of these buildings.

Each building on the two-dimensional plane has a start and end x-coordinates, and a y-coordinate height. Skyline is defined as a unique representation of rectangular strips of different heights which are created after the overlap of multiple buildings on a two-dimensional plane.

The following picture demonstrates some buildings on the left side and their skyline on the right.

Buildings Buildings

Example
```json
{
"buildings": [
[2, 9, 10],
[3, 7, 15],
[5, 12, 12],
[15, 20, 10],
[19, 24, 8]
]
}
```
Output:
```json
[
[2, 10],
[3, 15],
[7, 12],
[12, 0],
[15, 10],
[20, 8],
[24, 0]
]
```
From the image referenced above, we see the blue building at the start and the corresponding red dot in the right image at (2, 10). The next change in skyline occurs at an x coordinate of 3 with the red building coming up at the height of 15, so in the output, the next line is printed as (3, 15). Similarly, all the buildings are traversed to find the output as given in the sample output section.

## Notes
- The input of buildings is given in a two-dimensional integer array format. The outer array contains multiple buildings where each building is an array of integers of size 3. The first integer represents the start coordinate of the building, the second integer represents the end coordinate of the building and the third integer represents its height.
- The output is a two-dimensional integer array. The outer array has different rectangular strips, each element is an array of size two. The first element in the inner array is the x coordinate of the strip and the second element is the y coordinate of the strip (red dots in the image above). The order of strips must be in increasing order of x-coordinate.

## Constraints:
- 1 <= n <= 10<sup>5</sup>
- 1 <= x, y, height <= 2 * 10<sup>9</sup>