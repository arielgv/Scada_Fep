###### REQUIERE : pandas, openpyxl
import os
import pandas as pd

####
# Instrucciones:
# 0. pip install pandas openpyxl
# 1. Crear una carpeta llamada 'PreFiles' en la misma carpeta que este archivo.
# 2. Colocar en la carpeta 'PreFiles' los archivos.xlsx que se quieran procesar.
# 3. Ejecutar el archivo.
# 4. Los archivos.xlsx procesados se guardarán en la carpeta 'Output_merge', con el nombre all_stations_equivalency.csv
####



carpeta_prefiles = 'PreFiles'


columnas_esperadas = ['Point ID', 'Station', 'Pnuemonic', 'Description', 'COM', 'RTU', 'Pg', 'Status P', 'Analog P', 'Relay P', 'Value', 'Scale', 'Type', 'Helper Column', 'IP Address', 'DNPAddress', 'DNP Point', '', '']


archivos = [archivo for archivo in os.listdir(carpeta_prefiles) if archivo.endswith('.xlsx')]


print(f"Se van a procesar {len(archivos)} archivos.")


dataframes = []


for archivo in archivos:
    ruta_archivo = os.path.join(carpeta_prefiles, archivo)
    df = pd.read_excel(ruta_archivo, header=None, names=columnas_esperadas)
    

    if df.shape[1] != len(columnas_esperadas):
        print(f"El archivo {archivo} no tiene la estructura esperada. Se omitirá.")
        continue
    
    dataframes.append(df)

df_merged = pd.concat(dataframes, ignore_index=True)
df_merged = df_merged[pd.to_numeric(df_merged['Point ID'], errors='coerce').notna()]


carpeta_output = 'Output_merge'
os.makedirs(carpeta_output, exist_ok=True)

outputfilename = 'all_stations_equivalency.csv'
ruta_output = os.path.join(carpeta_output, outputfilename)

df_merged.to_csv(ruta_output, index=False)

print(f'Proceso completado. El archivo {outputfilename} se ha generado en la carpeta {carpeta_output}.')