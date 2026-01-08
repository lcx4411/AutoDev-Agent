from typing import Union

from src.utils.llm_utils import call_llm_python
from src.utils.config_utils import load_all_configs
from src.core.plan_schema import Plan


class CodeGenerator:
    def __init__(self):
        self.prompts = load_all_configs()["prompts"]

    def generate(self, task: Union[Plan, str]) -> str:
        """
        task can be:
        - Plan (dict-like): from Planner, used for code generation
        - str: raw prompt, used for SWE-Bench Bug Fix
        """

        # =========================
        # Case 1: SWE-Bench / BugFix
        # =========================
        if isinstance(task, str):
            return call_llm_python(task)

        # =========================
        # Case 2: Code Generation (Planner output)
        # =========================
        if isinstance(task, dict):
            if "task_description" not in task:
                raise KeyError(
                    f"Plan missing 'task_description': {task}"
                )

            prompt = self.prompts["code_generation"].format(
                task_description=task["task_description"],
                function_signature=task.get("function_signature", ""),
            )
            return call_llm_python(prompt)

        # =========================
        # Unsupported
        # =========================
        raise TypeError(f"Unsupported task type: {type(task)}")
