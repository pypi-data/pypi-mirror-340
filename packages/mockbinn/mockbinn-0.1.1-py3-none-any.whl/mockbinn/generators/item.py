from .base import BaseGenerator
import random

class ItemGenerator(BaseGenerator):
    """Gerador de nomes de itens/comprodutos comuns para e-commerce.
    
    Gera nomes de produtos aleatórios de categorias variadas.

    Example:
        >>> ItemGenerator().generate()
        'Notebook'
        >>> ItemGenerator().generate()
        'Cadeira Gamer'

    Notas:
        - A lista de itens pode ser estendida conforme necessidade
        - Para categorias específicas, criar geradores especializados
    """
    def generate(self) -> str:
        """Gera um nome de item aleatório.
        
        Returns:
            str: Nome do item gerado
        """
        items = ['Notebook', 'Livro', 'Mesa', 'Caneta', 'Quadro', 'Bicicleta', 'Cadeira']

        return random.choice(items)