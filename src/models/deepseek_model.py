from openai import OpenAI
from src.models.base_model import BaseModel
from src.utils.config_utils import load_all_configs


class DeepSeekModel(BaseModel):
    def __init__(self):
        cfg = load_all_configs()["model"]
        model_cfg = cfg["models"]["deepseek"]

        self.model_name = model_cfg["model_name"]
        self.temperature = model_cfg["temperature"]
        self.max_tokens = model_cfg["max_tokens"]

        self.client = OpenAI(
            api_key=model_cfg["api_key"],
            base_url=model_cfg["base_url"]
        )

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )

        return response.choices[0].message.content
