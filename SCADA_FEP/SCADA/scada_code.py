#!/usr/bin/env python
# coding: utf-8

# ## Required Files:
# 
# Station.csv
# 
# Status.csv
# 
# Analog.csv
# 
# all_stations_equivalency.csv
# 
# ## Outputs generated and needed for run FEP :
# 
# status_xref.csv 
# 
# analog_xref.csv 
# 
# 

# In[1]:


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

# In[2]:


InputStationFile = "Station.csv"


# In[3]:


df = pd.read_csv(InputStationFile, skipinitialspace=True)
df.columns = df.columns.str.strip()

df_output = pd.DataFrame()
df_output['Order'] = range(1, len(df)+1) 
df_output['Key'] = '"'+ df['Name'].str.rstrip() + '"'  
df_output['Name'] = '"' + df['Desc'].str.rstrip() + '"' 
df_output['AOR'] = df['Zones']


df_output = df_output[['Order', 'Key', 'Name', 'AOR']]
df_station = df_output

print(df_station)


# In[4]:


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


# In[5]:


df_station


# # Select Output name: (default: station_dat.dat)

# In[6]:


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

# In[7]:


df_device_instance = pd.read_csv('Status.csv')


# In[8]:


df_device_instance = df_device_instance[['Name  ']]


# In[9]:


df_device_instance['Name  '] = df_device_instance['Name  '].str.split(',', expand=True)[1].str.strip()


# In[10]:


df_device_instance


# In[11]:


df_device_instance = df_device_instance.drop_duplicates()


# In[12]:


df_device_instance


# In[13]:


df_device_instance['Number'] = range(1,len(df_device_instance)+1)


# In[14]:


df_device_instance = df_device_instance[['Number', 'Name  ']]


# In[15]:


df_device_instance


# In[16]:


folder_name = "SCADA_DAT_FILES"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)


# In[17]:


device_inst_filename = os.path.join(folder_name, "device_instance_dat.dat")


# In[18]:


with open(device_inst_filename, 'w') as f:
    f.write("*\n")
    f.write("\t53\tDEVICE_INSTANCE\t0\n")
    f.write("*\tIndex\tName\n")

    for index, row in df_device_instance.iterrows():
        f.write("\t{}\t{}\n".format(row['Number'], row['Name  ']))
    
    f.write("0")


# In[19]:


df_analog_instance = pd.read_csv('Analog.csv')

df_analog_instance = df_analog_instance[['Name  ']]
df_analog_instance['Name  '] = df_analog_instance['Name  '].apply(lambda x: x.split(',')[1].strip())

#df_device_instance['Name  '] = df_device_instance['Name  '].str.split(',', expand=True)[1].str.strip()

#df_analog_instance['Name  '] = df_analog_instance['Name  '].strsplit(',', expand=True)[1].str.strip()
df_analog_instance = df_analog_instance.drop_duplicates()


# In[20]:


df_analog_instance


# In[21]:


# Concatenar los DataFrames df_device_instance y df_analog_instance
result_df = pd.concat([df_device_instance, df_analog_instance], ignore_index=True)
result_df.drop_duplicates(subset='Name  ', inplace=True, keep='first')

# Mostrar el DataFrame resultante
print(result_df)


# In[22]:


result_df


# In[23]:


df_device_instance = result_df


# In[24]:


df_device_instance['Number'] = range(1,len(df_device_instance)+1)


# In[25]:


df_device_instance


# In[26]:


device_inst_filename = os.path.join(folder_name, "device_instance_dat.dat")


# In[27]:


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
# 
# ----------
#  15.1 Updates for TYPE: (
#        
#        "RG 1/15:
#         If (PreSuffix == 7) then (T_R&L) Type=6 
#         If (PreSuffix ==20 and (Desc contains 'LTC' or Desc contains 'REG')) then (T_CTL) Type=3 
# Telem_A=any number then (T_IND) Type =1
# Open_B=12 then (T_I&C) Type =2
# Telem_A=<blank>  then (C_IND) Type =5
# "
# 
#  )
# 
# --------
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
#   **update 01/22 : ICAddress . double quotations "" 
# 
# * ***UPDATE : 
# (107) pDeviceInstance : Column "Name" in Status.csv . Get the string after the comma, then search for the matching record of the objet DEVICE_INSTANCE. 
# 

# TYPE update
# RG 1/18: If (Open_A is.notEmpty && Close_A is.NotEmpty) then (T_I&C) Type =2

# UPDATE : 3/26/24
# (44) pCtrlState : If point type is 6 (T_R/L) then set to 238 , else leave blank "".
# (74) pScale :  If point type is 6 (T_R/L) then set to 25, else leave blank "".

# (38) FeedbackKey :  RG 4/3: For status points that are set to type 6 (T_R/L) add the SCADA key of the homologous analog key, if point type != 6, then only add "™. If there is no match, also only add " The homologous analog key is found by adding a letter L after the comma in the Name column
# Example RG 4/3: for status point name AC, TC1 the homologous analog will be AC, LTC1
# For status point name DB,TC3 the analog point will be DB, LTC3

