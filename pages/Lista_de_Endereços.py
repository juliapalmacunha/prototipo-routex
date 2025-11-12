import streamlit as st
import pandas as pd
from database import listar_enderecos


class Estilos:
    @staticmethod
    def aplicar_css():
        st.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
        <style>
            .titulo-pagina {
                text-align: center;
                color: #2c3e50;
                font-size: 32px;
                margin: 15px 0 30px 0;
                font-weight: 700;
            }

            .info-box {
                background-color: #f0f4f8;
                border-left: 6px solid #3498db;
                padding: 15px 20px;
                border-radius: 12px;
                box-shadow: 0px 3px 8px rgba(0,0,0,0.05);
                color: #34495e;
                font-size: 16px;
                margin-bottom: 20px;
            }

            .dataframe-container {
                display: flex;
                justify-content: center;
                margin-bottom: 20px;
            }

            .dataframe-container table {
                border-collapse: collapse;
                width: auto;
                max-width: 100%;
            }

            .dataframe-container th {
                background-color: #dfe3e6;
                color: #2c3e50;
                font-weight: 600;
                padding: 10px 15px;
                text-align: center;
            }

            .dataframe-container td {
                padding: 8px 12px;
                color: #2c3e50;
                text-align: center;
            }

            .dataframe-container tr:nth-child(even) {
                background-color: #f7f9fa;
            }

            .dataframe-container tr:hover {
                background-color: #e6e9eb;
            }
        </style>
        """, unsafe_allow_html=True)


class EnderecosCadastrados:

    def __init__(self):
        self.enderecos = []

    def carregar_enderecos(self):
        self.enderecos = listar_enderecos()

    def exibir_titulo(self):
        st.markdown("""
        <h2 class="titulo-pagina">
            <i class="fa-solid fa-map-location-dot"></i> Endereços Cadastrados
        </h2>
        """, unsafe_allow_html=True)

    def exibir_mensagem_vazia(self):
        st.markdown(
            '<div class="info-box"><i class="fa-solid fa-circle-info"></i> Nenhum endereço cadastrado ainda.</div>',
            unsafe_allow_html=True
        )

    def exibir_tabela(self):
        dados = [
            {
                "ID": e["id"],
                "Nome do local": e["nome_local"],
                "Tipo de logradouro": e["tipo_logradouro"],
                "Nome do logradouro": e["nome_logradouro"],
                "Número": e["número"],
                "Complemento": e.get("complemento", "-"),
                "Bairro": e.get("bairro", "-"),
                "Cidade": e["cidade"],
                "Estado": e["estado"],
                "CEP": e["cep"],
            }
            for e in self.enderecos
        ]

        df = pd.DataFrame(dados)
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.markdown(df.to_html(index=False, escape=False), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    def renderizar_pagina(self):
        self.exibir_titulo()
        self.carregar_enderecos()

        if not self.enderecos:
            self.exibir_mensagem_vazia()
        else:
            self.exibir_tabela()


def main():
    Estilos.aplicar_css()
    pagina = EnderecosCadastrados()
    pagina.renderizar_pagina()


if __name__ == "__main__":
    main()
