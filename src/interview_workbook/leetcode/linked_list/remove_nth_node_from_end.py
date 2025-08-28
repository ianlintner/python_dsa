"""
LeetCode 19: Remove Nth Node From End of List

Given the head of a linked list, remove the nth node from the end of the list and return its head.

Example 1:
Input: head = [1,2,3,4,5], n = 2
Output: [1,2,3,5]

Example 2:
Input: head = [1], n = 1
Output: []

Example 3:
Input: head = [1,2], n = 1
Output: [1]

Constraints:
- The number of nodes in the list is sz.
- 1 <= sz <= 30
- 0 <= Node.val <= 100
- 1 <= n <= sz

Follow up: Could you do this in one pass?
"""

from typing import Optional
from interview_workbook.leetcode._registry import register_problem


# Definition for singly-linked list node
class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode({self.val})"


class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        """
        Remove nth node from end using two-pointer technique (one pass).

        Time: O(L) where L is the length of the list
        Space: O(1)

        Algorithm:
        1. Use dummy node to handle edge cases (removing first node)
        2. Use two pointers with n+1 gap between them
        3. Move both pointers until fast reaches end
        4. Slow pointer will be at the node before the target
        5. Remove the target node by adjusting pointers
        """
        # Dummy node simplifies edge cases
        dummy = ListNode(0)
        dummy.next = head

        # Initialize two pointers
        slow = dummy
        fast = dummy

        # Move fast pointer n+1 steps ahead
        # This creates a gap of n+1 nodes between slow and fast
        for _ in range(n + 1):
            fast = fast.next

        # Move both pointers until fast reaches end
        # Slow will be at the node before the target
        while fast:
            slow = slow.next
            fast = fast.next

        # Remove the nth node from end
        slow.next = slow.next.next

        return dummy.next

    def removeNthFromEndTwoPass(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        """
        Two-pass solution: first pass to count, second pass to remove.

        Time: O(L)
        Space: O(1)
        """
        # First pass: count total nodes
        length = 0
        curr = head
        while curr:
            length += 1
            curr = curr.next

        # Edge case: remove first node
        if length == n:
            return head.next

        # Second pass: find the node before target
        curr = head
        for _ in range(length - n - 1):
            curr = curr.next

        # Remove the target node
        curr.next = curr.next.next

        return head

    def removeNthFromEndRecursive(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        """
        Recursive solution that counts from the end.

        Time: O(L)
        Space: O(L) due to recursion stack
        """

        def helper(node: Optional[ListNode]) -> int:
            """Returns the position from end (1-indexed)"""
            if not node:
                return 0

            pos = helper(node.next) + 1

            # If this is the node before target, remove target
            if pos == n + 1:
                node.next = node.next.next

            return pos

        # Handle edge case: removing first node
        dummy = ListNode(0)
        dummy.next = head
        helper(dummy)
        return dummy.next


def create_linked_list(values: list[int]) -> Optional[ListNode]:
    """Helper function to create a linked list from a list of values."""
    if not values:
        return None

    head = ListNode(values[0])
    curr = head

    for val in values[1:]:
        curr.next = ListNode(val)
        curr = curr.next

    return head


def linked_list_to_list(head: Optional[ListNode]) -> list[int]:
    """Helper function to convert a linked list to a list of values."""
    result = []
    curr = head

    while curr:
        result.append(curr.val)
        curr = curr.next

    return result


def demo():
    """Demo of Remove Nth Node From End of List."""
    solution = Solution()

    test_cases = [
        {
            "values": [1, 2, 3, 4, 5],
            "n": 2,
            "expected": [1, 2, 3, 5],
            "description": "Example 1: remove 2nd from end",
        },
        {"values": [1], "n": 1, "expected": [], "description": "Example 2: remove only node"},
        {"values": [1, 2], "n": 1, "expected": [1], "description": "Example 3: remove last node"},
        {"values": [1, 2], "n": 2, "expected": [2], "description": "Remove first node of two"},
        {
            "values": [1, 2, 3, 4, 5],
            "n": 1,
            "expected": [1, 2, 3, 4],
            "description": "Remove last node",
        },
        {
            "values": [1, 2, 3, 4, 5],
            "n": 5,
            "expected": [2, 3, 4, 5],
            "description": "Remove first node",
        },
        {"values": [1, 2, 3], "n": 2, "expected": [1, 3], "description": "Remove middle node"},
    ]

    print("=== LeetCode 19: Remove Nth Node From End of List ===\n")

    for i, test in enumerate(test_cases, 1):
        values = test["values"]
        n = test["n"]
        expected = test["expected"]
        description = test["description"]

        print(f"Test Case {i}:")
        print(f"Description: {description}")
        print(f"Input: {values}, n = {n}")
        print(f"Expected: {expected}")

        # Test one-pass solution
        head1 = create_linked_list(values)
        result_head1 = solution.removeNthFromEnd(head1, n)
        result_values1 = linked_list_to_list(result_head1)
        print(f"Result (One-pass): {result_values1}")
        status1 = "✓ PASS" if result_values1 == expected else "✗ FAIL"
        print(f"Status: {status1}")

        # Test two-pass solution
        head2 = create_linked_list(values)
        result_head2 = solution.removeNthFromEndTwoPass(head2, n)
        result_values2 = linked_list_to_list(result_head2)
        print(f"Result (Two-pass): {result_values2}")
        status2 = "✓ PASS" if result_values2 == expected else "✗ FAIL"

        # Test recursive solution
        head3 = create_linked_list(values)
        result_head3 = solution.removeNthFromEndRecursive(head3, n)
        result_values3 = linked_list_to_list(result_head3)
        print(f"Result (Recursive): {result_values3}")
        print()


if __name__ == "__main__":
    demo()


# Register the problem
register_problem(
    id="19",
    title="Remove Nth Node From End of List",
    difficulty="Medium",
    category="Linked List",
    url="https://leetcode.com/problems/remove-nth-node-from-end-of-list/",
    tags=["Linked List", "Two Pointers"],
)
