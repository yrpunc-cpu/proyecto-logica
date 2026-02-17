import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# ==============================
# CONFIGURACIÓN GENERAL
# ==============================

ARCHIVO = "datos_estudiantes.csv"
st.set_page_config(page_title="Sistema de Análisis Estudiantil", layout="wide")

# ==============================
# SIDEBAR - CONTROL DE ACCESO
# ==============================

st.sidebar.title("🔐 Acceso al Sistema")
modo = st.sidebar.selectbox("Seleccionar modo:", ["Estudiante", "Administrador"])

if modo == "Administrador":
    password = st.sidebar.text_input("Contraseña", type="password")
    if password != "admin123":
        st.warning("Acceso restringido.")
        st.stop()

# ==============================
# MODO ESTUDIANTE
# ==============================

if modo == "Estudiante":

    st.title("📝 Encuesta Académica")
    st.write("Complete la siguiente información")

    with st.form("form_estudiante"):
        carrera = st.text_input("Carrera")
        semestre = st.selectbox("Semestre", ["1", "2", "3", "4", "5"])
        trabaja = st.radio("¿Trabaja?", ["si", "no"])
        estres = st.slider("Nivel de Estrés (1-5)", 1, 5)
        horas_estudio = st.number_input("Horas de estudio diarias", 0.0, 12.0)

        submit = st.form_submit_button("Enviar")

    if submit:

        datos = {
            "Carrera": carrera,
            "Semestre": semestre,
            "Trabaja": trabaja,
            "Estres": estres,
            "Horas_estudio": horas_estudio
        }

        df_nuevo = pd.DataFrame([datos])

        if os.path.exists(ARCHIVO):
            df_nuevo.to_csv(ARCHIVO, mode="a", header=False, index=False)
        else:
            df_nuevo.to_csv(ARCHIVO, index=False)

        st.success("✅ Datos enviados correctamente.")

        # -------------------------
        # REGLAS LÓGICAS
        # -------------------------
        # P: Trabaja
        # Q: Estres ≥ 4
        # R: Riesgo académico alto

        P = trabaja == "si"
        Q = estres >= 4
        R = P and Q

        if R:
            st.warning("⚠ Según la regla lógica (P ∧ Q → R), existe posible riesgo académico alto.")

# ==============================
# MODO ADMINISTRADOR
# ==============================

if modo == "Administrador":

    st.title("📊 Panel Administrativo")
    st.write("Visualización y análisis de datos")

    if os.path.exists(ARCHIVO):

        df = pd.read_csv(ARCHIVO)

        # -------------------------
        # MÉTRICAS PRINCIPALES
        # -------------------------

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Registros", len(df))
        col2.metric("Promedio Estrés", round(df["Estres"].mean(), 2))
        col3.metric("Promedio Horas Estudio", round(df["Horas_estudio"].mean(), 2))

        st.divider()

        # -------------------------
        # GRÁFICO 1 - DISTRIBUCIÓN ESTRÉS
        # -------------------------

        st.subheader("Distribución del Nivel de Estrés")

        fig1, ax1 = plt.subplots()
        df["Estres"].hist()
        ax1.set_xlabel("Nivel de Estrés")
        ax1.set_ylabel("Frecuencia")
        st.pyplot(fig1)

        # -------------------------
        # GRÁFICO 2 - TRABAJA
        # -------------------------

        st.subheader("Estudiantes que trabajan")

        fig2, ax2 = plt.subplots()
        df["Trabaja"].value_counts().plot(kind="bar")
        ax2.set_xlabel("Trabaja")
        ax2.set_ylabel("Cantidad")
        st.pyplot(fig2)

        # -------------------------
        # TABLA DE DATOS
        # -------------------------

        st.subheader("Base de datos completa")
        st.dataframe(df, use_container_width=True)

        # -------------------------
        # DESCARGA CSV
        # -------------------------

        st.download_button(
            "⬇ Descargar base de datos",
            df.to_csv(index=False),
            "datos_estudiantes.csv",
            "text/csv"
        )

    else:
        st.info("Aún no hay datos registrados.")
