# ============================================
#               PERSONAL PROJECT
#          TRAID - App de asesoramiento
# ============================================

import streamlit as st
import sqlite3
import hashlib
from docx import Document
from io import BytesIO
import datetime

st.set_page_config(page_title="TRAID", layout="centered")

# --------------------------------------------
#              BASE DE DATOS
# --------------------------------------------
def crear_base_datos():
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 usuario TEXT UNIQUE,
                 email TEXT UNIQUE,
                 contrasena TEXT,
                 kyc_completed INTEGER,
                 risk_profile_completed INTEGER)''')
    conn.commit()
    conn.close()

def encriptar_contrasena(contrasena):
    return hashlib.sha256(contrasena.encode()).hexdigest()

def registrar_usuario(usuario, email, contrasena):
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO usuarios (usuario, email, contrasena, kyc_completed, risk_profile_completed) VALUES (?, ?, ?, 0, 0)",
                  (usuario, email, encriptar_contrasena(contrasena)))
        conn.commit()
        st.success("Cuenta creada correctamente. Vamos a conocerte mejor.")
        st.session_state.step = "KYC"
        st.session_state.email = email
    except sqlite3.IntegrityError:
        st.error("El email o usuario ya están registrados.")
    conn.close()

def verificar_usuario(usuario, contrasena):
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE usuario = ? AND contrasena = ?", (usuario, encriptar_contrasena(contrasena)))
    usuario = c.fetchone()
    conn.close()
    return usuario

def complete_kyc():
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    c.execute("UPDATE usuarios SET kyc_completed = 1 WHERE email = ?", (st.session_state.email,))
    conn.commit()
    conn.close()
    st.session_state.step = "Risk Profile"

def complete_risk_profile():
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    c.execute("UPDATE usuarios SET risk_profile_completed = 1 WHERE email = ?", (st.session_state.email,))
    conn.commit()
    conn.close()
    st.session_state.usuario_autenticado = True

# --------------------------------------------
# DASHBOARD
# --------------------------------------------
def mostrar_dashboard():
    st.sidebar.title("TRAID")
    menu = ["Resumen", "Información del Usuario", "Documentos", "Análisis", "Carteras", "Operaciones", "Propuestas", "Alertas"]
    opcion = st.sidebar.radio("Ir a:", menu)
    st.title(opcion)
    st.write("(Contenido en desarrollo)")

# --------------------------------------------
# APP PRINCIPAL
# --------------------------------------------
def main():
    crear_base_datos()

    if "usuario_autenticado" not in st.session_state:
        st.session_state.usuario_autenticado = False
    if "step" not in st.session_state:
        st.session_state.step = "Start"

    if st.session_state.usuario_autenticado:
        mostrar_dashboard()
    else:
        if st.session_state.step == "KYC":
            formulario_kyc()
        elif st.session_state.step == "Risk Profile":
            formulario_riesgo()
        else:
            st.title("TRAID")
            opcion = st.radio("", ["Log In", "Sign Up"], horizontal=True)

            if opcion == "Log In":
                st.subheader("Log In")
                usuario = st.text_input("DNI / CIF")
                contrasena = st.text_input("Contraseña", type="password")
                if st.button("Iniciar Sesión"):
                    u = verificar_usuario(usuario, contrasena)
                    if u:
                        st.session_state.usuario_autenticado = True
                        st.experimental_rerun()
                    else:
                        st.error("Credenciales incorrectas")
                st.markdown("<p style='font-size: 14px;'><a href='#'>¿Olvidaste tu contraseña?</a></p>", unsafe_allow_html=True)

            elif opcion == "Sign Up":
                st.subheader("Sign Up")
                usuario = st.text_input("DNI / CIF")
                email = st.text_input("Email")
                contrasena = st.text_input("Contraseña", type="password")
                confirmar = st.text_input("Confirmar Contraseña", type="password")
                privacidad = st.checkbox("I have read and understand the Privacy and Cookies Policy")

                if st.button("Crear Cuenta"):
                    if not privacidad:
                        st.error("Debes aceptar la política de privacidad para continuar.")
                    elif contrasena != confirmar:
                        st.error("Las contraseñas no coinciden")
                    else:
                        registrar_usuario(usuario, email, contrasena)

if __name__ == "__main__":
    main()
