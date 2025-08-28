"""
LeetCode 142: Linked List Cycle II

Given the head of a linked list, return the node where the cycle begins.
If there is no cycle, return null.

There is a cycle in a linked list if there is some node in the list that can be
reached again by continuously following the next pointer. Internally, pos is used
to denote the index of the node that tail's next pointer is connected to (0-indexed).
It is -1 if there is no cycle. Note that pos is not passed as a parameter.

Do not modify the linked list.

Example 1:
Input: head = [3,2,0,-4], pos = 1
Output: tail connects to node index 1
Explanation: There is a cycle in the linked list, where tail connects to the second node.

Example 2:
Input: head = [1,2], pos = 0
Output: tail connects to node index 0
Explanation: There is a cycle in the linked list, where tail connects to the first node.

Example 3:
Input: head = [1], pos = -1
Output: no cycle
Explanation: There is no cycle in the linked list.

Constraints:
- The number of the nodes in the list is in the range [0, 10^4]
- -10^5 <= Node.val <= 10^5
- pos is -1 or a valid index in the linked-list

Follow up: Can you solve it using O(1) (i.e. constant) memory?
"""

from typing import Optional

from interview_workbook.leetcode._registry import register_problem


# Definition for singly-linked list node
class ListNode:
    def __init__(self, val: int = 0):
        self.val = val
        self.next = None

    def __repr__(self):
        return f"ListNode({self.val})"


