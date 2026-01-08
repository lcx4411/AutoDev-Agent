from src.utils.llm_utils import call_llm_python
from src.utils.config_utils import load_all_configs
from src.core.plan_schema import Plan

class TestGenerator:
    def __init__(self):
        self.prompts = load_all_configs()["prompts"]

    def generate(self, task: Plan) -> str:
        prompt = self.prompts["test_generation"].format(
            task_description=task["task_description"],
            function_signature=task["function_signature"],
        )
        return call_llm_python(prompt)
