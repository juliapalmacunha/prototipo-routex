import streamlit as st
from database import listar_rotas, deletar_rota


class Estilos:
    @staticmethod
    def aplicar_css():
        st.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
        <style>
            .titulo-painel {
                text-align: center;
                color: #2c3e50;
                font-size: 28px;
                margin-bottom: 25px;
                font-weight: 600;
            }
            .rota-card {
                background-color: #ffffff;
                border-radius: 12px;
                padding: 16px 20px;
                margin-bottom: 15px;
                box-shadow: 0px 3px 8px rgba(0,0,0,0.08);
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .rota-texto {
                font-size: 16px;
                color: #333;
                line-height: 1.5;
            }
            .rota-nome {
                font-weight: 600;
                color: #2c3e50;
                font-size: 17px;
            }
            .stButton>button {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 14px;
                cursor: pointer;
                font-size: 14px;
                transition: all 0.2s ease-in-out;
            }
            .stButton>button:hover {
                background-color: #c0392b;
                transform: scale(1.03);
            }
        </style>
        """, unsafe_allow_html=True)


class RotasSalvas:

    def __init__(self):
        self.rotas = []

    def carregar_rotas(self):
        self.rotas = listar_rotas()

    def exibir_titulo(self):
        st.markdown("""
        <h2 class="titulo-painel">
            <i class="fa-solid fa-route"></i> Rotas Salvas
        </h2>
        """, unsafe_allow_html=True)

    def exibir_mensagem_vazia(self):
        st.info("Nenhuma rota salva ainda.")

    def exibir_rota(self, rota, index):
        enderecos_formatados = " ⮕ ".join(rota["enderecos"])
        col1, col2 = st.columns([4, 1])

        with col1:
            st.markdown(f"""
            <div class="rota-card">
                <div class="rota-texto">
                    <span class="rota-nome">
                        <i class="fa-solid fa-truck"></i> {rota['nome_rota']}
                    </span><br>
                    <i class="fa-solid fa-location-dot" style="color:#e67e22;"></i> {enderecos_formatados}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            if st.button("🗑️ Excluir", key=f"del_{index}"):
                deletar_rota(rota["nome_rota"])
                st.success(f"Rota '{rota['nome_rota']}' excluída com sucesso!")
                st.rerun()

    def exibir_rotas(self):
        
        if not self.rotas:
            self.exibir_mensagem_vazia()
        else:
            for i, rota in enumerate(self.rotas):
                self.exibir_rota(rota, i)

    def renderizar_pagina(self):
      
        self.exibir_titulo()
        self.carregar_rotas()
        self.exibir_rotas()


def main():
    Estilos.aplicar_css()
    pagina = RotasSalvas()
    pagina.renderizar_pagina()


if __name__ == "__main__":
    main()
