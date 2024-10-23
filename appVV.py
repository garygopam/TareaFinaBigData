import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def main():
    # Configurar la página para que ocupe todo el ancho
    st.set_page_config(layout="wide")

    # Título centrado
    st.title("Estadística de Planta v1")

    # Subir el archivo CSV
    uploaded_file = st.file_uploader("Elige un archivo CSV", type=["csv"])

    # Opción para usar un archivo predeterminado si no se carga uno
    if uploaded_file is None:
        use_default_file = st.checkbox("Usar archivo predeterminado")
        if use_default_file:
            default_file_name = "Data_Mayor_Train_CSV.csv"  # Nombre del archivo en la carpeta del proyecto
            if os.path.exists(default_file_name):
                uploaded_file = default_file_name
            else:
                st.error("El archivo predeterminado no se encuentra en la carpeta del proyecto.")
    
    if uploaded_file is not None:
        try:
            # Leer el archivo CSV
            if isinstance(uploaded_file, str):  # Si se usó el archivo predeterminado
                df_MG = pd.read_csv(uploaded_file, encoding='latin-1')  # Cambia 'latin-1' según sea necesario
            else:  # Si se subió un archivo
                df_MG = pd.read_csv(uploaded_file, encoding='latin-1')

            # Dividir la página en dos columnas (1/4 para datos y 3/4 para gráficos)
            col1, col2 = st.columns([1, 3])  # Proporciones

            with col1:
                st.write("Datos del archivo:")
                st.dataframe(df_MG)

            with col2:
                # Título para la primera sección de gráficos
                st.subheader("Gráfico 1: Estadística Malla -200")

                # Crear los subplots para el primer gráfico
                fig, ax = plt.subplots(1, 3, figsize=(22, 5))
                sns.despine()

                # Configuración del primer subplot
                ax[0].tick_params(axis='x', labelrotation=0)
                ax[0].set(xlabel='Malla -200 in %', ylabel='')
                ax[0].set_title('Malla -200 amount by Target %R type - Distribution', size=15)

                # Configuración del segundo subplot
                ax[1].tick_params(axis='x', labelrotation=0)
                ax[1].set_title('Malla -200 amount by Target %R type - Boxplot', size=15)

                # Configuración del tercer subplot
                ax[2].tick_params(axis='x', labelrotation=0)
                ax[2].set_title('Malla -200 amount by Target %R type - Violinplot', size=15)

                # Definir la paleta de colores personalizada
                palette = "Set2"

                # Graficar el primer subplot con histplot
                sns.histplot(data=df_MG, x="% Malla -200", hue="Target %R", bins=30, kde=True, ax=ax[0], palette=palette)

                # Graficar el segundo subplot con boxplot
                sns.boxplot(data=df_MG, x="Target %R", y="% Malla -200", ax=ax[1], palette=palette).set(xlabel='Target %R', ylabel='% Malla -200')

                # Graficar el tercer subplot con violinplot
                sns.violinplot(data=df_MG, x="Target %R", y="% Malla -200", ax=ax[2], palette=palette).set(xlabel='Target %R', ylabel='% Malla -200')

                # Mostrar los gráficos del primer subplot en Streamlit
                st.pyplot(fig)

                # Segunda sección: Estadística de Malla -200 vs %Rec SULFURO POR TIPO DE MINERAL
                st.subheader("Gráfico 2: Estadística Malla -200 VS %Rec SULFURO POR TIPO DE MINERAL")

                # Filtrar las filas que no contienen "MIXTO" o "SULFURO/MIXTO"
                df_Msulf = df_MG.copy()
                filtered_dfsulf = df_Msulf[~df_Msulf['Tipo de Mineral'].str.contains('MIXTO|SULFURO/MIXTO', case=False, na=False)]

                # Exportar la tabla estadística a Excel
                descripcionSULF = filtered_dfsulf.describe()
                descripcionSULF.to_excel('descripcionSULF.xlsx', engine='openpyxl')

                # Crear los subplots para el gráfico de Sulfuro
                fig, ax = plt.subplots(1, 3, figsize=(22, 5))
                sns.despine()

                # Configuración del primer subplot
                ax[0].tick_params(axis='x', labelrotation=0)
                ax[0].set(xlabel='Malla -200 in %', ylabel='')
                ax[0].set_title('Sulfuro Malla -200 amount by Target %R type - Distribution', size=15)

                # Configuración del segundo subplot
                ax[1].tick_params(axis='x', labelrotation=0)
                ax[1].set_title('Sulfuro Malla -200 amount by Target %R type - Boxplot', size=15)

                # Configuración del tercer subplot
                ax[2].tick_params(axis='x', labelrotation=0)
                ax[2].set_title('Sulfuro Malla -200 amount by Target %R type - Violinplot', size=15)

                # Graficar el primer subplot con histplot
                sns.histplot(data=filtered_dfsulf, x="% Malla -200", hue="Target %R", bins=30, kde=True, ax=ax[0], palette=palette)

                # Graficar el segundo subplot con boxplot
                sns.boxplot(data=filtered_dfsulf, x="Target %R", y="% Malla -200", ax=ax[1], palette=palette).set(xlabel='Target %R', ylabel='% Malla -200')

                # Graficar el tercer subplot con violinplot
                sns.violinplot(data=filtered_dfsulf, x="Target %R", y="% Malla -200", ax=ax[2], palette=palette).set(xlabel='Target %R', ylabel='Sulfuro % Malla -200')

                # Mostrar los gráficos del segundo subplot en Streamlit
                st.pyplot(fig)

        except Exception as e:
            st.error(f"Ocurrió un error al leer el archivo: {e}")

if __name__ == "__main__":
    main()