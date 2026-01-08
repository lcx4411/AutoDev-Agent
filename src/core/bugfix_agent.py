from src.core.generator import CodeGenerator


class BugFixAgent:
    """
    Standard single-shot Bug Fix agent for SWE-Bench.
    No planning, no testing, no iteration.
    """

    def __init__(self):
        self.generator = CodeGenerator()

    def solve(self, task: str) -> str:
        """
        Generate a patch or corrected code directly from the issue description.
        """
        return self.generator.generate(task)
