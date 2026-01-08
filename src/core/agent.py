from src.core.planner import TaskPlanner
from src.core.generator import CodeGenerator
from src.core.tester import TestGenerator
from src.core.fixer import BugFixer
from src.tools.python_repl import PythonREPL
from src.utils.config_utils import load_all_configs


class DevAgent:
    def __init__(self, max_iter: int = None):
        cfg = load_all_configs()["global"]
        self.max_iter = max_iter or cfg["agent"]["max_iter"]

        # 需求理解
        self.planner = TaskPlanner()
        # 代码生成
        self.generator = CodeGenerator()
        # 测试生成
        self.tester = TestGenerator()
        # 代码修复
        self.fixer = BugFixer()
        # 代码执行
        self.executor = PythonREPL()

    def solve(self, task: str) -> str:
        plan = self.planner.plan(task)
        print(f"Plan:\n{plan}\n")

        assert isinstance(plan, dict), "Planner must return a dict"

        code = None

        for i in range(self.max_iter):
            print(f"\n=== Iteration {i + 1} ===")


            # 1. 代码生成（只在第一次 or 修复后）
            if code is None:
                code = self.generator.generate(plan)

            # 2. 测试生成（每轮都可以重新生成）
            tests = self.tester.generate(plan)

            # 3. 执行
            success, output = self.executor.run(code, tests)

            if success:
                print("✅ Success")
                return code

            print("❌ Failed, fixing...")
            code = self.fixer.fix(code, output, plan)

        return code