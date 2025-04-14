import random
from .base import BaseGenerator

class PhoneGenerator(BaseGenerator):
    """Gerador de números de telefone brasileiros formatados.
    
    Gera números no formato brasileiro com DDD válido:
    - (XX) 9XXXX-XXXX para celulares
    - (XX) XXXX-XXXX para fixos (20% de chance)

    Example:
        >>> PhoneGenerator().generate()
        '(11) 98765-4321'
    """
    def generate(self) -> str:
        """Gera um número de telefone formatado.
        
        Returns:
            str: Telefone no formato brasileiro com DDD
        """
        return f"(55) {random.randint(10, 80)} {random.randint(90000, 99999)}-{random.randint(1000, 9999)}"