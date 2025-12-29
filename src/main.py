# src/main.py 或临时脚本
from src.core.agent import DevAgent

task = {
    "prompt": "Write a function to check whether a string is a palindrome.",
    "signature": "def is_palindrome(s: str) -> bool:"
}

agent = DevAgent(max_iter=3)
code = agent.solve(task)

print("\n===== Final Code =====")
print(code)
