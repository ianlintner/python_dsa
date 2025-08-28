"""
LeetCode 621: Task Scheduler

You are given an array of CPU tasks, each represented by letters A to Z, and a cooling time, n. 
Each cycle, the CPU can complete a task or be idle. Tasks can be completed in any order, 
but there's a constraint: identical tasks must be separated by at least n intervals due to cooling time.

Return the minimum number of intervals required to complete all tasks.

Examples:
    Input: tasks = ["A","A","A","B","B","B"], n = 2
    Output: 8
    Explanation: A -> B -> idle -> A -> B -> idle -> A -> B

    Input: tasks = ["A","A","A","B","B","B"], n = 0
    Output: 6
    Explanation: No cooling time, so tasks can be completed immediately

    Input: tasks = ["A","A","A","A","A","A","B","C","D","E","F","G"], n = 2  
    Output: 16

Constraints:
    1 <= tasks.length <= 10^4
    tasks[i] is an uppercase English letter.