class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Find cycle start using Floyd's cycle detection algorithm with mathematical insight.

        Time: O(n)
        Space: O(1)

        Algorithm:
        1. Phase 1: Use slow/fast pointers to detect if cycle exists
        2. Phase 2: If cycle exists, find the cycle start node
           - Mathematical insight: when slow and fast meet, if we start a new pointer
             from head and move both slow and new pointer one step at a time,
             they will meet at the cycle start

        Mathematical proof:
        Let's say distance from head to cycle start is 'a',
        distance from cycle start to meeting point is 'b',
        remaining cycle length is 'c'.

        When they meet:
        - Slow traveled: a + b
        - Fast traveled: a + b + c + b = a + 2b + c

        Since fast travels twice as fast: 2(a + b) = a + 2b + c
        Solving: 2a + 2b = a + 2b + c  =>  a = c

        This means distance from head to cycle start equals
        distance from meeting point to cycle start.
        """
        if not head or not head.next:
            return None

        # Phase 1: Detect if cycle exists using Floyd's algorithm
        slow = fast = head

        # Find meeting point in cycle (if exists)
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

            if slow == fast:
                break
        else:
            # No cycle found
            return None

        # Phase 2: Find cycle start
        # Start new pointer from head, move both one step at a time
        start = head
        while start != slow:
            start = start.next
            slow = slow.next

        return start

    def detectCycleHashSet(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Find cycle start using hash set (uses extra space).

        Time: O(n)
        Space: O(n)
        """
        if not head:
            return None

        visited = set()
        current = head

        while current:
            if current in visited:
                return current
            visited.add(current)
            current = current.next

        return None

    def detectCycleTortoisePlusDistance(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Alternative implementation with explicit distance calculation.

        Time: O(n)
        Space: O(1)
        """
        if not head or not head.next:
            return None

        # Step 1: Detect cycle using Floyd's algorithm
        slow = fast = head
        has_cycle = False

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

            if slow == fast:
                has_cycle = True
                break

        if not has_cycle:
            return None

        # Step 2: Find cycle length
        cycle_length = 1
        current = slow.next
        while current != slow:
            current = current.next
            cycle_length += 1

        # Step 3: Find cycle start
        # Move first pointer cycle_length steps ahead
        first = second = head
        for _ in range(cycle_length):
            first = first.next

        # Move both pointers until they meet at cycle start
        while first != second:
            first = first.next
            second = second.next

        return first


def create_linked_list_with_cycle(values: list[int], pos: int = -1) -> Optional[ListNode]:
    """
    Helper function to create a linked list with optional cycle.

    Args:
        values: list of node values
        pos: index where tail connects to (-1 for no cycle)
    """
    if not values:
        return None

    # Create nodes
    nodes = [ListNode(val) for val in values]

    # Link nodes
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]

    # Create cycle if specified
    if pos != -1 and pos < len(nodes):
        nodes[-1].next = nodes[pos]

    return nodes[0]


def demo():
    """Demo of Linked List Cycle II."""
    solution = Solution()

    test_cases = [
        {
            "values": [3, 2, 0, -4],
            "pos": 1,
            "expected_pos": 1,
            "description": "Example 1: cycle starts at position 1",
        },
        {
            "values": [1, 2],
            "pos": 0,
            "expected_pos": 0,
            "description": "Example 2: cycle starts at position 0",
        },
        {"values": [1], "pos": -1, "expected_pos": -1, "description": "Example 3: no cycle"},
        {"values": [], "pos": -1, "expected_pos": -1, "description": "Empty list"},
        {
            "values": [1, 2, 3, 4, 5],
            "pos": 2,
            "expected_pos": 2,
            "description": "Cycle starts at middle",
        },
        {
            "values": [1, 2, 3, 4, 5],
            "pos": -1,
            "expected_pos": -1,
            "description": "No cycle in longer list",
        },
        {
            "values": [1],
            "pos": 0,
            "expected_pos": 0,
            "description": "Single node pointing to itself",
        },
    ]

    print("=== LeetCode 142: Linked List Cycle II ===\n")

    for i, test in enumerate(test_cases, 1):
        values = test["values"]
        pos = test["pos"]
        expected_pos = test["expected_pos"]
        description = test["description"]

        print(f"Test Case {i}:")
        print(f"Description: {description}")
        print(f"Values: {values}")
        print(f"Cycle position: {pos}")
        print(f"Expected cycle start position: {expected_pos}")

        # Create linked list with cycle
        head = create_linked_list_with_cycle(values, pos)

        # Test Floyd's algorithm (main solution)
        cycle_start1 = solution.detectCycle(head)

        # Determine actual position
        if cycle_start1 is None:
            actual_pos1 = -1
        else:
            # Find position by traversing from head
            actual_pos1 = 0
            curr = head
            while curr != cycle_start1:
                curr = curr.next
                actual_pos1 += 1

        print(f"Result (Floyd's): position {actual_pos1}")
        status1 = "✓ PASS" if actual_pos1 == expected_pos else "✗ FAIL"
        print(f"Status: {status1}")

        # Test hash set solution
        head2 = create_linked_list_with_cycle(values, pos)
        cycle_start2 = solution.detectCycleHashSet(head2)

        if cycle_start2 is None:
            actual_pos2 = -1
        else:
            actual_pos2 = 0
            curr = head2
            while curr != cycle_start2:
                curr = curr.next
                actual_pos2 += 1

        print(f"Result (HashSet): position {actual_pos2}")
        status2 = "✓ PASS" if actual_pos2 == expected_pos else "✗ FAIL"

        # Test alternative Floyd's solution
        head3 = create_linked_list_with_cycle(values, pos)
        cycle_start3 = solution.detectCycleTortoisePlusDistance(head3)

        if cycle_start3 is None:
            actual_pos3 = -1
        else:
            actual_pos3 = 0
            curr = head3
            while curr != cycle_start3:
                curr = curr.next
                actual_pos3 += 1

        print(f"Result (Alt Floyd's): position {actual_pos3}")
        print()


if __name__ == "__main__":
    demo()


# Register the problem
register_problem(
    id="142",
    title="Linked List Cycle II",
    difficulty="Medium",
    category="Linked List",
    url="https://leetcode.com/problems/linked-list-cycle-ii/",
    tags=["Hash Table", "Linked List", "Two Pointers"],
)
