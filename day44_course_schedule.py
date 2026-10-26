
from collections import deque


def build_graph(num_courses, prerequisites):
    """
    [course, prerequisite] means:
    prerequisite -> course
    """
    graph = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses

    for course, prerequisite in prerequisites:
        graph[prerequisite].append(course)
        indegree[course] += 1

    return graph, indegree


def can_finish_bfs(num_courses, prerequisites, show_trace=False):
    """Detect cycles using Kahn's topological sorting algorithm."""

    graph, indegree = build_graph(num_courses, prerequisites)

    queue = deque(
        course
        for course in range(num_courses)
        if indegree[course] == 0
    )

    completed = 0

    if show_trace:
        print("Initial in-degree:", indegree)
        print("Initially available courses:", list(queue))

    while queue:
        course = queue.popleft()
        completed += 1

        if show_trace:
            print(f"\nComplete course {course}")

        for dependent in graph[course]:
            indegree[dependent] -= 1

            if show_trace:
                print(
                    f"  Course {dependent} now has "
                    f"in-degree {indegree[dependent]}"
                )

            if indegree[dependent] == 0:
                queue.append(dependent)

                if show_trace:
                    print(f"  Course {dependent} is now available")

    if show_trace:
        print(f"\nCompleted {completed} of {num_courses} courses")

        if completed < num_courses:
            remaining = [
                course
                for course in range(num_courses)
                if indegree[course] > 0
            ]
            print("Courses still blocked:", remaining)
            print("A cycle exists in the prerequisite graph.")

    return completed == num_courses


def can_finish_dfs(num_courses, prerequisites):
    """Detect cycles using DFS and three node states.

    0 = unvisited
    1 = currently exploring
    2 = fully processed
    """
    graph, _ = build_graph(num_courses, prerequisites)
    state = [0] * num_courses

    def dfs(course):
        if state[course] == 1:
            # Reached a node already on the current DFS path.
            return False

        if state[course] == 2:
            return True

        state[course] = 1

        for dependent in graph[course]:
            if not dfs(dependent):
                return False

        state[course] = 2
        return True

    for course in range(num_courses):
        if state[course] == 0:
            if not dfs(course):
                return False

    return True


def visualize_graph(num_courses, prerequisites):
    """Print prerequisite relationships."""
    graph, indegree = build_graph(num_courses, prerequisites)

    print("Prerequisite relationships:")

    has_edges = False
    for prerequisite in range(num_courses):
        for course in graph[prerequisite]:
            print(f"  {prerequisite} -> {course}")
            has_edges = True

    if not has_edges:
        print("  No dependencies")

    print("In-degree per course:", indegree)


def run_tests():
    tests = [
        (
            "Linear prerequisites",
            3,
            [[1, 0], [2, 1]],
            True,
        ),
        (
            "Circular prerequisites",
            3,
            [[1, 0], [2, 1], [0, 2]],
            False,
        ),
        (
            "Independent courses",
            4,
            [],
            True,
        ),
        (
            "Disconnected graph with cycle",
            4,
            [[1, 0], [2, 3], [3, 2]],
            False,
        ),
        (
            "Self-dependency",
            1,
            [[0, 0]],
            False,
        ),
        (
            "No courses",
            0,
            [],
            True,
        ),
        (
            "Multiple prerequisites",
            4,
            [[2, 0], [2, 1], [3, 2]],
            True,
        ),
    ]

    print("\n=== TEST RESULTS ===")
    all_passed = True

    for name, num_courses, prerequisites, expected in tests:
        bfs_result = can_finish_bfs(num_courses, prerequisites)
        dfs_result = can_finish_dfs(num_courses, prerequisites)

        passed = bfs_result == expected and dfs_result == expected
        all_passed = all_passed and passed

        print(
            f"{name}: BFS={bfs_result}, DFS={dfs_result}, "
            f"Expected={expected} -> {'PASS' if passed else 'FAIL'}"
        )

    print(
        "\nOverall:",
        "ALL TESTS PASSED" if all_passed else "SOME TESTS FAILED",
    )


def main():
    num_courses = 4
    prerequisites = [[1, 0], [2, 1], [3, 2]]

    print("=" * 50)
    print("       UNIVERSITY COURSE SCHEDULER")
    print("=" * 50)

    print("\n=== VALID SCHEDULE ===")
    visualize_graph(num_courses, prerequisites)

    result = can_finish_bfs(
        num_courses, prerequisites, show_trace=True
    )
    print("\nCan finish all courses:", result)

    cyclic_prerequisites = [[1, 0], [2, 1], [0, 2]]

    print("\n=== CYCLIC SCHEDULE ===")
    visualize_graph(3, cyclic_prerequisites)

    cyclic_result = can_finish_bfs(
        3, cyclic_prerequisites, show_trace=True
    )
    print("\nCan finish all courses:", cyclic_result)

    print("\n=== DFS COMPARISON ===")
    print(
        "Valid graph:",
        can_finish_dfs(num_courses, prerequisites),
    )
    print(
        "Cyclic graph:",
        can_finish_dfs(3, cyclic_prerequisites),
    )

    print("\n=== COMPLEXITY ===")
    print("Time: O(V + E)")
    print("Space: O(V + E)")
    print("V = number of courses, E = number of prerequisites")

    run_tests()


if __name__ == "__main__":
    main()
