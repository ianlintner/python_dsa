"""
LeetCode 206: Reverse Linked List

Given the head of a singly linked list, reverse the list, and return the reversed list.

Example 1:
Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]

Example 2:
Input: head = [1,2]
Output: [2,1]

Example 3:
Input: head = []
Output: []

Constraints:
- The number of nodes in the list is in the range [0, 5000]
- -5000 <= Node.val <= 5000

Follow up: A linked list can be reversed either iteratively or recursively. Could you implement both?
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
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Reverse linked list iteratively.
        
        Time: O(n) - visit each node once
        Space: O(1) - only use constant extra space
        
        Algorithm:
        1. Use three pointers: prev, curr, next
        2. For each node: save next, reverse link, advance pointers
        3. Return prev when curr becomes None
        """
        prev = None
        curr = head
        
        while curr:
            # Save the next node before we lose it
            next_temp = curr.next
            
            # Reverse the link
            curr.next = prev
            
            # Move pointers forward
            prev = curr
            curr = next_temp
            
        return prev
    
    def reverseListRecursive(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Reverse linked list recursively.
        
        Time: O(n) - visit each node once
        Space: O(n) - recursion stack depth
        
        Algorithm:
        1. Base case: empty or single node returns itself
        2. Recursively reverse the rest of the list
        3. Reverse the current link and return new head
        """
        # Base case: empty list or single node
        if not head or not head.next:
            return head
            
        # Recursively reverse the rest of the list
        new_head = self.reverseListRecursive(head.next)
        
        # Reverse the current connection
        head.next.next = head
        head.next = None
        
        return new_head
    
    def reverseListThreePointer(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Alternative iterative approach with explicit three pointers.
        
        Time: O(n)
        Space: O(1)
        """
        if not head:
            return None
            
        prev, curr, next_node = None, head, head.next
        
        while curr:
            curr.next = prev
            prev = curr
            curr = next_node
            if next_node:
                next_node = next_node.next
                
        return prev


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
    """Demo of Reverse Linked List."""
    solution = Solution()
    
    test_cases = [
        {
            "values": [1, 2, 3, 4, 5],
            "expected": [5, 4, 3, 2, 1],
            "description": "Example 1: typical case"
        },
        {
            "values": [1, 2],
            "expected": [2, 1],
            "description": "Example 2: two nodes"
        },
        {
            "values": [],
            "expected": [],
            "description": "Example 3: empty list"
        },
        {
            "values": [1],
            "expected": [1],
            "description": "Single node"
        },
        {
            "values": [1, 2, 3],
            "expected": [3, 2, 1],
            "description": "Three nodes"
        },
    ]
    
    print("=== LeetCode 206: Reverse Linked List ===\n")
    
    for i, test in enumerate(test_cases, 1):
        values = test["values"]
        expected = test["expected"]
        description = test["description"]
        
        print(f"Test Case {i}:")
        print(f"Description: {description}")
        print(f"Input: {values}")
        print(f"Expected: {expected}")
        
        # Test iterative solution
        head1 = create_linked_list(values)
        result1 = solution.reverseList(head1)
        result_values1 = linked_list_to_list(result1)
        print(f"Result (Iterative): {result_values1}")
        status1 = "✓ PASS" if result_values1 == expected else "✗ FAIL"
        print(f"Status: {status1}")
        
        # Test recursive solution
        head2 = create_linked_list(values)
        result2 = solution.reverseListRecursive(head2)
        result_values2 = linked_list_to_list(result2)
        print(f"Result (Recursive): {result_values2}")
        status2 = "✓ PASS" if result_values2 == expected else "✗ FAIL"
        
        # Test three-pointer solution
        head3 = create_linked_list(values)
        result3 = solution.reverseListThreePointer(head3)
        result_values3 = linked_list_to_list(result3)
        print(f"Result (Three-pointer): {result_values3}")
        print()


if __name__ == "__main__":
    demo()


# Register the problem
register_problem(
    id="206",
    title="Reverse Linked List",
    difficulty="Easy",
    category="Linked List",
    url="https://leetcode.com/problems/reverse-linked-list/",
    tags=["Linked List", "Recursion"]
)
