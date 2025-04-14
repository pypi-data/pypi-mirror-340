# Mockbinn - Gerador de Dados Fictícios em Python

[![PyPI Version](https://img.shields.io/pypi/v/mockbinn)](https://pypi.org/project/mockbinn/)
[![Python Versions](https://img.shields.io/pypi/pyversions/mockbinn)](https://pypi.org/project/mockbinn/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Biblioteca Python para geração de dados fictícios estruturados, perfeita para testes, desenvolvimento e prototipagem.

## Instalação

```bash
pip install mockbinn
```

## Uso Básico

```python
from mockbinn import Mockbinn
from mockbinn.generators import NameGenerator, EmailGenerator, DateGenerator

# Inicializar o Mockbin
mocker = Mockbinn()

# Configurar um modelo de dados
mocker.set_model("users", 10).set_columns("users", {
    "id": UUIDGenerator,
    "name": NameGenerator,
    "email": EmailGenerator,
    "signup_date": DateGenerator,
    "is_active": BooleanGenerator
})

# Gerar DataFrame
df = mocker.get_df_from_model("users")
print(df)
```

## Exemplos de Uso

```python
# Gerar usuários e pedidos relacionados
users = mocker.model("users", 100).columns("users", {
    "user_id": UUIDGenerator,
    "name": NameGenerator
}).get_df_from_model("users")

orders = mocker.model("orders", 500).columns("orders", {
    "order_id": UUIDGenerator,
    "user_id": lambda: random.choice(users['user_id']),
    "item": ItemGenerator,
    "value": NumberGenerator(10, 1000, decimal=True)
}).get_df_from_model("orders")
```

## Customização de Geradores

```python
# Criando geradores customizados
corporate_email = EmailGenerator(domain="empresa.com.br")
high_value = NumberGenerator(1000, 10000, decimal=True)

mocker.model("employees", 50).columns("employees", {
    "name": NameGenerator,
    "email": corporate_email,
    "salary": high_value
})
```

## Exportando Dados

Você pode exportar os modelos gerados para CSV ou Parquet:

```python
from mockbinn import Mockbinn
from mockbinn.generators import NameGenerator

mocker = Mockbinn()
mocker.model("users", 100).columns("users", {
    "name": NameGenerator
})

# Método alternativo
mocker.export_model(
    model_name="users",
    output_path="data/users.csv",
    format='csv',
    index=False
)
```

Para usar exportação Parquet, instale as dependências extras:
```bash
pip install mockbinn[parquet]
# ou
pip install pyarrow
```

## Licença

Distribuído sob a licença MIT. Veja LICENSE para mais informações.

## Contato

Nathan Rodrigo - nathan.lopes@sptech.school