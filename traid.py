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

# Pantalla de inicio
def pantalla_inicio():
    image = Image.open("traid_logo.png")  # La imagen de la pantalla de inicio
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
        st.session_state.pantalla = "registro"  # Redirige a la pantalla de registro

    # Espacio
    st.markdown("<div style='margin: 20px;'></div>", unsafe_allow_html=True)

    # Botón "Iniciar sesión"
    if st.button("Iniciar sesión", key="login", use_container_width=True):
        st.session_state.pantalla = "login"  # Va al login

# Pantalla de inicio de sesión
def pantalla_login():
    # Logo pequeño encima del Login
    image = Image.open("traid_logo.png")  # Usamos la misma imagen pero más pequeña
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
        st.image("google_logo.png", width=50)  # Asegúrate de que estas imágenes estén en el mismo directorio
    with col2:
        st.image("facebook_logo.png", width=50)  # Asegúrate de que estas imágenes estén en el mismo directorio
    with col3:
        st.image("apple_logo.png", width=50)  # Asegúrate de que estas imágenes estén en el mismo directorio

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

# Pantalla de Sofia (Chat Interactivo KYC)
def pantalla_sofia():
    st.markdown("<h2 style='text-align: center; color:#7552F2;'>¡Hola! Soy Sofia, tu nueva asesora financiera. ¡Vamos por esas metas!</h2>", unsafe_allow_html=True)
    st.write("Voy a hacerte unas preguntas para poder ayudarte mejor. Todo es muy sencillo y rápido.")

    # Preguntas del KYC para persona física
    nombre_completo = st.text_input("¿Cuál es tu nombre completo?")
    dni = st.text_input("¿Cuál es tu DNI/CIF?")
    correo = st.text_input("¿Cuál es tu correo electrónico?")
    situacion_laboral = st.text_input("¿Cuál es tu ocupación o situación laboral?")
    ingresos_mensuales = st.text_input("¿Cuál es tu ingreso mensual aproximado?")

    # Botón de continuar al siguiente paso
    if st.button("Continuar", key="continuar_sofia"):
        if nombre_completo and dni and correo and situacion_laboral and ingresos_mensuales:
            # Guardamos los datos en la base de datos
            conn = sqlite3.connect("usuarios.db")
            c = conn.cursor()
            c.execute('''
                INSERT INTO usuarios (nombre, dni, email, telefono) 
                VALUES (?, ?, ?, ?)
            ''', (nombre_completo, dni, correo, situacion_laboral))
            conn.commit()
            conn.close()
            st.success("¡Datos guardados correctamente! Vamos a continuar.")
            st.session_state.pantalla = "verificacion_numero"  # Avanzamos a la siguiente pantalla
        else:
            st.error("Por favor, completa todos los campos.")

# Pantalla de verificación de número (simulada)
def pantalla_verificacion_numero():
    st.markdown("<h2 style='text-align: center;'>¡Vamos a verificar que eres tú!</h2>", unsafe_allow_html=True)
    st.write("Se enviará un código de confirmación a tu número para conectarte con la aplicación.")

    # Campo para ingresar número
    telefono_input = st.text_input("Introduce tu número de teléfono", placeholder="+34 123 000 111 222", key="telefono")

    # Botón de continuar
    if st.button("Continuar", key="continuar_verificacion"):
        # Simulación del paso de verificación
        st.session_state.pantalla = "verificacion_codigo"  # Avanzar a la siguiente pantalla

# Pantalla de verificación del código de 4 dígitos
def pantalla_verificacion_codigo():
    st.markdown("<h2 style='text-align: center;'>Introduce el código de 4 dígitos que le hemos enviado</h2>", unsafe_allow_html=True)
    st.write("Código enviado a tu número: +34 123 000 111 222")

    # Campos para los 4 dígitos
    codigo_input = [st.text_input(f"Digite el número {i+1}", max_chars=1, key=f"codigo_{i}") for i in range(4)]

    # Botón para completar la verificación
    if st.button("Unite y toma el control de tus finanzas", key="finalizar_verificacion"):
        # Avanzar a la pantalla Sofia (pantalla de continuación)
        st.session_state.pantalla = "sofia"

# Pantalla de Sofia
def pantalla_sofia():
    st.title("¡Bienvenido a Sofia!")
    st.write("Esta es la siguiente pantalla después de la verificación de tu número. Aquí irán más detalles más adelante.")

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
        pantalla_registro()
    elif st.session_state.pantalla == "verificacion_numero":
        pantalla_verificacion_numero()
    elif st.session_state.pantalla == "verificacion_codigo":
        pantalla_verificacion_codigo()
    elif st.session_state.pantalla == "sofia":
        pantalla_sofia()

if __name__ == '__main__':
    main()
