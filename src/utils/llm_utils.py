import re
from src.models.qwen_model import QwenModel


def extract_python_code(text: str) -> str:
    """
    去除 ```python ``` 等 Markdown 包裹
    """
    match = re.search(r"```(?:python)?\s*(.*?)```", text, re.S)
    if match:
        return match.group(1).strip()
    return text.strip()


def call_llm(prompt: str) -> str:
    model = QwenModel()
    raw = model.generate(prompt)
    return extract_python_code(raw)
