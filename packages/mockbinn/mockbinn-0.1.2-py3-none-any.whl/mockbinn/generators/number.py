from .base import BaseGenerator
import random
from typing import Union

class NumberGenerator(BaseGenerator):
    """Gerador de números aleatórios inteiros ou decimais.
    
    Args:
        min_val (int/float): Valor mínimo. Padrão: 0
        max_val (int/float): Valor máximo. Padrão: 100
        decimal (bool): Se True, gera números decimais. Padrão: False
        precision (int): Casas decimais (apenas para decimal=True). Padrão: 2

    Example:
        >>> NumberGenerator(1, 10).generate()  # Inteiro
        7
        >>> NumberGenerator(0, 1, decimal=True).generate()  # Decimal
        0.57
    """
    def __init__(self, min_val: int = 0, max_val: int = 100, decimal: bool = False):
        self.min_val = min_val
        self.max_val = max_val
        self.decimal = decimal
    
    def generate(self) -> Union[int, float]:
        """Gera um número aleatório dentro do intervalo especificado.
        
        Returns:
            Union[int, float]: Número gerado (int ou float)
        """
        if self.decimal:
            return round(random.uniform(self.min_val, self.max_val), 2)
        return random.randint(self.min_val, self.max_val)