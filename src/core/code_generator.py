from src.utils.llm_utils import call_llm
from src.utils.config_utils import load_all_configs


class CodeGenerator:
    def __init__(self):
        self.prompts = load_all_configs()["prompts"]

    def generate(self, task: dict) -> str:
        prompt = self.prompts["code_generation"].format(
            task_description=task["prompt"],
            signature=task["signature"],
        )
        return call_llm(prompt)
