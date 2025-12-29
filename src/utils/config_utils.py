import yaml
from pathlib import Path

CONFIG_DIR = Path(__file__).resolve().parents[2] / "config"


def load_yaml(filename: str):
    path = CONFIG_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_all_configs():
    return {
        "global": load_yaml("config.yaml"),
        "model": load_yaml("model_config.yaml"),
        "prompts": load_yaml("prompt_templates.yaml"),
    }
