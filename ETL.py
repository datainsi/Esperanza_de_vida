
################################################      EXTRACCIÓN DE DATOS       #####################################################

# IMPORTAMOS LAS LIBRERIAS A USAR
import pandas as pd
import requests
import io
from azure.storage.blob import BlobServiceClient
import wbgapi as wb

### Cargando los datos extraídos de manera estática.
df_csv = pd.read_csv("Tendencia_LE_y_HALE_data.csv", sep= ";")

#### Extraemos el dataset mediante la libreria que te propoeciona la data del API del Banco Mundial.
# Considerando como cliente a Pfizer delimitamos los indicadores.
indicators = [
    'SP.DYN.CBRT.IN', 'SP.DYN.CDRT.IN', 'SP.DYN.TFRT.IN', 'SP.DYN.LE00.FE.IN', 'SP.DYN.LE00.MA.IN',
    'SP.DYN.LE00.IN', 'SP.DYN.AMRT.FE', 'SP.DYN.AMRT.MA', 'SP.DYN.IMRT.IN', 'SP.DYN.IMRT.FE.IN',
    'SP.DYN.IMRT.MA.IN', 'SH.DYN.NMRT', 'SP.POP.GROW', 'SH.DTH.IMRT', 'SH.DTH.NMRT', 'SM.POP.NETM',
    'SP.POP.TOTL.FE.IN', 'SP.POP.TOTL.FE.ZS', 'SP.POP.TOTL.MA.IN', 'SP.POP.TOTL.MA.ZS', 'SP.POP.TOTL',
    'SP.RUR.TOTL', 'SP.RUR.TOTL.ZS', 'SP.RUR.TOTL.ZG', 'SP.URB.TOTL', 'SP.URB.TOTL.IN.ZS', 'SP.URB.GROW',
    'SP.POP.BRTH.MF', 'SP.ADO.TFRT', 'NY.GDP.MKTP.CD', 'NY.GDP.MKTP.KD.ZG', 'SH.IMM.IDPT', 'SH.IMM.MEAS'
]

code_country = ["ARG", "AUS", "BLZ", "BOL", "BRA", "CAN", "CHL", "COL", "CRI", "CUB", "ECU", "SLV", "FJI", "GTM", "GUY", "HTI",
                "HND", "KIR", "MHL", "MEX", "FSM", "NRU", "NZL", "NIC", "PLW", "PAN", "PNG", "PRY", "PER", "WSM", "SLB", 
                "SUR", "TON", "TUV", "USA", "URY", "VUT", "VEN"]

start_year = 1987
end_year = 2021

# Obtener los datos para los indicadores, países y rango de tiempo específico
data_df = wb.data.DataFrame(indicators, code_country, range(start_year, end_year + 1), numericTimeKeys= True)

# Guardando en un csv la data extraída de la API
data_df.to_csv("nueva_df_I.csv")

# Leyendo el archivo csv
df = pd.read_csv("nueva_df_I.csv")

############################################      TRANSFORMACIÓN DE DATOS       ##################################################

### ANÁLISIS PRELIMINAR DEL DATASET EXTRAÍDO DE MANERA ESTÁTICA
# Normalizando 
df_pivot = df_csv.pivot(index=['Year of Dated Year', 'País'], columns='Sexo Nombre', values='HALE')

# Reiniciar los nombres de las columnas
df_pivot.columns.name = None

# Reiniciar el índice
df_pivot.reset_index(inplace=True)

df_pivot.rename(columns={'Year of Dated Year': 'Time', "País": "Country Name", "Ambos sexos": "Healthy life expectancy, total (years)", 
                "Hombre": "Healthy life expectancy, male (years)", "Mujer": "Healthy life expectancy, female (years)"}, inplace=True)

# Lista de columnas a convertir a tipo numérico
columnas_indicadores = list(df_pivot.columns[2:])

# Iterar sobre las columnas y convertirlas a tipo numérico
for columna in columnas_indicadores:
    df_pivot[columna] = pd.to_numeric(df_pivot[columna], errors='coerce').round(1)


####  ANÁLISIS PRELIMINAR DEL DATASET EXTRAÍDO MEDIANTE LA API
# Normalizando 
# Realizar la transformación de los datos utilizando melt
melted_data = df.melt(id_vars=['economy', 'series'], var_name='time', value_name='valor')

# Realizar la transformación de los datos utilizando pivot_table
pivoted_data = melted_data.pivot_table(index=['time', 'economy'], columns='series', values='valor').reset_index()

# Reordenar las columnas
pivoted_data = pivoted_data[['time', 'economy'] + list(pivoted_data.columns[2:])]

Dicc_country = {"ARG": "Argentina", "AUS": "Australia", "BLZ": "Belize", "BOL": "Bolivia", "BRA": "Brazil",
                "CAN": "Canada", "CHL": "Chile", "COL": "Colombia", "CRI": "Costa Rica", "CUB": "Cuba",
                "ECU": "Ecuador", "SLV": "El Salvador", "FJI": "Fiji", "GTM": "Guatemala", "GUY": "Guyana",
                "HTI": "Haiti", "HND": "Honduras", "KIR": "Kiribati", "MHL": "Marshall Islands", "MEX": "Mexico",
                "FSM": "Micronesia", "NRU": "Nauru", "NZL": "New Zealand", "NIC": "Nicaragua", "PLW": "Palau",
                "PAN": "Panama", "PNG": "Papua New Guinea", "PRY": "Paraguay", "PER": "Peru", "WSM": "Samoa",
                "SLB": "Solomon Islands", "SUR": "Suriname", "TON": "Tonga", "TUV": "Tuvalu", "USA": "United States",
                "URY": "Uruguay", "VUT": "Vanuatu", "VEN": "Venezuela"}

