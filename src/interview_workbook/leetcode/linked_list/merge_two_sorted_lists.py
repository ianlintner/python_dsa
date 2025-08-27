"""
LeetCode 21: Merge Two Sorted Lists

You are given the heads of two sorted linked lists list1 and list2.

Merge the two lists in a one sorted list. The list should be made by splicing 
together the nodes of the first two lists.

Return the head of the merged linked list.

Example 1:
Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]

Example 2:
Input: list1 = [], list2 = []
Output: []

Example 3:
Input: list1 = [], list2 = [0]
Output: [0]

Constraints:
- The number of nodes in both lists is in the range [0, 50]
- -100 <= Node.val <= 100
- Both list1 and list2 are sorted in non-decreasing order
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
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        """
        Merge two sorted lists iteratively using dummy node.
        
        Time: O(m + n) where m, n are lengths of the two lists
        Space: O(1) - only use constant extra space
        
        Algorithm:
        1. Create dummy node to simplify edge cases
        2. Use two pointers to compare nodes from both lists
        3. Always append the smaller node to result
        4. Handle remaining nodes from non-empty list
        """
        # Create dummy node to simplify logic
        dummy = ListNode(0)
        current = dummy
        
        # Merge while both lists have nodes
        while list1 and list2:
            if list1.val <= list2.val:
                current.next = list1
                list1 = list1.next
            else:
                current.next = list2
                list2 = list2.next
            current = current.next
        
        # Append remaining nodes (at most one list is non-empty)
        current.next = list1 if list1 else list2
        
        return dummy.next
    
    def mergeTwoListsRecursive(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        """
        Merge two sorted lists recursively.
        
        Time: O(m + n)
        Space: O(m + n) - recursion stack depth
        
        Algorithm:
        1. Base case: if one list is empty, return the other
        2. Compare heads: choose smaller as new head
        3. Recursively merge remaining with the other list
        """
        # Base cases
        if not list1:
            return list2
        if not list2:
            return list1
        
        # Choose smaller head and recursively merge
        if list1.val <= list2.val:
            list1.next = self.mergeTwoListsRecursive(list1.next, list2)
            return list1
        else:
            list2.next = self.mergeTwoListsRecursive(list1, list2.next)
            return list2
    
    def mergeTwoListsInPlace(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        """
        Merge without dummy node (slightly more complex but saves one node).
        
        Time: O(m + n)
        Space: O(1)
        """
        if not list1:
            return list2
        if not list2:
            return list1
        
        # Determine the head of merged list
        if list1.val <= list2.val:
            head = list1
            list1 = list1.next
        else:
            head = list2
            list2 = list2.next
        
        current = head
        
        # Merge remaining nodes
        while list1 and list2:
            if list1.val <= list2.val:
                current.next = list1
                list1 = list1.next
            else:
                current.next = list2
                list2 = list2.next
            current = current.next
        
        # Append remaining nodes
        current.next = list1 if list1 else list2
        
        return head


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
    """Demo of Merge Two Sorted Lists."""
    solution = Solution()
    
    test_cases = [
        {
            "list1": [1, 2, 4],
            "list2": [1, 3, 4],
            "expected": [1, 1, 2, 3, 4, 4],
            "description": "Example 1: both lists have elements"
        },
        {
            "list1": [],
            "list2": [],
            "expected": [],
            "description": "Example 2: both lists empty"
        },
        {
            "list1": [],
            "list2": [0],
            "expected": [0],
            "description": "Example 3: first list empty"
        },
        {
            "list1": [1, 2, 3],
            "list2": [],
            "expected": [1, 2, 3],
            "description": "Second list empty"
        },
        {
            "list1": [1],
            "list2": [2],
            "expected": [1, 2],
            "description": "Single element lists"
        },
        {
            "list1": [1, 3, 5],
            "list2": [2, 4, 6],
            "expected": [1, 2, 3, 4, 5, 6],
            "description": "Interleaving elements"
        },
        {
            "list1": [-10, -5, 0],
            "list2": [-8, -2, 5],
            "expected": [-10, -8, -5, -2, 0, 5],
            "description": "Negative numbers"
        },
    ]
    
    print("=== LeetCode 21: Merge Two Sorted Lists ===\n")
    
    for i, test in enumerate(test_cases, 1):
        list1_vals = test["list1"]
        list2_vals = test["list2"]
        expected = test["expected"]
        description = test["description"]
        
        print(f"Test Case {i}:")
        print(f"Description: {description}")
        print(f"List1: {list1_vals}")
        print(f"List2: {list2_vals}")
        print(f"Expected: {expected}")
        
        # Test iterative solution
        head1 = create_linked_list(list1_vals)
        head2 = create_linked_list(list2_vals)
        result1 = solution.mergeTwoLists(head1, head2)
        result_values1 = linked_list_to_list(result1)
        print(f"Result (Iterative): {result_values1}")
        status1 = "✓ PASS" if result_values1 == expected else "✗ FAIL"
        print(f"Status: {status1}")
        
        # Test recursive solution
        head1 = create_linked_list(list1_vals)
        head2 = create_linked_list(list2_vals)
        result2 = solution.mergeTwoListsRecursive(head1, head2)
        result_values2 = linked_list_to_list(result2)
        print(f"Result (Recursive): {result_values2}")
        status2 = "✓ PASS" if result_values2 == expected else "✗ FAIL"
        
        # Test in-place solution
        head1 = create_linked_list(list1_vals)
        head2 = create_linked_list(list2_vals)
        result3 = solution.mergeTwoListsInPlace(head1, head2)
        result_values3 = linked_list_to_list(result3)
        print(f"Result (In-place): {result_values3}")
        print()


if __name__ == "__main__":
    demo()


# Register the problem
register_problem(
    id="21",
    title="Merge Two Sorted Lists",
    difficulty="Easy",
    category="Linked List",
    url="https://leetcode.com/problems/merge-two-sorted-lists/",
    tags=["Linked List", "Recursion"]
)
