from src.core.code_generator import CodeGenerator
from src.core.tester import Tester
from src.core.fixer import Fixer
from src.tools.python_repl import PythonREPL
from src.utils.config_utils import load_all_configs


class DevAgent:
    def __init__(self, max_iter: int = None):
        cfg = load_all_configs()["global"]
        self.max_iter = max_iter or cfg["agent"]["max_iter"]

        self.generator = CodeGenerator()
        self.tester = Tester()
        self.fixer = Fixer()
        self.executor = PythonREPL()

    def solve(self, task: dict) -> str:
        code = None

        for i in range(self.max_iter):
            print(f"\n=== Iteration {i + 1} ===")

            if code is None:
                code = self.generator.generate(task)

            tests = self.tester.generate(task)
            success, output = self.executor.run(code, tests)

            if success:
                print("✅ Success")
                return code

            print("❌ Failed, fixing...")
            code = self.fixer.fix(code, output)

        return code
