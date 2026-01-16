import streamlit as st
from database import init_db, create_user, verify_user

def auth_screen():
    # Asegurar que la carpeta storage existe
    import os
    if not os.path.exists("storage"): os.makedirs("storage")
    init_db()

    st.markdown("""
        <div style='text-align:center; padding-top:30px; margin-bottom:20px;'>
            <h1 style='color:#00CC96; font-size:42px; margin:0;'>⚡DATASTRIKE</h1>
            <p style='color:#8a8d97; font-size:12px; letter-spacing:5px;'>Sports Analytic</p>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Iniciar Sesión", "Crear Cuenta"])

    with tab1:
        with st.form("login"):
            email = st.text_input("Correo Electrónico")
            password = st.text_input("Contraseña", type="password")
            if st.form_submit_button("INGRESAR"):
                if verify_user(email, password):
                    st.session_state.authenticated = True
                    st.session_state.user = email
                    st.rerun()
                else:
                    st.error("Correo o contraseña incorrectos")

    with tab2:
        with st.form("register"):
            new_email = st.text_input("Nuevo Correo")
            new_pass = st.text_input("Nueva Contraseña", type="password")
            confirm_pass = st.text_input("Confirmar Contraseña", type="password")
            
            if st.form_submit_button("REGISTRARSE"):
                if "@" not in new_email:
                    st.warning("Ingresa un correo válido")
                elif new_pass != confirm_pass:
                    st.error("Las contraseñas no coinciden")
                else:
                    if create_user(new_email, new_pass):
                        st.success("Cuenta creada. Ahora puedes iniciar sesión.")
                    else:
                        st.error("El usuario ya existe")

def check_auth():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        auth_screen()
        st.stop()