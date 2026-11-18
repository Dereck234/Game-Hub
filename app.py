"""Interface Streamlit do MVP GameHub."""

from uuid import uuid4

import streamlit as st

from services import carrinho, catalogo, pedidos, recomendacoes, sessao

st.set_page_config(page_title="GameHub", page_icon="🎮", layout="wide")
st.title("🎮 GameHub")
st.caption("Loja demonstrativa de jogos digitais")

try:
    clientes = catalogo.listar_clientes()
except Exception as error:
    st.error(f"Não foi possível carregar os clientes: {type(error).__name__}.")
    st.stop()

if not clientes:
    st.warning("Nenhum cliente disponível. Execute `python -m scripts.seed` primeiro.")
    st.stop()

nomes = {str(cliente["_id"]): cliente["nome"] for cliente in clientes}
ids = list(nomes)
selecionado = st.sidebar.selectbox(
    "Cliente da demonstração", ids,
    format_func=lambda cliente_id: nomes[cliente_id],
    key="cliente_selecionado",
)
if st.session_state.get("cliente_token_id") != selecionado:
    st.session_state["cliente_token"] = sessao.criar_sessao(selecionado)
    st.session_state["cliente_token_id"] = selecionado
elif not sessao.obter_cliente(st.session_state.get("cliente_token", "")):
    st.session_state["cliente_token"] = sessao.criar_sessao(selecionado)

pagina = st.sidebar.radio(
    "Navegação", ("Catálogo e busca", "Carrinho", "Recomendações", "Checkout")
)


def mostrar_jogo(jogo: dict) -> None:
    coluna_dados, coluna_acao = st.columns([4, 1])
    with coluna_dados:
        st.subheader(jogo["nome"])
        st.write(jogo["descricao"])
        st.write(f"**Marca:** {jogo.get('marca', '—')} · **Categorias:** {', '.join(jogo.get('categorias', []))}")
        st.write(f"**Preço:** R$ {float(jogo['preco']):.2f} · **Lançamento:** {jogo.get('ano', '—')}")
        if jogo.get("imagem_url"):
            st.image(jogo["imagem_url"], width=180)
    with coluna_acao:
        if st.button("Adicionar ao carrinho", key=f"add_{jogo['_id']}"):
            try:
                carrinho.adicionar(selecionado, str(jogo["_id"]))
                st.success("Jogo adicionado.")
            except Exception as error:
                st.error(str(error))


if pagina == "Catálogo e busca":
    st.header("Catálogo")
    busca = st.text_input("Buscar por nome")
    categoria = st.selectbox("Categoria", ["Todas", *catalogo.listar_categorias()])
    jogos = catalogo.listar_jogos(busca, categoria)
    if not jogos:
        st.info("Nenhum jogo corresponde aos filtros.")
    for jogo in jogos:
        with st.container(border=True):
            mostrar_jogo(jogo)

elif pagina == "Carrinho":
    st.header("Carrinho")
    pending = pedidos.obter_pedido_pendente(selecionado)
    if pending:
        st.warning("Há um checkout pendente. Retome-o na tela Checkout antes de alterar o carrinho.")
    itens = carrinho.obter_itens(selecionado)
    total = 0.0
    for jogo_id, quantidade in itens.items():
        jogo = catalogo.obter_jogo(jogo_id)
        if not jogo:
            st.warning(f"O jogo {jogo_id} não está mais no catálogo.")
            continue
        subtotal = float(jogo["preco"]) * quantidade
        total += subtotal
        esquerda, meio, direita = st.columns([4, 2, 1])
        esquerda.write(f"**{jogo['nome']}** · R$ {float(jogo['preco']):.2f} cada")
        nova_quantidade = meio.number_input(
            "Quantidade", min_value=1, value=quantidade,
            key=f"qtd_{selecionado}_{jogo_id}", disabled=bool(pending),
        )
        if nova_quantidade != quantidade:
            try:
                carrinho.definir_quantidade(selecionado, jogo_id, nova_quantidade)
                st.rerun()
            except Exception as error:
                st.error(str(error))
        if direita.button("Remover", key=f"rem_{selecionado}_{jogo_id}", disabled=bool(pending)):
            try:
                carrinho.remover(selecionado, jogo_id)
                st.rerun()
            except Exception as error:
                st.error(str(error))
        st.caption(f"Subtotal: R$ {subtotal:.2f}")
    st.subheader(f"Total: R$ {total:.2f}")

elif pagina == "Recomendações":
    st.header("Recomendações para você")
    try:
        jogos = recomendacoes.recomendar(selecionado)
    except Exception as error:
        st.error(f"Não foi possível consultar o grafo: {type(error).__name__}.")
        jogos = []
    if not jogos:
        st.info("Ainda não há recomendações para este cliente.")
    for jogo in jogos:
        st.write(f"**{jogo['nome']}** · R$ {float(jogo['preco']):.2f} · relevância {jogo['relevancia']}")
        if st.button("Adicionar ao carrinho", key=f"rec_{jogo['id']}"):
            try:
                carrinho.adicionar(selecionado, jogo["id"])
                st.success("Jogo adicionado.")
            except Exception as error:
                st.error(str(error))

else:
    st.header("Checkout")
    pending = pedidos.obter_pedido_pendente(selecionado)
    checkout_key = f"checkout_id_{selecionado}"
    if pending:
        st.warning("Existe um pedido pendente. A tentativa será retomada com o mesmo identificador.")
        st.session_state[checkout_key] = pending["checkout_id"]
        st.write(f"Pedido pendente: R$ {float(pending['total']):.2f}")
    else:
        itens = carrinho.obter_itens(selecionado)
        if not itens:
            st.info("Adicione jogos ao carrinho para iniciar o checkout.")
        else:
            total = 0.0
            for jogo_id, quantidade in itens.items():
                jogo = catalogo.obter_jogo(jogo_id)
                if jogo:
                    subtotal = float(jogo["preco"]) * quantidade
                    total += subtotal
                    st.write(f"{quantidade} × {jogo['nome']} — R$ {subtotal:.2f}")
            st.subheader(f"Total: R$ {total:.2f}")
    if (pending or carrinho.obter_itens(selecionado)) and st.button("Confirmar compra"):
        checkout_id = st.session_state.setdefault(checkout_key, str(uuid4()))
        try:
            pedido = pedidos.finalizar(selecionado, checkout_id)
            st.session_state.pop(checkout_key, None)
            st.success(f"Pedido concluído: R$ {float(pedido['total']):.2f}. O carrinho foi limpo.")
        except Exception as error:
            st.error(f"Checkout pendente; o carrinho foi preservado. Tente novamente: {type(error).__name__}.")

st.sidebar.caption("Sessão demonstrativa temporária no Redis")
