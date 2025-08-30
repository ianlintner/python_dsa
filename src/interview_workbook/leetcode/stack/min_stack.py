"""
Min Stack

TODO: Add problem description
"""


class Solution:
    def solve(self, operations, values):
        """Execute operations on MinStack and return results list."""

        class MinStack:
            def __init__(self):
                self.stack = []
                self.min_stack = []

            def push(self, val):
                self.stack.append(val)
                if not self.min_stack or val <= self.min_stack[-1]:
                    self.min_stack.append(val)
                else:
                    self.min_stack.append(self.min_stack[-1])

            def pop(self):
                self.stack.pop()
                self.min_stack.pop()

            def top(self):
                return self.stack[-1]

            def get_min(self):
                return self.min_stack[-1]

        obj = None
        res = []
        for op, val in zip(operations, values):
            if op == "MinStack":
                obj = MinStack()
                res.append(None)
            elif op == "push":
                obj.push(val[0])
                res.append(None)
            elif op == "pop":
                obj.pop()
                res.append(None)
            elif op == "top":
                res.append(obj.top())
            elif op == "getMin":
                res.append(obj.get_min())
        return res


def demo():
    ops = ["MinStack", "push", "push", "push", "getMin", "pop", "top", "getMin"]
    vals = [[], [-2], [0], [-3], [], [], [], []]
    return str(Solution().solve(ops, vals))


from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._types import Category, Difficulty

register_problem(
    id=155,
    slug="min_stack",
    title="Min Stack",
    category=Category.STACK,
    difficulty=Difficulty.MEDIUM,
    tags=["stack", "design"],
    url="https://leetcode.com/problems/min-stack/",
    notes="Maintain two stacks: values and running mins.",
)
