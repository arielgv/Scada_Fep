#!/usr/bin/env python
# coding: utf-8

# In[112]:


import pandas as pd
import os
from datetime import datetime
import numpy as np


# # STATION 

# Description: This script takes in a file named Station.csv(default) , recognizes its information and interprets the columns. Finally prints and save a Dat format file with the predefined tables for further processing

# Station Data Conversion REFERENCE : 
# 
# ORDER : Padded with incremental index numbering
# 
# Key : Column "Name" in Station.csv  . Erased blank spaces.('Example_ _')
# 
# Name : Column "Desc" in Station.csv . Erased blank spaces.('Example_ _')
# 
# AOR : Column Zones in Station.csv. 

# The .str.rstrip() method is widely used since many fields (almost all of them) have their value ending with two blank spaces.

# In[113]:


#Input Filename (default = Station.csv)
InputStationFile = "Station.csv"


# In[114]:


df = pd.read_csv(InputStationFile, skipinitialspace=True)
df.columns = df.columns.str.strip()

df_output = pd.DataFrame()
df_output['Order'] = range(1, len(df)+1) # Order column was not  specified in documentation. So in default is a unique incremental index.
df_output['Key'] = '"'+ df['Name'].str.rstrip() + '"'  
df_output['Name'] = '"' + df['Desc'].str.rstrip() + '"' 
df_output['AOR'] = df['Zones']

#sorting
df_output = df_output[['Order', 'Key', 'Name', 'AOR']]
df_station = df_output

#verification
print(df_station)


# In[115]:


# Crear un diccionario que mapee los valores actuales a los valores de reemplazo
replacement_dict = {
    '1  ': 1,
    '2  ': 2,
    '3  ': 3,
    '4  ': 4,
    '5  ': 5,
    '6  ': 6,
    '7  ': 7,
    '8  ': 8,
    '1 2 3 4 5 6 7  ': 9,
    '1 2 3 4 5 6 7 8  ': 10,
    '2 8  ': 11,
    '7 8  ': 12,
    '1 2  ': 13,
    '1 4  ': 14,
    '3 4  ': 15,
    '3 8  ': 16
}

df_station['AOR'] = df_station['AOR'].replace(replacement_dict)


# In[116]:


df_station


# # Select Output name: (default: station_dat.dat)

# In[117]:


folder_name = "SCADA_DAT_FILES"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

stationfilename = os.path.join(folder_name, "station_dat.dat")

now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
with open(stationfilename, 'w') as f:
    f.write("*\n")
    f.write("*\n")
    f.write(f"* Creation Date/Time: {now}\n")
    f.write("*\n")
    f.write("*\tOrder\tKey\tName\tAOR\n")
    f.write("*\n")
    f.write("\t2\tSTATION\t0\t3\t4\t13\n")
    f.write("*\n")

    for index, row in df_station.iterrows():
        f.write("{}\t{}\t{}\t{}\t{}\t{}\n".format
                ("", row['Order'], row['Order'], row['Key'], row['Name'], row['AOR']))
    f.write(" 0")  


# # END STATION

# --------------------------------------------------

# # DEVICE_INSTANCE

# Description: This script takes in a file named STATUS.csv , uses a column named 'NAME'
# Instruction : Remove the first three characters so only the text after the comma remains. Then delete repetitions . From the 5000 records we should end with about 3800. 

# Desired output:
# 
# */             Order  Name
# */             ----  -----      
# 	53	DEVICE_INSTANCE	0
# *---------------------------------------------------------------
# 	1	"MTXTOT"
# 	2	"DRD"
# 	3	"35C109"  

# In[118]:


df_device_instance = pd.read_csv('Status.csv')


# In[119]:


df_device_instance = df_device_instance[['Name  ']]


# In[120]:


df_device_instance['Name  '] = df_device_instance['Name  '].str.split(',', expand=True)[1].str.strip()


# In[121]:


df_device_instance


# In[122]:


df_device_instance = df_device_instance.drop_duplicates()


# In[123]:


df_device_instance


# In[124]:


df_device_instance['Number'] = range(1,len(df_device_instance)+1)


# In[125]:


df_device_instance = df_device_instance[['Number', 'Name  ']]


# In[126]:


df_device_instance


# In[127]:


device_inst_filename = os.path.join(folder_name, "device_instance_dat.dat")


# In[128]:


with open(device_inst_filename, 'w') as f:
    f.write("*\n")
    f.write("\t53\tDEVICE_INSTANCE\t0\n")
    f.write("*\tIndex\tName\n")

    for index, row in df_device_instance.iterrows():
        f.write("\t{}\t{}\n".format(row['Number'], row['Name  ']))
    
    f.write("0")


# In[129]:


df_analog_instance = pd.read_csv('Analog.csv')

df_analog_instance = df_analog_instance[['Name  ']]
df_analog_instance['Name  '] = df_analog_instance['Name  '].apply(lambda x: x.split(',')[1].strip())

#df_device_instance['Name  '] = df_device_instance['Name  '].str.split(',', expand=True)[1].str.strip()