# In[28]:


InputStatusFile = "Status.csv"


# In[29]:


status_df = pd.read_csv(InputStatusFile)
status_df.dropna(how='all', inplace=True)
df_status = pd.DataFrame()


# In[30]:


status_df['PreSuffx  ']


# In[31]:


df_status['record'] = range(1, len(status_df)+1) 
df_status['OrderNo'] = range(1, len(status_df)+1) 
##### TYPE ######
status_df['PreSuffx  '] = status_df['PreSuffx  '].astype(str).str.strip()

#### conditions ###
cond1 = status_df['PreSuffx  '].str.contains('20') & status_df['Desc  '].str.contains('LTC|REG')
cond2 = status_df['PreSuffx  '].isin(['7.0', '7'])
cond3 = (status_df['Open_A  '] != '  ') & (status_df['Close_A  '] != '  ')
cond4 = (status_df['Open_B  '] == '12  ')
cond5 = (status_df['Telem_A  '].replace('  ', np.nan).notna())
cond6 = np.bitwise_not(status_df['Telem_A  '].replace('  ', np.nan).notna()) 


## values 
conditions = [cond1, cond2, cond3, cond4, cond5, cond6]
values = [3, 6, 2, 2, 1, 5]


df_status['Type'] = np.select(conditions, values, default=5)

#### agregar aqui el FeedbackKey ####
df_status['FeedbackKey'] = '""'


#####################################
df_status['Name'] = status_df['Desc  ']
df_status['AOR'] = status_df['Zones  '].str.rstrip()
df_status['AOR'] = df_status['AOR'].str.replace(r'\s+', '', regex=True)
df_status['pState'] = status_df['PreSuffx  ']
df_status['Norm'] = status_df['Normal_State  ']
df_status['AlarmGroup'] = 1
df_status['ICAddress'] = '""'


# In[32]:


df_status['Type'].value_counts()


# _______

# In[33]:


status_df['PreSuffx  '].unique()


# ________

# In[34]:


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


# In[35]:


df_status


# In[36]:


status_df


# In[ ]:





# In[37]:


df_status['TempName'] = status_df['Name  '].str.split(',', expand=True)[1].str.strip()
df_status['pDeviceInstance'] = df_status['TempName'].map(df_device_instance.set_index('Name  ')['Number'])
df_status.drop(columns=['TempName'], inplace=True)


# # Stn :

# This code strips the Name column in status and search the matching row Key in Station Dataframe
# then, it reads the Order column value and assign this to the Stn column

# In[38]:


status_df['Key'] = status_df['Name  '].str.split(',').str[0].str.strip()  
df_station['Key'] = df_station['Key'].str.replace('"', '')
stn_values = [] 


# In[39]:


status_df['Key'] = status_df['Name  '].str.split(',').str[0].str.strip()


stn_values = []

for i in range(len(status_df)):
    key_value = status_df.loc[i, 'Key']
    
    if key_value == 'PS':
        first_two_chars_after_comma = status_df.loc[i, 'Name  '].split(',')[1][:2].strip()


        if first_two_chars_after_comma in df_station['Key'].values:
            key_value = first_two_chars_after_comma
        elif first_two_chars_after_comma == 'FP':  
            #print(f"FP encontrado, cambiando a FSP en fila {i}")
            key_value = 'FSP'
        elif first_two_chars_after_comma == 'UC': 
            #print(f"UC encontrado, cambiando a UCI en fila {i}")
            key_value = 'UCI'
        else:
            key_value = 'PS'
    
    matching_row = df_station[df_station['Key'] == key_value]
    if not matching_row.empty:
        stn_values.append(f"{matching_row['Order'].values[0]:03}")
    else:
        stn_values.append(np.nan)

df_status['Stn'] = stn_values


# In[40]:


count_054 = df_status['Stn'].value_counts().get('055', 0)
print(f"El conteo de '055' (PS) en la columna 'Stn' es: {count_054}")


# In[41]:


df_status['Stn'].value_counts()


# Replacement case: Pseudo Points.
# IF stn = 054 (PS. Pseudo points.) Set type to 8 .   And then set XX Value to 12

# In[42]:


df_status.loc[df_status['Name'].str.startswith("PS"), 'Type'] = 8

for i in range(len(df_status)):
    if df_status.loc[i, 'Stn'] == '054':
        key_to_search = df_status.loc[i, 'Name'][3:5]


        matching_row = df_station[df_station['Key'] == key_to_search]

      
        if not matching_row.empty:
            df_status.loc[i, 'Stn'] = f"{matching_row['Order'].values[0]:03}"


# # KEY

# In[43]:


key_values = []
xx_yyy_counters = {}  


# In[44]:


df_status['Type'].value_counts()


# In[45]:


