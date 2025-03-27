import streamlit as st
import sqlite3
import hashlib
from PIL import Image

# ----------------------
# CONFIGURACIÓN
# ----------------------
st.set_page_config(page_title="TRAID", layout="centered")

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
def pantalla_inicio():
    image = Image.open("traid_intro.png")
    st.image(image, use_column_width=True)

    st.markdown("""
    <h1 style='text-align: center; font-size: 36px;'>Bienvenido a <span style='color:#7552F2;'>Traid</span></h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='text-align: center; color: #555; font-size: 16px;'>
    Invertir sin saber, ahora es posible.<br>
    Un gusto saludarte desde donde el futuro de tus finanzas está cuidado, sin complicación y fuera de comisiones.
    </p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Iniciar sesión"):
            st.session_state.pantalla = "login"
    with col2:
        if st.button("Empecemos a crecer juntos"):
            st.session_state.pantalla = "registro"

    st.markdown("""
    <div style='text-align: center; margin-top: 30px;'>
        <span style='height: 10px; width: 10px; background-color: #7552F2; border-radius: 50%; display: inline-block; margin: 0 5px;'></span>
        <span style='height: 10px; width: 10px; background-color: #ddd; border-radius: 50%; display: inline-block; margin: 0 5px;'></span>
        <span style='height: 10px; width: 10px; background-color: #ddd; border-radius: 50%; display: inline-block; margin: 0 5px;'></span>
    </div>
    """, unsafe_allow_html=True)

def pantalla_login():
    st.markdown("<h2 style='text-align: center;'>Iniciar sesión</h2>", unsafe_allow_html=True)
    st.write("Accede con tu email o DNI")

    usuario_input = st.text_input("Email o DNI")
    contrasena_input = st.text_input("Contraseña", type="password")

    if st.button("Entrar"):
        user = verificar_credenciales(usuario_input, contrasena_input)
        if user:
            st.success(f"Bienvenido, {user[1]} 👋")
            st.session_state.pantalla = "dashboard"
            st.session_state.usuario = user[1]
            st.session_state.email = user[3]
        else:
            st.error("Credenciales incorrectas")

    if st.button("← Volver"):
        st.session_state.pantalla = "inicio"

def dashboard():
    st.title(f"Hola {st.session_state.get('usuario', '')} 👋")
    st.write("Has iniciado sesión correctamente. Aquí irá tu panel de control 🧠")

    if st.button("Cerrar sesión"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
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
        dashboard()
    elif st.session_state.pantalla == "registro":
        st.info("Aquí irá el registro muy pronto...")

if __name__ == '__main__':
    main()
