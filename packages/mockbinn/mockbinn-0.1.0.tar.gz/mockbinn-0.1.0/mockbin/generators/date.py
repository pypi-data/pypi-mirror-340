from .base import BaseGenerator
import random
from datetime import datetime, timedelta

class DateGenerator(BaseGenerator):
    """Gerador de datas aleatórias dentro de um intervalo especificado.
    
    Args:
        start_date (str): Data inicial no formato 'YYYY-MM-DD'. Padrão: '2000-01-01'
        end_date (str): Data final ou 'today' para data atual. Padrão: 'today'
        date_format (str): Formato de saída da data. Padrão: '%Y-%m-%d'

    Example:
        >>> DateGenerator(start_date='2020-01-01', end_date='2020-12-31').generate()
        '2020-06-15'
    """
    def __init__(self, start_date: str = '2000-01-01', end_date: str = 'today'):
        self.start = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date == 'today':
            self.end = datetime.now().date()
        else:
            self.end = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    def generate(self) -> str:
        """Gera uma data aleatória no intervalo especificado.
        
        Returns:
            str: Data formatada conforme date_format
            
        Raises:
            ValueError: Se start_date > end_date
        """
        delta = self.end - self.start
        random_days = random.randint(0, delta.days)
        random_date = self.start + timedelta(days=random_days)
        return random_date.strftime('%Y-%m-%d')