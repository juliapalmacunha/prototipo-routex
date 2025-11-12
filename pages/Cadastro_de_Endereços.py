import streamlit as st
import time
from database import adicionar_endereco


class Estilos:
    @staticmethod
    def aplicar_css():
        st.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
        <style>
        .titulo-principal {
            text-align: center;
            color: #000000;
            font-size: 30px;
            font-weight: 600;
            margin-bottom: 20px;
        }
        .subtitulo {
            font-size: 20px;
            color: #2c3e50;
            font-weight: 600;
            margin-top: 30px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        hr {
            border: 1px solid #dcdcdc;
            margin-top: 0;
            margin-bottom: 30px;
        }
        .sucesso-popup {
            position: fixed;
            top: 40%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: #2ecc71;
            color: white;
            padding: 20px 40px;
            border-radius: 10px;
            font-size: 18px;
            text-align: center;
            box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
            z-index: 9999;
        }
        </style>
        """, unsafe_allow_html=True)


class CadastroEndereco:
    def __init__(self):
        self.estados_cidades = self._obter_estados_cidades()
        if "show_popup" not in st.session_state:
            st.session_state.show_popup = False

    def _obter_estados_cidades(self):
        return {
            "Alagoas": ["Maceió", "Arapiraca", "Palmeira dos Índios"],
            "Bahia": ["Salvador", "Feira de Santana", "Vitória da Conquista"],
            "Ceará": ["Fortaleza", "Juazeiro do Norte", "Sobral"],
            "Maranhão": ["São Luís", "Imperatriz", "Caxias"],
            "Paraíba": ["João Pessoa", "Campina Grande", "Patos"],
            "Pernambuco": ["Recife", "Caruaru", "Petrolina"],
            "Piauí": ["Teresina", "Parnaíba", "Picos"],
            "Rio Grande do Norte": ["Natal", "Mossoró", "Caicó", "Parnamirim"],
            "Sergipe": ["Aracaju", "Lagarto", "Itabaiana"],
        }

    def exibir_titulo(self):
        st.markdown("""
        <h1 class="titulo-principal">
            <i class="fa-solid fa-house-chimney"></i> Cadastro de Endereços
        </h1>
        <hr>
        """, unsafe_allow_html=True)

    def selecionar_estado_cidade(self):
        st.markdown("""
        <div class="subtitulo">
            <i class="fa-solid fa-location-dot" style="color:#2c3e50;"></i> Localização
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            estados_lista = ["Selecione um estado"] + list(self.estados_cidades.keys())
            estado = st.selectbox("Estado (UF)", estados_lista)
        with col2:
            if estado != "Selecione um estado":
                cidades_opcoes = ["Selecione uma cidade"] + self.estados_cidades[estado]
            else:
                cidades_opcoes = ["Selecione um estado primeiro"]
            cidade = st.selectbox("Cidade", cidades_opcoes)

        return estado, cidade

    def preencher_campos_endereco(self):
        st.markdown("""
        <div class="subtitulo">
            <i class="fa-solid fa-map-location-dot" style="color:#2c3e50;"></i> Dados do Endereço
        </div>
        """, unsafe_allow_html=True)

        col3, col4 = st.columns(2)
        with col3:
            tipo_logradouro = st.text_input("Tipo de logradouro", placeholder="Ex: Rua, Avenida, Travessa")
            nome_logradouro = st.text_input("Nome do logradouro", placeholder="Ex: Aníbal Brandão")
            numero = st.text_input("Número", placeholder="Ex: 246")
        with col4:
            complemento = st.text_input("Complemento", placeholder="Ex: Loja 11")
            bairro = st.text_input("Bairro", placeholder="Ex: Nova Parnamirim")
            cep = st.text_input("CEP", placeholder="Ex: 59151-800")

        nome_local = st.text_input("Nome do local (opcional)", placeholder="Ex: Casa, Escritório")

        return tipo_logradouro, nome_logradouro, numero, complemento, bairro, cep, nome_local

    def validar_campos(self, estado, cidade, tipo_logradouro, nome_logradouro, numero, bairro):
        if (
            estado != "Selecione um estado"
            and cidade not in ["Selecione uma cidade", "Selecione um estado primeiro"]
            and tipo_logradouro.strip()
            and nome_logradouro.strip()
            and numero.strip()
            and bairro.strip()
        ):
            return True
        return False

    def cadastrar_endereco(self, estado, cidade, tipo_logradouro, nome_logradouro, numero, complemento, bairro, cep, nome_local):
        adicionar_endereco(
            tipo_logradouro.strip(),
            nome_logradouro.strip(),
            numero.strip(),
            complemento.strip(),
            bairro.strip(),
            cidade.strip(),
            estado.strip(),
            cep.strip(),
            nome_local.strip()
        )

    def exibir_popup_sucesso(self):
        placeholder = st.empty()
        with placeholder:
            st.markdown("""
                <div class="sucesso-popup">
                    <i class="fa-solid fa-circle-check"></i> Endereço cadastrado com sucesso!
                </div>
            """, unsafe_allow_html=True)
            time.sleep(2)
        placeholder.empty()
        st.session_state.show_popup = False
        st.rerun()

    def renderizar_pagina(self):
        self.exibir_titulo()
        estado, cidade = self.selecionar_estado_cidade()
        tipo_logradouro, nome_logradouro, numero, complemento, bairro, cep, nome_local = self.preencher_campos_endereco()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Cadastrar Endereço", use_container_width=True):
            if self.validar_campos(estado, cidade, tipo_logradouro, nome_logradouro, numero, bairro):
                self.cadastrar_endereco(estado, cidade, tipo_logradouro, nome_logradouro, numero, complemento, bairro, cep, nome_local)
                st.session_state.show_popup = True
                st.rerun()
            else:
                st.warning("⚠️ Preencha todos os campos obrigatórios (logradouro, número, bairro, estado e cidade).")

        if st.session_state.get("show_popup", False):
            self.exibir_popup_sucesso()


def main():
    Estilos.aplicar_css()
    app = CadastroEndereco()
    app.renderizar_pagina()

if __name__ == "__main__":
    main()
