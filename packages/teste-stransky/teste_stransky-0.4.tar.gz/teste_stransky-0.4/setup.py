from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='teste_stransky',
    version='0.4',
    packages=find_packages(),
    install_requires=[],
    author='Marcelo Stransky',
    author_email='marcelostransky@gmail.com',
    description='Uma biblioteca para cálculos de investimentos. Simulador de investimentos para estudos',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/marcelostransky/meu_investimento',
    classifiers=['Programming Language :: Python :: 3','License :: OSI Approved :: MIT License','Operating System :: OS Independent',],
    python_requires='>=3.6',
    )