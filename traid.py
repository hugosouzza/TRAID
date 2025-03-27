import streamlit as st
import sqlite3
import hashlib
from PIL import Image

# ----------------------
# CONFIGURACIÓN
# ----------------------
st.set_page_config(page_title="TRAID", layout="centered")

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
    image = Image.open("traid_logo.png")  # La imagen de la pantalla de inicio
    st.image(image, use_column_width=True)

    st.markdown("""
        <h1 style='text-align: center; font-size: 30px;'>Bienvenido a <span style='color:#7552F2;'>Traid</span>, te estábamos esperando</h1>
        <p style='text-align: center; color: #555; font-size: 16px;'>
        <span style='color:#7552F2;'>Invertir sin saber, ahora es posible.</span><br>
        Bienvenido al futuro de tus finanzas, fuera complicaciones, fuera comisiones.<br>
        Hola a las <span style='color:#7552F2;'>Inversiones sin estrés</span>.
        </p>
    """, unsafe_allow_html=True)

    # Botón "Empecemos a crecer Juntos" (fondo morado, texto blanco)
    if st.button("Empecemos a crecer Juntos", key="signup", use_container_width=True):
        st.session_state.pantalla = "registro"  # Este no hace nada aún

    # Espacio
    st.markdown("<div style='margin: 20px;'></div>", unsafe_allow_html=True)

    # Botón "Iniciar sesión" (fondo blanco, borde morado, texto morado)
    if st.button("Iniciar sesión", key="login", use_container_width=True):
        st.session_state.pantalla = "login"  # Va al login

def pantalla_login():
    # Logo pequeño encima del Login (mismo logo que en la pantalla de inicio, más pequeño)
    image = Image.open("traid_intro.png")  # Usamos la misma imagen pero más pequeña
    st.image(image, use_column_width=False, width=150)  # Este es el logo pequeño que aparece encima del login

    st.markdown("<h2 style='text-align: center;'>Iniciar sesión</h2>", unsafe_allow_html=True)
    st.write("Accede con tu email o DNI")

    # Campo Email/DNI
    usuario_input = st.text_input("Introduce tu correo o DNI", key="usuario")

    # Campo Contraseña
    contrasena_input = st.text_input("Contraseña", type="password", key="contrasena")

    # Botón "Iniciar sesión"
    if st.button("Iniciar sesión", key="iniciar_sesion"):
        user = verificar_credenciales(usuario_input, contrasena_input)
        if user:
            st.success(f"Bienvenido, {user[1]} 👋")
            st.session_state.pantalla = "dashboard"
            st.session_state.usuario = user[1]
            st.session_state.email = user[3]
        else:
            st.error("Credenciales incorrectas")

    # Opción "No nos olvidamos de ti"
    st.checkbox("No nos olvidamos de ti", key="recuerdo")

    # Botón "Recuperar contraseña"
    st.markdown("<p style='text-align: center;'><a href='#' style='color:#7552F2;'>Recuperar Contraseña</a></p>", unsafe_allow_html=True)

    # Espacio entre los botones
    st.markdown("<div style='margin: 20px;'></div>", unsafe_allow_html=True)

    # Botones de redes sociales (Google, Facebook, Apple)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("google_logo.png", width=30)  # Asegúrate de que estas imágenes estén en el mismo directorio
    with col2:
        st.image("facebook_logo.png", width=30)  # Asegúrate de que estas imágenes estén en el mismo directorio
    with col3:
        st.image("apple_logo.png", width=30)  # Asegúrate de que estas imágenes estén en el mismo directorio

    st.markdown("""
        <div style="text-align: center;">
            <span style="font-size: 12px;">Puedes entrar también con</span>
        </div>
    """, unsafe_allow_html=True)

    # Espacio entre los botones
    st.markdown("<div style='margin: 20px;'></div>", unsafe_allow_html=True)

    # Botón para ir a la pantalla de inicio
    if st.button("← Volver", key="volver"):
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
