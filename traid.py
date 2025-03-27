# ============================================
#               PERSONAL PROJECT
#          TRAID - App de asesoramiento
# ============================================
import streamlit as st
import sqlite3
import hashlib
from PIL import Image

# ----------------------
# CONFIGURACIÓN
# ----------------------
st.set_page_config(page_title="TRAID", layout="centered")

# ----------------------
# BASE DE DATOS (Ferrari style)
# ----------------------

def crear_base_datos():
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            dni TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            usuario TEXT,
            telefono TEXT,
            contrasena TEXT NOT NULL,
            verificado INTEGER DEFAULT 0,
            kyc_completado INTEGER DEFAULT 0,
            riesgo_completado INTEGER DEFAULT 0,
            fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

crear_base_datos()  # Se ejecuta al abrir la app

# ----------------------
# ENCRIPTADO DE CONTRASEÑAS
# ----------------------

def encriptar_contrasena(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

# ----------------------
# PANTALLA DE BIENVENIDA VISUAL
# ----------------------

def main():
    # Imagen de bienvenida (usa la que subiste como captura)
    image = Image.open("traid_intro.png")  # Asegúrate de subir esta imagen a tu repo
    st.image(image, use_column_width=True)

    # Título
    st.markdown("""
    <h1 style='text-align: center;'>Bienvenido a <span style='color:#7552F2;'>Traid</span></h1>
    """, unsafe_allow_html=True)

    # Subtítulo
    st.markdown("""
    <p style='text-align: center; color: #555; font-size: 16px;'>
    Invertir sin saber, ahora es posible.<br>
    Un gusto saludarte desde donde el futuro de tus finanzas está cuidado, sin complicación y fuera de comisiones.
    </p>
    """, unsafe_allow_html=True)

    # Botones
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        <button style='background-color: #7552F2; color: white; padding: 12px 24px; border: none; border-radius: 5px; font-size: 16px; width: 100%;'>
            Empecemos a crecer juntos
        </button>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <button style='background-color: white; color: #7552F2; border: 2px solid #7552F2; padding: 12px 24px; border-radius: 5px; font-size: 16px; width: 100%;'>
            Iniciar sesión
        </button>
        """, unsafe_allow_html=True)

    # Puntos de navegación (simulados)
    st.markdown("""
    <div style='text-align: center; margin-top: 30px;'>
        <span style='height: 10px; width: 10px; background-color: #7552F2; border-radius: 50%; display: inline-block; margin: 0 5px;'></span>
        <span style='height: 10px; width: 10px; background-color: #ddd; border-radius: 50%; display: inline-block; margin: 0 5px;'></span>
        <span style='height: 10px; width: 10px; background-color: #ddd; border-radius: 50%; display: inline-block; margin: 0 5px;'></span>
    </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()


