# Projeto Individual de MAC0350

## O que foi desenvolvido
Uma aplicação web de gerenciamento de blocos de tarefas e tarefas.

### Descrição da aplicação

Foi desenvolvido uma aplicação web utilizando FastAPI e SQLite para o backend e html, css e javascript para o frontend. É um sistema de gerenciamento de blocos de tarefas e suas respectivas tarefas, permitindo criar, editar e excluir blocos e tarefas, além de marcar tarefas como concluídas.

## Requisitos para executar o projeto

- Python 3.10 ou superior.
- As dependências do projeto listadas no arquivo `requirements.txt`.

## Como executar

Para executar o projeto em modo desenvolvimento:

1. Clone o repositório.
2. Navegue até o diretório do projeto `/projeto`.
3. Crie um ambiente virtual python e ative-o.
4. Instale as dependências com `pip install -r requirements.txt`.
5. Execute o comando `fastapi dev` para iniciar o servidor em modo de desenvolvimento.
6. Acesse `http://127.0.0.1:8000` no seu navegador para usar a aplicação.

## Uso de IA no projeto

A IA foi utilizada para auxiliar nas seguintes tarefas:
- Escolha de bibliotecas de tooltip e modal para o frontend.
- Dúvidas sobre utilização de htmx para tarefas específicas.
- Dúvidas de melhores práticas para nomes de arquivos, funções, variáveis, etc.
- Dúvida e escolha de melhor prática para implementação de modo escuro/claro em css + javascript.
- Correção de bibliotecas faltantes do fastapi e do sqlmodel na main do projeto.
- No frontend, o css e a responsividade do grid de tarefas foram feitos com auxílio da IA, um exemplo disso é a classe `grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));` (sendo modificado para `grid-template-columns: repeat(auto-fill, minmax(30vw, 1fr)) !important;`, por mim) que foi sugerida pela IA para criar um grid funcional.
- No backend algumas dúvidas de sintax, estrutura do python e do fastapi, alguns retornos corretos para melhor funcionamento da aplicação e dúvidas gerais foram resolvidas com auxílio da IA.