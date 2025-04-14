import random
from .base import BaseGenerator

class BooleanGenerator(BaseGenerator):
    """Gerador de valores booleanos aleatórios ou com probabilidade configurável.
    
    Args:
        true_prob (float): Probabilidade de gerar True (0.0 a 1.0). Padrão: 0.5

    Example:
        >>> BooleanGenerator().generate()
        True
        >>> BooleanGenerator(true_prob=0.8).generate()  # 80% chance de True
        False
    """
    def __init__(self, true_prob: float = 0.5):
        if not 0 <= true_prob <= 1:
            raise ValueError("true_prob must be between 0 and 1")
        self.true_prob = true_prob

    def generate(self) -> bool:
        """Gera um valor booleano aleatório.
        
        Returns:
            bool: True ou False de acordo com a probabilidade definida
        """
        return random.random() < self.true_prob