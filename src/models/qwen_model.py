from dashscope import Generation
from src.models.base_model import BaseModel
from src.utils.config_utils import load_all_configs


class QwenModel(BaseModel):
    def __init__(self):
        cfg = load_all_configs()["model"]
        model_cfg = cfg["models"]["qwen"]

        self.model_name = model_cfg.get("model_name")
        self.temperature = model_cfg.get("temperature")
        self.max_tokens = model_cfg.get("max_tokens")

    def generate(self, prompt: str) -> str:
        response = Generation.call(
            model=self.model_name,
            prompt=prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        return response["output"]["text"]
