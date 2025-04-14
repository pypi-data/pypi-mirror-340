from abc import ABC, abstractmethod
from typing import Any

class BaseGenerator(ABC):
    """Classe base para todos os geradores"""
    @abstractmethod
    def generate(self) -> Any:
        """Método principal para gerar dados"""
        pass