#df_analog_instance['Name  '] = df_analog_instance['Name  '].strsplit(',', expand=True)[1].str.strip()
df_analog_instance = df_analog_instance.drop_duplicates()


# In[130]:


df_analog_instance


# In[131]:


# Concatenar los DataFrames df_device_instance y df_analog_instance
result_df = pd.concat([df_device_instance, df_analog_instance], ignore_index=True)
result_df.drop_duplicates(subset='Name  ', inplace=True, keep='first')

# Mostrar el DataFrame resultante
print(result_df)


# In[132]:


result_df


# In[133]:


df_device_instance = result_df


# In[134]:


df_device_instance['Number'] = range(1,len(df_device_instance)+1)


# In[135]:


df_device_instance


# In[136]:


device_inst_filename = os.path.join(folder_name, "device_instance_dat.dat")


# In[137]:


with open(device_inst_filename, 'w') as f:
    f.write("*\n")
    f.write("\t53\tDEVICE_INSTANCE\t0\n")
    f.write("*\tIndex\tName\n")

    for index, row in df_device_instance.iterrows():
        f.write("\t{}\t{}\n".format(row['Number'], row['Name  ']))
    
    f.write("0")


# _________________

# _________

# # STATUS

# Description: This script takes in a file named Status.csv(default) , recognizes its information and interprets the columns. Finally prints and save a Dat format file with the predefined tables for further processing

# Station Data Conversion REFERENCE : 
# 
# (1)Type : ( 
#        
#             If column "Telem_A" in status.csv = empty. C_IND.   Type = 5
# 
#             If column "Telem_A" in status.csv = any number. T_IND.  Type = 1
#             
#             If column "Open_B" in status.csv = 12.  T_I&C.     Type = 2  ) 
#                 Criteria: only 42 rows (0,49%) has Open_B= 12.
#                         so its gonna be Type = 2 regardless the value of Telem_A, 
#                         giving priority to Open_B.
#                         (In evey case of Open_B=12, Telem_A showed a number also)
#               
#               Edited:  IF column Stn = 054 (PS. PSEUDO POINTS) , M_IND. Type = 8 
# 
# (3)Key : Format XXYYYZZZ
#                          XX =   If type (descripted before) = 1 , XX = 01
#                                 If type (descripted before) = 2 , XX = 01
#                                 If type (descripted before) = 5 , XX = 02
#                                 If type (descripted before) = 8 , XX = 12
#                          YYY = Stn (Station Order number.)(descripted in this Markdown)
#                          ZZZ = Incremental number per station
# 
# (4)Name : Column "Name" + column "Desc" in Status.csv. Replace the commas (,) with blank spaces.
# 
#       *****
#        Updated : 2019-03-06 . (4) Name : Column "Desc" in Status.csv . If not defined will be set to Key 
# 
# (5) Stn : (XXX) -> The first characters of the "Name" column in the current dataset, before the comma (,), reference the value of the KEY column in the previous dataset (Station). This value is based on the Order column. This number should be expressed in three digits (e.g., 38 = 038).
# 
# (10) Aor : Column "Zones" in Status.csv
# 
# (19) pState : Column "Presuffx" in Status.csv
# 
# (49) Norm : Column "Normal_State" in Status.csv
# 
# (29) AlarmGroup: Will be set to 1 unless defined in mapping document
# 
# (41) ICAddress : Refer to documentation. This script leaves it in blank
# 
# * ***UPDATE : 
# (107) pDeviceInstance : Column "Name" in Status.csv . Get the string after the comma, then search for the matching record of the objet DEVICE_INSTANCE. 
# 

# In[138]:


#Input filename(default: "Status.csv")
InputStatusFile = "Status.csv"


# In[139]:


status_df = pd.read_csv(InputStatusFile)
df_status = pd.DataFrame()


# In[140]:


df_status['record'] = range(1, len(status_df)+1) 
df_status['OrderNo'] = range(1, len(status_df)+1) 


df_status['Type'] = np.where(status_df['Open_B  '] == '12  ', 2, np.where(status_df['Telem_A  '].replace('  ', np.nan).notna(), 1, 5))
#df_status['Name'] = status_df['Name  '].str.replace(',',' ') + " " + status_df['Desc  ']
#df_status['Name'] = df_status['Name'].str.rstrip()
df_status['Name'] = status_df['Desc  ']
df_status['AOR'] = status_df['Zones  '].str.rstrip()
df_status['AOR'] = df_status['AOR'].str.replace(r'\s+', '', regex=True)
df_status['pState'] = status_df['PreSuffx  ']
df_status['Norm'] = status_df['Normal_State  ']
df_status['AlarmGroup'] = 1
df_status['ICAddress'] = 0


# In[141]:


replacement_dict = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '1234567': 9,
    '12345678': 10,
    '28': 11,
    '78': 12,
    '12': 13,
    '14': 14,
    '34': 15,
    '38': 16
}


