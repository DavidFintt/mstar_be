# Mstar Supply

**Mstar Supply** é um software desenvolvido para gerenciar mercadorias, entradas e saídas para uma empresa de logística. Este projeto oferece uma interface simples e eficiente para acompanhar o fluxo de mercadorias dentro da empresa.

## Tecnologias Utilizadas

- **Flask**: 3.0.3
- **Python**: 3.9.12
- **JWT (JSON Web Token)**: Autenticação com PyJWT
- **Marshmallow**: Validação e serialização de dados

## Funcionalidades

- Gerenciamento de mercadorias.
- Controle de entradas e saídas de produtos.
- Gerenciamento de unidades
- Dashboards graficos com ApexCharts.
- Relatorios mensais, em PDF.

## Instalação

Siga os passos abaixo para configurar e rodar o projeto localmente, e garanta que você possui o Python 3.9 instalado em sua máquina:

1. Clone o repositório do projeto:
   ```bash
   git clone https://github.com/DavidFintt/mstar_be
   ```

2. Crie um ambiente virtual com python:
   ```bash
   py -m venv venv
   ```

3. Instale os requirements.txt:
   ```bash
   py -m pip install -r requirements.txt
   ```

4. Inicie o servidor na porta padrão (5000):
   ```bash
   py main.py
   ```