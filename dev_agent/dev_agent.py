# dev_agent.py

from typing import Dict
from prompts import (
    TASK_PLANNER_PROMPT,
    CODE_GEN_PROMPT,
    TEST_GEN_PROMPT,
    BUG_FIX_PROMPT,
    REFLECTION_PROMPT,
)
from executor import run_python
from utils import llm_call, safe_json_loads


class DevAgent:
    def __init__(self, model: str = "qwen-coder-plus", max_iter: int = 5):
        self.model = model
        self.max_iter = max_iter

    # ========= 需求理解 =========
    def plan(self, requirement: str) -> Dict:
        prompt = TASK_PLANNER_PROMPT.format(requirement=requirement)
        resp = llm_call(prompt, self.model)
        return safe_json_loads(resp)

    # ========= 代码生成 =========
    def generate_code(self, task: str, signature: str) -> str:
        prompt = CODE_GEN_PROMPT.format(
            task=task,
            signature=signature
        )
        return llm_call(prompt, self.model)

    # ========= 测试生成 =========
    def generate_tests(self, task: str, code: str) -> str:
        prompt = TEST_GEN_PROMPT.format(
            task=task,
            code=code
        )
        return llm_call(prompt, self.model)

    # ========= Bug 修复 =========
    def fix_bug(self, code: str, error: str) -> str:
        prompt = BUG_FIX_PROMPT.format(
            code=code,
            error=error
        )
        return llm_call(prompt, self.model)

    # ========= 反思 =========
    def reflect(self, error: str):
        prompt = REFLECTION_PROMPT.format(error=error)
        _ = llm_call(prompt, self.model)

    # ========= 主循环 =========
    def solve(self, task: Dict) -> str:
        """
        task example:
        {
            "prompt": "...",
            "signature": "def foo(x):"
        }
        """
        code = self.generate_code(task["prompt"], task["signature"])

        for i in range(self.max_iter):
            print(f"\n🔁 Iteration {i + 1}")

            tests = self.generate_tests(task["prompt"], code)
            result = run_python(code, tests)

            if result["success"]:
                print("✅ All tests passed")
                return code

            print("❌ Failed:")
            print(result["error"])

            self.reflect(result["error"])
            code = self.fix_bug(code, result["error"])

        print("⚠️ Reached max iterations")
        return code


# ========= CLI 示例 =========
if __name__ == "__main__":
    example_task = {
        "prompt": "Write a function to check whether a string is a palindrome.",
        "signature": "def is_palindrome(s: str) -> bool:"
    }

    agent = DevAgent(max_iter=3)
    final_code = agent.solve(example_task)

    print("\n===== Final Code =====")
    print(final_code)
