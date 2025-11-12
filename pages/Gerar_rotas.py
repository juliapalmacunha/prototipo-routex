import streamlit as st
import folium
from streamlit_folium import st_folium
import openrouteservice
from geopy.geocoders import Nominatim
from database import listar_enderecos, salvar_rota
from streamlit.components.v1 import html


class Estilos:
    @staticmethod
    def aplicar_css():
        st.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
        <style>
        body {
            background-color: #f6f8fa;
            font-family: "Segoe UI", sans-serif;
        }
        h1 {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 10px;
            font-weight: 700;
        }
        hr {
            margin: 20px 0;
        }
        .stMarkdown p, label, span {
            color: #2c3e50 !important;
            font-size: 15px;
        }
        .stSelectbox, .stMultiSelect {
            background-color: white;
        }
        input[type="text"] {
            border-radius: 10px !important;
            border: 1px solid #ccc !important;
            padding: 10px !important;
            font-size: 15px !important;
            width: 100%;
        }
        .stButton>button {
            border: none;
            border-radius: 10px;
            padding: 10px 16px;
            font-size: 15px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.25s ease-in-out;
        }
        .stButton>button:hover {
            transform: scale(1.03);
        }
        .stButton>button:first-child {
            background-color: #1abc9c !important;
            color: white !important;
        }
        button:has(i.fa-floppy-disk),
        button:has(span:contains("Salvar")) {
            background-color: #3498db !important;
            color: white !important;
        }
        button:has(i.fa-trash),
        button:has(span:contains("Limpar")) {
            background-color: #e74c3c !important;
            color: white !important;
        }
        .map-container {
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            margin-top: 15px;
        }
        .stAlert {
            border-radius: 10px !important;
        }
        </style>
        """, unsafe_allow_html=True)


class CriarRota:
    def __init__(self):
        self.enderecos = listar_enderecos()
        self.geolocator = Nominatim(user_agent="rota_app", timeout=5)
        self.client = openrouteservice.Client(
            key="eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImVkNjJmNTg2MTJiMTRlMDI5M2ExMTg4MmFhY2E1MzRmIiwiaCI6Im11cm11cjY0In0="
        )

        for key, value in {
            "enderecos_selecionados": [],
            "rota_gerada": False,
            "map_html": None
        }.items():
            if key not in st.session_state:
                st.session_state[key] = value

    def exibir_titulo(self):
        st.markdown("<h1><i class='fa-solid fa-map-location-dot'></i> Criar Rota</h1>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

    def exibir_formulario(self):
        if not self.enderecos:
            st.info("Nenhum endereço cadastrado ainda.")
            st.stop()

        opcoes = [
            f"{e['tipo_logradouro']} {e['nome_logradouro']}, {e['número']} - {e['cidade']}/{e['estado']}"
            for e in self.enderecos
        ]

        st.markdown(
            '<p><i class="fa-solid fa-map-pin" style="color:#16a085;"></i> '
            '<b>Selecione os endereços para montar a rota:</b></p>',
            unsafe_allow_html=True
        )

        selecionados = st.multiselect(
            "",
            options=opcoes,
            default=st.session_state["enderecos_selecionados"]
        )

        if selecionados != st.session_state["enderecos_selecionados"]:
            st.session_state["enderecos_selecionados"] = selecionados

    def gerar_rota(self):
        if len(st.session_state["enderecos_selecionados"]) < 2:
            st.warning("Selecione pelo menos dois endereços para gerar uma rota.")
            return

        coordenadas = []
        with st.spinner("Convertendo endereços em coordenadas..."):
            for endereco in st.session_state["enderecos_selecionados"]:
                location = self.geolocator.geocode(endereco)
                if location:
                    coordenadas.append((location.longitude, location.latitude))

        if len(coordenadas) < 2:
            st.warning("Alguns endereços não foram reconhecidos. Verifique e tente novamente.")
            return

        rota = self.client.directions(
            coordinates=coordenadas,
            profile='driving-car',
            format='geojson',
            optimize_waypoints=True
        )

        m = folium.Map(location=[coordenadas[0][1], coordenadas[0][0]], zoom_start=12)

        for i, (lon, lat) in enumerate(coordenadas):
            folium.Marker([lat, lon], tooltip=f"Parada {i+1}").add_to(m)

        folium.GeoJson(rota, name="Rota").add_to(m)
        folium.LayerControl().add_to(m)

        st.session_state["map_html"] = m._repr_html_()
        st.session_state["rota_gerada"] = True
        st.success("✅ Rota gerada com sucesso!")

    def salvar_rota(self):
        nome_rota = st.text_input("💬 Dê um nome para esta rota:")
        if st.button("💾 Salvar Rota"):
            if not nome_rota:
                st.warning("Dê um nome à rota antes de salvar.")
                return
            salvar_rota(nome_rota, st.session_state["enderecos_selecionados"])
            st.success(f"✅ Rota '{nome_rota}' salva com sucesso!")
            self.limpar_selecao()

    def limpar_selecao(self):
        st.session_state["enderecos_selecionados"] = []
        st.session_state["rota_gerada"] = False
        st.session_state["map_html"] = None
        st.success("Seleção limpa!")
        st.rerun()

    def exibir_mapa(self):
        if st.session_state["rota_gerada"] and st.session_state["map_html"]:
            st.subheader("🗺️ Mapa da Rota")
            st.markdown('<div class="map-container">', unsafe_allow_html=True)
            html(st.session_state["map_html"], height=500)
            st.markdown('</div>', unsafe_allow_html=True)
            self.salvar_rota()

    def renderizar_pagina(self):
        Estilos.aplicar_css()
        self.exibir_titulo()
        self.exibir_formulario()

        st.write("---")
        if st.button("🚗 Gerar Rota"):
            self.gerar_rota()

        self.exibir_mapa()

        if st.button("🧹 Limpar seleção"):
            self.limpar_selecao()


if __name__ == "__main__":
    app = CriarRota()
    app.renderizar_pagina()
