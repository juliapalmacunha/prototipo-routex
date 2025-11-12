import streamlit as st
import pandas as pd
from database import listar_enderecos

st.title("📍 Selecionar Endereços para Rota")

# Busca os endereços do banco
enderecos = listar_enderecos()

if not enderecos:
    st.info("Nenhum endereço cadastrado ainda.")
else:
    # Cria um DataFrame com os endereços vindos do banco
    dados = [
        {
            "ID": e["id"],
            "Tipo": e["tipo_logradouro"],
            "Logradouro": e["nome_logradouro"],
            "Número": e["número"],
            "Complemento": e["complemento"],
            "Bairro": e["bairro"],
            "Cidade": e["cidade"],
            "Estado": e["estado"],
            "CEP": e["cep"],
            "Local": e["nome_local"],
        }
        for e in enderecos
    ]
    df = pd.DataFrame(dados)

    

    # Selecionar endereços para a rota
    opcoes = [f"{e['nome_logradouro']}, {e['número']} - {e['cidade']}/{e['estado']}" for e in enderecos]
    selecionados = st.multiselect("Selecione os endereços para montar a rota:", opcoes)

    if st.button("🚗 Montar rota"):
        if selecionados:
            st.session_state["enderecos_selecionados"] = selecionados
            st.success(f"{len(selecionados)} endereços selecionados para a rota.")
            st.info("Volte para a página 'Geração de Rotas' para visualizar o mapa.")
