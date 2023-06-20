
################################################      EXTRACCIÓN DE DATOS       #####################################################

# IMPORTAMOS LAS LIBRERIAS A USAR
import pandas as pd
import requests
import io
from azure.storage.blob import BlobServiceClient

### Cargando los datos.
df1 = pd.read_csv("P_Data_Extract_From_Gender_Statistics.csv")
df2 = pd.read_csv("P_Data_Extract_From_Education_Statistics_-_All_Indicators.csv")
df3 = pd.read_csv("P_Data_Extract_From_Population_estimates_and_projections.csv")

#### Extraemos una nuevo  dataset mediante API.
url_01 = "https://apps.who.int/gho/athena/data/GHO/cpmowho,cpmt,fps,fpsmowho?filter=COUNTRY:*;AGEGROUP:*&ead=&x-sideaxis=COUNTRY;YEAR;DATASOURCE&x-topaxis=GHO;AGEGROUP&profile=crosstable&format=csv"

response = requests.get(url_01)

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Leer el contenido de la respuesta en un DataFrame de pandas
    df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
    # Guardar el DataFrame en un archivo CSV
    df.to_csv("API_01.csv", index=False)
    print("Archivo descargado exitosamente.")
else:
    print("No se pudo realizar la descarga.")

# Ruta del archivo CSV
csv_url_01 = "API_01.csv"

# Leer el archivo CSV en un DataFrame de pandas
df = pd.read_csv(csv_url_01)

# Eliminar las primeras 1 fila
df = df.iloc[1:]

# Escribir el DataFrame modificado en un nuevo archivo CSV
df.to_csv("API_01.csv", index=False)

# Leer el archivo CSV en un DataFrame de pandas con encabezados
df_API = pd.read_csv("API_01.csv")


############################################      TRANSFORMACIÓN DE DATOS       ##################################################

### ANALISIS PRELIMINAR: DATASET N°01 - Data_Extract_From_Education_Statistics_-_All_Indicators

# Considerando como cliente a una ONG relacionada a la investigación, delimitamos los indicadores.
indicadores_deseados = ["Country Name", "Country Code", "Time", "Adolescent fertility rate (births per 1,000 women ages 15-19) [SP.ADO.TFRT]", 
                        "GDP (current US$) [NY.GDP.MKTP.CD]", "GDP growth (annual %) [NY.GDP.MKTP.KD.ZG]","Immunization, DPT (% of children ages 12-23 months) [SH.IMM.IDPT]",
                        "Immunization, measles (% of children ages 12-23 months) [SH.IMM.MEAS]"
                        ]
df1 = df1[indicadores_deseados]

# Normalizando 
# Lista de columnas a convertir a tipo numérico
columnas_indicadores = list(df1.columns[3:])

# Iterar sobre las columnas y convertirlas a tipo numérico
for columna in columnas_indicadores:
    df1[columna] = pd.to_numeric(df1[columna], errors='coerce')

df1 = df1.iloc[:-5]

####  ANALISIS PRELIMINAR: DATASET N°02 - Data_Extract_From_Education_Statistics_-_All_Indicators

# Considerando como cliente a una ONG relacionada a la investigación, delimitamos los indicadores.
indicadores_deseados = ["Country Name", "Country Code", "Time", "GDP at market prices (current US$) [NY.GDP.MKTP.CD]", "GDP per capita (current US$) [NY.GDP.PCAP.CD]"
                        ]
df2 = df2[indicadores_deseados]

# Normalizando 
# Lista de columnas a convertir a tipo numérico
columnas_indicadores = list(df2.columns[3:])

# Iterar sobre las columnas y convertirlas a tipo numérico
for columna in columnas_indicadores:
    df2[columna] = pd.to_numeric(df2[columna], errors='coerce')

df2 = df2.iloc[:-5]

###   ANALISIS PRELIMINAR: DATASET N°03 - Data_Extract_From_Population_estimates_and_projections

# Normalizando 
# Eliminado columnas
df3 = df3.drop(["Time Code"], axis=1)

# Lista de columnas a convertir a tipo numérico
columnas_indicadores = list(df3.columns[3:])

# Iterar sobre las columnas y convertirlas a tipo numérico
for columna in columnas_indicadores:
    df3[columna] = pd.to_numeric(df3[columna], errors='coerce')

df3 = df3.iloc[:-5]


###### Analizando los dataset, vimos que hay varios indicadores que se repiten en cada dataset, 
###### por eso decidimos unir el datset-3 y el dataset-1.

# Uniendo los dataset
df_unido = pd.merge(df3, df1, on=["Country Name", "Country Code", "Time"], how='left')

