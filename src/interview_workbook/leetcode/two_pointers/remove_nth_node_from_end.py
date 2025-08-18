"""
Remove Nth Node From End of List - LeetCode Problem

Given the head of a linked list, remove the nth node from the end of the list and return its head.
"""

from typing import Optional
from .._registry import register_problem
from .._runner import TestCase, run_test_cases, create_demo_output
from .._types import Category, Difficulty


# Definition for singly-linked list
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    
    def __eq__(self, other):
        """Compare two linked lists for equality."""
        if not isinstance(other, ListNode):
            return False
        current1, current2 = self, other
        while current1 and current2:
            if current1.val != current2.val:
                return False
            current1, current2 = current1.next, current2.next
        return current1 is None and current2 is None
    
    def __repr__(self):
        """String representation of linked list."""
        values = []
        current = self
        while current:
            values.append(str(current.val))
            current = current.next
        return " -> ".join(values)


class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        """
        Remove nth node from end using two pointers technique.
        
        Time Complexity: O(L) - where L is length of linked list
        Space Complexity: O(1) - only using pointer variables
        
        Args:
            head: Head of the linked list
            n: Position from end to remove (1-indexed)
            
        Returns:
            Optional[ListNode]: Head of modified linked list
        """
        # Create a dummy node to handle edge case where head is removed
        dummy = ListNode(0)
        dummy.next = head
        
        # Use two pointers with n+1 gap between them
        slow = fast = dummy
        
        # Move fast pointer n+1 steps ahead
        for _ in range(n + 1):
            fast = fast.next
        
        # Move both pointers until fast reaches the end
        while fast:
            slow = slow.next
            fast = fast.next
        
        # Remove the nth node from end
        slow.next = slow.next.next
        
        return dummy.next
    
    def removeNthFromEndTwoPass(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        """
        Alternative two-pass approach.
        
        Time Complexity: O(L) - two passes through the list
        Space Complexity: O(1) - constant extra space
        """
        # First pass: count total nodes
        length = 0
        current = head
        while current:
            length += 1
            current = current.next
        
        # Handle edge case: remove head node
        if length == n:
            return head.next
        
        # Second pass: find the node before the one to remove
        current = head
        for _ in range(length - n - 1):
            current = current.next
        
        # Remove the nth node from end
        current.next = current.next.next
        
        return head


def create_linked_list(values):
    """Helper function to create linked list from list of values."""
    if not values:
        return None
    
    head = ListNode(values[0])
    current = head
    for val in values[1:]:
        current.next = ListNode(val)
        current = current.next
    
    return head


def linked_list_to_list(head):
    """Helper function to convert linked list to list of values."""
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.next
    return result


def demo():
    """Demonstrate Remove Nth Node From End solution with test cases."""
    solution = Solution()
    
    test_cases = [
        TestCase(
            input_args=(create_linked_list([1, 2, 3, 4, 5]), 2), 
            expected=[1, 2, 3, 5],
            description="Remove 2nd node from end"
        ),
        TestCase(
            input_args=(create_linked_list([1]), 1), 
            expected=[],
            description="Remove only node"
        ),
        TestCase(
            input_args=(create_linked_list([1, 2]), 1), 
            expected=[1],
            description="Remove last node"
        ),
        TestCase(
            input_args=(create_linked_list([1, 2]), 2), 
            expected=[2],
            description="Remove first node"
        ),
        TestCase(
            input_args=(create_linked_list([1, 2, 3, 4, 5, 6]), 6), 
            expected=[2, 3, 4, 5, 6],
            description="Remove head node"
        ),
        TestCase(
            input_args=(create_linked_list([1, 2, 3, 4, 5, 6]), 1), 
            expected=[1, 2, 3, 4, 5],
            description="Remove tail node"
        ),
        TestCase(
            input_args=(create_linked_list([1, 2, 3, 4, 5, 6]), 3), 
            expected=[1, 2, 3, 5, 6],
            description="Remove middle node"
        ),
    ]
    
    results = []
    for i, test_case in enumerate(test_cases):
        try:
            import time
            start_time = time.perf_counter()
            
            # Execute the solution
            result_head = solution.removeNthFromEnd(*test_case.input_args)
            actual = linked_list_to_list(result_head)
            
            end_time = time.perf_counter()
            
            passed = actual == test_case.expected
            results.append({
                'test_case': i + 1,
                'description': test_case.description,
                'input': f"List: {linked_list_to_list(test_case.input_args[0])}, n: {test_case.input_args[1]}",
                'expected': test_case.expected,
                'actual': actual,
                'passed': passed,
                'time_ms': (end_time - start_time) * 1000
            })
        except Exception as e:
            results.append({
                'test_case': i + 1,
                'description': test_case.description,
                'input': f"List: {linked_list_to_list(test_case.input_args[0]) if test_case.input_args[0] else []}, n: {test_case.input_args[1]}",
                'expected': test_case.expected,
                'actual': f"Error: {str(e)}",
                'passed': False,
                'time_ms': 0
            })
    
    return create_demo_output(
        title="Remove Nth Node From End of List",
        description="Remove nth node from end using two pointers technique",
        results=results,
        complexity_analysis={
            "time": "O(L) - single pass through linked list where L is length",
            "space": "O(1) - only using pointer variables"
        },
        key_insights=[
            "Two pointers maintain n+1 gap to find node before target",
            "Dummy node simplifies edge case handling (removing head)",
            "Fast pointer moves n+1 steps ahead, then both move together",
            "When fast reaches end, slow is at node before target"
        ],
        common_pitfalls=[
            "Handle edge case where head node needs to be removed",
            "Remember n is 1-indexed (1st from end is last node)",
            "Use dummy node to avoid special cases",
            "Ensure fast pointer moves n+1 steps, not n steps"
        ],
        follow_up_questions=[
            "What if n is larger than the list length?",
            "How would you handle doubly linked lists?",
            "Can you solve without knowing the list length?",
            "What about removing multiple nodes from end?"
        ]
    )


# Register this problem
register_problem(
    id=19,
    slug="remove-nth-node-from-end-of-list",
    title="Remove Nth Node From End of List",
    category=Category.TWO_POINTERS,
    difficulty=Difficulty.MEDIUM,
    tags={"linked-list", "two-pointers"},
    module="src.interview_workbook.leetcode.two_pointers.remove_nth_node_from_end",
    url="https://leetcode.com/problems/remove-nth-node-from-end-of-list/",
    notes="Two pointers technique for linked list manipulation in single pass"
)
