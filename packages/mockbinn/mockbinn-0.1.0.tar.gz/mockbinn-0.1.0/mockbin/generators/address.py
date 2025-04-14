import random
import string
from .base import BaseGenerator
from typing import Dict

class AddressGenerator(BaseGenerator):
    """Gerador de endereços completos e realistas.
    
    Gera endereços no formato brasileiro por padrão, incluindo:
    - Logradouro
    - Número
    - Cidade
    - Estado
    - CEP formatado

    Example:
        >>> AddressGenerator().generate()
        {
            'street': 'Av. Paulista 123',
            'city': 'São Paulo',
            'state': 'SP',
            'zip_code': '01310-100'
        }
    """
    def generate(self) -> Dict[str, str]:
        """Gera um endereço completo como dicionário.
        
        Returns:
            Dict[str, str]: Dicionário com os componentes do endereço
        """
        streets = ['Av. Laranjeira', 'Av. dos Estados', 'Av. Paulista', 'Rua Santos', 'Rua Interlargos']
        cities = ['São Paulo', 'Rio de Janeiro', 'Rio Grande do Sul', 'Bahia', 'Distrito Federal']
        states = ['SP', 'RJ', 'RG', 'BH', 'DF']
        
        return {
            'street': f"{random.randint(1, 999)} {random.choice(streets)}",
            'city': random.choice(cities),
            'state': random.choice(states),
            'zip_code': ''.join(random.choices(string.digits, k=5)) + '-' + ''.join(random.choices(string.digits, k=3)),
        }