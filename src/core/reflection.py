from src.utils.llm_utils import call_llm_python
from src.utils.config_utils import load_all_configs

class ReflectionEngine:
    def __init__(self):
        self.prompts = load_all_configs()["prompts"]

    def reflect(self, error: str) -> str:
        prompt = self.prompts["reflection"].format(
            error=error,
        )
        return call_llm_python(prompt)