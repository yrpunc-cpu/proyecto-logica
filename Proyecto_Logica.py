import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

archivo = "datos_estudiantes.csv"

st.set_page_config(page_title="Sistema de Análisis Estudiantil", layout="wide")

st.title("📊 Sistema de Detección de Problemáticas Estudiantiles")
st.write("Proyecto de Lógica y Ciencia de Datos")

# -----------------------------
# REGISTRO DE DATOS
# -----------------------------
st.header("📝 Registro de Estudiante")

carrera = st.text_input("Carrera")
semestre = st.selectbox("Semestre", ["1", "2", "3", "4", "5"])
trabaja = st.radio("¿Trabaja?", ["si", "no"])
estres = st.slider("Nivel de Estrés (1-5)", 1, 5)
horas_estudio = st.number_input("Horas de estudio diarias", 0.0, 12.0)

if st.button("Guardar Datos"):

    datos = {
        "Carrera": carrera,
        "Semestre": semestre,
        "Trabaja": trabaja,
        "Estres": estres,
        "Horas_estudio": horas_estudio
    }

    df = pd.DataFrame([datos])

    if os.path.exists(archivo):
        df.to_csv(archivo, mode='a', header=False, index=False)
    else:
        df.to_csv(archivo, index=False)

    st.success("Datos guardados correctamente")

    # -----------------------------
    # REGLAS LÓGICAS FORMALES
    # -----------------------------
    # P: Trabaja
    # Q: Estres >= 4
    # R: Riesgo académico alto

    P = trabaja == "si"
    Q = estres >= 4
    R = P and Q

    if R:
        st.warning("⚠ Según la regla lógica (P ∧ Q → R), existe posible riesgo académico alto.")


# -----------------------------
# ANÁLISIS
# -----------------------------
st.header("📈 Análisis General")

if os.path.exists(archivo):

    df = pd.read_csv(archivo)

    col1, col2 = st.columns(2)

    col1.metric("Promedio Estrés", round(df["Estres"].mean(),2))
    col2.metric("Promedio Horas Estudio", round(df["Horas_estudio"].mean(),2))

    st.subheader("Distribución de Estrés")
    fig1, ax1 = plt.subplots()
    df["Estres"].hist()
    st.pyplot(fig1)

    st.subheader("Estudiantes que trabajan")
    fig2, ax2 = plt.subplots()
    df["Trabaja"].value_counts().plot(kind="bar")
    st.pyplot(fig2)

else:
    st.info("Aún no hay datos registrados.")