for i in range(len(df_status)):
    
    if df_status.loc[i, 'Type'] == 2:
        xx = '01'
    elif df_status.loc[i, 'Type'] == 3:
        xx = '41'
    elif df_status.loc[i, 'Type'] == 6:
        xx = '41'
    elif df_status.loc[i, 'Type'] == 1:
        xx = '01'
    elif df_status.loc[i, 'Type'] == 5:
        xx = '02'
    elif df_status.loc[i, 'Type'] == 8:
        xx = '12'
    else:
        xx = '99'  # ERROR CASE . In case of being unable to find a coincidence.

    yyy = df_status.loc[i, 'Stn']

    #print(f'xx= {xx}  yyy= {yyy}  ')
    # combination
    key = xx + yyy

    if key in xx_yyy_counters:
        xx_yyy_counters[key] += 1
    else:
        xx_yyy_counters[key] = 1


    zz = f"{xx_yyy_counters[key]:03}"  

    key_values.append(xx + yyy + zz)


# In[46]:


df_status['Key'] = key_values


# In[47]:


type_counts = df_status['Type'].value_counts()
print(type_counts)


# In[48]:


new_order = ['record', 'OrderNo','Type','Key','Name','Stn','AOR','pState','Norm','AlarmGroup','ICAddress','pDeviceInstance']
df_status = df_status[new_order]


# In[49]:


df_status


# In[50]:


df_status['Key'] = '"'+ df_status['Key'].str.rstrip() + '"'


# In[51]:


df_status['Name'] = '"'+ df_status['Name'].str.rstrip() + '"'


# In[52]:


df_status


# In[53]:


df_status['pState'] = pd.to_numeric(df_status['pState'], errors='coerce').astype(int)
df_status['pState'] = df_status['pState'] + 201


# In[54]:


def set_pctrlstate(row):
    if row['Type'] == 6:
        return 238
    else:
        return '""'

df_status['pCtrlState'] = df_status.apply(set_pctrlstate, axis=1)


# In[55]:


def set_pscale(row):
    if row['Type'] == 6:
        return 25
    else:
        return '""'
        
df_status['pScale'] = df_status.apply(set_pscale, axis=1)


# In[ ]:





# In[56]:


df_status


# # DATASET Status ready.

# The program will create a csv version of the Status Dataframe edited and builded here . Intended to be mixed with the original datasource "Status.csv". The name for this csv is gonna be "Status_xref.csv"

# Columnas utilizadas de Status.csv(Datasource):
# 'Telem_A  ','Open_B  ','Stn  ', 'PreSuffx  ', 'Name  ','Desc  ', 'Zones  ', 'Presuffx  ', 'Normal_State  ', 'Open_A  ', 'Close_A  ', 
# Columnas del objeto construido como dataframe 'Status':
# TODAS las columnas generadas 
# 
# Crear status_xref.csv 

# In[57]:


columnas_seleccionadas = [
    'Telem_A  ','Open_B  ','PreSuffx  ', 'Name  ','Desc  ', 'Zones  ', 'Normal_State  ', 'Open_A  ', 'Close_A  '  
]


source_status_df = pd.read_csv('Status.csv', usecols=columnas_seleccionadas)


# In[58]:


source_status_df


# # OUTPUT TO DAT FILE :

# In[59]:


folder_name = "SCADA_DAT_FILES"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)


# In[60]:


output_status_name = 'status_dat.dat'


# In[61]:


statusfilename = os.path.join(folder_name, output_status_name)


# In[62]:


with open(statusfilename, 'w') as f:
    f.write('*\n')
    f.write('\t4\tSTATUS\t0\t1\t3\t4\t5\t10\t19\t49\t29\t41\t44\t74\t107\n')
    f.write('*\trecord\tOrderNo\tType\tKey\tName\tStn\tAOR\tpState\tNorm\tAlarmGroup\tICAddress\tpCtrlState\tpScale\tpDeviceInstance\n')

    for index, row in df_status.iterrows():
        f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format
                (row['record'], row['OrderNo'], row['Type'], row['Key'], row['Name'], row['Stn'], row['AOR'], row['pState'], row['Norm'], row['AlarmGroup'], row['ICAddress'],row['pCtrlState'], row['pScale'] ,row['pDeviceInstance']))
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
# New item:
# 
# RawCountFormat (54) : Assign "3"
# 
#     
#    

# In[63]:


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

# In[64]:


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



df_new['Name'] = df_analog['Desc  ']
df_new['Name_match'] = df_analog['Name  ']
df_new['AOR'] = df_analog['Zones  ']
df_new['AlarmGrp'] = 1
df_new['ICAddress'] = ''

print(f"'Type' = 3: {count_type_3}")


# HI LOW LIMITS

# In[65]:


for col in ['77,0', '77,1', '77,2', '77,3', '77,4', '78,0', '78,1', '78,2', '78,3', '78,4']:
    df_new[col] = 0  

for col in ['91,1', '91,2', '91,3', '91,4', '91,5']:
    df_new[col] = np.nan


    
column_mapping = {
    'Alm_emgHi  ': '77,1',
    'Alm_preHi  ': '77,0',
    'Alm_unrHi  ': '77,4',
    'Alm_preLo  ': '78,0',
    'Alm_emgLo  ': '78,1',
    'Alm_unrLo  ': '78,4',
}


