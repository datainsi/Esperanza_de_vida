import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from itertools import combinations
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import warnings
import pyodbc

# Desactivar las advertencias
warnings.filterwarnings("ignore")

# Título de la aplicación
st.title("ESPERANZA DE VIDA AL NACER")

st.markdown("<br>", unsafe_allow_html=True)  # Agregar espacio

# Localmente funciona con esta línea de codigo:
# # # Credenciales en AZURE
# # server = 'database1234.database.windows.net'
# # database = 'DataBase'
# # username = 'administrador'
# # password = '42757875P.'

# # # Crear la cadena de conexión
# # connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
# # # Conectarse a la base de datos
# # conn = pyodbc.connect(connection_string)
# # #cursor = conn.cursor()
# # # Consulta SQL
# # query = '''
# #     SELECT *
# #     FROM [dbo].[Data-Bank]
# #     ORDER BY [Country Name], [Time]
# # '''
# # # Definir los tipos de datos esperados para cada columna
# # data_types = {
# #     'Time': int,
# #     'Country Name': str,
# #     'Country Code': str,
# #     'Birth rate, crude (per 1,000 people)': float,
# #     'Death rate, crude (per 1,000 people)': float,
# #     'Fertility rate, total (births per woman)': float,
# #     'Life expectancy at birth, female (years)': float,
# #     'Life expectancy at birth, male (years)': float,
# #     'Life expectancy at birth, total (years)': float,
# #     'Mortality rate, adult, female (per 1,000 female adults)': float,
# #     'Mortality rate, adult, male (per 1,000 male adults)': float,
# #     'Mortality rate, infant (per 1,000 live births)': float,
# #     'Mortality rate, infant, female (per 1,000 live births)': float,
# #     'Mortality rate, infant, male (per 1,000 live births)': float,
# #     'Mortality rate, neonatal (per 1,000 live births)': float,
# #     'Population growth (annual %)': float,
# #     'Number of infant deaths': float,
# #     'Number of neonatal deaths': float,
# #     'Net migration': float,
# #     'Population, female': float,
# #     'Population, female (% of total population)': float,
# #     'Population, male': float,
# #     'Population, male (% of total population)': float,
# #     'Population, total': float,
# #     'Rural population': float,
# #     'Rural population (% of total population)': float,
# #     'Rural population growth (annual %)': float,
# #     'Urban population': float,
# #     'Urban population (% of total population)': float,
# #     'Urban population growth (annual %)': float,
# #     'Sex ratio at birth (male births per female births)': float,
# #     'Adolescent fertility rate (births per 1,000 women ages 15-19)': float,
# #     'GDP (current US$)': float,
# #     'GDP growth (annual %)': float,
# #     'Immunization, DPT (% of children ages 12-23 months)': float,
# #     'Immunization, measles (% of children ages 12-23 months)': float,
# #     'Healthy life expectancy, total (years)': float,
# #     'Healthy life expectancy, male (years)': float,
# #     'Healthy life expectancy, female (years)': float
# # }

# # # Leer los datos en un DataFrame y especificar los tipos de datos
# # data = pd.read_sql(query, conn, dtype=data_types)

# Cargar los datos con la data generada.
data = pd.read_csv('data.csv')
data['Time'] = pd.to_datetime(data['Time'], format='%Y')
data = data.set_index('Time')

# Obtener la lista de años disponibles en orden descendente
available_years = data.index.year.unique()[::-1]

# Subtítulo y selección de la data
st.subheader("  0. Restricción de la data:")

# Filtrar los datos hasta el año seleccionado
selected_year = st.selectbox("Selecciona el año límite:", available_years, key="year")


#########
######### I. 'Life expectancy at birth, total (years)' por pais.

# Subtítulo - Series de tiempo
st.subheader("I. SERIES DE TIEMPO")

# Subtítulo y selección por País
st.subheader("  I.1. Análisis por País:")

# Filtrar los datos solo para el año seleccionado
data_filtered = data[data.index.year <= selected_year]

# Lista de países de interés
paises_interes = data_filtered['Country Name'].unique()

# Selección del país
selected_pais = st.selectbox("Selecciona un país:", paises_interes, key="country")

# Filtrar los datos solo para el país seleccionado
datos_pais = data_filtered[data_filtered['Country Name'] == selected_pais]
dato = datos_pais[['Life expectancy at birth, total (years)']]

