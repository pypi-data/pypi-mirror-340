import uuid
from .base import BaseGenerator

class UUIDGenerator(BaseGenerator):
    """Gerador de UUIDs (Universally Unique Identifier) versão 4.
    
    Gera identificadores únicos no formato 8-4-4-4-12, seguindo o padrão RFC 4122.
    Ideal para chaves primárias, identificadores de sessão e outros cenários
    que requerem unicidade garantida.

    Example:
        >>> generator = UUIDGenerator()
        >>> generator.generate()
        'f47ac10b-58cc-4372-a567-0e02b2c3d479'

    Notas:
        - Os UUIDs gerados são do tipo 4 (aleatórios)
        - A probabilidade de colisão é extremamente baixa
    """
    def generate(self) -> str:
        """Gera um novo UUID aleatório.
        
        Returns:
            str: UUID no formato string (hexadecimal com hifens)
        """
        return str(uuid.uuid4())