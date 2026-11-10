import streamlit as pd_stream
import pandas as pd
import os

# Configuración de la página web (Título en la pestaña y diseño ancho)
pd_stream.set_page_config(page_title="SEMBRIEXPORT", page_icon="🌱", layout="centered")

# Estilos visuales personalizados (Colores elegantes verde agrícola y gris)
pd_stream.markdown("""
    <style>
    .main-title { font-size:32px !important; font-weight: bold; color: #2E7D32; text-align: center; margin-bottom: 5px; }
    .sub-title { font-size:18px !important; color: #555555; text-align: center; margin-bottom: 30px; border-bottom: 2px solid #2E7D32; padding-bottom: 10px; }
    .result-box { background-color: #E8F5E9; border-left: 5px solid #2E7D32; padding: 20px; border-radius: 5px; margin-top: 20px; }
    .result-text { font-size: 24px !important; font-weight: bold; color: #1B5E20; }
    </style>
""", unsafe_allow_html=True)

# Cabecera elegante solicitada
pd_stream.markdown('<p class="main-title">SEMBRIEXPORT</p>', unsafe_allow_html=True)
pd_stream.markdown('<p class="sub-title">TABLA DE CONVERSIONES (GRAMOS A CC)</p>', unsafe_allow_html=True)

# Cargar la base de datos de Excel
ruta_archivo = "base_datos_agroquimicos.xlsx"

if not os.path.exists(ruta_archivo):
    pd_stream.error(f"❌ No se encontró el archivo '{ruta_archivo}' en la carpeta.")
else:
    try:
        df = pd.read_excel(ruta_archivo)
        df['Marca / Producto'] = df['Marca / Producto'].astype(str).str.strip()
        
        # MENÚ DESPLEGABLE WEB: El operario puede buscar o seleccionar el producto visualmente
        lista_productos = sorted(df['Marca / Producto'].unique())
        producto_seleccionado = pd_stream.selectbox("🌱 Selecciona o escribe la marca del producto:", lista_productos)
        
        # Buscar datos del producto seleccionado
        resultado = df[df['Marca / Producto'] == producto_seleccionado]
        
        if not resultado.empty:
            densidad = float(resultado.iloc[0]['Densidad (kg/L)'])
            tipo = resultado.iloc[0]['Tipo']
            
            # Recuadro informativo corregido
            pd_stream.info(f"📋 **Tipo:** {tipo} | **Densidad registrada:** {densidad} kg/L")
            
            # CASILLA DE ENTRADA NUMÉRICA WEB
            gramos = pd_stream.number_input("⚖️ Ingresa el peso en GRAMOS (g):", min_value=0.0, step=10.0, value=0.0)
            
            if gramos > 0:
                # Cálculo matemático a Centímetros Cúbicos
                cc = gramos / densidad
                
                # Cuadro de resultado elegante a colores
                pd_stream.markdown(f"""
                    <div class="result-box">
                        <p style="margin:0; color:#555;">Resultado de la conversión:</p>
                        <p class="result-text">➡️ {cc:,.1f} cc <span style="font-size:16px; font-weight:normal; color:#666;">(cm³ / ml)</span></p>
                    </div>
                """, unsafe_allow_html=True)
                
    except Exception as e:
        pd_stream.error(f"⚠️ Error al procesar el archivo Excel. Revisa los títulos de las columnas. ({e})")