df_status['AOR'] = df_status['AOR'].replace(replacement_dict)


# In[142]:


df_status


# In[143]:


status_df


# In[ ]:





# In[144]:


#df_status['TempName'] = status_df['Name  '].str[3:]

# Elimina espacios en blanco al final de la columna temporal
#df_status['TempName'] = df_status['TempName'].str.rstrip()



df_status['TempName'] = status_df['Name  '].str.split(',', expand=True)[1].str.strip()

# Realiza la asignación de números basada en el nombre temporal
df_status['pDeviceInstance'] = df_status['TempName'].map(df_device_instance.set_index('Name  ')['Number'])

# Borra la columna temporal
df_status.drop(columns=['TempName'], inplace=True)

# Muestra el DataFrame resultante con la nueva columna
print(df_status)



# # Stn :

# This code strips the Name column in status and search the matching row Key in Station Dataframe
# then, it reads the Order column value and assign this to the Stn column

# In[145]:


status_df['Key'] = status_df['Name  '].str.split(',').str[0].str.strip()  # make sure no blank spaces are in the begin & end of the name
df_station['Key'] = df_station['Key'].str.replace('"', '')
stn_values = []  #list for store stn values


# In[146]:


status_df['Key'] = status_df['Name  '].str.split(',').str[0].str.strip()

# Lista para almacenar los valores de 'Stn'
stn_values = []

for i in range(len(status_df)):
    key_value = status_df.loc[i, 'Key']
    
    if key_value == 'PS':
        # Extrae los dos primeros caracteres después de la coma
        first_two_chars_after_comma = status_df.loc[i, 'Name  '].split(',')[1][:2].strip()

        # Verifica si first_two_chars_after_comma está en df_station['Key']
        if first_two_chars_after_comma in df_station['Key'].values:
            key_value = first_two_chars_after_comma
        elif first_two_chars_after_comma == 'FP':  # Nueva condición para FP
            print(f"FP encontrado, cambiando a FSP en fila {i}")
            key_value = 'FSP'
        elif first_two_chars_after_comma == 'UC':  # Nueva condición para UC
            print(f"UC encontrado, cambiando a UCI en fila {i}")
            key_value = 'UCI'
        else:
            key_value = 'PS'
    
    matching_row = df_station[df_station['Key'] == key_value]
    if not matching_row.empty:
        stn_values.append(f"{matching_row['Order'].values[0]:03}")
    else:
        stn_values.append(np.nan)

df_status['Stn'] = stn_values


# In[147]:


count_054 = df_status['Stn'].value_counts().get('055', 0)
print(f"El conteo de '055' (PS) en la columna 'Stn' es: {count_054}")


# In[148]:


df_status['Stn'].value_counts()


# In[149]:


df_status.head(20)


# Replacement case: Pseudo Points.
# IF stn = 054 (PS. Pseudo points.) Set type to 8 .   And then set XX Value to 12

# In[150]:


df_status.loc[df_status['Name'].str.startswith("PS"), 'Type'] = 8

for i in range(len(df_status)):
    if df_status.loc[i, 'Stn'] == '054':
        key_to_search = df_status.loc[i, 'Name'][3:5]

        # Buscar valor 
        matching_row = df_station[df_station['Key'] == key_to_search]

        # != una fila correspondiente, 'Stn' en 'df_status'
        if not matching_row.empty:
            df_status.loc[i, 'Stn'] = f"{matching_row['Order'].values[0]:03}"


# # KEY

# In[151]:


key_values = []
xx_yyy_counters = {}  # creating a dict to store and count every YYY. It's used for a incremental ZZZ


# In[152]:


for i in range(len(df_status)):
    
    if df_status.loc[i, 'Type'] == 1:
        xx = '01'
    elif df_status.loc[i, 'Type'] == 2:
        xx = '01'
    elif df_status.loc[i, 'Type'] == 5:
        xx = '05'
    elif df_status.loc[i, 'Type'] == 8:
        xx = '12'
    else:
        xx = '99'  # ERROR CASE . In case of being unable to find a coincidence.

    yyy = df_status.loc[i, 'Stn']

    # combination
    key = xx + yyy

    # if key exists in counters, then add +1 , else, initialites it.
    if key in xx_yyy_counters:
        xx_yyy_counters[key] += 1
    else:
        xx_yyy_counters[key] = 1

    #   Current Value of ZZZ . 
    zz = f"{xx_yyy_counters[key]:03}"  #03 (Default). the number of Z in the format (default XX YYY ZZZ (3 Z))

    key_values.append(xx + yyy + zz)


# In[153]:


df_status['Key'] = key_values


# In[154]:


#obtaining and showing the counting of Types.
type_counts = df_status['Type'].value_counts()
print(type_counts)


# In[155]:


df_status


# In[156]:


new_order = ['record', 'OrderNo','Type','Key','Name','Stn','AOR','pState','Norm','AlarmGroup','ICAddress','pDeviceInstance']
df_status = df_status[new_order]


# In[157]:


df_status


# In[158]:


df_status['Key'] = '"'+ df_status['Key'].str.rstrip() + '"'


# In[159]:


df_status['Name'] = '"'+ df_status['Name'].str.rstrip() + '"'


# In[160]:


df_status


# In[161]:


df_status['pState'] = df_status['pState'] + 200 


# In[162]:


df_status


# # DATASET Status ready.

# # OUTPUT TO DAT FILE :

# In[163]:


output_status_name = 'Status99.dat'


# In[164]:


with open(output_status_name, 'w') as f:
    f.write('*\n')
    f.write('\t4\tSTATUS\t0\t1\t3\t4\t5\t10\t19\t49\t29\t41\t107\n')
    f.write('*\trecord\tOrderNo\tType\tKey\tName\tStn\tAOR\tpState\tNorm\tAlarmGroup\tICAddress\tpDeviceInstance\n')

    for index, row in df_status.iterrows():
        f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format
                (row['record'], row['OrderNo'], row['Type'], row['Key'], row['Name'], row['Stn'], row['AOR'], row['pState'], row['Norm'], row['AlarmGroup'], row['ICAddress'], row['pDeviceInstance']))
    f.write("0")  


# # END STATUS

# -------------------------------

# # ANALOG

# Description: This script takes in a file named Analog.csv(default) , recognizes its information and interprets the columns. Finally prints and save a Dat format file with the predefined tables for further processing

# ANALOG Data conversion REFERENCE :
# 
#  Type (1) :  Columns : 
#  ///
#  
#             IF Telem_B  !=  21  . T_ANLG  = type : 1
# 
#         IF Telem_RTU = blank .   C_ANLG =  Type : 2
# 
#         IF NOT Defined. Manual = Type: 3 
# 
# * CRITERIA: 100% of the Telem_B column is different from 21, while 40% of the Telem_RTU column is blank. To prioritize visibility of Telem_RTU in case of conflict, the priority will be given to C_ANLG (Type 2).
#     ///
# 
# 
# Key (3)   :  XX YYY ZZZ
# 
# Name (4)  :  Columns :  Desc . 
#                 If not defined, set to KEY 
# 
# Stn (5)   :  ###  -> The first characters of the "Name" column in the current dataset, before the comma (,), reference the value of the KEY column in the Station dataset. This value has a number based on the Order column. This number should be expressed in three digits (e.g., 38 = 038).
# 
# AOR (10)  :   Column Zones in Analog.csv
# 
# pScale (24): Column EU_HI in Analog.csv
# 
# AlarmGrp  (42)  :  Set to default: 1
# 
# ICAddress (66)  : 12/29 : Value : "". If this is Nan or 0 , it will raise an error.
# ______________________________________
# NominalHiLimits (77,1)
# 
# NominalHiLimits (77,2)
# 
# NominalHiLimits (77,3)
# 
# NominalHiLimits (77,4):  column * Alm_unrHi * in Analog.csv , named in this df:  Nominal_HiLim
# 
#  *Edited:  NominalHiLimits (77,4): RENAMED TO HiLim[1]  (Rsnblty)
# 
# NominalLowLimits (78,1)
# 
# NominalLowLimits (78,2)
# 
# NominalLowLimits (78,3)
# 
# NominalLowLimits (78,4):  column Alm_unrLo in Analog.csv  , named in this df: Nominal_LoLim
# 
#  *Edited: RENAMED TO LoLim[1]   (Rsnblty)
# 
#  ADDED:NominalHiLimits (77,0): Column Alm_preHi in Analog.csv, named in this df: HiLim[0]    (High)
# 
#  ADDED:NominalLowLimits (78,0): Colum Alm_preLo in Analog.csv, named in this df: LoLim[0]    (Low)
#  
# 
#  RG 9/14: There are three cases. 
# 
# 1. Hi limits are present but Lo are empty
# 
# If Alm_preHi, Alm_emgHi, Alm_unrHi have values but  Alm_preLo, Alm_emgLo, Alm_unrLo  are empty then set 78,0 to -99995 , 78,1 to -99996, 78,4 to -99999  and follow cells H89 and H90
# 
# 2. Lo limits are present but Hi are empty
# 
# If Alm_preLo, Alm_emgLo, Alm_unrLo have values but Alm_preHi, Alm_emgHi, Alm_unrHi are empty then set 77,0 to 99995 , 77,1 to 99996, 77,4 to 99999  and follow cells H91 and H92
# 
# 3. Hi and Lo limits are present. 
# 
# Follow indications of column H89, H90, H91 and H92
# Put the actual values presents.
# 
# 4. Hi and Lo are empty. Set 77,4 to 999999 and 78,4 -999999 , set 77,1 and 77,2 and 78,1 and 78,2 to 0.
# 
# 
# _____________________________________
# 
# NominalPairInactive (91) : RG 9/14: For cases 1,2 and 3 of cell I89 set to 0 the 91,1 and 91,2 and 91,3  , and set to 1 the  91,4 and 91,5 .
# 
# 91,1 91,2 91,3 . 91,4 91,5 
# 
# 
#     
#    

