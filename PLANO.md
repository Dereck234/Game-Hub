# GameHub — Plano de Implementação

## 1. Objetivo

Desenvolver um MVP acadêmico de uma loja digital de jogos chamada GameHub.

A aplicação permitirá consultar um catálogo de jogos, adicionar produtos ao carrinho, visualizar recomendações personalizadas e finalizar pedidos.

O projeto utilizará Python, Streamlit, MongoDB, Redis e Neo4j.

O objetivo principal é demonstrar a aplicação prática de persistência poliglota (Polyglot Persistence).

## 2. Escopo

### Funcionalidades incluídas

1. Catálogo de jogos com dados iniciais.
2. Seleção de cliente para demonstração.
3. Token temporário de demonstração associado ao cliente selecionado.
4. Carrinho de compras.
5. Cache individual de produtos no Redis com TTL.
6. Recomendações baseadas em relacionamentos.
7. Checkout simplificado com retomada de operações pendentes.

### Funcionalidades excluídas

- Autenticação comercial completa, cadastro e recuperação de senha.
- Pagamentos.
- Integração com APIs externas.
- Inteligência artificial.
- Cadastro administrativo de produtos.
- Cupons e promoções.
- Sistema de avaliações interativo.
- Funcionalidades sociais.

## 3. Etapas de implementação

### Etapa 1 — Infraestrutura

- Criar Docker Compose.
- Configurar MongoDB.
- Configurar Redis.
- Configurar Neo4j.
- Configurar variáveis de ambiente.
- Verificar a disponibilidade dos serviços.

Critério de conclusão: os três bancos devem iniciar e aceitar conexões.

### Etapa 2 — Camada de conexão

Criar os módulos de conexão:

- database/mongodb.py
- database/redis_db.py
- database/neo4j_db.py

Implementar conexões reutilizáveis e tratamento básico de erros.

Critério de conclusão: os três módulos devem conectar-se aos respectivos bancos.

### Etapa 3 — Dados iniciais

Criar `scripts/seed.py` para inicializar e carregar os dados de demonstração nos três bancos.

O script deverá:

- Criar pelo menos 6 jogos.
- Criar pelo menos 3 clientes.
- Criar histórico de compras.
- Criar avaliações.
- Criar categorias.
- Popular MongoDB e Neo4j; verificar a conexão com Redis e preencher o cache inicial de produtos a partir dos documentos do MongoDB, com TTL.
- Ser executável novamente sem duplicar registros.

Criar índices e restrições necessários no MongoDB e no Neo4j, incluindo índice único para `checkout_id` no MongoDB e restrições de unicidade para IDs dos nós no Neo4j. Redis não possui esquema fixo nem índices: o script verifica a conexão e carrega o cache inicial de produtos a partir do MongoDB; sessão e carrinho são criados durante os fluxos demonstrados. Não criar estruturas ou métricas de popularidade.

Critério de conclusão: os dados devem estar disponíveis nos respectivos bancos e permitir demonstrar recomendações.

### Etapa 4 — Catálogo

Implementar:

- Listagem de jogos.
- Busca por nome.
- Filtro por gênero.
- Exibição de preço e informações.
- Cache individual de produtos no Redis com TTL de 60 segundos.

O cache individual atende à estratégia de cache do MVP. Ele não contabiliza acessos nem prioriza produtos por popularidade.

Critério de conclusão: listagem, busca e filtro consultam o catálogo; a leitura individual do produto usa a chave Redis quando válida e consulta MongoDB quando ausente ou expirada.

### Etapa 5 — Carrinho

Implementar:

- Adicionar jogo.
- Remover jogo.
- Alterar quantidade.
- Consultar itens.
- Calcular subtotal e total.

O carrinho deve utilizar Redis como armazenamento principal.

Critério de conclusão: alterações no carrinho devem persistir no Redis.

### Etapa 6 — Recomendações

Implementar consultas Cypher no Neo4j.

A recomendação deverá:

- Identificar clientes que compraram jogos em comum.
- Identificar outros jogos comprados por esses clientes.
- Considerar avaliações positivas.
- Excluir jogos que o cliente atual já comprou.
- Retornar uma lista ordenada de recomendações.

Critério de conclusão: as recomendações devem ser produzidas por consultas reais no Neo4j.

### Etapa 7 — Checkout

Implementar:

- Revisão do carrinho.
- Cálculo do pedido.
- Confirmação da compra.
- Persistência do pedido no MongoDB.
- Atualização dos relacionamentos de compra no Neo4j.
- Limpeza do carrinho no Redis.

Não implementar pagamentos reais.

Cada tentativa de checkout recebe um identificador único, persistido no documento do pedido, que também possui status `PENDENTE` ou `CONCLUIDO`. Manter o identificador na sessão da interface enquanto houver pendência e reutilizá-lo na retomada. Primeiro localizar um pedido com o identificador: se estiver concluído, apenas repetir a limpeza do carrinho; se estiver pendente, retomar usando os itens e valores persistidos; se não existir, calcular o pedido a partir do carrinho e gravá-lo como `PENDENTE`. Atualizar as relações de compra no Neo4j usando o mesmo identificador para evitar duplicações. Se essa atualização falhar, manter o pedido como `PENDENTE`, preservar o carrinho e informar a conclusão parcial. Enquanto houver pedido pendente para o cliente, bloquear alterações no carrinho e outro checkout. Somente após confirmar a atualização do Neo4j, marcar o pedido como `CONCLUIDO` no MongoDB e limpar o carrinho no Redis. Se a limpeza falhar após a conclusão, uma repetição do mesmo identificador apenas repete a limpeza. Não usar transações distribuídas.

Critério de conclusão: pedido único confirmado no MongoDB, relações atualizadas no Neo4j, status `CONCLUIDO` e carrinho vazio no Redis; falhas intermediárias mantêm o status pendente e o carrinho para retomada.

### Etapa 8 — Interface

Criar uma interface Streamlit simples com as quatro telas mínimas do estudo de caso:

1. Catálogo e busca.
2. Carrinho.
3. Recomendações.
4. Checkout.

Uma tela inicial ou histórico de pedidos só deve ser incluído se for simples e ajudar a demonstração. A interface deve utilizar os serviços implementados, sem duplicar regras de negócio.

### Etapa 9 — Verificação e documentação

- Verificar conexão com os três bancos.
- Executar os critérios objetivos de teste abaixo e o fluxo completo.
- Corrigir erros encontrados.
- Criar README.md.
- Documentar instalação e execução.
- Documentar a responsabilidade de cada banco.
- Manter o código organizado e comentado; preparar a defesa para que todos os integrantes expliquem a arquitetura, os bancos e o fluxo demonstrado.

## 4. Regras de desenvolvimento

- Priorizar simplicidade.
- Evitar abstrações desnecessárias.
- Não adicionar funcionalidades fora do escopo.
- Não utilizar dados simulados diretamente na interface.
- Utilizar os bancos reais.
- Não armazenar credenciais no código.
- Não ignorar erros de conexão.
- Manter os dados iniciais reproduzíveis.

## 5. Critério final de aceitação

### Critérios objetivos de teste

- **Inicialização:** MongoDB e Neo4j recebem os dados de demonstração de forma reproduzível, sem duplicação; Redis responde à verificação de conexão e recebe entradas iniciais de cache individual copiadas do catálogo MongoDB, com TTL de 60 segundos. A seleção do cliente cria a chave temporária de sessão.
- **Catálogo:** produto com chave válida (incluindo cache carregado pelo seed) é lido do Redis; após expiração ou ausência, consultar MongoDB e repopular o Redis com TTL de 60 segundos.
- **Sessão e carrinho:** selecionar cliente cria token temporário associado a ele; adicionar, alterar, remover e recuperar itens persiste os valores no Redis.
- **Recomendações:** uma consulta Cypher real considera compras em comum e avaliações positivas, exclui jogos já comprados e retorna resultados ordenados.
- **Checkout concluído:** pedido e valores são persistidos no MongoDB, relações de compra são atualizadas no Neo4j, status termina como `CONCLUIDO` e carrinho fica vazio no Redis.
- **Checkout repetido ou parcial:** repetir o mesmo identificador não cria outro pedido; se a atualização do Neo4j falhar após a gravação no MongoDB, o pedido continua `PENDENTE`, o carrinho permanece e uma nova tentativa com o mesmo identificador retoma a atualização; não é possível alterar o carrinho enquanto existir a pendência. Repetir uma operação já concluída não recria pedido nem relações e pode finalizar uma limpeza Redis pendente.
- **Separação de camadas:** a interface chama serviços e não executa consultas diretamente aos bancos.

O projeto será considerado funcional quando for possível executar o seguinte fluxo:

1. Selecionar um cliente.
2. Consultar o catálogo.
3. Adicionar jogos ao carrinho.
4. Consultar recomendações.
5. Finalizar o pedido.
6. Confirmar o pedido no MongoDB.
7. Confirmar a atualização do Neo4j.
8. Confirmar a limpeza do carrinho no Redis.

A prioridade é a integração funcional entre os três bancos e a demonstração acadêmica, não a complexidade ou sofisticação visual.
