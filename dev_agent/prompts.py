# prompts.py

TASK_PLANNER_PROMPT = """
You are a software engineering assistant.

User requirement:
{requirement}

Please analyze and output a JSON with the following fields:
- task_type
- language
- steps
"""

CODE_GEN_PROMPT = """
You are a professional Python developer.

Task:
{task}

Function signature:
{signature}

Requirements:
- Correctness first
- Handle edge cases
- Do NOT include test code
Return ONLY the function implementation.
"""

TEST_GEN_PROMPT = """
Given the following function specification and implementation,
generate Python test cases using assert statements.

Specification:
{task}

Code:
{code}

Focus on:
- Typical cases
- Edge cases
- Corner cases

Return ONLY test code.
"""

BUG_FIX_PROMPT = """
The following Python code fails some tests.

Code:
{code}

Error message:
{error}

Please:
1. Analyze the root cause
2. Fix the bug

Return ONLY the corrected code.
"""

REFLECTION_PROMPT = """
The previous attempt failed.

Error:
{error}

Please reflect:
- Why did it fail?
- What assumption was wrong?
- How can it be improved?
"""