# In[165]:


#Data CSV Name entry
analog_file = "Analog.csv"


# las condiciones para el llenado de las columnas son las siguientes :
# 
# 1. Hi limits are present but Lo are empty:
# 
# If 'Alm_preHi  ', 'Alm_emgHi  ', 'Alm_unrHi  '(columnas encontradas dentro de df_analog)  have values but  'Alm_preLo  ', 'Alm_emgLo  ', 'Alm_unrLo  '(columnas encontradas dentro de df_analog)  are empty , then set Alm_preLo (de df_new) to -99995 , 78,1(crear esta columna) to -99996, 78,4(crear esta columna) to -99999  
# 
# Condicion 2:
# 2. Lo limits are present but Hi are empty
# 
# If 'Alm_preLo  ', 'Alm_emgLo  ', 'Alm_unrLo  '(columnas de df_analog)  have values but 'Alm_preHi  ', 'Alm_emgHi  ', 'Alm_unrHi  ' are empty then set Alm_preHi(de df_new) to 99995 , 77,1(crear esta columna) to 99996, 77,4(crear esta columna ) to 99999 
# 
# Condicion 3:
# 3. Hi and Lo limits are present. 
# 
# Tomar los valores presentes en df_analog para las columnas 'Alm_preHi  ', 'Alm_unrHi  ' y 'Alm_preLo  ', 'Alm_unrLo  ' y asignarlos a las columnas 'Alm_preHi', 'Alm_unrHi' y 'Alm_preLo', 'Alm_unrLo' de df_new.
# 
# 
# 

# In[166]:


df_analog = pd.read_csv(analog_file)

df_new = pd.DataFrame()
df_new['record'] = range(1, len(df_analog)+1) 
df_new['OrderNo'] = range(1, len(df_analog)+1) 


df_new['Type'] = 1

count_type_3 = 0

for index, row in df_analog.iterrows():
    name = row['Name  ']
    telem_rtu = row['Telem_RTU  ']

    # Primera condición: si 'Name' contiene 'PS' en los primeros 4 caracteres
    if 'PS' in name[:4]:
        df_new.at[index, 'Type'] = 3
        count_type_3 += 1
        continue  # Saltar a la siguiente iteración

    # Segunda condición: si 'Telem_RTU' es igual a dos espacios en blanco
    if telem_rtu == "  ":
        df_new.at[index, 'Type'] = 2

# Las demás columnas

df_new['Name'] = df_analog['Desc  ']
df_new['AOR'] = df_analog['Zones  ']
df_new['AlarmGrp'] = 1
df_new['ICAddress'] = ''

print(f"'Type' = 3: {count_type_3}")


# HI LOW LIMITS

# In[167]:


for col in ['77,0', '77,1', '77,2', '77,3', '77,4', '78,0', '78,1', '78,2', '78,3', '78,4']:
    df_new[col] = 0  

for col in ['91,1', '91,2', '91,3', '91,4', '91,5']:
    df_new[col] = np.nan


    # SE PRUEBA LO SIGUIENTE:
# Mapeo entre las columnas en df_analog y las columnas en df_new
column_mapping = {
    'Alm_emgHi  ': '77,1',
    'Alm_preHi  ': '77,0',
    'Alm_unrHi  ': '77,4',
    'Alm_preLo  ': '78,0',
    'Alm_emgLo  ': '78,1',
    'Alm_unrLo  ': '78,4',
}

# Aplicar las condiciones y asignar los valores
for analog_col, new_col in column_mapping.items():
    # Crear una máscara para identificar las filas donde el valor no es "0  " o es no nulo
    mask = (df_analog[analog_col] != "0  ") & (df_analog[analog_col].notna())
    # Asignar el valor de la columna en df_analog a la columna correspondiente en df_new
    df_new.loc[mask, new_col] = df_analog.loc[mask, analog_col]



    #####

# Condición 1:
mask1 = (
    df_analog[['Alm_preHi  ', 'Alm_emgHi  ', 'Alm_unrHi  ']].notna().any(axis=1) &
    df_analog[['Alm_preLo  ', 'Alm_emgLo  ', 'Alm_unrLo  ']].isin(["0  ", "  "]).all(axis=1)
)
df_new.loc[mask1, '78,0'] = -999995
df_new.loc[mask1, '78,1'] = -999996
df_new.loc[mask1, '78,4'] = -999999
df_new.loc[mask1, ['91,1', '91,2', '91,3']] = 0
df_new.loc[mask1, ['91,4', '91,5']] = 1


# Condición 2:
mask2 = (
    df_analog[['Alm_preLo  ', 'Alm_emgLo  ', 'Alm_unrLo  ']].notna().any(axis=1) &
    df_analog[['Alm_preHi  ', 'Alm_emgHi  ', 'Alm_unrHi  ']].isin(["0  ", "  "]).all(axis=1)
)
df_new.loc[mask2, '77,0'] = 999995
df_new.loc[mask2, '77,1'] = 999996
df_new.loc[mask2, '77,4'] = 999999
df_new.loc[mask2, ['91,1', '91,2', '91,3']] = 0
df_new.loc[mask2, ['91,4', '91,5']] = 1


