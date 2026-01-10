import json
import re
from src.models.qwen_model import QwenModel
from src.models.deepseek_model import DeepSeekModel


def extract_python_code(text: str) -> str:
    """
    去除 ```python ``` 等 Markdown 包裹
    """
    match = re.search(r"```(?:python)?\s*(.*?)```", text, re.S)
    if match:
        return match.group(1).strip()
    return text.strip()

def extract_json_code(text: str) -> str:
    """
    去除 ```json ``` 等 Markdown 包裹
    """
    match = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    if match:
        return match.group(1).strip()
    return text.strip()

def call_llm_python(prompt: str) -> str:
    model = QwenModel()
    raw = model.generate(prompt)
    return extract_python_code(raw)

def call_llm_json(prompt: str) -> dict:
    model = QwenModel()
    raw = model.generate(prompt)
    json_str = extract_json_code(raw)

    try:
        obj = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM output as JSON:\n{json_str}") from e

    return obj