for analog_col, new_col in column_mapping.items():

    mask = (df_analog[analog_col] != "0  ") & (df_analog[analog_col].notna())
  
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


# In[66]:


df_new


# In[67]:


df_new['pScale EU_Hi'] = df_analog['EU_Hi  ']


# In[68]:


df_new


# # STN 

# In[69]:


df_analog['Key'] = df_analog['Name  '].str.split(',').str[0].str.strip()

stn_values = []

for i in range(len(df_analog)):
    
    matching_row = df_station[df_station['Key'] == df_analog.loc[i, 'Key']]
    
    if not matching_row.empty:
        stn_values.append(f"{matching_row['Order'].values[0]:03}")
    else:
        stn_values.append(np.nan)
df_new['Stn'] = stn_values


# In[70]:


df_new


# # KEY

# In[71]:


cols = ['Alm_unrHi', 'Alm_unrLo', 'Alm_preHi', 'Alm_preLo', '78,1', '78,4', '77,1', '77,4']
for col in cols:
    if col not in df_new.columns:
        df_new[col] = np.nan



# In[72]:


key_values = []
xx_yyy_counters = {}


# In[73]:


for i in range(len(df_new)):
    

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


# In[74]:


df_new


# df_ner['NominalPairInactive'] 

# In[75]:


new_column_order = ['record', 'OrderNo', 'Type','Name_match', 'Key', 'Name', 'Stn', 'AOR',
                    '77,0', '77,1', '77,2', '77,3', '77,4',
                    '78,0', '78,1', '78,2', '78,3', '78,4',
                    '91,1', '91,2', '91,3', '91,4', '91,5',
                    'pScale EU_Hi', 'AlarmGrp', 'ICAddress']


df_new = df_new[new_column_order]



# In[76]:


df_new['77,1'].head(10)


# In[77]:


df_new['Key'] = '"'+ df_new['Key'].str.rstrip() + '"'
df_new['Name'] = '"'+ df_new['Name'].str.rstrip() + '"'


# In[78]:


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


# In[79]:


df_analog['Alm_preLo  '] = df_analog['Alm_preLo  '].astype(str).str.strip()
df_new['78,0'] = df_new['78,0'].astype(str).str.strip()


mask = (df_analog['Alm_preLo  '] == '0  ') & (df_new['78,0'] == '-999995')


df_new.loc[mask, '78,0'] = df_analog.loc[mask, 'Alm_preLo  ']




# In[80]:


df_new.head(10)


# In[81]:


df_new['AOR'] = df_new['AOR'].str.replace(r'\s+', '', regex=True)


# In[82]:


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


df_new['AOR'] = df_new['AOR'].replace(replacement_dict)


# In[83]:


df_new['78,1'] = df_new['78,1'].replace({'0  ': -999996})
df_new['78,4'] = df_new['78,4'].replace({'0  ': -999999})


# In[84]:


def modificar_type(fila):
    if fila['Name'].startswith('"PS'):
        return 3
    else:
        return fila['Type']
df_new['Type'] = df_new.apply(modificar_type, axis=1)


# In[85]:


filas_con_ps = df_new[df_new['Name'].str.startswith('"PS')]

numero_de_filas = len(filas_con_ps)

#print("Número de filas que comienzan con 'PS':", numero_de_filas)


# df_new [punit]

# In[86]:


analog_file = "Analog.csv"
df_analog = pd.read_csv(analog_file)


df_unit = pd.DataFrame()
df_unit['name'] = df_analog['EuText  '].drop_duplicates(keep='first').reset_index(drop=True)
df_unit = df_unit[df_unit['name'].notna() & (df_unit['name'].str.strip() != '')]


df_unit['record'] = range(1, len(df_unit['name']) + 1)


unit_mapping = df_unit.set_index('name')['record'].to_dict()
df_new['pUNIT'] = df_analog['EuText  '].map(unit_mapping)
df_new['pUNIT'] = df_new['pUNIT'].apply(lambda x: '""' if pd.isna(x) else str(int(x)))


# In[87]:


df_new['pUNIT'].isna().sum()


# In[88]:


empty_vals = df_new['pUNIT'].isna() | (df_new['pUNIT'] == '""')
num_empty = empty_vals.sum()
print(f'Number of empty values: {num_empty}')


# In[89]:


df_new['pUNIT'].head(6)


# In[90]:


df_new.loc[:, 'RawCountFormat'] = 1


# In[91]:


df_new


# Output Filename:

# In[92]:


df_new.to_csv('SOURCE_analog.csv', index=False)


# In[93]:


folder_name = "SCADA_DAT_FILES"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)


# In[94]:


output_analog_name = 'analog_dat.dat'


# In[95]:


analog_filename = os.path.join(folder_name, output_analog_name)


# In[96]:


with open(analog_filename, 'w') as f:
    f.write('* \n')
    f.write('\t5\tANALOG\t0\t1\t3\t4\t5\t10\t23\t24\t42\t54\t77,4\t77,1\t77,0\t78,0\t78,1\t78,4\t91,1\t91,2\t91,3\t91,4\t91,5\t66\n')
    f.write('*\trecord\tOrderNo\tType\tKey\tName\tStn\tAOR\tpUNIT\tpScale EU_Hi\tAlarmGrp\tRawCountFormat\t77,4\t77,1\t77,0\t78,0\t78,1\t78,4\tNomPairInactive91,1\t91,2\t91,3\t91,4\t91,5\tICAddress\n')

    for index, row in df_new.iterrows():
        f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format
                ("", row['record'], row['OrderNo'], row['Type'], row['Key'], row['Name'], row['Stn'], row['AOR'],row['pUNIT'],row['pScale EU_Hi'], row['AlarmGrp'],row['RawCountFormat'], row['77,4'], row['77,1'], row['77,0'], row['78,0'], row['78,1'], row['78,4'], row['91,1'], row['91,2'], row['91,3'], row['91,4'], row['91,5'], row['ICAddress']))
    f.write("0")  


# ________

# ### ANALOG XREF

# Crear otro archivo csv. Este archivo CSV se va a crear cuando se esta creando el objeto SCADA/Analog. Y va a tener informacion del Analog.csv y del objeto Analog de SCADA.dat .
# Llamemosle analog_xref.csv y va a tener las columnas de Analog.csv que se utilizan en la conversion (de entrada), y tambien tener las columnas que se escriben al SCADA.dat objeto Analog (de salida).
# Importante agregar la columna Name_Analog_Source que va a venir de la columna Analog.csv/Name .

# Analog.csv['Name'] rename to Analog.csv['Name_Analog_Source']

# Columnas que utiliza el df Analog desde Analog.csv:
# 
# 'Desc  '
# 'Name  '   - - - - - > convertir a Name_Analog_Source
# 'Zones  '
# 'Alm_preHi  '
# 'Alm_emgHi  '
# 'Alm_unrHi  '
# 'Alm_preLo  '
# 'Alm_emgLo  '
# 'Alm_unrLo  '
# 'EU_Hi  '
# 'Key'
# 'EuText  '
# 
# y utilizar df_new, con estas columnas
# ['record'], ['OrderNo'], ['Type'], ['Key'], ['Name'], ['Stn'], ['AOR'],['pUNIT'],['pScale EU_Hi'], ['AlarmGrp'],['RawCountFormat'], ['77,4'], ['77,1'], ['77,0'], ['78,0'], ['78,1'], ['78,4'], ['91,1'], ['91,2'], ['91,3'], ['91,4'], ['91,5'], ['ICAddress']
# 

# In[97]:


xranalog_df = pd.read_csv('Analog.csv')

analog_xref = xranalog_df[['Desc  ', 'Name  ', 'Zones  ', 'Alm_preHi  ', 'Alm_emgHi  ', 'Alm_unrHi  ', 'Alm_preLo  ', 'Alm_emgLo  ', 'Alm_unrLo  ', 'EU_Hi  ', 'EuText  ']]
analog_xref = analog_xref.rename(columns={'Name  ': 'Name_Analog_Source'})


df_new_columns = ['record', 'OrderNo', 'Type', 'Key', 'Name', 'Stn', 'AOR', 'pUNIT', 'pScale EU_Hi', 'AlarmGrp', 'RawCountFormat', '77,4', '77,1', '77,0', '78,0', '78,1', '78,4', '91,1', '91,2', '91,3', '91,4', '91,5', 'ICAddress']
df_new_selected = df_new[df_new_columns]

analog_xref = pd.concat([analog_xref, df_new_selected], axis=1)

analog_xref.to_csv('analog_xref.csv', index=False)


# In[98]:


xranalog_df


# ## Analog_xref.csv debe ser colocado en la carpeta FEP

# __________ 

# # AGREGAR AQUI CODIGO PARA STATUS / FeedbackKey

# In[99]:


InputStatusFile = "Status.csv"
status_df = pd.read_csv(InputStatusFile)
status_df.dropna(how='all', inplace=True)
df_status = pd.DataFrame()
df_status['record'] = range(1, len(status_df)+1) 
df_status['OrderNo'] = range(1, len(status_df)+1) 
##### TYPE ######
status_df['PreSuffx  '] = status_df['PreSuffx  '].astype(str).str.strip()

#### conditions ###
cond1 = status_df['PreSuffx  '].str.contains('20') & status_df['Desc  '].str.contains('LTC|REG')
cond2 = status_df['PreSuffx  '].isin(['7.0', '7'])
cond3 = (status_df['Open_A  '] != '  ') & (status_df['Close_A  '] != '  ')
cond4 = (status_df['Open_B  '] == '12  ')
cond5 = (status_df['Telem_A  '].replace('  ', np.nan).notna())
cond6 = np.bitwise_not(status_df['Telem_A  '].replace('  ', np.nan).notna()) 


## values 
conditions = [cond1, cond2, cond3, cond4, cond5, cond6]
values = [3, 6, 2, 2, 1, 5]
#conditions.append(cond5)  
#values.append(2)

df_status['Type'] = np.select(conditions, values, default=5)


