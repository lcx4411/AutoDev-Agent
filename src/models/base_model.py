from abc import ABC, abstractmethod


class BaseModel(ABC):
    """
    模型统一接口
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        raise NotImplementedError