# Condición 3:
df_new['77,0'] = df_analog['Alm_preHi  ']
df_new['77,4'] = df_analog['Alm_unrHi  ']
df_new['78,1'] = df_analog['Alm_emgLo  ']
df_new['78,4'] = df_analog['Alm_unrLo  ']
df_new.loc[df_new['77,0'].notna() | df_new['78,1'].notna(), ['91,1', '91,2', '91,3']] = 0
df_new.loc[df_new['77,0'].notna() | df_new['78,1'].notna(), ['91,4', '91,5']] = 1


# Condición 4:
mask4 = (
    df_analog[['Alm_preHi  ', 'Alm_emgHi  ', 'Alm_unrHi  ', 'Alm_preLo  ', 'Alm_emgLo  ', 'Alm_unrLo  ']].isin(["0  ", "  "]).all(axis=1)
)
df_new.loc[mask4, '77,4'] = 999999
df_new.loc[mask4, '78,4'] = -999999
df_new.loc[mask4, ['77,1', '77,2', '78,1', '78,2']] = 0


# In[168]:


df_new


# In[169]:


#df_analog['EU_Hi  '] = df_analog['EU_Hi  '].apply(keep_decimal_precision)
df_new['pScale EU_Hi'] = df_analog['EU_Hi  ']


# In[170]:


df_new


# # STN 

# In[171]:


df_analog['Key'] = df_analog['Name  '].str.split(',').str[0].str.strip()

stn_values = []

for i in range(len(df_analog)):
    
    matching_row = df_station[df_station['Key'] == df_analog.loc[i, 'Key']]
    
    if not matching_row.empty:
        stn_values.append(f"{matching_row['Order'].values[0]:03}")
    else:
        stn_values.append(np.nan)
df_new['Stn'] = stn_values


# In[172]:


df_new


# # KEY

# In[173]:


cols = ['Alm_unrHi', 'Alm_unrLo', 'Alm_preHi', 'Alm_preLo', '78,1', '78,4', '77,1', '77,4']
for col in cols:
    if col not in df_new.columns:
        df_new[col] = np.nan



# In[174]:


key_values = []
xx_yyy_counters = {}


# In[175]:


for i in range(len(df_new)):
    
    # Asignamos el valor correspondiente a 'XX' según el valor de 'Type'
    if df_new.loc[i, 'Type'] == 1:
        xx = '03'
    elif df_new.loc[i, 'Type'] == 2:
        xx = '04'
    else:
        xx = '99'  # ERROR CASE


    yyy = str(df_new.loc[i, 'Stn'])

    key = xx + yyy

    if key in xx_yyy_counters:
        xx_yyy_counters[key] += 1
    else:
        xx_yyy_counters[key] = 1

    zz = f"{xx_yyy_counters[key]:03}"

    key_values.append(xx + yyy + zz)

df_new['Key'] = key_values


# In[176]:


df_new


# In[177]:


#df_new = df_new[['record', 'OrderNo','Type', 'Key', 'Name', 'Stn', 'AOR', 'Nominal_HiLim', 'Nominal_HiLim1', 'Nominal_LoLim', 'Nominal_LoLim1', 'pScale EU_Hi', 'AlarmGrp']].copy()
#df_new['ICAddress'] = "NaN"


# df_ner['NominalPairInactive'] 

# In[178]:


new_column_order = ['record', 'OrderNo', 'Type', 'Key', 'Name', 'Stn', 'AOR',
                    '77,0', '77,1', '77,2', '77,3', '77,4',
                    '78,0', '78,1', '78,2', '78,3', '78,4',
                    '91,1', '91,2', '91,3', '91,4', '91,5',
                    'pScale EU_Hi', 'AlarmGrp', 'ICAddress']


df_new = df_new[new_column_order]



# In[179]:


df_new['77,1'].head(10)


# In[180]:


df_new['Key'] = '"'+ df_new['Key'].str.rstrip() + '"'
df_new['Name'] = '"'+ df_new['Name'].str.rstrip() + '"'


# In[181]:


df_new.loc[df_new['77,4'] == 0, '77,4'] = 999999
df_new.loc[df_new['77,4'] == '  ', '77,4'] = 999999

df_new.loc[df_new['77,1'] == 0, '77,1'] = 999996
df_new.loc[df_new['77,1'] == '  ', '77,1'] = 999996

df_new.loc[df_new['77,0'] == 0, '77,0'] = 999995
df_new.loc[df_new['77,0'] == '  ', '77,0'] = 999995

#df_new.loc[df_new['78,0'] == 0, '78,0'] = -999995
df_new.loc[df_new['78,0'] == '  ', '78,0'] = -999995

df_new.loc[df_new['78,1'] == 0, '78,1'] = -999996
df_new.loc[df_new['78,1'] == '  ', '78,1'] = -999996

