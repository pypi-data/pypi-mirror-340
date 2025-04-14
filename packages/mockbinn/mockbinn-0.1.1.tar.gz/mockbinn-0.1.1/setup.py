from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mockbinn',
    version='0.1.1',
    author='Nathan',
    author_email='nathan.lopes@sptech.school',
    description='Uma biblioteca para gerar dados fictícios para testes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/NathanBin/mockbinn',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    extras_require={
        'parquet': ['pyarrow>=6.0.0'],
        'dev': [
            'pytest>=6.0.0',
            'twine>=3.0.0',
        ],
        'all': ['pyarrow>=6.0.0'],
    }
)