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
    st.session_state.step = "Dashboard"

# --------------------------------------------
#              FORMULARIO KYC
# --------------------------------------------
def formulario_kyc():
    if "tipo_cliente" not in st.session_state:
        st.session_state.tipo_cliente = None

    if st.session_state.tipo_cliente is None:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Persona Física")
            if st.button("Seleccionar Persona Física"):
                st.session_state.tipo_cliente = "Persona Física"
        with col2:
            st.subheader("Persona Jurídica")
            if st.button("Seleccionar Persona Jurídica"):
                st.session_state.tipo_cliente = "Persona Jurídica"

    if st.session_state.tipo_cliente:
        st.header(f"Formulario KYC - {st.session_state.tipo_cliente}")
        datos_cliente = {}

        if st.session_state.tipo_cliente == "Persona Física":
            datos_cliente["nombre_apellidos"] = st.text_input("Nombre y Apellidos")
            datos_cliente["tipo_documento"] = st.selectbox("Tipo de Documento", ["DNI", "Pasaporte", "NIE"])
            datos_cliente["numero_documento"] = st.text_input("Número de Documento")
            datos_cliente["fecha_nacimiento"] = st.date_input("Fecha de Nacimiento")
            datos_cliente["nacionalidad"] = st.text_input("Nacionalidad")
            datos_cliente["pais_residencia"] = st.text_input("País de Residencia")
            datos_cliente["direccion"] = st.text_input("Dirección")
            datos_cliente["telefono"] = st.text_input("Teléfono")
            datos_cliente["email"] = st.text_input("Email")
            datos_cliente["situacion_laboral"] = st.text_input("Situación Laboral")
            datos_cliente["actividad_empresa"] = st.text_input("Actividad Empresarial")
            datos_cliente["patrimonio"] = st.text_input("Patrimonio Aportado")
        else:
            datos_cliente["razon_social"] = st.text_input("Razón Social")
            datos_cliente["tipo_documento"] = st.selectbox("Tipo de Documento", ["CIF", "NIF"])
            datos_cliente["numero_documento"] = st.text_input("Número de Documento")
            datos_cliente["fecha_constitucion"] = st.date_input("Fecha de Constitución")
            datos_cliente["pais_constitucion"] = st.text_input("País de Constitución")
            datos_cliente["objeto_social"] = st.text_input("Objeto Social")
            datos_cliente["actividad_real"] = st.text_input("Actividad Real")
            datos_cliente["direccion"] = st.text_input("Dirección Fiscal")
            datos_cliente["telefono"] = st.text_input("Teléfono")
            datos_cliente["email"] = st.text_input("Email")
            datos_cliente["ingresos_anuales"] = st.text_input("Ingresos Anuales Estimados")

        if st.button("Finalizar KYC"):
            complete_kyc()
            st.experimental_rerun()

# --------------------------------------------
#         TEST DE PERFIL DE RIESGO (sin cambios aquí)
# --------------------------------------------
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
        return "Error en la clasificación"

def formulario_riesgo():
    st.write("## Cuestionario de Perfil de Riesgo")
    st.info("(Contenido temporal oculto para simplificar)")
    complete_risk_profile()

# --------------------------------------------
#                 DASHBOARD
# --------------------------------------------
def mostrar_dashboard():
    st.sidebar.title("TRAID")
    menu = ["Resumen", "Información del Usuario", "Documentos", "Análisis", "Carteras", "Operaciones", "Propuestas", "Alertas"]
    opcion = st.sidebar.radio("Ir a:", menu)
    st.title(opcion)
    st.write("(Contenido en desarrollo)")

# --------------------------------------------
#                 APP PRINCIPAL
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
        if st.session_state.step == "Start":
            st.markdown("""
                <div style='text-align: center; margin-top: 10%;'>
                    <h1 style='font-size: 64px;'>TRAID</h1>
                    <p style='font-size: 20px;'>Disfruta de una experiencia personalizada de inversión.</p>
                    <br>
                    <form>
                        <input type="submit" value="LOG IN" onclick="window.location.href='#login'" style='width: 200px; height: 45px; font-size: 16px; background-color: black; color: white; border: none; margin-bottom: 10px;'>
                        <br>
                        <input type="submit" value="SIGN UP" onclick="window.location.href='#signup'" style='width: 200px; height: 45px; font-size: 16px; background-color: white; color: black; border: 1px solid black;'>
                    </form>
                </div>
            """, unsafe_allow_html=True)

            opcion = st.radio("", ["Login", "Sign Up"], horizontal=True)

            if opcion == "Login":
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

        elif st.session_state.step == "KYC":
            formulario_kyc()

        elif st.session_state.step == "Risk Profile":
            formulario_riesgo()

        elif st.session_state.step == "Dashboard":
            st.session_state.usuario_autenticado = True
            st.experimental_rerun()

if __name__ == "__main__":
    main()

