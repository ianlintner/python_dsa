"""
LeetCode 155: Min Stack

Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

Implement the MinStack class:
- MinStack() initializes the stack object.
- void push(int val) pushes the element val onto the stack.
- void pop() removes the element on the top of the stack.
- int top() gets the top element of the stack.
- int getMin() retrieves the minimum element in the stack.

You must implement a solution with O(1) time complexity for each function.

URL: https://leetcode.com/problems/min-stack/
Difficulty: Easy
Category: Stack

Patterns:
- Stack design pattern
- Auxiliary stack for tracking minimums

Complexity:
- Time: O(1) for all operations
- Space: O(n) where n is the number of elements

Pitfalls:
- Need to handle the case where the minimum element is popped
- Must maintain the minimum efficiently after each pop operation

Follow-ups:
- How would you implement this with a single stack?
- Can you optimize space usage when there are many duplicate minimums?
"""

from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._runner import TestCase, create_demo_output, run_test_cases
from interview_workbook.leetcode._types import Category, Difficulty


class MinStack:
    def __init__(self):
        """
        Initialize the MinStack data structure.
        Uses two stacks: main stack for elements, min stack for tracking minimums.
        """
        self.stack = []      # Main stack to store all elements
        self.min_stack = []  # Stack to store minimum values at each level

    def push(self, val: int) -> None:
        """
        Push element val onto stack.
        
        Args:
            val: Integer value to push
        """
        self.stack.append(val)
        
        # Push onto min_stack if it's empty or val is <= current minimum
        # We use <= to handle duplicates correctly
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self) -> None:
        """
        Remove the element on top of the stack.
        """
        if not self.stack:
            return
        
        # If the popped element was the minimum, also pop from min_stack
        popped = self.stack.pop()
        if self.min_stack and popped == self.min_stack[-1]:
            self.min_stack.pop()

    def top(self) -> int:
        """
        Get the top element of the stack.
        
        Returns:
            The top element of the stack
        """
        return self.stack[-1] if self.stack else None

    def getMin(self) -> int:
        """
        Retrieve the minimum element in the stack.
        
        Returns:
            The minimum element in the stack
        """
        return self.min_stack[-1] if self.min_stack else None


class Solution:
    def test_min_stack_operations(self, operations: list, values: list) -> list:
        """
        Test MinStack with a sequence of operations.
        
        Args:
            operations: List of operation names
            values: List of values for each operation (None for operations without values)
            
        Returns:
            List of results for operations that return values
        """
        min_stack = MinStack()
        results = []
        
        for i, op in enumerate(operations):
            if op == "MinStack":
                results.append(None)
            elif op == "push":
                min_stack.push(values[i])
                results.append(None)
            elif op == "pop":
                min_stack.pop()
                results.append(None)
            elif op == "top":
                results.append(min_stack.top())
            elif op == "getMin":
                results.append(min_stack.getMin())
        
        return results


# Test cases
test_cases = [
    TestCase(
        (["MinStack", "push", "push", "push", "getMin", "pop", "top", "getMin"],
         [None, -2, 0, -3, None, None, None, None]),
        [None, None, None, None, -3, None, 0, -2],
        "Basic operations example"
    ),
    TestCase(
        (["MinStack", "push", "push", "getMin", "getMin", "push", "getMin", "getMin", "top", "getMin", "pop", "getMin"],
         [None, 2, 0, None, None, 3, None, None, None, None, None, None]),
        [None, None, None, 0, 0, None, 0, 0, 3, 0, None, 0],
        "Multiple getMin calls"
    ),
    TestCase(
        (["MinStack", "push", "push", "push", "top", "pop", "getMin", "pop", "getMin", "pop", "push", "top", "getMin", "push", "top", "getMin", "pop", "getMin"],
         [None, 1, 2, 1, None, None, None, None, None, None, 1, None, None, -1, None, None, None, None]),
        [None, None, None, None, 1, None, 1, None, 1, None, None, 1, 1, None, -1, -1, None, 1],
        "Complex sequence with duplicates"
    ),
    TestCase(
        (["MinStack", "push", "getMin", "push", "getMin", "push", "getMin"],
         [None, 5, None, 3, None, 1, None]),
        [None, None, 5, None, 3, None, 1],
        "Decreasing sequence"
    ),
    TestCase(
        (["MinStack", "push", "getMin", "push", "getMin", "push", "getMin"],
         [None, 1, None, 3, None, 5, None]),
        [None, None, 1, None, 1, None, 1],
        "Increasing sequence - minimum stays same"
    ),
    TestCase(
        (["MinStack", "push", "push", "push", "getMin", "pop", "pop", "pop"],
         [None, 1, 1, 1, None, None, None, None]),
        [None, None, None, None, 1, None, None, None],
        "All elements are the same"
    ),
    TestCase(
        (["MinStack", "push", "top", "getMin"],
         [None, -1, None, None]),
        [None, None, -1, -1],
        "Single element"
    ),
    TestCase(
        (["MinStack", "push", "push", "getMin", "pop", "getMin"],
         [None, 0, 1, None, None, None]),
        [None, None, None, 0, None, 0],
        "Minimum not affected by pop"
    ),
    TestCase(
        (["MinStack", "push", "push", "getMin", "pop", "getMin"],
         [None, 1, 0, None, None, None]),
        [None, None, None, 0, None, 1],
        "Minimum changes after pop"
    ),
    TestCase(
        (["MinStack", "push", "push", "push", "push", "pop", "pop", "pop", "pop"],
         [None, 2147483646, 2147483646, 2147483647, 2147483647, None, None, None, None]),
        [None, None, None, None, None, None, None, None, None],
        "Large numbers edge case"
    ),
]


def demo() -> str:
    """Run Min Stack demo with test cases."""
    solution = Solution()

    test_results = run_test_cases(solution.test_min_stack_operations, test_cases, "LeetCode 155: Min Stack")

    return create_demo_output(
        "Min Stack",
        test_results,
        time_complexity="O(1)",
        space_complexity="O(n)",
        approach_notes="""
Key insights:
1. Use two stacks: main stack for all elements, min_stack for tracking minimums
2. When pushing: add to min_stack only if value <= current minimum (handles duplicates)
3. When popping: remove from min_stack only if popped value equals current minimum
4. This ensures all operations remain O(1) while correctly maintaining the minimum
        """.strip(),
    )


# Register the problem
register_problem(
    id=155,
    slug="min_stack",
    title="Min Stack",
    category=Category.STACK,
    difficulty=Difficulty.EASY,
    tags=['stack', 'design'],
    url="https://leetcode.com/problems/min-stack/",
    notes="Classic stack design problem using auxiliary stack to track minimums in O(1) time",
)
