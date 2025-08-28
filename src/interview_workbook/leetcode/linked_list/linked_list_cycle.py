"""
LeetCode 141: Linked List Cycle

Given head, the head of a linked list, determine if the linked list has a cycle in it.

There is a cycle in a linked list if there is some node in the list that can be
reached again by continuously following the next pointer. Internally, pos is used
to denote the index of the node that tail's next pointer is connected to.
Note that pos is not passed as a parameter.

Return true if there is a cycle in the linked list. Otherwise, return false.

Example 1:
Input: head = [3,2,0,-4], pos = 1
Output: true
Explanation: There is a cycle in the linked list, where the tail connects to the 1st node (0-indexed).

Example 2:
Input: head = [1,2], pos = 0
Output: true
Explanation: There is a cycle in the linked list, where the tail connects to the 0th node.

Example 3:
Input: head = [1], pos = -1
Output: false
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
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        """
        Detect cycle using Floyd's cycle detection algorithm (tortoise and hare).

        Time: O(n) - each node visited at most once by slow pointer
        Space: O(1) - only use two pointers

        Algorithm:
        1. Use two pointers: slow (moves 1 step) and fast (moves 2 steps)
        2. If there's no cycle, fast will reach None
        3. If there's a cycle, fast will eventually meet slow inside the cycle
        """
        if not head or not head.next:
            return False

        slow = head
        fast = head

        # Move pointers until fast reaches end or they meet
        while fast and fast.next:
            slow = slow.next  # Move 1 step
            fast = fast.next.next  # Move 2 steps

            if slow == fast:  # Cycle detected
                return True

        return False  # No cycle

    def hasCycleHashSet(self, head: Optional[ListNode]) -> bool:
        """
        Detect cycle using hash set to track visited nodes.

        Time: O(n)
        Space: O(n) - store all nodes in worst case

        This approach is simpler but uses more space.
        """
        if not head:
            return False

        visited = set()
        current = head

        while current:
            if current in visited:
                return True
            visited.add(current)
            current = current.next

        return False

    def hasCycleModification(self, head: Optional[ListNode]) -> bool:
        """
        Detect cycle by modifying node values (not recommended for real use).

        Time: O(n)
        Space: O(1)

        Note: This modifies the original list, which is generally not acceptable.
        """
        if not head:
            return False

        # Use a special marker value
        VISITED = float("inf")
        current = head

        while current:
            if current.val == VISITED:
                return True

            # Mark as visited (modifies original list!)
            temp = current.next
            current.val = VISITED
            current = temp

        return False


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
    """Demo of Linked List Cycle."""
    solution = Solution()

    test_cases = [
        {
            "values": [3, 2, 0, -4],
            "pos": 1,
            "expected": True,
            "description": "Example 1: cycle at position 1",
        },
        {
            "values": [1, 2],
            "pos": 0,
            "expected": True,
            "description": "Example 2: cycle at position 0",
        },
        {
            "values": [1],
            "pos": -1,
            "expected": False,
            "description": "Example 3: single node, no cycle",
        },
        {"values": [], "pos": -1, "expected": False, "description": "Empty list"},
        {
            "values": [1, 2, 3, 4, 5],
            "pos": -1,
            "expected": False,
            "description": "No cycle in longer list",
        },
        {
            "values": [1, 2, 3, 4, 5],
            "pos": 2,
            "expected": True,
            "description": "Cycle at position 2",
        },
        {
            "values": [1],
            "pos": 0,
            "expected": True,
            "description": "Single node pointing to itself",
        },
    ]

    print("=== LeetCode 141: Linked List Cycle ===\n")

    for i, test in enumerate(test_cases, 1):
        values = test["values"]
        pos = test["pos"]
        expected = test["expected"]
        description = test["description"]

        print(f"Test Case {i}:")
        print(f"Description: {description}")
        print(f"Values: {values}")
        print(f"Cycle position: {pos}")
        print(f"Expected: {expected}")

        # Test Floyd's algorithm (main solution)
        head1 = create_linked_list_with_cycle(values, pos)
        result1 = solution.hasCycle(head1)
        print(f"Result (Floyd's): {result1}")
        status1 = "✓ PASS" if result1 == expected else "✗ FAIL"
        print(f"Status: {status1}")

        # Test hash set solution
        head2 = create_linked_list_with_cycle(values, pos)
        result2 = solution.hasCycleHashSet(head2)
        print(f"Result (HashSet): {result2}")
        status2 = "✓ PASS" if result2 == expected else "✗ FAIL"

        # Note: Skip modification test as it destroys the list
        print()


if __name__ == "__main__":
    demo()


# Register the problem
register_problem(
    id="141",
    title="Linked List Cycle",
    difficulty="Easy",
    category="Linked List",
    url="https://leetcode.com/problems/linked-list-cycle/",
    tags=["Hash Table", "Linked List", "Two Pointers"],
)