# In[100]:


#### agregar aqui el FeedbackKey ####
df_status['FeedbackKey'] = '""'
# df_new es el dataframe de Analog 
#(38) FeedbackKey :  RG 4/3: For status points that are set to type 6 (T_R/L) add the SCADA key of the homologous analog key, if point type != 6, then only add "™. If there is no match, also only add " The homologous analog key is found by adding a letter L after the comma in the Name column
#Example RG 4/3: for status point name AC, TC1 the homologous analog will be AC, LTC1
#For status point name DB,TC3 the analog point will be DB, LTC3
#
#if df_status['type'] == 6 , ]


# In[101]:


df_status


# In[102]:


df_status['Name'] = status_df['Desc  ']
df_status['name_to_match'] = status_df['Name  '].str.rstrip()
df_status['AOR'] = status_df['Zones  '].str.rstrip()
df_status['AOR'] = df_status['AOR'].str.replace(r'\s+', '', regex=True)
df_status['pState'] = status_df['PreSuffx  ']
df_status['Norm'] = status_df['Normal_State  ']
df_status['AlarmGroup'] = 1
df_status['ICAddress'] = '""'

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
df_status['TempName'] = status_df['Name  '].str.split(',', expand=True)[1].str.strip()


df_status['pDeviceInstance'] = df_status['TempName'].map(df_device_instance.set_index('Name  ')['Number'])


df_status.drop(columns=['TempName'], inplace=True)


status_df['Key'] = status_df['Name  '].str.split(',').str[0].str.strip() 
df_station['Key'] = df_station['Key'].str.replace('"', '')
stn_values = []  
status_df['Key'] = status_df['Name  '].str.split(',').str[0].str.strip()


stn_values = []

for i in range(len(status_df)):
    key_value = status_df.loc[i, 'Key']
    
    if key_value == 'PS':
 
        first_two_chars_after_comma = status_df.loc[i, 'Name  '].split(',')[1][:2].strip()

    
        if first_two_chars_after_comma in df_station['Key'].values:
            key_value = first_two_chars_after_comma
        elif first_two_chars_after_comma == 'FP':  
            print(f"FP encontrado, cambiando a FSP en fila {i}")
            key_value = 'FSP'
        elif first_two_chars_after_comma == 'UC': 
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
count_054 = df_status['Stn'].value_counts().get('055', 0)

df_status.loc[df_status['Name'].str.startswith("PS"), 'Type'] = 8

for i in range(len(df_status)):
    if df_status.loc[i, 'Stn'] == '054':
        key_to_search = df_status.loc[i, 'Name'][3:5]


        matching_row = df_station[df_station['Key'] == key_to_search]


        if not matching_row.empty:
            df_status.loc[i, 'Stn'] = f"{matching_row['Order'].values[0]:03}"
key_values = []
xx_yyy_counters = {}  
for i in range(len(df_status)):
    
    if df_status.loc[i, 'Type'] == 2:
        xx = '01'
    elif df_status.loc[i, 'Type'] == 3:
        xx = '41'
    elif df_status.loc[i, 'Type'] == 6:
        xx = '41'
    elif df_status.loc[i, 'Type'] == 1:
        xx = '01'
    elif df_status.loc[i, 'Type'] == 5:
        xx = '02'
    elif df_status.loc[i, 'Type'] == 8:
        xx = '12'
    else:
        xx = '99' 

    yyy = df_status.loc[i, 'Stn']

  
    key = xx + yyy


    if key in xx_yyy_counters:
        xx_yyy_counters[key] += 1
    else:
        xx_yyy_counters[key] = 1

 
    zz = f"{xx_yyy_counters[key]:03}" 

    key_values.append(xx + yyy + zz)

df_status['Key'] = key_values







new_order = ['record', 'name_to_match','OrderNo','Type','Key','Name','Stn','AOR','pState','Norm','AlarmGroup','ICAddress','FeedbackKey','pDeviceInstance']
df_status = df_status[new_order]

df_status['Key'] = '"'+ df_status['Key'].str.rstrip() + '"'
df_status['Name'] = '"'+ df_status['Name'].str.rstrip() + '"'


df_status['pState'] = pd.to_numeric(df_status['pState'], errors='coerce').astype(int)
df_status['pState'] = df_status['pState'] + 201
def set_pctrlstate(row):
    if row['Type'] == 6:
        return 238
    else:
        return '""'

df_status['pCtrlState'] = df_status.apply(set_pctrlstate, axis=1)
def set_pscale(row):
    if row['Type'] == 6:
        return 25
    else:
        return '""'
        
df_status['pScale'] = df_status.apply(set_pscale, axis=1)







# In[103]:


def set_feedbackkey(row):
    if row['Type'] == 6:
        name_to_match_with_L = row['name_to_match'].split(',')[0] + ',L' + row['name_to_match'].split(',')[1]
        print(name_to_match_with_L)
        if df_new['Name_match'].str.contains(name_to_match_with_L).any():
            return df_new.loc[df_new['Name_match'].str.contains(name_to_match_with_L), 'Key'].values[0]
    return '""'