# Lista de columnas a convertir a tipo numérico
columnas_indicadores = list(df_unido.columns[3:])

# Iterar sobre las columnas y convertirlas a tipo numérico
for columna in columnas_indicadores:
    df_unido[columna] = pd.to_numeric(df_unido[columna], errors='coerce').round(1)

# Convertir solo en años la columna "Time"
df_unido["Time"] = df_unido["Time"].astype(int)

# Guardamos la columna en una variable
columna_time = df_unido["Time"]

# Eliminar la columna "Time"
df_unido = df_unido.drop("Time", axis=1)

# Insertar la columna "Time" en la primera posición
df_unido.insert(0, "Time", columna_time)

# Creamos la funcion 
def separar_nombre_codigo(columna):
    nombre = columna.rsplit(' [', 1)[0]
    codigo = columna.rsplit(' [', 1)[1][:-1]
    return nombre, codigo

# Lista de columnas que permanecerán iguales
columnas_iguales = ['Time', 'Country Name', 'Country Code']

# Crear un nuevo DataFrame con las columnas iniciales
nuevo_df = df_unido[columnas_iguales].copy()

# Definir columnas_a_eliminar como una lista vacía
columnas_a_eliminar = []

# Cambiar los nombres de las columnas y guardar los códigos de indicador en nuevas columnas
for columna in df_unido.columns[len(columnas_iguales):]:
    nuevo_nombre, nuevo_codigo = separar_nombre_codigo(columna)
    nuevo_df[nuevo_nombre] = df_unido[columna]
    #nuevo_df[nuevo_nombre + ' Code'] = nuevo_codigo
    columnas_a_eliminar.append(columna)  # Agregar la columna a la lista de columnas a eliminar

# Obtener la intersección entre las columnas a eliminar y las columnas en nuevo_df
columnas_a_eliminar = list(set(columnas_a_eliminar).intersection(nuevo_df.columns))

# Eliminar las columnas existentes en nuevo_df
nuevo_df.drop(columns=columnas_a_eliminar, inplace=True)

# Generando la data.
nuevo_df.to_csv("DATA_PF_III.csv", index= False)
print("Archivo final")

#Abriendo el archivo 
df = pd.read_csv("DATA_PF_III.csv")
df["Country Name"] = df["Country Name"].replace("Venezuela, RB", "Venezuela" ) 

df_4 = pd.read_csv("Tendencia_LE_y_HALE_data.csv", sep= ";")

df_pivot = df_4.pivot(index=['Year of Dated Year', 'País'], columns='Sexo Nombre', values='HALE')

# Reiniciar los nombres de las columnas
df_pivot.columns.name = None

# Reiniciar el índice
df_pivot.reset_index(inplace=True)

df_pivot.rename(columns={'Year of Dated Year': 'Time', "País": "Country Name", "Ambos sexos": "Esperanza de vida saludable, total", 
                "Hombre": "Esperanza de vida saludable, hombres", "Mujer": "Esperanza de vida saludable, mujeres"}, inplace=True)

# Lista de columnas a convertir a tipo numérico
columnas_indicadores = list(df_pivot.columns[2:])

# Iterar sobre las columnas y convertirlas a tipo numérico
for columna in columnas_indicadores:
    df_pivot[columna] = pd.to_numeric(df_pivot[columna], errors='coerce').round(1)

df_consolidado = pd.merge(df, df_pivot, on=["Country Name", "Time"], how='left')
df_consolidado.to_csv("DATA_PF_IV.csv", index= False)


##################################################   Automatizando la data   ##########################################################
##################################################   ---------------------   ##########################################################                        


# Cadena de conexión de tu cuenta de Azure Blob Storage
connection_string = "DefaultEndpointsProtocol=https;AccountName=almacendato;AccountKey=jOBJtA8VOALGZNx5/vS9JzQoP0U8qxWunaLFWrHSOnbRt9VO97/j6IvT8iVS6KBxgJsEwkUPjOml+AStZ10Bbw==;EndpointSuffix=core.windows.net"

# Nombre del contenedor y el archivo que deseas cargar
container_name = "almacen"
local_file_path = "DATA_PF_IV.csv"
blob_name = "DATA_PF_IV.csv"

# Crea una instancia del cliente BlobServiceClient utilizando la cadena de conexión
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Obtiene una referencia al contenedor
container_client = blob_service_client.get_container_client(container_name)

# Sube un archivo al contenedor
with open(local_file_path, "rb") as data:
    container_client.upload_blob(name=blob_name, data=data)

print("Archivo cargado correctamente en el Azure Blob Storage.")


