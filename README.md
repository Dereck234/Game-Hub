# GameHub

MVP acadêmico de uma loja digital de jogos, desenvolvido com Streamlit, MongoDB, Redis e Neo4j para demonstrar persistência poliglota.

## Requisitos

- Docker Desktop com Docker Compose.
- Python 3.10 ou superior.

## Configuração e execução

1. Copie `.env.example` para `.env` e configure credenciais locais. Não versionar `.env`.
2. Inicie os bancos:

   ```powershell
   docker compose up -d --wait
   ```

3. Crie e ative o ambiente virtual e instale as dependências:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

4. Verifique as conexões e carregue os dados demonstrativos:

   ```powershell
   python -m scripts.check_connections
   python -m scripts.seed
   ```

5. Inicie a interface:

   ```powershell
   streamlit run app.py
   ```

Se outro serviço MongoDB do Windows estiver usando `127.0.0.1:27017`, configure `MONGODB_HOST=::1` no `.env` para usar o encaminhamento IPv6 do Docker Desktop. O construtor de URI do projeto envolve endereços IPv6 entre colchetes. Essa configuração não altera credenciais nem dados persistidos.

## Responsabilidade dos bancos

- **MongoDB:** catálogo de jogos, clientes e pedidos, incluindo o status e o identificador idempotente do checkout.
- **Redis:** carrinhos e tokens temporários da sessão demonstrativa; também mantém cache individual de jogos por 60 segundos.
- **Neo4j:** relações de clientes, produtos e categorias usadas pelas recomendações; registra compras e avaliações.

O seed pode ser executado novamente: atualiza os documentos e nós demonstrativos por identificadores estáveis e carrega no Redis somente cópias dos produtos do catálogo com TTL de 60 segundos. Não cria carrinhos ou tokens.

O checkout não processa pagamentos. Ele grava o pedido pendente no MongoDB, atualiza as compras no Neo4j de forma idempotente, marca o pedido como concluído e só então limpa o carrinho. Uma falha intermediária preserva o pedido pendente e o carrinho para retomada.

As capas dos seis jogos ficam em `images/`. O seed grava caminhos relativos no campo `imagem_path`, e a interface usa esses arquivos locais no catálogo, no carrinho, nas recomendações e no checkout.
