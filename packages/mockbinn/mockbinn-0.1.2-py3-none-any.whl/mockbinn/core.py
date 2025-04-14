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
        """Define ou atualiza um modelo de dados.
    
        Cria um novo modelo ou atualiza o tamanho de um modelo existente.
        Deve ser chamado antes de definir as colunas.

        Args:
            model_name: Nome único do modelo a ser criado/atualizado
            model_size: Quantidade de registros a serem gerados. Default: 100

        Returns:
            Mockbin: A própria instância para method chaining

        Example:
            >>> mocker = Mockbin()
            >>> mocker.set_model("users", 50)  # Cria modelo com 50 registros
            >>> mocker.set_model("users", 100)  # Atualiza para 100 registros
        """
        if model_name not in self.models:
            self.models[model_name] = {
                'size': model_size,
                'columns': {}
            }
        else:
            self.models[model_name]['size'] = model_size
        return self
    
    def set_columns(self, model_name: str, columns: Dict[str, Type[BaseGenerator]]) -> 'Mockbinn':
        """Define as colunas e geradores para um modelo.
    
        Configura como cada coluna do modelo será gerada, aceitando:
        - Classes geradoras (subclasses de BaseGenerator)
        - Funções/lambdas que retornam valores
        - Valores estáticos para todas as linhas

        Args:
            model_name: Nome do modelo previamente criado com set_model()
            columns: Dicionário com definições das colunas onde:
                - Chave: nome da coluna
                - Valor: pode ser:
                    * Classe geradora (ex: UUIDGenerator)
                    * Função/lambda (ex: lambda: random.choice(...))
                    * Valor estático (ex: "constant_value")

        Returns:
            Mockbinn: A própria instância para method chaining

        Raises:
            ValueError: Se o modelo não existir (não foi criado com set_model())

        Example:
            >>> mocker.set_columns("users", {
            ...     "id": UUIDGenerator,
            ...     "name": NameGenerator,
            ...     "active": True,  # Valor estático
            ...     "signup_date": lambda: datetime.now().strftime("%Y-%m-%d")
            ... })
        """
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not found. Call set_model() first.")
        
        self.models[model_name]['columns'] = columns
        return self
    
    def get_df_from_model(self, model_name: str) -> pd.DataFrame:
        """Gera um DataFrame pandas com dados fictícios baseados no modelo.
        
        Processa todas as definições de coluna e gera os dados aleatórios
        no formato especificado.

        Args:
            model_name: Nome do modelo a ser gerado

        Returns:
            pd.DataFrame: DataFrame contendo os dados gerados

        Raises:
            ValueError: Se o modelo não existir

        Example:
            >>> df = mocker.get_df_from_model("users")
            >>> print(df.head())
            id          name  active signup_date
            0  abc123     João Silva    True  2023-10-01
            1  def456  Maria Santos    True  2023-10-01
        """
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not found.")
        
        model = self.models[model_name]
        size = model['size']
        columns = model['columns']
        
        data = {}
        for column_name, column_def in columns.items():
            if isinstance(column_def, type) and issubclass(column_def, BaseGenerator):
                # Caso 1: É uma classe geradora
                generator = column_def()
                data[column_name] = [generator.generate() for _ in range(size)]
            elif callable(column_def):
                # Caso 2: É uma função/lambda
                data[column_name] = [column_def() for _ in range(size)]
            else:
                # Caso 3: Valor estático
                data[column_name] = [column_def for _ in range(size)]
    
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
            df.to_json(output_path, orient='records', force_ascii=False, **kwargs)
        else:
            raise ValueError(f"Unsupported format: {format}. Use 'csv' or 'parquet'.")
        
    def export_to_buffer(self, model_name: str, format: str = 'csv', **kwargs):
        """Exporta os dados do modelo para um buffer de bytes em memória.
    
        Suporta múltiplos formatos de serialização sem necessidade de arquivos temporários.

        Args:
            model_name: Nome do modelo a ser exportado
            format: Formato de exportação ('csv' ou 'parquet'). Default: 'csv'
            **kwargs: Argumentos adicionais para pandas.to_csv() ou pandas.to_parquet()

        Returns:
            bytes: Dados serializados em formato binário

        Raises:
            ValueError: Se o formato não for suportado ou modelo não existir
            ImportError: Para formato parquet sem pyarrow instalado

        Example:
            >>> # Exportar como CSV
            >>> csv_data = mocker.export_to_buffer("users")
            >>> # Exportar como Parquet
            >>> parquet_data = mocker.export_to_buffer("users", format='parquet')
            >>> # Com parâmetros customizados
            >>> csv_data = mocker.export_to_buffer(
            ...     "users",
            ...     sep=';',
            ...     index=False
            ... )
        """
        df = self.get_df_from_model(model_name)
        if format == 'csv':
            return df.to_csv(**kwargs).encode()
        elif format =='json':
            buffer = BytesIO()
            df.to_json(buffer, **kwargs)
            return buffer.getvalue()
        elif format == 'parquet':
            buffer = BytesIO()
            df.to_parquet(buffer, **kwargs)
            return buffer.getvalue()
        else:
            raise ValueError(f"Unsupported format: {format}. Use 'csv', 'parquet' or 'json'.")