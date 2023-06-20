#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.impute import SimpleImputer
import streamlit as st
from collections import Counter
from sqlalchemy import create_engine

server = 'database1234.database.windows.net'
database = 'DataBase'
username = 'administrador'
password = '42757875P.'
driver = 'ODBC Driver 17 for SQL Server'
connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'

engine = create_engine(connection_string)
query = 'SELECT * FROM [dbo].[Data-Bank]'

data = pd.read_sql(query, engine)



# Título de la aplicación
st.title("ESPERANZA DE VIDA AL NACER")

# Cargar los datos en un DataFrame de pandas
#data = pd.read_csv('https://raw.githubusercontent.com/perico3372/life_expectancy/main/DATA_PF_IV.csv')
#data = pd.read_csv('data.csv')

# Seleccionar los indicadores como características
features = ['Birth rate, crude (per 1,000 people)',
            'Death rate, crude (per 1,000 people)',
            'Fertility rate, total (births per woman)',
            'Life expectancy at birth, female (years)',
            'Life expectancy at birth, male (years)',
            'Life expectancy at birth, total (years)',
            'Mortality rate, adult, female (per 1,000 female adults)',
            'Mortality rate, adult, male (per 1,000 male adults)',
            'Mortality rate, infant (per 1,000 live births)',
            'Mortality rate, infant, female (per 1,000 live births)',
            'Mortality rate, infant, male (per 1,000 live births)',
            'Mortality rate, neonatal (per 1,000 live births)',
            'Population growth (annual %)', 'Number of infant deaths',
            'Number of neonatal deaths', 'Net migration', 'Population, female',
            'Population, female (% of total population)', 'Population, male',
            'Population, male (% of total population)', 'Population, total',
            'Rural population', 'Rural population (% of total population)',
            'Rural population growth (annual %)', 'Urban population',
            'Urban population (% of total population)',
            'Urban population growth (annual %)',
            'Sex ratio at birth (male births per female births)',
            'Adolescent fertility rate (births per 1,000 women ages 15-19)',
            'GDP (current US$)', 'GDP growth (annual %)',
            'Immunization, DPT (% of children ages 12-23 months)',
            'Immunization, measles (% of children ages 12-23 months)',
            'Healthy life expectancy, total (years)',
            'Healthy life expectancy, male (years)',
            'Healthy life expectancy, female (years)']

# Crear una matriz de características
X = data[features].values

# Aplicar imputación para manejar los valores faltantes
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

# Crear un modelo KNN y ajustarlo a los datos
model = NearestNeighbors(metric='euclidean')
model.fit(X_imputed)


def get_recommendations(country_index, n_recommendations=3):
    distances, indices = model.kneighbors(X_imputed[country_index].reshape(1, -1), n_neighbors=n_recommendations+1)
    indicator_indices = indices[0][1:]
    valid_indices = [i for i in indicator_indices if i < len(features)]
    return valid_indices

# Mostrar la data con opción para seleccionar una muestra aleatoria
show_random_sample = st.checkbox("Mostrar base de datos eligiendo cantidad de filas de manera aleatoria ")
if show_random_sample:
    # Obtener el tamaño de la muestra deseada
    sample_size = st.number_input("Seleccione el tamaño de la muestra", min_value=1, max_value=len(data), value=5, step=1)

    # Obtener una muestra aleatoria de los datos
    random_sample = data.sample(n=sample_size)

    # Mostrar la muestra aleatoria
    st.write(f"Muestra aleatoria de {sample_size} registros:")
    st.dataframe(random_sample)
    
# Subtítulo - Series de tiempo
st.subheader("Modelo KNN")

# Obtener la cantidad de indicadores a mostrar
num_indicators = st.number_input("Seleccione la cantidad de indicadores a mostrar", min_value=1, max_value=len(features), value=7)
    
# Generar los indicadores más influyentes al hacer clic en un botón
if st.button("Generar indicadores más influyentes"):
    # Crear una lista para almacenar todas las recomendaciones de indicadores
    all_recommended_indicators = []

    for country_index in range(len(data)):
        recommendations = get_recommendations(country_index)
        recommended_indicators = [features[i] for i in recommendations]
        all_recommended_indicators.extend(recommended_indicators)

    # Contar la frecuencia de cada indicador recomendado
    counter = Counter(all_recommended_indicators)



    # Obtener los indicadores más influyentes
    top_indicators = counter.most_common(num_indicators)

    # Mostrar los indicadores seleccionados
    st.title("Indicadores más influyentes para la esperanza de vida")
    st.write(f"Los {num_indicators} indicadores más influyentes para la esperanza de vida:")

    for indicator, count in top_indicators:
        st.write(f"- {indicator}")
