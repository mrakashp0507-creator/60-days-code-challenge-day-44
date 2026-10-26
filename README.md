
# Day 44 - Course Schedule

## Problem Statement
Given a number of courses and their prerequisite relationships,
determine whether all courses can be completed.

A cycle in the directed prerequisite graph makes completion
impossible.

## Algorithms Implemented
1. BFS using Kahn's Topological Sorting Algorithm
2. DFS using three-state cycle detection

## BFS Approach
1. Build a directed graph.
2. Calculate the in-degree of every course.
3. Add all courses with in-degree zero to a queue.
4. Process available courses and reduce the in-degree
   of their dependent courses.
5. Add newly available courses to the queue.
6. Compare completed courses with the total number of courses.
7. If they differ, a cycle exists.

## Example

Valid:
0 -> 1 -> 2 -> 3

Output: True

Invalid:
0 -> 1 -> 2 -> 0

Output: False

## Test Cases
- Linear prerequisites
- Circular prerequisites
- Independent courses
- Disconnected graph containing a cycle
- Self-dependency
- Empty course list
- Multiple prerequisites

## Complexity
Time: O(V + E)
Space: O(V + E)

V = number of courses
E = number of prerequisite relationships

## Real-World Applications
- Package managers
- CI/CD pipelines
- Build systems
- University scheduling
- Task dependency management

## Run
python day44_course_schedule.py