df_new.loc[df_new['78,4'] == 0, '78,4'] = -999999
df_new.loc[df_new['78,4'] == '  ', '78,4'] = -999999


# In[182]:


borrador = """df_new['77,4'] = df_new['77,4'].replace({0: 999999, '  ': 999999})
df_new['77,1'] = df_new['77,1'].replace({0: 999996, '  ': 999996})
df_new['77,0'] = df_new['77,0'].replace({0: 999995, '  ': 999995})
df_new['78,0'] = df_new['78,0'].replace({0: -999995, '  ': -999995})
df_new['78,1'] = df_new['78,1'].replace({0: -999996, '  ': -999996})
df_new['78,4'] = df_new['78,4'].replace({0: -999999, '  ': -999999})"""


# In[183]:


#df_analog['Alm_preLo  '].to_csv('borrrrar.csv')


# In[184]:


df_analog['Alm_preLo  '] = df_analog['Alm_preLo  '].astype(str).str.strip()
df_new['78,0'] = df_new['78,0'].astype(str).str.strip()

# Encontrar las filas donde 'Alm_preLo' es '0' y la columna 78,0 es '-999995'
mask = (df_analog['Alm_preLo  '] == '0  ') & (df_new['78,0'] == '-999995')

# Copiar los valores de 'Alm_preLo' a la columna 78.0 en las filas correspondientes
df_new.loc[mask, '78,0'] = df_analog.loc[mask, 'Alm_preLo  ']




# In[185]:


df_new.head(10)


# In[186]:


df_new['AOR'] = df_new['AOR'].str.replace(r'\s+', '', regex=True)


# In[187]:


# Crear un diccionario que mapee los valores actuales a los valores de reemplazo
replacement_dict = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '1234567': 9,
    '12345678': 10,
    '28': 11,
    '78': 12,
    '12': 13,
    '14': 14,
    '34': 15,
    '38': 16
}

# Reemplazar los valores en la columna 'AOR' usando el diccionario de reemplazo
df_new['AOR'] = df_new['AOR'].replace(replacement_dict)


# In[188]:


df_new['78,1'] = df_new['78,1'].replace({'0  ': -999996})
df_new['78,4'] = df_new['78,4'].replace({'0  ': -999999})


# In[189]:


def modificar_type(fila):
    if fila['Name'].startswith('"PS'):
        return 3
    else:
        return fila['Type']
df_new['Type'] = df_new.apply(modificar_type, axis=1)


# In[190]:


#df_new.to_csv('borrardf_new.csv', index=False)


# In[191]:


filas_con_ps = df_new[df_new['Name'].str.startswith('"PS')]

# Contamos el número de filas
numero_de_filas = len(filas_con_ps)

print("Número de filas que comienzan con 'PS':", numero_de_filas)


# Output Filename:

# In[192]:


output_analog_name = 'Analog99.dat'


# In[193]:


with open(output_analog_name, 'w') as f:
    f.write('* \n')
    f.write('\t5\tANALOG\t0\t1\t3\t4\t5\t10\t24\t42\t77,4\t77,1\t77,0\t78,0\t78,1\t78,4\t91,1\t91,2\t91,3\t91,4\t91,5\t66\n')
    f.write('*\trecord\tOrderNo\tType\tKey\tName\tStn\tAOR\tpScale EU_Hi\tAlarmGrp\t77,4\t77,1\t77,0\t78,0\t78,1\t78,4\tNomPairInactive91,1\t91,2\t91,3\t91,4\t91,5\tICAddress\n')

    for index, row in df_new.iterrows():
        f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format
                ("", row['record'], row['OrderNo'], row['Type'], row['Key'], row['Name'], row['Stn'], row['AOR'],row['pScale EU_Hi'], row['AlarmGrp'], row['77,4'], row['77,1'], row['77,0'], row['78,0'], row['78,1'], row['78,4'], row['91,1'], row['91,2'], row['91,3'], row['91,4'], row['91,5'], row['ICAddress']))
    f.write("0")  


# ________

# ________

# # ANALOG_CONFIG

# vamos a crear un dataframe llamado Analog_config , el cual tendrá solo dos columnas, una columna se llamara Key , cuyo contenido será exactamente el contenido de Key del df  llamado df_new . y una columna se llamara name , que vendra de df_analog['Name  '] 

# In[194]:


Analog_config = pd.DataFrame({
    'Key': df_new['Key'],
    'name': df_analog['Name  '].str.split(',', expand=True)[1].str.strip()# Obtener los caracteres a partir de la coma
    
})

#df_analog['Name  '].str.split(',', expand=True)[1].str.strip()


# Crear una función para buscar el número en df_device_instance
def find_number(name):
    match = df_device_instance[df_device_instance['Name  '] == name]
    if not match.empty:
        return match.iloc[0]['Number']
    else:
        return None

# Aplicar la función para obtener los números y almacenarlos en Analog_config['pDeviceInstance']
Analog_config['pDeviceInstance'] = Analog_config['name'].apply(find_number)

