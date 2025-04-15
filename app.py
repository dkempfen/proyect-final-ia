#preciso que me hagas Aplicación Inteligente para el Análisis de Ventas con Gemini IA. Su Objetivo del proyecto: 
# Crear una aplicación en Python que permita a empresas y emprendedores subir sus datos de ventas y obtener:
# Análisis automáticos con IA (Gemini)
# Identificación de productos más vendidos
# Detección de tendencias
# Recomendaciones de mejora
# Exportación de informes en PDF y Excel
# Visualización interactiva de los datos

# Crear una aplicación en Python que permita a empresas y emprendedores subir sus datos de ventas y obtener:
# Análisis automáticos con IA (Gemini)
# Identificación de productos más vendidos
# Detección de tendencias
# Recomendaciones de mejora
# Exportación de informes en PDF y Excel
# Visualización interactiva de los datos

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Cargar API KEY 
load_dotenv()
api_key = "AIzaSyAuHYHyyrsP4IohexQ3W8fvtMkPEfWNsrk"
genai.configure(api_key=api_key)

# Inicializar modelo Gemini
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

# Función de análisis con IA
def analyze_sales_data(df):
    resumen = df.describe().to_string()
    tendencias = df.groupby("Fecha")["Ventas"].sum().to_string()
    nulos = df.isnull().sum().to_string()

    prompt = f"""Analizá los siguientes datos de ventas. 
    Datos generales:
    {resumen}

    Ventas por fecha:
    {tendencias}

    Valores faltantes:
    {nulos}

    Necesito que indiques productos más vendidos, tendencias detectadas y recomendaciones de mejora."""
    
    response = model.generate_content(prompt)
    return response.text

# Generar PDF
def generate_pdf_report(df, analysis_results):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("📊 Informe de Análisis de Ventas", styles['Title']))
    elements.append(Paragraph("🔍 Análisis de Ventas:", styles['Heading2']))
    elements.append(Paragraph(df.describe().to_string(), styles['BodyText']))
    elements.append(Paragraph("📈 Tendencias de Ventas por Fecha:", styles['Heading2']))
    elements.append(Paragraph(df.groupby('Fecha')["Ventas"].sum().to_string(), styles['BodyText']))
    elements.append(Paragraph("🚨 Valores Faltantes:", styles['Heading2']))
    elements.append(Paragraph(df.isnull().sum().to_string(), styles['BodyText']))
    elements.append(Paragraph("🤖 Análisis con Gemini IA:", styles['Heading2']))
    elements.append(Paragraph(analysis_results, styles['BodyText']))

    doc.build(elements)
    return buffer.getvalue()

# Main App
def main():
    st.set_page_config(page_title="Análisis de Ventas IA", layout="wide")
    st.title("📈 Aplicación Inteligente para el Análisis de Ventas con Gemini IA")

    uploaded_file = st.file_uploader("📂 Cargá tus datos de ventas (.csv)", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.subheader("📋 Vista previa de los datos")
        st.dataframe(df)

        # Gráfico de productos más vendidos si hay una columna "Producto"
        if "Producto" in df.columns:
            st.subheader("🏆 Productos más vendidos")
            top_productos = df["Producto"].value_counts().head(10)
            st.bar_chart(top_productos)

        # Análisis con Gemini
        with st.spinner("Analizando con Gemini IA..."):
            resultado_ia = analyze_sales_data(df)

        st.subheader("🧠 Análisis Automático con IA")
        st.write(resultado_ia)

        # Exportar PDF
        pdf_bytes = generate_pdf_report(df, resultado_ia)
        st.download_button(
            label="📥 Descargar Informe en PDF",
            data=pdf_bytes,
            file_name="informe_ventas.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()
