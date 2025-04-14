import pandas as pd
from typing import Dict, Any, Type, Union
from .generators import BaseGenerator
from pathlib import Path
from io import BytesIO

class Mockbinn:
    """Classe principal para geração de dados fictícios estruturados.
    
    Permite definir modelos com colunas específicas e gerar DataFrames pandas
    com dados aleatórios para testes e desenvolvimento.
    
    Exemplo de uso:
        >>> from mockbinn import Mockbinn
        >>> mocker = Mockbinn()
        >>> mocker.set_model("users", 5).set_columns("users", {"name": NameGenerator})
        >>> df = mocker.get_df_from_model("users")
    
    Attributes:
        models (Dict[str, Dict[str, Any]]): Dicionário contendo os modelos registrados
    """

    def __init__(self):
        """Inicializa uma nova instância de Mockbinn."""
        self.models: Dict[str, Dict[str, Any]] = {}
        
    def set_model(self, model_name: str, model_size: int = 100) -> 'Mockbinn':
        """Define ou atualiza um modelo"""
        if model_name not in self.models:
            self.models[model_name] = {
                'size': model_size,
                'columns': {}
            }
        else:
            self.models[model_name]['size'] = model_size
        return self
    
    def set_columns(self, model_name: str, columns: Dict[str, Type[BaseGenerator]]) -> 'Mockbinn':
        """Define as colunas para um modelo"""
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not found. Call set_model() first.")
        
        self.models[model_name]['columns'] = columns
        return self
    
    def get_df_from_model(self, model_name: str) -> pd.DataFrame:
        """Gera um DataFrame pandas com os dados fictícios"""
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not found.")
        
        model = self.models[model_name]
        size = model['size']
        columns = model['columns']
        
        data = {}
        for column_name, generator_class in columns.items():
            generator = generator_class()
            data[column_name] = [generator.generate() for _ in range(size)]
        
        return pd.DataFrame(data)
    
    def export_model(
        self,
        model_name: str,
        output_path: Union[str, Path],
        format: str = 'csv',
        **kwargs
    ) -> None:
        """Exporta um modelo para um arquivo no formato especificado.
        
        Args:
            model_name: Nome do modelo a ser exportado
            output_path: Caminho do arquivo de saída
            format: Formato de exportação ('csv', 'parquet' ou 'json')
            **kwargs: Argumentos adicionais para pandas.to_csv() ou pandas.to_parquet()
            
        Raises:
            ValueError: Se o formato não for suportado ou modelo não existir
        """
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not found.")
            
        df = self.get_df_from_model(model_name)
        output_path = Path(output_path)
        
        if format == 'csv':
            df.to_csv(output_path, **kwargs)
        elif format == 'parquet':
            df.to_parquet(output_path, **kwargs)
        # Adicione no método export_model
        elif format == 'json':
            df.to_json(output_path, **kwargs)
        else:
            raise ValueError(f"Unsupported format: {format}. Use 'csv' or 'parquet'.")
        
    def export_to_buffer(self, model_name: str, format: str = 'csv', **kwargs):
        """Retorna os dados em um buffer de bytes."""
        df = self.get_df_from_model(model_name)
        if format == 'csv':
            return df.to_csv(**kwargs).encode()
        elif format == 'parquet':
            buffer = BytesIO()
            df.to_parquet(buffer, **kwargs)
            return buffer.getvalue()