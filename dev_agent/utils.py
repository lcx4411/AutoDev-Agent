# utils.py

import json
import dashscope
from dashscope import Generation
import re

# dashscope.api_key = "sk-ef3b83ec51e042408768a45fd8014781"

def llm_call(prompt: str, model: str = "qwen-coder-plus") -> str:
    """
    使用 Qwen-Coder API 进行代码生成

    model 可选：
    - qwen-coder-plus（推荐）
    - qwen-coder-turbo（更快更便宜）
    """

    response = Generation.call(
        model=model,
        prompt=prompt,
        temperature=0.2,
        top_p=0.95,
        max_tokens=512,
        result_format="message"
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Qwen API Error: {response.code}, {response.message}"
        )

    # 取模型回复文本
    raw_output = response.output.choices[0].message["content"]
    code = extract_python_code(raw_output)

    return code

def extract_python_code(text: str) -> str:
    """
    从 LLM 返回中提取纯 Python 代码
    """
    # 情况 1：```python ... ```
    match = re.search(r"```(?:python)?\s*(.*?)```", text, re.S)
    if match:
        return match.group(1).strip()

    # 情况 2：没有代码块，直接返回
    return text.strip()

def safe_json_loads(text: str):
    """
    防止 LLM 输出带解释文本导致 JSON 解析失败
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            return json.loads(text[start:end + 1])
        raise
