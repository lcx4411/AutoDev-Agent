from src.utils.llm_utils import call_llm_python
from src.utils.config_utils import load_all_configs
from src.core.plan_schema import Plan

class BugFixer:
    def __init__(self):
        self.prompts = load_all_configs()["prompts"]

    def fix(self, code: str, error: str, task: Plan) -> str:
        prompt = self.prompts["bug_fixing"].format(
            function_signature=task["function_signature"],
            code=code,
            error=error
        )
        return call_llm_python(prompt)