df_status['FeedbackKey'] = df_status.apply(set_feedbackkey, axis=1)


coincidencias = (df_status['FeedbackKey'] != '""').sum()


print(f"Se encontraron {coincidencias} coincidencias.")


# In[104]:


df_status['Type']


# SCADA/STATUS 51 HiControlLimit : RG 4/24: For status points that are set to type 6 (T_R/L) set to 16
# 
# 
# SCADA/STATUS 52 LoControlLimit : RG 4/24: For status points that are set to type 6 (T_R/L) set to -16
# 
# 
# SCADA/STATUS 73:3 Setpoint Emulation : RG 4/24: For status points that are set to type 6 (T_R/L) set to 1
# 
# 

# In[105]:


def set_control_limits(row):
    if row['Type'] == 6:
        return 16
    else:
        return '""'

def set_setpoint_emulation(row):
    if row['Type'] == 6:
        return 1
    else:
        return '""'

df_status['HiControlLimit'] = df_status.apply(set_control_limits, axis=1)
df_status['LoControlLimit'] = df_status.apply(lambda row: -16 if row['Type'] == 6 else '""', axis=1)
df_status['Setpoint_emulation'] = df_status.apply(set_setpoint_emulation, axis=1)


# In[106]:


df_status


# # Output dat file for status

# In[107]:


folder_name = "SCADA_DAT_FILES"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

output_status_name = 'status_dat.dat'

statusfilename = os.path.join(folder_name, output_status_name)




# In[108]:


with open(statusfilename, 'w') as f:
    f.write('*\n')
    f.write('\t4\tSTATUS\t0\t1\t3\t4\t5\t10\t19\t49\t29\t38\t41\t44\t51\t52\t73,4\t74\t107\n')
    f.write('*\trecord\tOrderNo\tType\tKey\tName\tStn\tAOR\tpState\tNorm\tAlarmGroup\tFeedbackKey\tICAddress\tpCtrlState\tHiControlLimit\tLoControlLimit\tSetpoint_emulation\tpScale\tpDeviceInstance\n')

    for index, row in df_status.iterrows():
        f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format
                (row['record'], row['OrderNo'], row['Type'], row['Key'], row['Name'], row['Stn'], row['AOR'], row['pState'], row['Norm'], row['AlarmGroup'],row['FeedbackKey'], row['ICAddress'],row['pCtrlState'],row['HiControlLimit'],row['LoControlLimit'],row['Setpoint_emulation'], row['pScale'] ,row['pDeviceInstance']))
    f.write("0")  


# Status XREF

# In[109]:


columnas_seleccionadas = [
    'Telem_A  ','Open_B  ','PreSuffx  ', 'Name  ','Desc  ', 'Zones  ', 'Normal_State  ', 'Open_A  ', 'Close_A  '  
]


source_status_df = pd.read_csv('Status.csv', usecols=columnas_seleccionadas)
source_status_df = source_status_df.rename(columns={'Name  ': 'Name_Status_Source  '})
source_status_df.reset_index(drop=True, inplace=True)
df_status.reset_index(drop=True, inplace=True)
combined_df = pd.concat([df_status, source_status_df], axis=1)
combined_df.to_csv('status_xref.csv', index=False)



# ________

# __________

# # ANALOG_CONFIG

# vamos a crear un dataframe llamado Analog_config , el cual tendrá solo dos columnas, una columna se llamara Key , cuyo contenido será exactamente el contenido de Key del df  llamado df_new . y una columna se llamara name , que vendra de df_analog['Name  '] 

# In[110]:


Analog_config = pd.DataFrame({
    'Key': df_new['Key'],
    'name': df_analog['Name  '].str.split(',', expand=True)[1].str.strip()
    
})

def find_number(name):
    match = df_device_instance[df_device_instance['Name  '] == name]
    if not match.empty:
        return match.iloc[0]['Number']
    else:
        return None


Analog_config['pDeviceInstance'] = Analog_config['name'].apply(find_number)




# In[111]:


Analog_config


# In[112]:


df_device_instance


# In[113]:


print(set(Analog_config['name']).intersection(set(df_device_instance['Name  '])))


# In[114]:


print("Unique names in Analog_config:", Analog_config['name'].unique()[:10])  # muestra los primeros 10
print("Unique names in df_device_instance:", df_device_instance['Name  '].unique()[:10])  # muestra los primeros 10


# In[115]:


df_device_instance


# In[116]:


Analog_config


# In[ ]:





# In[117]:


Analog_config['record'] = range(1, len(Analog_config) + 1)


# In[118]:


Analog_config


# In[119]:


Analog_config.to_csv('AnalogConfig.csv', index=False)


# In[120]:


folder_name = "SCADA_DAT_FILES"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)


# In[121]:


analog_config_filename = "analog_config_dat.dat"


# In[122]:


analog_config_path = os.path.join(folder_name, analog_config_filename)


# In[123]:


with open(analog_config_path, 'w') as f:
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

# In[124]:


analog_file = "Analog.csv"
df_analog = pd.read_csv(analog_file)


