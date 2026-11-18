# GameHub — Arquitetura do Sistema

## 1. Visão geral

GameHub é uma aplicação de comércio digital de jogos.

A arquitetura utiliza persistência poliglota, distribuindo os dados entre MongoDB, Redis e Neo4j conforme as características de cada banco.

A interface Streamlit utiliza serviços Python para acessar os bancos.

## 2. Arquitetura geral

Streamlit (Interface)
|
+--- CatalogService
| |
| +--- Redis (Cache)
| +--- MongoDB (Catálogo)
|
+--- CartService
| |
| +--- Redis (Carrinho)
|
+--- RecommendationService
| |
| +--- Neo4j (Grafo)
|
+--- OrderService
|
+--- MongoDB (Pedidos)
+--- Neo4j (Compras)
+--- Redis (Limpeza do carrinho)

## 3. MongoDB

Banco responsável pelos dados persistentes e documentos da aplicação.

### Coleção clientes

Campos:

- \_id
- nome
- email

### Coleção jogos

Campos:

- \_id
- nome
- genero
- descricao
- marca
- categorias
- imagem_url
- especificacoes (objeto JSON flexível)
- preco
- ano

`imagem_url` referencia uma imagem externa; não há upload de arquivos.

### Coleção pedidos

Campos:

- \_id
- cliente_id
- itens
- total
- status
- checkout_id (identificador único da tentativa)
- data_criacao

`status` assume `PENDENTE` enquanto a atualização no Neo4j não estiver confirmada e `CONCLUIDO` após a confirmação das operações necessárias. `checkout_id` deve ser único para impedir outro pedido na repetição da mesma tentativa.

Cada item do pedido deverá armazenar:

- jogo_id
- nome
- quantidade
- preco_unitario

O preço deverá ser registrado como uma cópia do preço vigente no momento da compra.

## 4. Redis

Banco responsável por dados temporários e operações rápidas.

### Carrinho

Chave:

gamehub:carrinho:{cliente_id}

Tipo: Hash.

Campos:

- ID do jogo como chave.
- Quantidade como valor.

Operações:

- HSET para adicionar ou atualizar.
- HDEL para remover.
- HGETALL para recuperar os itens.
- DEL para limpar após o checkout.

### Sessão

Chave:

gamehub:token_demo:{token}

Armazena o ID do cliente selecionado associado ao token temporário.

Utilizar TTL de 30 minutos para expiração do token. Esse mecanismo serve apenas para a sessão demonstrativa; não implementa autenticação completa, cadastro ou recuperação de senha.

### Cache

Chave:

gamehub:produto:{produto_id}

Tipo: String com conteúdo JSON.

Utilizar TTL de 60 segundos.

Quando o cache individual não existir ou expirar, consultar MongoDB e armazenar o resultado do produto no Redis. O TTL é de 60 segundos. Essa estratégia atende ao cache do MVP, mas não contabiliza nem prioriza produtos por popularidade.

### Inicialização

O script de carga verifica a conexão com Redis e preenche as chaves individuais iniciais do cache a partir do catálogo MongoDB, com TTL de 60 segundos. Redis não possui esquema fixo nem índices no projeto; as chaves de sessão e carrinho são criadas pelos fluxos da aplicação. Não criar métricas ou estruturas adicionais.

## 5. Neo4j

Banco responsável pelos relacionamentos e recomendações.

### Nós

(:Cliente)

- id
- nome

(:Produto)

- id
- nome
- preco

(:Categoria)

- nome

### Relacionamentos

(:Cliente)-[:COMPROU {checkout_id, data}]->(:Produto)

(:Cliente)-[:AVALIOU {nota}]->(:Produto)

(:Produto)-[:PERTENCE_A]->(:Categoria)

Os dados iniciais e restrições do grafo são criados pelo script de carga de forma reproduzível. `checkout_id` identifica cada compra para que a repetição da mesma tentativa não duplique relações. Consultas Cypher utilizam parâmetros.

### Recomendação

A consulta deverá:

1. Localizar o cliente atual.
2. Encontrar outros clientes que compraram produtos em comum.
3. Encontrar produtos comprados pelos clientes semelhantes.
4. Considerar avaliações iguais ou superiores a 4.
5. Excluir produtos que o cliente atual já comprou.
6. Ordenar os resultados por relevância.

A implementação deverá utilizar parâmetros nas consultas Cypher.

A recomendação não deverá ser calculada apenas em Python.

## 6. Integração entre os bancos

### Consulta do catálogo

1. Consultar MongoDB para a listagem, busca e filtro do catálogo.
2. Ao ler um produto individual, consultar `gamehub:produto:{produto_id}` no Redis.
3. Se houver cache válido, retornar os dados; caso contrário, consultar MongoDB e gravar o resultado no Redis com TTL de 60 segundos.

### Adição ao carrinho

1. Identificar o cliente.
2. Recuperar o carrinho do Redis.
3. Atualizar a quantidade do produto.
4. Salvar a alteração no Redis.

### Checkout

1. Receber ou criar um `checkout_id` único para a tentativa; manter o ID na sessão da interface enquanto o pedido estiver pendente e reutilizá-lo na retomada.
2. Procurar no MongoDB um pedido com esse `checkout_id`. Se estiver `CONCLUIDO`, repetir a limpeza do carrinho no Redis e retornar o resultado concluído.
3. Se estiver `PENDENTE`, reutilizar os itens e valores já persistidos no pedido. Se não existir, recuperar o carrinho, consultar os preços atuais no MongoDB, calcular o total no servidor e gravar o pedido com status `PENDENTE`.
4. Atualizar no Neo4j as relações `COMPROU` para os itens do pedido, usando operações idempotentes identificadas pelo `checkout_id`.
5. Após confirmar a atualização no Neo4j, marcar o pedido como `CONCLUIDO` no MongoDB.
6. Somente então limpar o carrinho no Redis e informar o resultado à interface.

Se a atualização do Neo4j falhar após a gravação do pedido, manter o status `PENDENTE`, preservar o carrinho e informar que a operação ficou parcialmente concluída. Enquanto houver pedido pendente para o cliente, bloquear alterações no carrinho e iniciar outro checkout; permitir a retomada com o mesmo `checkout_id`. A retomada localiza o pedido existente e repete a gravação idempotente no Neo4j, sem inserir outro pedido. Se o pedido já estiver `CONCLUIDO`, uma repetição não recria pedido nem relações; apenas confirma/repete a limpeza do carrinho, se necessário. Não são usadas transações distribuídas. O carrinho só é apagado após o pedido estar `CONCLUIDO`.

## 7. Infraestrutura

Utilizar Docker Compose para iniciar:

- MongoDB.
- Redis.
- Neo4j.

A aplicação Streamlit será executada localmente pelo Python.

As configurações deverão ser obtidas por variáveis de ambiente.

## 8. Organização do projeto

GameHub/
app.py
config.py
database/
mongodb.py
redis_db.py
neo4j_db.py
services/
catalogo.py
carrinho.py
pedidos.py
recomendacoes.py
scripts/
seed.py
docker-compose.yml
requirements.txt
.env.example
.gitignore
README.md
PLANO.md
ARQUITETURA.md

## 9. Princípios

- MongoDB é a fonte dos dados persistentes de catálogo, clientes e pedidos.
- Redis é a fonte do estado temporário do carrinho e do token de demonstração; também armazena o cache individual de produtos com TTL de 60 segundos, sem contagem de popularidade.
- Neo4j é a fonte dos relacionamentos utilizados nas recomendações.
- Streamlit não deve conter consultas diretas aos bancos.
- Regras de negócio devem permanecer nos serviços.
- Não adicionar tecnologias ou serviços desnecessários.