# Ahora, Analog_config contendrá la columna 'pDeviceInstance' con los números correspondientes.


# In[195]:


Analog_config


# In[196]:


df_device_instance


# In[197]:


print(set(Analog_config['name']).intersection(set(df_device_instance['Name  '])))


# In[198]:


print("Unique names in Analog_config:", Analog_config['name'].unique()[:10])  # muestra los primeros 10
print("Unique names in df_device_instance:", df_device_instance['Name  '].unique()[:10])  # muestra los primeros 10


# In[199]:


df_device_instance


# In[200]:


Analog_config


# In[201]:


# HABILITAR ESTO Analog_config.drop('name', axis=1, inplace = True )


# In[202]:


Analog_config['record'] = range(1, len(Analog_config) + 1)


# In[203]:


Analog_config


# In[204]:


Analog_config.to_csv('AnalogConfig.csv', index=False)


# In[205]:


with open('ANALOG_CONFIG.dat', 'w') as f:
    f.write("*\n")
    f.write("\t41\tANALOG_CONFIG\t0\t9\n")
    f.write("*\tKEY\tpDeviceInstance\n")

    for index, row in Analog_config.iterrows():
        f.write("\t{}\t{}\t{}\n".format(row['record'],row['Key'], row['pDeviceInstance']))
    
    f.write("0")


# _____________
# ___________

# # UNIT
# 
# Source: Analog.csv
# 
# 
# Record (0): ORDER Padded with incremental index numbering
# 
# 
# Name (0) : Analog['EuText  '] : RG 12/29: Delete repetitions and shift records up to avoid having empty spaces. 
# 
# 

# In[206]:


analog_file = "Analog.csv"
df_analog = pd.read_csv(analog_file)


df_unit = pd.DataFrame()
df_unit['name'] = df_analog['EuText  '].drop_duplicates(keep='first').reset_index(drop=True)
df_unit = df_unit[df_unit['name'].notna() & (df_unit['name'].str.strip() != '')]


df_unit['record'] = range(1, len(df_unit['name']) + 1)

print(df_unit.head())



# In[207]:


with open('Unit.dat', 'w') as f:
    f.write("*\n")
    f.write("\t42\tUnit\t0,1\t0\n")
    f.write("*\tRecord\tName\n")

    for index, row in df_unit.iterrows():
        f.write("\t{}\t{}\n".format(row['record'],row['name']))
    
    f.write("0")


# __________
# ____________

# # ACCUMULATOR

# ANALOG ACCUMULATOR - REFERENCE :
# Resource : Analog.csv
# Type (1) = Analog ['Telem_B '] : If Telem_B = 21, then T_ACCUM=1. If not defined will be set to 3: Manual
# Key (3) = 8 characters.  See Key Strategy
# Name (4) = Analog : Name + Desc. 
# Station (5) = Analog['Name '] . pstation, XXX. Where pstation links to 'Name' in COSERV_STATION. If not defined will be set to dummy station
# pAORGroup (10) = Analog['Zones '] =  Will be set to 1 unless defined in mapping document
# 
# pUNIT (19) = Analog['EUText ']  = RG 12/29: Pointer to the matching record of the object UNIT
# 
# pScale (38) = Analog['Eu_Hi ']. If not defined (Type 1 only) will be set to Scale=1, Offset=0
# 
# pALARM_GROUP (42) = Will be set to 1 unless defined in mapping document

# In[208]:


#Data CSV Name entry
analog_file = "Analog.csv"
df_analog = pd.read_csv(analog_file)

df_accumulator = pd.DataFrame()

df_accumulator['Type'] = df_analog['Telem_B  '].apply(lambda x: 1 if x == '21  ' else 3)

df_accumulator['Name'] = df_analog['Desc  ']

df_accumulator['pAORGroup'] = 1



# In[209]:


unit_mapping = df_unit.set_index('name')['record'].to_dict()
df_accumulator['pUNIT'] = df_analog['EuText  '].map(unit_mapping)

print(df_accumulator.head())


# In[210]:


df_accumulator['pUNIT'] = df_accumulator['pUNIT'].apply(lambda x: '' if pd.isna(x) else str(int(x)))



# In[211]:


df_accumulator['pScale'] = df_analog['EU_Hi  ']


# In[212]:


df_accumulator['pALARM_GROUP'] = 1


# In[213]:


df_accumulator


# In[214]:


with open('Accumulator.dat', 'w') as f:
    f.write("*\n")
    f.write("\t6\tAccumulator\t1\t4\t10\t19\t38\t42\n")
    f.write("*\tType\tName\tpAORGROUP\tpUNIT\tpScale\tpALARM_GROUP\n")

    for index, row in df_accumulator.iterrows():
        f.write("\t{}\t{}\t{}\t{}\t{}\t{}\n".format(row['Type'],row['Name'],row['pAORGroup'],row['pUNIT'],row['pScale'],row['pALARM_GROUP']))
    
    f.write("0")


# 
