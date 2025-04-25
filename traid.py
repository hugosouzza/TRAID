import streamlit as st
import sqlite3
import hashlib
from PIL import Image

# ----------------------
# CONFIGURACIÓN
# ----------------------
st.set_page_config(page_title="TRAID", layout="wide")

# ----------------------
# BASE DE DATOS
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

crear_base_datos()

# ----------------------
# FUNCIONES AUXILIARES
# ----------------------
def encriptar_contrasena(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

def verificar_credenciales(usuario_o_email, contrasena):
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE dni = ? OR email = ?", (usuario_o_email, usuario_o_email))
    user = c.fetchone()
    conn.close()
    if user and user[6] == encriptar_contrasena(contrasena):
        return user
    return None

# ----------------------
# PANTALLAS
# ----------------------

# Pantalla de inicio (Dashboard)
def pantalla_dashboard():
    image = Image.open("traid_logo.png")
    st.image(image, use_column_width=True)

    st.markdown("""
        <h2 style='text-align: center;'>Tu Dashboard</h2>
        <p style='text-align: center;'>Aquí puedes ver toda la información relevante de tus inversiones.</p>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image("me_logo.png", width=50)
    with col2:
        st.image("news_logo.png", width=50)
    with col3:
        st.image("portfolio_logo.png", width=50)
    with col4:
        st.image("operations_logo.png", width=50)
    with col5:
        st.image("sofia_logo.png", width=50)

    st.markdown("<div style='text-align: center;'><a href='#' style='color:#7552F2;'>🏠 Volver al inicio</a></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'><a href='#' style='color:#7552F2;'>← Volver atrás</a></div>", unsafe_allow_html=True)

# Pantalla de inicio

def pantalla_inicio():
    col1, col2 = st.columns([1, 2])

    with col1:
        image = Image.open("traid_logo.png")
        st.image(image, use_column_width=True)

    with col2:
        st.markdown("""
            <div style='padding: 20px 40px;'>
                <h1 style='font-size: 36px; color: #333;'>Bienvenido a <span style='color:#7552F2;'>Traid</span>, te estábamos esperando</h1>
                <p style='font-size: 18px; color: #555;'>
                    <span style='color:#7552F2;'>Invertir sin saber, ahora es posible.</span><br>
                    Bienvenido al futuro de tus finanzas, fuera complicaciones, fuera comisiones.<br>
                    Hola a las <span style='color:#7552F2;'>Inversiones sin estrés</span>.
                </p>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Empecemos a crecer Juntos", key="signup", use_container_width=True):
            st.session_state.pantalla = "registro"

        st.markdown("<div style='margin: 20px;'></div>", unsafe_allow_html=True)

        if st.button("Iniciar sesión", key="login", use_container_width=True):
            st.session_state.pantalla = "login"

# Pantalla de inicio de sesión
def pantalla_login():
    image = Image.open("traid_logo.png")
    st.image(image, use_column_width=False, width=150)

    st.markdown("<h2 style='text-align: center;'>Iniciar sesión</h2>", unsafe_allow_html=True)
    st.write("Accede con tu email o DNI")

    usuario_input = st.text_input("Introduce tu correo o DNI", key="usuario")
    contrasena_input = st.text_input("Contraseña", type="password", key="contrasena")

    if st.button("Iniciar sesión", key="iniciar_sesion"):
        user = verificar_credenciales(usuario_input, contrasena_input)
        if user:
            st.success(f"Bienvenido, {user[1]} 👋")
            st.session_state.pantalla = "dashboard"
            st.session_state.usuario = user[1]
            st.session_state.email = user[3]
        else:
            st.error("Credenciales incorrectas")

    st.checkbox("No nos olvidamos de ti", key="recuerdo")

    st.markdown("<p style='text-align: center;'><a href='#' style='color:#7552F2;'>Recuperar Contraseña</a></p>", unsafe_allow_html=True)
    st.markdown("<div style='margin: 20px;'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("google_logo.png", width=50)
    with col2:
        st.image("facebook_logo.png", width=50)
    with col3:
        st.image("apple_logo.png", width=50)

    st.markdown("""
        <div style="text-align: center;">
            <span style="font-size: 12px;">Puedes entrar también con</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin: 20px;'></div>", unsafe_allow_html=True)

    if st.button("← Volver", key="volver"):
        st.session_state.pantalla = "inicio"

# ----------------------
# MAIN
# ----------------------
def main():
    if "pantalla" not in st.session_state:
        st.session_state.pantalla = "inicio"

    if st.session_state.pantalla == "inicio":
        pantalla_inicio()
    elif st.session_state.pantalla == "login":
        pantalla_login()
    elif st.session_state.pantalla == "dashboard":
        pantalla_dashboard()
    elif st.session_state.pantalla == "registro":
        pantalla_registro()

if __name__ == '__main__':
    main()
