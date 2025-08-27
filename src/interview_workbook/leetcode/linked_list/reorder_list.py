"""
LeetCode 143: Reorder List

You are given the head of a singly linked-list. The list can be represented as:

L0 → L1 → … → Ln - 1 → Ln

Reorder the list to be on the following form:

L0 → Ln → L1 → Ln - 1 → L2 → Ln - 2 → …

You may not modify the values in the list's nodes. Only nodes themselves may be changed.

Example 1:
Input: head = [1,2,3,4]
Output: [1,4,2,3]

Example 2:
Input: head = [1,2,3,4,5]
Output: [1,5,2,4,3]

Constraints:
- The number of nodes in the list is in the range [1, 5 * 10^4]
- 1 <= Node.val <= 1000
"""

from typing import Optional
from interview_workbook.leetcode._registry import register_problem


# Definition for singly-linked list node
class ListNode:
    def __init__(self, val: int = 0, next: Optional['ListNode'] = None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode({self.val})"


class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        """
        Reorder list in-place using three-step approach.
        
        Time: O(n)
        Space: O(1)
        
        Algorithm:
        1. Find the middle of the list using slow/fast pointers
        2. Reverse the second half of the list
        3. Merge the first half and reversed second half alternately
        
        Do not return anything, modify head in-place instead.
        """
        if not head or not head.next:
            return
        
        # Step 1: Find middle using slow/fast pointers
        slow = fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        
        # Step 2: Reverse the second half
        second_half = slow.next
        slow.next = None  # Split the list
        second_half = self._reverse_list(second_half)
        
        # Step 3: Merge first half and reversed second half
        first_half = head
        while second_half:  # second_half might be shorter
            # Save next nodes
            temp1 = first_half.next
            temp2 = second_half.next
            
            # Link alternately
            first_half.next = second_half
            second_half.next = temp1
            
            # Move to next pair
            first_half = temp1
            second_half = temp2
    
    def _reverse_list(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """Helper function to reverse a linked list."""
        prev = None
        curr = head
        
        while curr:
            next_temp = curr.next
            curr.next = prev
            prev = curr
            curr = next_temp
        
        return prev
    
    def reorderListStack(self, head: Optional[ListNode]) -> None:
        """
        Alternative approach using stack (uses extra space).
        
        Time: O(n)
        Space: O(n)
        """
        if not head or not head.next:
            return
        
        # Store all nodes in a list for easy access
        nodes = []
        curr = head
        while curr:
            nodes.append(curr)
            curr = curr.next
        
        # Reorder using two pointers
        left, right = 0, len(nodes) - 1
        
        while left < right:
            # Connect left to right
            nodes[left].next = nodes[right]
            left += 1
            
            if left == right:
                break
            
            # Connect right to next left
            nodes[right].next = nodes[left]
            right -= 1
        
        # End the list
        nodes[left].next = None
    
    def reorderListDeque(self, head: Optional[ListNode]) -> None:
        """
        Another approach using deque for educational purposes.
        
        Time: O(n)
        Space: O(n)
        """
        from collections import deque
        
        if not head or not head.next:
            return
        
        # Store nodes in deque
        dq = deque()
        curr = head
        while curr:
            dq.append(curr)
            curr = curr.next
        
        # Build reordered list
        dummy = ListNode(0)
        current = dummy
        take_from_left = True
        
        while dq:
            if take_from_left:
                node = dq.popleft()
            else:
                node = dq.pop()
            
            current.next = node
            current = node
            take_from_left = not take_from_left
        
        # End the list
        current.next = None


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
    """Demo of Reorder List."""
    solution = Solution()
    
    test_cases = [
        {
            "values": [1, 2, 3, 4],
            "expected": [1, 4, 2, 3],
            "description": "Example 1: even number of nodes"
        },
        {
            "values": [1, 2, 3, 4, 5],
            "expected": [1, 5, 2, 4, 3],
            "description": "Example 2: odd number of nodes"
        },
        {
            "values": [1],
            "expected": [1],
            "description": "Single node"
        },
        {
            "values": [1, 2],
            "expected": [1, 2],
            "description": "Two nodes"
        },
        {
            "values": [1, 2, 3],
            "expected": [1, 3, 2],
            "description": "Three nodes"
        },
        {
            "values": [1, 2, 3, 4, 5, 6],
            "expected": [1, 6, 2, 5, 3, 4],
            "description": "Six nodes"
        },
    ]
    
    print("=== LeetCode 143: Reorder List ===\n")
    
    for i, test in enumerate(test_cases, 1):
        values = test["values"]
        expected = test["expected"]
        description = test["description"]
        
        print(f"Test Case {i}:")
        print(f"Description: {description}")
        print(f"Input: {values}")
        print(f"Expected: {expected}")
        
        # Test main solution (in-place)
        head1 = create_linked_list(values)
        solution.reorderList(head1)
        result_values1 = linked_list_to_list(head1)
        print(f"Result (In-place): {result_values1}")
        status1 = "✓ PASS" if result_values1 == expected else "✗ FAIL"
        print(f"Status: {status1}")
        
        # Test stack solution
        head2 = create_linked_list(values)
        solution.reorderListStack(head2)
        result_values2 = linked_list_to_list(head2)
        print(f"Result (Stack): {result_values2}")
        status2 = "✓ PASS" if result_values2 == expected else "✗ FAIL"
        
        # Test deque solution
        head3 = create_linked_list(values)
        solution.reorderListDeque(head3)
        result_values3 = linked_list_to_list(head3)
        print(f"Result (Deque): {result_values3}")
        print()


if __name__ == "__main__":
    demo()


# Register the problem
register_problem(
    id="143",
    title="Reorder List",
    difficulty="Medium",
    category="Linked List",
    url="https://leetcode.com/problems/reorder-list/",
    tags=["Linked List", "Two Pointers", "Stack", "Recursion"]
)
