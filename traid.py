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

def registrar_usuario(nombre, dni, correo, usuario, contrasena):
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    try:
        c.execute('''INSERT INTO usuarios (nombre, dni, email, usuario, contrasena, verificado, kyc_completado, riesgo_completado)
                    VALUES (?, ?, ?, ?, ?, 0, 0, 0)''', 
                    (nombre, dni, correo, usuario, encriptar_contrasena(contrasena)))
        conn.commit()
        st.success("Cuenta creada con éxito!")
        st.session_state.pantalla = "login"
    except sqlite3.IntegrityError:
        st.error("El DNI o correo electrónico ya está registrado.")
    conn.close()

# ----------------------
# PANTALLAS
# ----------------------
def pantalla_inicio():
    image = Image.open("traid_intro.png")  # La imagen de la pantalla de inicio
    st.image(image, use_column_width=True)  # Ajuste para que ocupe el ancho total

    st.markdown("""
        <h1 style='text-align: center; font-size: 30px;'>Bienvenido a <span style='color:#7552F2;'>Traid</span>, te estábamos esperando</h1>
        <p style='text-align: center; color: #555; font-size: 16px;'>
        <span style='color:#7552F2;'>Invertir sin saber, ahora es posible.</span><br>
        Bienvenido al futuro de tus finanzas, fuera complicaciones, fuera comisiones.<br>
        Hola a las <span style='color:#7552F2;'>Inversiones sin estrés</span>.
        </p>
    """, unsafe_allow_html=True)

    # Botón "Empecemos a crecer Juntos"
    if st.button("Empecemos a crecer Juntos", key="signup", use_container_width=True):
        st.session_state.pantalla = "registro"  # Este no hace nada aún

    # Espacio
    st.markdown("<div style='margin: 20px;'></div>", unsafe_allow_html=True)

    # Botón "Iniciar sesión"
    if st.button("Iniciar sesión", key="login", use_container_width=True):
        st.session_state.pantalla = "login"  # Va al login

def pantalla_registro():
    # Logo pequeño encima del registro
    image = Image.open("traid_intro.png")  # Usamos la misma imagen pero más pequeña
    st.image(image, use_column_width=False, width=150)  # Este es el logo pequeño

    st.markdown("<h2 style='text-align: center;'>¡Creemos tu cuenta!</h2>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center;'>Estás a un paso de alcanzar tus metas</h5>", unsafe_allow_html=True)

    nombre = st.text_input("Nombre Completo")
    dni = st.text_input("DNI")
    correo = st.text_input("Correo electrónico")
    usuario = st.text_input("Nombre de Usuario")
    contrasena = st.text_input("Contraseña", type="password")
    repetir_contrasena = st.text_input("Repetir Contraseña", type="password")

    if st.button("Crear Cuenta"):
        if contrasena != repetir_contrasena:
            st.error("Las contraseñas no coinciden.")
        elif not nombre or not dni or not correo or not usuario or not contrasena:
            st.error("Por favor, llena todos los campos.")
        else:
            registrar_usuario(nombre, dni, correo, usuario, contrasena)

    if st.button("← Volver"):
        st.session_state.pantalla = "inicio"

# ----------------------
# MAIN
# ----------------------
def main():
    if "pantalla" not in st.session_state:
        st.session_state.pantalla = "inicio"

    if st.session_state.pantalla == "inicio":
        pantalla_inicio()
    elif st.session_state.pantalla == "registro":
        pantalla_registro()
    elif st.session_state.pantalla == "login":
        pantalla_login()
    elif st.session_state.pantalla == "dashboard":
        dashboard()

if __name__ == '__main__':
    main()
