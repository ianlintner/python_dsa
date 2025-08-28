"""
LeetCode 2: Add Two Numbers

You are given two non-empty linked lists representing two non-negative integers.
The digits are stored in reverse order, and each of their nodes contains a single digit.
Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.

Example 1:
Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
Explanation: 342 + 465 = 807.

Example 2:
Input: l1 = [0], l2 = [0]
Output: [0]

Example 3:
Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
Output: [8,9,9,9,0,0,0,1]

Constraints:
- The number of nodes in each linked list is in the range [1, 100]
- 0 <= Node.val <= 9
- It is guaranteed that the list represents a number that does not have leading zeros
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
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        """
        Add two numbers represented as linked lists.

        Time: O(max(m, n)) where m, n are lengths of the two lists
        Space: O(max(m, n)) for the result list

        Algorithm:
        1. Use dummy node to simplify result construction
        2. Iterate through both lists simultaneously
        3. Add corresponding digits plus carry from previous addition
        4. Handle carry and create new node for each digit
        5. Continue until both lists are exhausted and no carry remains
        """
        # Dummy node to simplify result construction
        dummy = ListNode(0)
        current = dummy
        carry = 0

        # Process both lists and carry
        while l1 or l2 or carry:
            # Get values from current nodes (0 if node is None)
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0

            # Calculate sum and new carry
            total = val1 + val2 + carry
            carry = total // 10
            digit = total % 10

            # Create new node with the digit
            current.next = ListNode(digit)
            current = current.next

            # Move to next nodes (if they exist)
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None

        return dummy.next

    def addTwoNumbersRecursive(
        self, l1: Optional[ListNode], l2: Optional[ListNode], carry: int = 0
    ) -> Optional[ListNode]:
        """
        Recursive solution for adding two numbers.

        Time: O(max(m, n))
        Space: O(max(m, n)) due to recursion stack
        """
        # Base case: no more nodes and no carry
        if not l1 and not l2 and carry == 0:
            return None

        # Get values from current nodes
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0

        # Calculate sum and carry
        total = val1 + val2 + carry
        new_carry = total // 10
        digit = total % 10

        # Create current node and recursively build next node
        result = ListNode(digit)
        next_l1 = l1.next if l1 else None
        next_l2 = l2.next if l2 else None
        result.next = self.addTwoNumbersRecursive(next_l1, next_l2, new_carry)

        return result

    def addTwoNumbersSimplified(
        self, l1: Optional[ListNode], l2: Optional[ListNode]
    ) -> Optional[ListNode]:
        """
        Simplified version with cleaner code structure.

        Time: O(max(m, n))
        Space: O(max(m, n))
        """
        dummy = ListNode(0)
        current = dummy
        carry = 0

        while l1 or l2 or carry:
            total = carry

            if l1:
                total += l1.val
                l1 = l1.next

            if l2:
                total += l2.val
                l2 = l2.next

            current.next = ListNode(total % 10)
            current = current.next
            carry = total // 10

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


def list_to_number(values: list[int]) -> int:
    """Convert list of digits (reverse order) to actual number."""
    if not values:
        return 0

    number = 0
    for i, digit in enumerate(values):
        number += digit * (10**i)
    return number


def number_to_list(number: int) -> list[int]:
    """Convert number to list of digits in reverse order."""
    if number == 0:
        return [0]

    digits = []
    while number > 0:
        digits.append(number % 10)
        number //= 10
    return digits


def demo():
    """Demo of Add Two Numbers."""
    solution = Solution()

    test_cases = [
        {
            "l1": [2, 4, 3],
            "l2": [5, 6, 4],
            "expected": [7, 0, 8],
            "description": "Example 1: 342 + 465 = 807",
        },
        {"l1": [0], "l2": [0], "expected": [0], "description": "Example 2: 0 + 0 = 0"},
        {
            "l1": [9, 9, 9, 9, 9, 9, 9],
            "l2": [9, 9, 9, 9],
            "expected": [8, 9, 9, 9, 0, 0, 0, 1],
            "description": "Example 3: 9999999 + 9999 = 10009998",
        },
        {"l1": [1], "l2": [9, 9], "expected": [0, 0, 1], "description": "1 + 99 = 100"},
        {
            "l1": [9],
            "l2": [1, 9, 9, 9, 9, 9, 9, 9, 9, 9],
            "expected": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "description": "9 + 9999999991 = 10000000000",
        },
        {"l1": [5], "l2": [5], "expected": [0, 1], "description": "5 + 5 = 10"},
    ]

    print("=== LeetCode 2: Add Two Numbers ===\n")

    for i, test in enumerate(test_cases, 1):
        l1_vals = test["l1"]
        l2_vals = test["l2"]
        expected = test["expected"]
        description = test["description"]

        print(f"Test Case {i}:")
        print(f"Description: {description}")
        print(f"L1: {l1_vals} (represents {list_to_number(l1_vals)})")
        print(f"L2: {l2_vals} (represents {list_to_number(l2_vals)})")
        print(f"Expected: {expected} (represents {list_to_number(expected)})")

        # Test iterative solution
        head1 = create_linked_list(l1_vals)
        head2 = create_linked_list(l2_vals)
        result_head1 = solution.addTwoNumbers(head1, head2)
        result_values1 = linked_list_to_list(result_head1)
        print(f"Result (Iterative): {result_values1}")
        status1 = "✓ PASS" if result_values1 == expected else "✗ FAIL"
        print(f"Status: {status1}")

        # Test recursive solution
        head1 = create_linked_list(l1_vals)
        head2 = create_linked_list(l2_vals)
        result_head2 = solution.addTwoNumbersRecursive(head1, head2)
        result_values2 = linked_list_to_list(result_head2)
        print(f"Result (Recursive): {result_values2}")
        status2 = "✓ PASS" if result_values2 == expected else "✗ FAIL"

        # Test simplified solution
        head1 = create_linked_list(l1_vals)
        head2 = create_linked_list(l2_vals)
        result_head3 = solution.addTwoNumbersSimplified(head1, head2)
        result_values3 = linked_list_to_list(result_head3)
        print(f"Result (Simplified): {result_values3}")

        # Verify arithmetic
        num1 = list_to_number(l1_vals)
        num2 = list_to_number(l2_vals)
        expected_num = list_to_number(expected)
        actual_sum = num1 + num2
        print(f"Verification: {num1} + {num2} = {actual_sum} (expected {expected_num})")
        print()


if __name__ == "__main__":
    demo()


# Register the problem
register_problem(
    id="2",
    title="Add Two Numbers",
    difficulty="Medium",
    category="Linked List",
    url="https://leetcode.com/problems/add-two-numbers/",
    tags=["Linked List", "Math", "Recursion"],
)
