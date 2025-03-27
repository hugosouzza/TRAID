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
        <h1 style='text-align: center; font-size: 30px;'>Bienvenido a <span style='color:#7552F2;'>Traid</span>, te estábamos esperando</h1>
        <p style='text-align: center; color: #555; font-size: 16px;'>
        <span style='color:#7552F2;'>Invertir sin saber, ahora es posible.</span><br>
        Bienvenido al futuro de tus finanzas, fuera complicaciones, fuera comisiones.<br>
        Hola a las <span style='color:#7552F2;'>Inversiones sin estrés</span>.
        </p>
    """, unsafe_allow_html=True)

    # Botones centrados
    st.markdown("<div style='display: flex; flex-direction: column; align-items: center;'>", unsafe_allow_html=True)

    # Botón 1 – REGISTRO (desactivado por ahora)
    if st.button("Empecemos a crecer Juntos", key="signup"):
        pass  # No hace nada aún

    st.markdown("<div style='margin: 10px;'></div>", unsafe_allow_html=True)

    # Botón 2 – LOGIN (funciona)
    if st.button("Iniciar sesión", key="login"):
        st.session_state.pantalla = "login"

    st.markdown("</div>", unsafe_allow_html=True)

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
