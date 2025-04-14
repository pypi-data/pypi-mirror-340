import random
import string
from typing import Optional
from .base import BaseGenerator

class EmailGenerator(BaseGenerator):
    """Gerador de endereços de e-mail fictícios.
    
    Gera e-mails aleatórios no formato username@domain, onde o domínio
    pode ser customizado.
    
    Args:
        domain (str, optional): Domínio a ser usado no e-mail. 
            Padrão: "example.com"
    
    Example:
        >>> generator = EmailGenerator(domain="test.org")
        >>> generator.generate()
        'username@test.org'
    """
    def __init__(self, domain: Optional[str] = None):
        self.domain = domain or "example.com"
    
    def generate(self) -> str:
        """Gera um e-mail aleatório.
        
        Returns:
            str: Endereço de e-mail gerado no formato username@domain
        
        Example:
            >>> EmailGenerator().generate()
            'randomname@example.com'
        """
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        return f"{username}@{self.domain}"