# Mostrar los datos históricos
show_data = st.checkbox("Mostrar datos históricos")
if show_data:
    st.subheader("Datos Históricos")
    st.dataframe(dato)

# Definir la variable forecast_steps fuera de la sección de análisis de series de tiempo
forecast_steps = st.number_input("Número de años para el pronóstico:", min_value=1, max_value=10, value=3, key="forecast_steps")

# Análisis de series de tiempo
#if st.button("Realizar Análisis de Series de Tiempo"):
# Definir los posibles valores de los parámetros
p_values = range(0, 3)  # Valores posibles para p
d_values = range(0, 2)  # Valores posibles para d
q_values = range(0, 3)  # Valores posibles para q

# Realizar la búsqueda en cuadrícula para encontrar los mejores parámetros
best_aic = float('inf')  # Inicializar el mejor valor de AIC como infinito
best_params = None

for p in p_values:
    for d in d_values:
        for q in q_values:
            try:
                model = ARIMA(dato, order=(p, d, q))
                model_fit = model.fit()

                # Calcular el criterio de información de Akaike (AIC)
                aic = model_fit.aic

                # Actualizar los mejores parámetros si se encuentra un valor de AIC menor
                if aic < best_aic:
                    best_aic = aic
                    best_params = (p, d, q)
            except:
                continue

# Ajustar el modelo ARIMA con los mejores parámetros encontrados
model = ARIMA(dato, order=best_params)
model_fit = model.fit()

# Generar pronósticos para los años siguientes
#forecast_steps = forecast_steps = st.number_input("Número de años para el pronóstico:", min_value=1, max_value=10, value=3, key="forecast_steps")
forecast = model_fit.get_forecast(steps=forecast_steps)
forecast_values = forecast.predicted_mean

# Visualizar los datos históricos y los pronósticos
fig, ax = plt.subplots(figsize=(15, 8))  # Establecer el tamaño del gráfico
ax.plot(dato.index, dato.values, label='Datos Históricos')
ax.plot(forecast_values.index, forecast_values.values, label='Pronóstico')
ax.set_xlabel('Tiempo')
ax.set_ylabel('Esperanza de Vida al Nacer (años)')
ax.set_title(f"Esperanza de Vida al Nacer - {selected_pais}")  # Agregar título con el nombre del país
ax.legend()

# Agregar marcadores sobre la línea de la serie
ax.scatter(dato.index, dato.values, color='green', zorder=5)

# Agregar marcadores para los años pronosticados
next_years = pd.date_range(start=dato.index[-1], periods=forecast_steps, freq='A')
ax.scatter(next_years, forecast_values, color='orange', zorder=5)

# Mostrar el gráfico en Streamlit
st.pyplot(fig)

# Imprimir los mejores parámetros encontrados
st.subheader("Mejores Parámetros (p, d, q)")
st.write(best_params)

# Imprimir los pronósticos para los años siguientes
st.subheader("Pronósticos para los siguientes años:")
for year, value in zip(next_years + pd.DateOffset(years=1), forecast_values):
    st.write(year.year, ":", round(value, 2))
st.markdown("<br>", unsafe_allow_html=True)  # Agregar espacio

# # Cerrar la conexión
# conn.close()


#########
######### I.2 Crecimiento/Decrecimiento por Región

# Subtítulo y selección de Región
st.subheader("  I.2. Top de paises Crecimiento/Decrecimiento por Región:")

# Subtítulo y selección de crecimiento o decrecimiento
opcion = st.selectbox("Seleccionar tipo de análisis:", ["Crecimiento", "Decrecimiento"])

# ##### AQUI
# # Filtrar los datos hasta el año seleccionado
# selected_year = st.selectbox("Selecciona el año límite:", data.index.year.unique().sort_values(ascending=False), key="year_selection")

# # Filtrar los datos solo para el año seleccionado
# data_filtered = data[data.index.year <= selected_year]

# Seleccionar las regiones deseadas como una lista
regiones = ['North America', 'Central America', 'South America', 'Oceania']

# Definir los países correspondientes a cada región seleccionada
paises_region = {
    'North America': ['Canada', 'United States', 'Mexico'],
    'South America': ['Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Guyana',
                      'Paraguay', 'Peru', 'Suriname', 'Uruguay', 'Venezuela, RB'],
    'Central America': ['Belize', 'Costa Rica', 'El Salvador', 'Guatemala', 'Honduras', 'Nicaragua', 'Panama'],
    'Oceania': ['Australia', 'Fiji', 'Marshall Islands', 'Solomon Islands', 'Kiribati', 'Micronesia, Fed. Sts.',
                'Nauru', 'New Zealand', 'Palau', 'Papua New Guinea', 'Samoa', 'Tonga', 'Tuvalu', 'Vanuatu']
}