# Crear la columna "country" basada en la columna "economy"
pivoted_data['country'] = pivoted_data['economy'].map(Dicc_country)

# Mover la columna "country" después de la columna "economy"
country_column = pivoted_data.pop('country')
pivoted_data.insert(pivoted_data.columns.get_loc('economy') + 1, 'country', country_column)

# Renombrar las columnas de forma permanente
pivoted_data.rename(columns={'NY.GDP.MKTP.CD': 'GDP (current US$)', 'NY.GDP.MKTP.KD.ZG': 'GDP growth (annual %)', 'SH.DTH.IMRT': "Number of infant deaths",
                   'SH.DTH.NMRT': "Number of neonatal deaths", 'SH.DYN.NMRT': "Mortality rate, neonatal (per 1,000 live births)", 
                   'SH.IMM.IDPT': "Immunization, DPT (% of children ages 12-23 months)", 'SH.IMM.MEAS': "Immunization, measles (% of children ages 12-23 months)",
                   'SM.POP.NETM': "Net migration", 'SP.ADO.TFRT': "Adolescent fertility rate (births per 1,000 women ages 15-19)",
                   'SP.DYN.AMRT.FE': "Mortality rate, adult, female (per 1,000 female adults)", 'SP.DYN.AMRT.MA': "Mortality rate, adult, male (per 1,000 male adults)",
                   'SP.DYN.CBRT.IN': "Birth rate, crude (per 1,000 people)", 'SP.DYN.CDRT.IN': "Death rate, crude (per 1,000 people)",
                   'SP.DYN.IMRT.FE.IN': "Mortality rate, infant, female (per 1,000 live births)", 'SP.DYN.IMRT.IN': "Mortality rate, infant (per 1,000 live births)",
                   'SP.DYN.IMRT.MA.IN': "Mortality rate, infant, male (per 1,000 live births)", 'SP.DYN.LE00.FE.IN': "Life expectancy at birth, female (years)",
                   'SP.DYN.LE00.IN': "Life expectancy at birth, total (years)", 'SP.DYN.LE00.MA.IN': "Life expectancy at birth, male (years)",
                   'SP.DYN.TFRT.IN': "Fertility rate, total (births per woman)", 'SP.POP.BRTH.MF': "Sex ratio at birth (male births per female births)",
                   'SP.POP.GROW': "Population growth (annual %)", 'SP.POP.TOTL': "Population, total", 'SP.POP.TOTL.FE.IN': "Population, female",
                   'SP.POP.TOTL.FE.ZS': "Population, female (% of total population)", 'SP.POP.TOTL.MA.IN': "Population, male",
                   'SP.POP.TOTL.MA.ZS': "Population, male (% of total population)", 'SP.RUR.TOTL': "Rural population", 'SP.RUR.TOTL.ZG': "Rural population growth (annual %)",
                   'SP.RUR.TOTL.ZS': "Rural population (% of total population)", 'SP.URB.GROW': "Urban population growth (annual %)", 'SP.URB.TOTL': "Urban population", 
                   'SP.URB.TOTL.IN.ZS': "Urban population (% of total population)", "time": "Time", "economy": "Country Code", "country": "Country Name"}, inplace=True)

# Lista de columnas a convertir a tipo numérico
columnas_indicadores = list(pivoted_data.columns[3:])

# Iterar sobre las columnas y convertirlas a tipo numérico
for columna in columnas_indicadores:
    pivoted_data[columna] = pd.to_numeric(pivoted_data[columna], errors='coerce').round(1)

#Modificando a int el tipo de dato "Time"
pivoted_data["Time"] = pivoted_data["Time"].astype(int)
# Imprimir el resultado++
pivoted_data.columns.name = None
pivoted_data

###### Uniendo los dos dataset en uno solo ###########

# Uniendo los dataset
df_consolidado = pd.merge(pivoted_data, df_pivot, on=["Country Name", "Time"], how='left')

# Generando la data.
df_consolidado.to_csv("DATA_PF.csv", index= False)
print("Archivo final")

##################################################   Automatizando la Data   ##########################################################
##################################################   ---------------------   ##########################################################                        


# Cadena de conexión de tu cuenta de Azure Blob Storage
connection_string = "DefaultEndpointsProtocol=https;AccountName=almacenamientoo;AccountKey=GrqlKIGJOEV+6YiIwZDMs1ku2IPwaeMSk5xQOyqZENTtaC/ZLex0N508slGKzaHVLEh2tmXKyUiM+AStuIlPcQ==;EndpointSuffix=core.windows.net"

# Nombre del contenedor y el archivo que deseas cargar
container_name = "dataset"
local_file_path = "DATA_PF.csv"
blob_name = "DATA_PF_I.csv"

#Crea una instancia del cliente BlobServiceClient utilizando la cadena de conexión
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Obtiene una referencia al contenedor
container_client = blob_service_client.get_container_client(container_name)

# Sube un archivo al contenedor
with open(local_file_path, "rb") as data:
    container_client.upload_blob(name=blob_name, data=data)

print("Archivo cargado correctamente en el Azure Blob Storage.")
