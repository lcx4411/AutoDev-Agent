import json
from src.utils.llm_utils import call_llm_json
from src.utils.config_utils import load_all_configs
from src.core.plan_schema import Plan


class TaskPlanner:
    REQUIRED_KEYS = {"task_type", "task_description", "function_signature"}

    def __init__(self):
        self.prompts = load_all_configs()["prompts"]

    def plan(self, requirement: str) -> Plan:
        prompt = self.prompts["task_planner"].format(requirement=requirement)

        # 调用 LLM
        llm_output = call_llm_json(prompt)

        # 如果 LLM 返回的是字符串 JSON，需要解析
        if isinstance(llm_output, str):
            try:
                plan = json.loads(llm_output)
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse LLM output as JSON: {e}\nOutput: {llm_output}")
        elif isinstance(llm_output, dict):
            plan = llm_output
        else:
            raise ValueError(f"Planner output must be dict or JSON string, got {type(llm_output)}")

        # 验证必需字段
        missing = self.REQUIRED_KEYS - plan.keys()
        if missing:
            raise ValueError(f"Planner missing keys: {missing}\nLLM output: {plan}")

        # 只保留 Plan 的必需字段
        plan_clean: Plan = {k: plan[k] for k in self.REQUIRED_KEYS}

        return plan_clean