# Selección de Región
selected_regions = st.multiselect("Seleccionar regiones", regiones)

# Iterar sobre las regiones seleccionadas
for region in selected_regions:
    # Verificar si la región seleccionada existe en el diccionario de regiones
    if region not in paises_region:
        st.write(f"La región '{region}' no es válida.")
        continue

    # Obtener los países correspondientes a la región seleccionada
    paises_seleccionados = paises_region[region]

    # Paso 2: Definir los posibles valores de los parámetros
    p_values = range(3)  # Valores posibles para p
    d_values = range(2)  # Valores posibles para d
    q_values = range(3)  # Valores posibles para q

    # Paso 2-5: Iterar sobre cada país y realizar el análisis de series de tiempo
    resultados_paises = {}

    for pais, dato in data_filtered.groupby('Country Name')['Life expectancy at birth, total (years)']:
        # Verificar si el país pertenece a la región seleccionada
        if pais not in paises_seleccionados:
            continue

        # Paso 3: Realizar la búsqueda en cuadrícula para encontrar los mejores parámetros
        best_aic = float('inf')  # Inicializar el mejor valor de AIC como infinito
        best_params = None

        for p in p_values:
            for d in d_values:
                for q in q_values:
                    try:
                        model = ARIMA(dato, order=(p, d, q))
                        model_fit = model.fit()

                        # Calcular el criterio de información de Akaike (AIC)
                        aic = model_fit.aic

                        # Actualizar los mejores parámetros si se encuentra un valor de AIC menor
                        if aic < best_aic:
                            best_aic = aic
                            best_params = (p, d, q)
                    except:
                        continue

        # Paso 4: Ajustar el modelo ARIMA con los mejores parámetros encontrados
        model = ARIMA(dato, order=best_params)
        model_fit = model.fit()

        # Paso 5: Generar pronósticos para los años siguientes
        #forecast_steps = 3
        forecast = model_fit.get_forecast(steps=forecast_steps)
        forecast_values = forecast.predicted_mean

        # Verificar si se desea analizar el crecimiento o el decrecimiento
        if opcion == "Crecimiento":
            # Verificar si el crecimiento ha sido positivo en cada año del pronóstico
            crecimiento_positivo = all(forecast_values[i] > forecast_values[i - 1] for i in range(1, forecast_steps))

            # Calcular el crecimiento esperado para los próximos años si el crecimiento ha sido positivo en cada año
            if crecimiento_positivo:
                crecimiento = (forecast_values[-1] - dato.values[-1]) / dato.values[-1] * 100
                if pd.isnull(crecimiento):
                    continue  # Ignorar este país si el crecimiento es NaN

                resultados_paises[pais] = crecimiento
        elif opcion == "Decrecimiento":
            # Verificar si el crecimiento ha sido negativo en cada año del pronóstico
            crecimiento_negativo = all(forecast_values[i] < forecast_values[i - 1] for i in range(1, forecast_steps))

            # Calcular el decrecimiento esperado para los próximos años si el crecimiento ha sido negativo en cada año
            if crecimiento_negativo:
                decrecimiento = (forecast_values[-1] - dato.values[-1]) / dato.values[-1] * 100
                if pd.isnull(decrecimiento):
                    continue  # Ignorar este país si el decrecimiento es NaN

                resultados_paises[pais] = decrecimiento

    # Paso 6: Ordenar los países según el crecimiento o decrecimiento esperado
    paises_ordenados = sorted(resultados_paises, key=resultados_paises.get, reverse=(opcion == "Crecimiento"))

    # Paso 7: Mostrar los resultados en una tabla
    st.subheader(f"Región: {region}")
    df_resultados = pd.DataFrame({"Nombre_País": paises_ordenados[:3], opcion + " (%)": [resultados_paises[pais] for pais in paises_ordenados[:3]]})
    st.dataframe(df_resultados)

    #st.markdown("<br>", unsafe_allow_html=True)  # Agregar espacio
st.markdown("<br>", unsafe_allow_html=True)  # Agregar espacio


#########
######### II. Regresión Lineal

# Subtítulo y selección de Región
st.subheader("II. REGRESION LINEAL")

# Lista de países únicos en los datos
paises = data['Country Name'].unique()

# Seleccionar los países mediante un multiselect en Streamlit
selected_countries = st.multiselect("Selecciona uno o varios países:", paises)

# Verificar si se han seleccionado países antes de continuar
if selected_countries:
    for selected_country in selected_countries:
        # Filtrar los datos para el país seleccionado
        pais_data = data[data['Country Name'] == selected_country]

        # Crear un nuevo DataFrame con las variables deseadas
        model_data = pais_data[['Birth rate, crude (per 1,000 people)',
                                'Death rate, crude (per 1,000 people)',
                                'Fertility rate, total (births per woman)',
                                'Mortality rate, infant (per 1,000 live births)',
                                'Population growth (annual %)',
                                'Net migration',
                                'Rural population (% of total population)',
                                'Urban population (% of total population)',
                                'Adolescent fertility rate (births per 1,000 women ages 15-19)',
                                'Life expectancy at birth, total (years)']]

        # Imputar los valores faltantes utilizando la media
        imputer = SimpleImputer(strategy='mean')
        model_data = pd.DataFrame(imputer.fit_transform(model_data), columns=model_data.columns)

        best_r2 = 0
        best_X = None
        best_coeficientes = None

        scaler = StandardScaler()

        for r in range(2, 4):  # Probar con 2 y 3 variables independientes
            for combo in combinations(model_data.columns[:-1], r):
                # Dividir los datos en características (X) y variable objetivo (y)
                X = model_data[list(combo)]
                y = model_data['Life expectancy at birth, total (years)']

                # Dividir los datos en conjuntos de entrenamiento y prueba
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                # Escalar las características
                X_train_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)

                # Crear y entrenar el modelo de regresión lineal
                model = LinearRegression()
                model.fit(X_train_scaled, y_train)

                # Calcular el coeficiente de determinación (R²)
                r2 = model.score(X_test_scaled, y_test)

                # Actualizar el mejor R², las variables seleccionadas y los coeficientes
                if r2 > best_r2:
                    best_r2 = r2
                    best_X = combo
                    best_coeficientes = model.coef_

        # Calcular los residuos para el mejor modelo
        X_best = model_data[list(best_X)]
        y_best = model_data['Life expectancy at birth, total (years)']
        X_train_best, X_test_best, y_train_best, y_test_best = train_test_split(X_best, y_best, test_size=0.2, random_state=42)
        X_train_scaled_best = scaler.fit_transform(X_train_best)
        X_test_scaled_best = scaler.transform(X_test_best)
        model_best = LinearRegression()
        model_best.fit(X_train_scaled_best, y_train_best)
        y_pred_best = model_best.predict(X_test_scaled_best)
        residuos_best = y_test_best - y_pred_best

        # Crear un DataFrame con las variables y sus relaciones
        relaciones_data = pd.DataFrame({'Variable': best_X, 'Relacion': best_coeficientes})
        # Ordenar las variables por su relación con Life expectancy at birth
        relaciones_data = relaciones_data.sort_values(by='Relacion', ascending=False)

        # Graficar la relación entre las variables independientes y la expectativa de vida
        fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))

        axs[0].barh(relaciones_data['Variable'], relaciones_data['Relacion'],
                    color=['green' if coeficiente > 0 else 'red' for coeficiente in relaciones_data['Relacion']])
        axs[0].set_title('Relación: Life Expectancy y Variables Independientes - ' + selected_country)
        axs[0].set_xlabel('Coeficiente de Regresión')
        axs[0].set_ylabel('Variables Independientes')

        for i, coeficiente in enumerate(relaciones_data['Relacion']):
            axs[0].text(coeficiente, i, f'{coeficiente:.2f}', ha='left', va='center')

        axs[1].scatter(y_test_best, y_pred_best)
        axs[1].plot([min(y_test_best), max(y_test_best)], [min(y_test_best), max(y_test_best)], color='r', linestyle='--')
        axs[1].set_xlabel('Valores reales')
        axs[1].set_ylabel('Pronósticos')
        axs[1].set_title('Valores reales vs. Pronósticos')

        # Mostrar el valor de R² en el gráfico
        axs[1].text(0.05, 0.95, f'R² = {best_r2:.4f}', transform=axs[1].transAxes, ha='left', va='top')

        plt.tight_layout()
        st.pyplot(fig)
else:
    st.write("No se han seleccionado países.")

# Cerrar la conexión
conn.close()