df_unit = pd.DataFrame()
df_unit['name'] = df_analog['EuText  '].drop_duplicates(keep='first').reset_index(drop=True)
df_unit = df_unit[df_unit['name'].notna() & (df_unit['name'].str.strip() != '')]


df_unit['record'] = range(1, len(df_unit['name']) + 1)

print(df_unit.head())



# In[125]:


folder_name = "SCADA_DAT_FILES"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)


# In[126]:


unit_filename = "unit_dat.dat"


# In[127]:


unit_config_path = os.path.join(folder_name, unit_filename)


# In[128]:


with open(unit_config_path, 'w') as f:
    f.write("*\n")
    f.write("\t10\tUNIT\t0\n")
    f.write("*\t#\tName\n")

    for index, row in df_unit.iterrows():
        f.write("\t{}\t{}\n".format(row['record'],row['name']))
    
    f.write("0")


# __________
# ____________

# # OBJETO ACCUMULATOR : Comentado. No se usará

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

# In[129]:


comment = """ #Data CSV Name entry
analog_file = "Analog.csv"
df_analog = pd.read_csv(analog_file)

df_accumulator = pd.DataFrame()

df_accumulator['Type'] = df_analog['Telem_B  '].apply(lambda x: 1 if x == '21  ' else 3)

df_accumulator['Name'] = df_analog['Desc  ']

df_accumulator['pAORGroup'] = 1 
"""


# In[130]:


comment = """
unit_mapping = df_unit.set_index('name')['record'].to_dict()
df_accumulator['pUNIT'] = df_analog['EuText  '].map(unit_mapping)

print(df_accumulator.head())
df_accumulator['pUNIT'] = df_accumulator['pUNIT'].apply(lambda x: '' if pd.isna(x) else str(int(x)))
df_accumulator['pScale'] = df_analog['EU_Hi  ']
df_accumulator['pALARM_GROUP'] = 1
"""


# In[131]:


comment = """
with open('Accumulator.dat', 'w') as f:
    f.write("*\n")
    f.write("\t6\tAccumulator\t1\t4\t10\t19\t38\t42\n")
    f.write("*\tType\tName\tpAORGROUP\tpUNIT\tpScale\tpALARM_GROUP\n")

    for index, row in df_accumulator.iterrows():
        f.write("\t{}\t{}\t{}\t{}\t{}\t{}\n".format(row['Type'],row['Name'],row['pAORGroup'],row['pUNIT'],row['pScale'],row['pALARM_GROUP']))
    
    f.write("0")
    """


# # RG 11/3 Object: Scale(9)

# # Debe existir un archivo all_stations_equivalency.csv para operar

# source: all_station_equivalency.csv
# 
# Scale(0) : Column 'Scale Factor' : RG 3/11: Delete repetitions and shift records up to avoid having empty spaces. If not defined will be set to 1
# 
# Offset(1) : If not defined will be set to 0
# 
# Name(12) : Column 'Scale Factor' : RG 3/11: Delete repetitions and shift records up to avoid having empty spaces. If not defined will be set to "<Scale #>, <Offset #>
# 
# 

# ADVERTENCIA. LOS ARCHIVOS XLSX TIENEN UN HEADER COMPUESTO POR DOS FILAS DISTINTAS. ES RECOMENDABLE GENERAR MANUALMENTE LOS COLUMN NAMES

# Point ID,Station,Pnuemonic,Description,COM,RTU,Pg,Status P,Analog P,Relay P,Value,Scale,Type,Helper Column,IP Address,DNPAddress,DNP Point,,

# In[132]:


import pandas as pd
df = pd.read_csv('all_stations_equivalency.csv')

df.dropna(subset=['Scale'], inplace=True)



# In[133]:


df


# In[134]:


df.drop_duplicates(subset=['Scale'], keep='first', inplace=True)


# In[135]:


def prepend_if_needed(x):
    if x.startswith('.'):
        return '0' + x
    else:
        return x


# In[136]:


df['Scale'] = df['Scale'].apply(prepend_if_needed)


# In[137]:


df = df[~df['Scale'].str.startswith('REV')] 


# 

# In[138]:


df


# salvar el objeto Scale en formato dat

# In[139]:


folder_name = "SCADA_DAT_FILES"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)


# In[140]:


scale_filename = "scale_dat.dat"


# In[141]:


scale_path = os.path.join(folder_name, scale_filename)


# In[142]:


n = 1
with open(scale_path, 'w') as f:
    f.write("*\n")
    f.write("\t9\tScale\t0\t12\n")
    f.write("*\tScale\tName\n")

    for index, row in df.iterrows():
        f.write("\t{}\t{}\t{}\n".format(n,row['Scale'],row['Scale']))

        n = n + 1
    f.write(f"\t{len(df) + 1}\t1.0\tOne_Unit\n")
    f.write(f"\t{len(df) + 2}\t2.0\tTwo_Units\n")
    f.write(f"\t{len(df) + 3}\t1.0\tRaiseLower_Scale\n")
    f.write("0")


# In[ ]:




