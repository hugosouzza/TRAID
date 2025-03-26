# ============================================
#               PERSONAL PROJECT
#          TRAID - App de asesoramiento
# ============================================

import streamlit as st
import sqlite3
import hashlib
from datetime import date

st.set_page_config(page_title="TRAID", layout="centered")

# ---------------------- DB ----------------------
def crear_base_datos():
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 usuario TEXT UNIQUE,
                 email TEXT UNIQUE,
                 contrasena TEXT,
                 kyc_completed INTEGER DEFAULT 0,
                 risk_completed INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

def encriptar_contrasena(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

def registrar_usuario(usuario, email, contrasena):
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO usuarios (usuario, email, contrasena, kyc_completed, risk_completed) VALUES (?, ?, ?, 0, 0)",
                  (usuario, email, encriptar_contrasena(contrasena)))
        conn.commit()
        st.session_state.email = email
        st.session_state.step = "KYC"
    except sqlite3.IntegrityError:
        st.error("El usuario o email ya están registrados.")
    conn.close()

def verificar_usuario(usuario, contrasena):
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE usuario = ? AND contrasena = ?", (usuario, encriptar_contrasena(contrasena)))
    user = c.fetchone()
    conn.close()
    return user

def completar_kyc():
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    c.execute("UPDATE usuarios SET kyc_completed = 1 WHERE email = ?", (st.session_state.email,))
    conn.commit()
    conn.close()
    st.session_state.step = "Riesgo"

def completar_riesgo():
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    c.execute("UPDATE usuarios SET risk_completed = 1 WHERE email = ?", (st.session_state.email,))
    conn.commit()
    conn.close()
    st.session_state.step = "Dashboard"

# ------------------- KYC -------------------
def formulario_kyc():
    st.header("Formulario KYC")
    tipo = st.radio("Tipo de cliente", ["Persona Física", "Persona Jurídica"])
    st.divider()

    if tipo == "Persona Física":
        st.text_input("Nombre y Apellidos")
        st.selectbox("Tipo de Documento", ["DNI", "Pasaporte", "NIE"])
        st.text_input("Número de Documento")
        st.date_input("Fecha de Nacimiento", min_value=date(1950,1,1))
        st.text_input("Nacionalidad")
        st.text_input("País de Residencia")
        st.text_input("Dirección")
        st.text_input("Teléfono")
        st.text_input("Email")
        st.text_input("Situación Laboral")
        st.text_input("Actividad Empresarial")
        st.text_input("Patrimonio Aportado")

    else:
        st.text_input("Razón Social")
        st.selectbox("Tipo de Documento", ["CIF", "NIF"])
        st.text_input("Número de Documento")
        st.date_input("Fecha de Constitución")
        st.text_input("País de Constitución")
        st.text_input("Objeto Social")
        st.text_input("Actividad Real")
        st.text_input("Dirección Fiscal")
        st.text_input("Teléfono")
        st.text_input("Email")
        st.text_input("Ingresos Anuales Estimados")

    if st.button("Finalizar KYC"):
        completar_kyc()

# -------------- PERFIL DE RIESGO --------------
def clasificar_perfil(puntaje_total):
    if 10 <= puntaje_total <= 17:
        return "Conservador"
    elif 18 <= puntaje_total <= 25:
        return "Moderado"
    elif 26 <= puntaje_total <= 33:
        return "Agresivo"
    elif 34 <= puntaje_total <= 40:
        return "Muy Agresivo"
    else:
        return "Error"

def formulario_riesgo():
    st.header("Cuestionario de Perfil de Riesgo")

    preguntas = {
        "Objetivos de inversión": ["Preservar capital", "Crecimiento medio", "Oportunidades con riesgo", "Crecimiento fuerte y volátil"],
        "Pérdidas aceptables": ["5%", "15%", "35%", "55%"],
        "Reacción ante pérdidas": ["Vender todo", "Vender parte", "Mantener", "Comprar más"],
        "Expectativas de rendimiento": ["<3%", "3%-6%", "6%-10%", ">10%"],
        "Volatilidad aceptada": ["Nada", "Poca", "Normal", "Mucha"]
    }

    puntaje = 0
    for pregunta, opciones in preguntas.items():
        respuesta = st.radio(pregunta, opciones, key=pregunta)
        if respuesta:
            puntaje += opciones.index(respuesta) + 1

    if st.button("Enviar Cuestionario"):
        perfil = clasificar_perfil(puntaje)
        st.success(f"Tu perfil es: {perfil}")
        completar_riesgo()

# ----------------- DASHBOARD -----------------
def dashboard():
    st.title("Bienvenido a TRAID")
    st.success("Has completado el registro y perfilamiento.")
    st.info("Aquí irá tu panel de análisis e inversión.")

# ------------------- INICIO -------------------
def main():
    crear_base_datos()
    if "step" not in st.session_state:
        st.session_state.step = "Inicio"

    if st.session_state.step == "Inicio":
        st.markdown("""
            <div style='text-align: center; margin-top: 10%;'>
                <h1 style='font-size: 64px;'>TRAID</h1>
                <p style='font-size: 18px;'>Enjoy the best investment experience.</p>
                <br>
            </div>
        """, unsafe_allow_html=True)

        opcion = st.radio("", ["Log In", "Sign Up"], horizontal=True)

        if opcion == "Log In":
            st.subheader("Log In")
            usuario = st.text_input("DNI / CIF")
            contrasena = st.text_input("Contraseña", type="password")
            if st.button("Iniciar Sesión"):
                user = verificar_usuario(usuario, contrasena)
                if user:
                    st.session_state.email = user[2]
                    st.session_state.step = "Dashboard"
                else:
                    st.error("Credenciales incorrectas")
            st.markdown("<small><a href='#'>¿Olvidaste tu contraseña?</a></small>", unsafe_allow_html=True)

        elif opcion == "Sign Up":
            st.subheader("Sign Up")
            usuario = st.text_input("DNI / CIF")
            email = st.text_input("Email")
            pwd1 = st.text_input("Contraseña", type="password")
            pwd2 = st.text_input("Confirmar Contraseña", type="password")
            acepta = st.checkbox("I have read and understand the Privacy and Cookies Policy")

            if st.button("Crear Cuenta"):
                if not acepta:
                    st.warning("Debes aceptar la política de privacidad.")
                elif pwd1 != pwd2:
                    st.error("Las contraseñas no coinciden.")
                else:
                    registrar_usuario(usuario, email, pwd1)

    elif st.session_state.step == "KYC":
        formulario_kyc()
    elif st.session_state.step == "Riesgo":
        formulario_riesgo()
    elif st.session_state.step == "Dashboard":
        dashboard()
    else:
        st.error("Algo salió mal. Estado de sesión:")
        st.write(st.session_state)

if __name__ == '__main__':
    main()
