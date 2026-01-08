from src.core.agent import DevAgent

task = "Write a function to check whether a string is a palindrome."

agent = DevAgent(max_iter=3)
code = agent.solve(task)

print("\n===== Final Code =====")
print(code)
