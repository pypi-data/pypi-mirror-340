from .base import BaseGenerator
import random
from typing import Optional

class NameGenerator(BaseGenerator):
    """Gerador de nomes completos realistas com suporte a múltiplos idiomas e gêneros.
    
    Args:
        gender (str, optional): Gênero para o nome ('male' ou 'female'). 
            Se None, escolhe aleatoriamente. Padrão: None
        locale (str): Localidade para nomes ('pt' para português ou 'en' para inglês).
            Padrão: 'pt'

    Example:
        >>> NameGenerator(gender='male', locale='pt').generate()
        'João Silva'
        >>> NameGenerator(gender='female', locale='en').generate()
        'Mary Johnson'

    Atributos:
        LOCALES_SUPPORTED: Lista de localidades suportadas
    """

    LOCALES_SUPPORTED = ['pt', 'en']

    def __init__(self, gender: Optional[str] = None, locale: str = 'pt'):
        self.gender = gender or random.choice(['male', 'female'])
        self.locale = locale if locale in self.LOCALES_SUPPORTED else 'pt'
    
    def generate(self) -> str:
        """Gera um nome completo no formato 'Primeiro Sobrenome'.
        
        Returns:
            str: Nome completo gerado aleatoriamente
            
        Raises:
            ValueError: Se o locale não for suportado
        """
        first_names = {
            'en': {
                'male': ['John', 'Michael', 'David', 'James', 'Robert'],
                'female': ['Mary', 'Jennifer', 'Linda', 'Patricia', 'Elizabeth']
            },
            'pt': {
                'male': ['João', 'Pedro', 'Lucas', 'Gabriel', 'Carlos'],
                'female': ['Maria', 'Ana', 'Juliana', 'Patrícia', 'Camila']
            }
        }
        
        last_names = {
            'en': ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones'],
            'pt': ['Silva', 'Santos', 'Oliveira', 'Souza', 'Pereira']
        }
        
        first = random.choice(first_names.get(self.locale, first_names['en'])[self.gender])
        last = random.choice(last_names.get(self.locale, last_names['en']))
        return f"{first} {last}"