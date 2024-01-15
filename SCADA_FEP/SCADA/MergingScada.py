#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os


# In[2]:


file_names = [
    'station_dat.dat',
    'Status99.dat',
    'Analog99.dat',
    'ANALOG_CONFIG.dat',
    'device_instance_dat.dat',
    'Unit.dat'
]

# Leer el contenido de los archivos .dat y concatenarlos con saltos de línea
compiled_content = ''
for file_name in file_names:
    with open(file_name, 'r') as file:
        content = file.read()
        compiled_content += content + '\n'  # Agregar un salto de línea

# Agregar la primera línea requerida
compiled_content = '10 SCADA.DB\n' + compiled_content

# Agregar una línea con un 0 al final del contenido compilado
compiled_content += '0'

# Crear un archivo compilado
final_file_name = 'SCADA_Finished_Fix11.dat'
with open(final_file_name, 'w') as final_file:
    final_file.write(compiled_content)

print(f"Archivo {final_file_name} generado correctamente.")


# In[ ]:




