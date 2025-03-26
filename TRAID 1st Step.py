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

# --------------------------------------------
#         TEST DE PERFIL DE RIESGO (REACTIVADO)
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

    preguntas = {
        "Objetivos de inversión": {
            "opciones": [
                "Preservar el capital y proteger mi inversión",
                "Crecimiento medio asumiendo fluctuaciones moderadas",
                "Aprovechar oportunidades asumiendo fluctuaciones elevadas",
                "Crecimiento fuerte asumiendo fluctuaciones muy elevadas y altos riesgos de pérdida"
            ],
            "peso": 0.25
        },
        "Nivel de pérdidas potenciales": {
            "opciones": ["Máximo 5%", "Máximo 15%", "Máximo 35%", "Máximo 55%"],
            "peso": 0.25
        },
        "Reacción ante pérdidas": {
            "opciones": [
                "Vender todo para evitar más pérdidas",
                "Vender una parte para limitar las pérdidas",
                "Mantener la inversión esperando recuperación",
                "Comprar más aprovechando el precio bajo"
            ],
            "peso": 0.15
        },
        "Expectativas de rendimiento": {
            "opciones": [
                "Menos del 3% (muy bajo riesgo)",
                "Entre 3% y 6% (moderado)",
                "Entre 6% y 10% (elevado)",
                "Más del 10% (muy alto)"
            ],
            "peso": 0.15
        },
        "Comodidad con la volatilidad": {
            "opciones": [
                "Muy incómodo, preferiría estabilidad",
                "Algo incómodo, pero dispuesto a asumir cierta volatilidad",
                "Cómodo, entiendo que es parte de invertir a largo plazo",
                "Muy cómodo, buscaría aprovechar la volatilidad"
            ],
            "peso": 0.10
        },
        "Conocimiento financiero": {
            "opciones": ["Nulo", "Bajo", "Medio", "Elevado o Muy elevado"],
            "peso": 0.02
        },
        "Horizonte temporal": {
            "opciones": ["Menos de 1 año", "Entre 1 y 3 años", "Entre 3 y 5 años", "Más de 5 años"],
            "peso": 0.02
        },
        "Porcentaje de patrimonio invertido": {
            "opciones": ["Menos del 5%", "Entre el 5% y el 25%", "Entre el 25% y el 50%", "Más del 50%"],
            "peso": 0.02
        },
        "Ingresos anuales": {
            "opciones": ["Menos de 25,000€", "Entre 25,000€ y 50,000€", "Entre 50,000€ y 100,000€", "Más de 100,000€"],
            "peso": 0.02
        },
        "Necesidades de liquidez": {
            "opciones": ["Más del 75%", "Entre el 50% y el 75%", "Entre el 25% y el 50%", "Ninguna"],
            "peso": 0.02
        }
    }

    respuestas = []
    for pregunta, detalles in preguntas.items():
        respuesta = st.radio(pregunta, detalles["opciones"])
        if respuesta:
            puntaje = (detalles["opciones"].index(respuesta) + 1) * detalles["peso"]
            respuestas.append(puntaje)

    if st.button("Enviar Cuestionario"):
        if len(respuestas) == len(preguntas):
            total = round(sum(respuestas) * 10)
            perfil = clasificar_perfil(total)
            st.success(f"Tu perfil de riesgo es: {perfil}")
            complete_risk_profile()
        else:
            st.warning("Responde todas las preguntas antes de enviar.")


