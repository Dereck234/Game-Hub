# AGENTS.md — GameHub

## 1. Contexto do projeto

GameHub é um projeto acadêmico de e-commerce de jogos digitais.

O objetivo é entregar um MVP funcional, simples e demonstrável, respeitando os requisitos do trabalho e o prazo disponível.

Antes de tomar decisões, consulte:

- `PLANO.md`
- `ARQUITETURA.md`
- O enunciado original do trabalho, caso esteja disponível no projeto.

Esses documentos devem ser considerados a referência principal do projeto.

## 2. Regras de desenvolvimento

- Priorize funcionalidade e simplicidade em vez de sofisticação.
- Não implemente funcionalidades fora do escopo definido.
- Não introduza abstrações ou padrões desnecessários.
- Evite dependências adicionais sem justificativa.
- Não substitua tecnologias definidas na arquitetura sem autorização.
- Não invente requisitos que não estejam no enunciado.
- Mantenha a implementação compreensível para um estudante de Ciência da Computação.

## 3. Arquitetura

- Respeite as responsabilidades definidas em `ARQUITETURA.md`.
- Mantenha a interface separada das regras de negócio e do acesso aos bancos.
- Centralize operações de banco de dados em módulos próprios.
- Evite duplicação de lógica.
- Utilize consultas parametrizadas quando aplicável.
- Não coloque credenciais diretamente no código.

## 4. Banco de dados

O projeto utiliza MongoDB, Redis e Neo4j conforme a arquitetura definida.

- MongoDB armazena jogos, clientes e pedidos, incluindo marca, categorias, URL de imagem, especificações flexíveis e o status/identificador de tentativa do pedido.
- Redis armazena o carrinho, o token temporário da sessão demonstrativa e o cache individual de produtos com TTL de 60 segundos. O cache não implementa contagem ou priorização por popularidade.
- Neo4j mantém os nós Cliente, Produto e Categoria e as relações COMPROU, AVALIOU e PERTENCE_A para recomendações.
- Não simule o funcionamento de um banco com estruturas locais em memória.
- O token de demonstração não deve se transformar em autenticação completa, cadastro ou recuperação de senha.
- Não copie credenciais reais do enunciado ou de outros arquivos para o projeto. Utilize variáveis de ambiente e valores fictícios em exemplos.

## 5. Qualidade e testes

- Implemente testes para as funcionalidades principais.
- Execute os testes relacionados às alterações realizadas.
- Utilize os critérios objetivos de fluxo definidos em `PLANO.md`.
- Corrija erros introduzidos pela implementação.
- Não remova testes apenas para fazer a execução passar.
- Informe claramente quais testes foram executados e seus resultados.
- Não afirme que algo funciona sem verificar.

## 6. Controle de escopo

Antes de implementar uma funcionalidade:

1. Verifique se ela está prevista no plano.
2. Identifique quais módulos precisam ser alterados.
3. Considere o impacto nas três bases de dados.
4. Implemente a menor solução que satisfaça o requisito.

Se encontrar uma necessidade fora do escopo, explique antes de implementá-la.

## 7. Comunicação e autonomia

- Trabalhe em etapas pequenas e verificáveis.
- Explique decisões técnicas relevantes de maneira objetiva.
- Não faça alterações destrutivas sem autorização.
- Não implemente etapas futuras sem solicitação.
- Ao encontrar ambiguidades no enunciado, sinalize-as em vez de inventar uma interpretação.
- Preserve o código existente sempre que possível.

## 8. Prioridade máxima

A prioridade é entregar um MVP funcional dentro do prazo acadêmico.

Ordem de importância:

1. Atender aos requisitos obrigatórios do trabalho.
2. Garantir o funcionamento das funcionalidades principais.
3. Integrar corretamente os bancos de dados.
4. Manter o projeto simples e compreensível.
5. Melhorar a apresentação visual, se houver tempo.
