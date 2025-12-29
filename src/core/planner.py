from src.utils.llm_utils import call_llm
from src.utils.config_utils import load_all_configs


class Fixer:
    def __init__(self):
        self.prompts = load_all_configs()["prompts"]

    def fix(self, code: str, error: str) -> str:
        prompt = self.prompts["bug_fixing"].format(
            code=code,
            error=error,
        )
        return call_llm(prompt)
