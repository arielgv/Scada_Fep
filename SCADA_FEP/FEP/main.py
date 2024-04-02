#!/usr/bin/env python
# coding: utf-8

# FEP , CHANNEL , and RTU_DATA
# ---------------

# ------------

# # FEP

# FEP dependencies: 
# 
# Indic 0             mapping:  1               (create only one record)
# 
# Mode   2            mapping:  1               (create only one record)
# 
# Hostname  4         mapping:  fepts01         (create only one record)
# 
# Name   5            mapping:  Comm_Server_1   (create only one record)
# 
# NumPorts 11         mapping:  16              (create only one record)
#  
# ipdaddress  17      mapping:  192.168.32.16   (create only one record)

# In[65]:


import pandas as pd
from datetime import datetime
#libraries


# In[66]:


data = {
    'Indic': [1],
    'Mode': [1],
    'Hostname': ['fepts01'],
    'Name': ['Comm_Server_1'],
    'NumPorts': [11],
    'ipdaddress': ['192.168.32.16']
}

FEP = pd.DataFrame(data)

print('Preview \n',FEP)


# In[67]:


with open('FEP.DAT', 'w') as file:
    file.write('*\n')
    file.write('\t4\tFEP\t0\t2\t4\t5\t11\t17\n')
    file.write('*\tIndic\tMode\tHostname\tName\tNumPorts\tipaddress\n')

    for index, row in FEP.iterrows():
        file.write(f'\t{row["Indic"]}\t{row["Indic"]}\t{row["Mode"]}\t{row["Hostname"]}\t{row["Name"]}\t{row["NumPorts"]}\t{row["ipdaddress"]}\n')

    file.write("0")


# # CHANNEL

# dependencies: 
# RTAC SCADA DNP IPs Reordered (1).csv   (DF)
# 
# RG 12/6 Indic 0          : one to one (DF [ RTAC Number ])
# 
# pFEP 1          mapping: Set all to 0   [Build: If not mapped will be manually configured by PE]
# 
# Character 13    mapping: Set all to 8
# 
# Stop_Bits 14    mapping: Set all to 1
# 
# RG 12/6  NoReplyLimit  18 :  Set all to 5
# 
# Name  19       [RTAC SCADA DNP IPs Reordered (1).csv] 
# RG 12/6 Name 19    : RG 12/6: String of Abreviation + "_" + Panel + "_Channel"
# 
# 
# baudrate 23    [COMM.csv] mapping: Comm_Line   . Detailed mapping : 9600
# 
# ChannelRespTimeoutMsec 24  [COMM.csv] mapping: Pri_Resp_TO
# RG 25/6 ChannelRespTimeoutMsec 24  :  Set All to 5000
# 
# 
# PhysicalPort 25    [COMM.csv]  mapping: Comm_Line
# RG 25/6 PhysicalPort 25    :  Set All to 20000
# 
# RG 25/6 ChannelReqDelay 27 :  Set all to 0
# 
# 
# Hostname  30    mapping: 
# RG 25/6  Hostname 30  :   one by one according to RTAC SCADA DNP IPs Reordered
# 
# RG 25/6  pCHANNEL_GROUP 40 :   one to one (DF [ RTAC Number ])
# 
# 
# ChannelConnTimeout 41   [COMM.csv]  mapping:  Pri_Resp_TO
# RG 25/6 ChannelConnTimeout 41   :  Set all to 5 
# 

# _Comm.csv_ Should be in the same folder

# In[68]:


rtac_data = pd.read_csv('RTAC SCADA DNP IPs Reordered (1).csv')
rtac_data['Panel'] = rtac_data['Panel'].str.replace('Panel ', '', regex=False)
channel = pd.DataFrame()

#COLUMNS OF CHANNEL 
#channel['Indic'] = range(1, len(comm_data) + 1)
channel['Indic'] = rtac_data['RTAC Number']
channel['pFEP'] = [0] * len(rtac_data)
channel['Character'] = [8] * len(rtac_data)
channel['Stop_Bits'] = [1] * len(rtac_data)
channel['NoReplyLimit'] = [5] * len(rtac_data)

#NAME
channel['Name'] = rtac_data['Abreviation'] + '_' + rtac_data['Panel'] + '_Ch'
#channel['baudrate'] = [9600] * len(comm_data)
#channel['ChannelResTimeoutMsec'] = comm_data['Pri_Resp_TO  ']
channel['ChannelResTimeoutMsec'] = [5000] * len(rtac_data)
#channel['PhysicalPort'] = comm_data['Comm_Line  ']
channel['PhysicalPort'] = [20000] * len(rtac_data)
channel['ChannelReqDelay'] = [0] * len(rtac_data)
channel['Hostname'] = rtac_data['RTAC SCADA IP']
#MODIFICAR HOSTNAME PARA QUE SEA IGUAL QUE INDIC, o un simple incremental de uno a uno
channel['pCHANNEL_GROUP'] = rtac_data['RTAC Number']
#channel['ChannelConnTimeout'] = comm_data['Pri_Resp_TO  ']
channel['ChannelConnTimeout'] = [5] * len(rtac_data)




# In[69]:


channel


# # Output : CHANNEL.DAT

# SE LE INCORPORA UNA COLUMNA CON VALORES '1' A CONTINUACION DE LA COLUMNA INDICE

# In[70]:


#line_number = 1
with open("CHANNEL.dat", 'w') as f:
    f.write('* \n')
    f.write('\t5\tCHANNEL\t0\t1\t13\t14\t18\t19\t24\t25\t27\t30\t40\t41\n')
    f.write('*\tIndic\t1s\tpFEP\tCharacter\tStop_Bits\tNoReplyLimit\tName\tChannelResTimeoutMsec\tPhysicalPort\tChannelReqDelay\tHostname\tpChannel_GROUP\tChannelConnTimeout\n')

    for index, row in channel.iterrows():
        f.write("\t{}\t{}\t{}\t{}\t{}\t{}\t\"{}\"\t{}\t{}\t{}\t{}\t{}\n".format(
                row['Indic'],row['Stop_Bits'], row['pFEP'], row['Character'], row['Stop_Bits'], row['NoReplyLimit'],
                row['Name'],  row['ChannelResTimeoutMsec'], 
                row['PhysicalPort'], row['ChannelReqDelay'], row['Hostname'], row['pCHANNEL_GROUP'], row['ChannelConnTimeout']))
        #line_number += 1
    f.write(" 0")  


# In[ ]:





# # RTU_DATA

# dependencies:
# 
# [DF](<RTAC SCADA DNP IPs Reordered (1).csv>)
# 
# Indics           0  [DF]
# RG 12/6 : Indics : RTAC NUMBER
# 
#   
# pCHANNEL_GROUP   2  [DF]
# RG 12/6 : pCHANNEL_GROUP : RTAC NUMBER
# 
# 
# Protocol         3  [DF] 
# RG 12/6 : Protocol : Set to 8
# 
# 
# Name             5  [DF]
# RG 12/6: String of Abreviation + "_" + Panel + "_RTU"
# 
# 
# Address          14 [RTU.csv] column: RTU_Number   Mapping: if == 8, "", else RTU_Number 
# RG 12/6: Set to 1
# 
# SubType          55 = RG 12/6: Set to 2

# RTU.csv should be in the same folder

# In[71]:


rtu_data = pd.read_csv('RTAC SCADA DNP IPs Reordered (1).csv')


# In[72]:


df = pd.DataFrame()
rtu_data['Panel'] = rtac_data['Panel'].str.replace('Panel ', '', regex=False)

#CHECK INDICS ******************
df['Indics'] = rtu_data['RTAC Number']

df['pCHANNEL_GROUP'] = rtu_data['RTAC Number']
df['Protocol'] = [8] * len(rtu_data)

df['Name'] = rtu_data['Abreviation'] + '_' + rtu_data['Panel'] + '_RTU'
df['Address'] = [1] * len(rtu_data)

df['SubType'] = [2] * len(rtu_data)


# In[73]:


df


# # OUTPUT : RTU_DATA.DAT

# Se incorpora una columna de '1s' siguiente al indice . 

# In[74]:


with open("RTU_DATA.dat", 'w') as f:
    f.write('* \n')
    f.write('\t6\tRTU_DATA\t0\t2\t3\t5\t14\t55\n')
    f.write('*\tIndics\t1s\tpCHANNEL_GROUP\tProtocol\tName\tAddress\tSubType\n')

    line_number = 1  # Inicializar la variable del número de línea

    for index, row in df.iterrows():
        f.write("\t{}\t{}\t{}\t{}\t\"{}\"\t{}\t{}\n".format(
                row['Indics'],row['Address'], row['pCHANNEL_GROUP'], row['Protocol'], 
                row['Name'], row['Address'], row['SubType']))
        line_number += 1  # Incrementar el número de línea

    f.write(" 0") 


# __________

# # CHANNEL_GROUP
# 
# dependencies:
# 
# [DF](<RTAC SCADA DNP IPs Reordered (1).csv>)
# 
# Indic           0  [DF]
# RG 12/6 : Indics : RTAC NUMBER 
# 
# 12/29 :
# MaxAPDU ( 3,3 ): : set to 23
# 
# ConnectionType ( 3,8 ) : Set to 1
# 
# APDU : ( 3,9 ) : Set to 2
# 
# 
# Protocol        4  [DF]
# RG 12/6 : Protocol : set to 8
# 
# Name            6  [DF]
# RG 12/6 : Name : RG 12/6: String of Abreviation + "_" + Panel + "_Ch_Group"
# 
# pCHANNEL       8,0  [DF]
# RG 12/6 : pCHANNEL : RTAC NUMBER
# 
# BackupMonDisable  20  [DF]
# RG 12/6 : BackupMonDisable : set to 1
# 
# 
# RG 12/29 :
#  pAORGroup  23  : set to 1
# 
# Type            24   [DF]
# RG 12/6 : Type : set to 5
# 
# 
# 

# In[75]:


rtac_data = pd.read_csv('RTAC SCADA DNP IPs Reordered (1).csv')
rtac_data['Panel'] = rtac_data['Panel'].str.replace('Panel ', '', regex=False)


channel_group = pd.DataFrame()

#COLUMNS OF CHANNEL_GROUP

channel_group['Indic'] = rtac_data['RTAC Number']

channel_group['MaxAPDU'] = [23] * len(rtac_data)
channel_group['ConnectionType'] = [1] * len(rtac_data)
channel_group['APDU'] = [2] * len(rtac_data)


channel_group['Protocol'] = [8] * len(rtac_data)
channel_group['Name'] = rtac_data['Abreviation'] + '_' + rtac_data['Panel'] + '_ChG'
channel_group['pCHANNEL'] = rtac_data['RTAC Number']
channel_group['BackupMonDisable'] = [1] * len(rtac_data)

channel_group['pAORGroup'] = [1] * len(rtac_data)

channel_group['Type'] = [5] * len(rtac_data)


# In[76]:


channel_group


# Columna siguiente a Indice agregada: 1s. Valores unicamente int 1

# In[77]:


with open("CHANNEL_GROUP.dat", 'w') as f:
    f.write('* \n')
    f.write('\t22\tCHANNEL_GROUP\t0\t3,3\t3,8\t3,9\t4\t6\t8,0\t20\t23\t24\n')
    f.write('*\tIndic\t1s\tMaxAPDU\tConnectionType\tAPDU\tProtocol\tName\tpCHANNEL\tBackupMonDisable\tpAORGroup\tType\n')

    #line_number = 1  # Inicializar la variable del número de línea

    for index, row in channel_group.iterrows():
        f.write("\t{}\t{}\t{}\t{}\t{}\t{}\t\"{}\"\t{}\t{}\t{}\t{}\n".format(
                row['Indic'],row['BackupMonDisable'],row['MaxAPDU'],row['ConnectionType'],row['APDU'], row['Protocol'], 
                row['Name'], row['pCHANNEL'], row['BackupMonDisable'],row['pAORGroup'] ,row['Type']))
        #line_number += 1  # Incrementar el número de línea

    f.write(" 0") 


# __________

# # RTU_DEFN

# dependencies:
# 
# RG 12/6
# 
# Indic 0 : one to one
# 
# PointType 1,0 : Set to 1
# 
# Start 3,0 : Set to 1
# 
# Count 4,0 : Set to 5
# 
# PointType 1,1 : Set to 4
# 
# Start 3,1 : Set to 1
# 
# Count 4,1 : Set to 5
# 
# 
# 

# In[78]:


rtu_data = pd.read_csv('RTAC SCADA DNP IPs Reordered (1).csv')
rtu_defn = pd.DataFrame()


# In[79]:


rtu_defn['Indics'] = range(1, len(rtu_data) + 1)
rtu_defn['PointType10'] = [1] * len(rtu_data)
rtu_defn['Start30'] = [1] * len(rtu_data)
rtu_defn['Count40'] = [5] * len(rtu_data)
rtu_defn['PointType11'] = [4] * len(rtu_data)
rtu_defn['Start31'] = [1] * len(rtu_data)
rtu_defn['Count41'] = [5] * len(rtu_data)


# In[80]:


rtu_defn


# In[81]:


with open("RTU_DEFN.dat", 'w') as f:
    f.write('* \n')
    f.write('\t27\tRTU_DEFN\t1,0\t3,0\t4,0\t1,1\t3,1\t4,1\n')
    f.write('*\tIndic\tPointtype(1,0)\tStart(3,0)\tCount(4,0)\tPointType(1,1)\tStart(3,1)\tCount(4,1)\n')

    #line_number = 1  # Inicializar la variable del número de línea

    for index, row in rtu_defn.iterrows():
        f.write("\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                row['Indics'], row['PointType10'], row['Start30'], row['Count40'], row['PointType11'], row['Start31'], row['Count41']))

        #line_number += 1  # Incrementar el número de línea

    f.write(" 0") 


# # CHANNEL_GROUP_DEFN

# dependencies:
# 
# RG 12/6
# Indic  0  : one to one
# 
# ConnectionType 3,8 : Set to 1
# 
# APDU 3,9 : Set to 2
# 
# Max APDU 3,3 : Set to 23
# 
# MasterAddr   12 :  Set to 1024
# 
# 
# 

# In[82]:


rtac_data = pd.read_csv('RTAC SCADA DNP IPs Reordered (1).csv')

channel_group_defn = pd.DataFrame()

#COLUMNS OF CHANNEL_GROUP
channel_group_defn['Indic'] = rtac_data['RTAC Number'] #Este es el indice incremental de a uno
channel_group_defn['ConnectionType'] = [1] * len(rtac_data)
channel_group_defn['APDU'] = [2] * len(rtac_data)

channel_group_defn['MaxApdu'] = [23] * len(rtac_data)
channel_group_defn['MasterAddr'] = [1024] * len(rtac_data)


# In[83]:


with open("CHANNEL_GROUP_DEFN.dat", 'w') as f:
    f.write('* \n')
    f.write('\t36\tCHANNEL_GROUP_DEFN\t0\t12\n')
    f.write('*\tIndic\t1s\tMasterAddr\n')

    for index, row in channel_group_defn.iterrows():
        f.write("\t{}\t{}\t{}\n".format(
                row['Indic'], row['ConnectionType'], row['MasterAddr']))
    

    f.write(" 0") 


# _________________

# # RTU CONTROL

# dependencies : Equivalency_station.csv
# & RTAC SCADA DNP IPs Reordered (1).csv
# 
# 1  =  KeySCADA: 
# 
# RG 2/11: If ( Point Type == RELAY) then merge column Name+ ',' + Description , and then search for it in the output file SCADA.dat object Status. Grab the key of the matching record
# 
# Create for every Status = Types 2,3,6,7 and Setpoint = Type 1
# 
# 2  =  control_type:  Field: "IP
# DNP Point #"
# 
# RG 2/11: If there are two records with same IP and same DNP Point # then create two records both with same KeySCADA, the first one will have control_type equal to 4, and the second equal to 5. 
# If there is only one record with unique IP and unique DNP Point # then create one record and control_type equal 6.
# 
# 
# 
# 
# 4  =  point_address: Field : "DNP Point #"
# 
# "RG 2/11:  If there are two records with same IP and same DNP Point # then use DNP Point # on each of the two records, 
# If there is only one record with unique IP and unique DNP Point # then use  DNP Point # in its own record."
# 
# 
# 
# 6  =  pRTU:   Field:   IP 
# 
# RG 2/11: Search IP column in the IP of RTAC SCADA DNP IPs Reordered.xlsx and point to the record of that RTU. 
# 
# Should be middle three digits of SCADA Key
# 

# In[84]:


import pandas as pd


equivalency_station = pd.read_csv('Equivalency_station.csv')

RtuControl = pd.DataFrame(index=equivalency_station.index)


RtuControl['KeySCADA'] = equivalency_station.apply(lambda row: row['Full Point Name'] + ' ' + row['Description'] if row['Point Type'] == 'RELAY' else '', axis=1)


# In[85]:


RtuControl


# In[86]:


import pandas as pd



source_status = pd.read_csv('status_xref.csv')


RtuControl['Key2'] = pd.NA


buscados = 0
encontrados = 0


for index, row in RtuControl.iterrows():
    if pd.notna(row['KeySCADA']): 
        buscados += 1
        
        match = source_status[source_status['Name'] == row['KeySCADA']]
        if not match.empty: 
            encontrados += 1
            
            RtuControl.at[index, 'Key2'] = match['Key'].values[0]

print(f"Items buscados: {buscados}")
print(f"Items encontrados: {encontrados}")


# In[87]:


import pandas as pd

df1 = pd.read_csv('equivalency_station.csv')
df2 = pd.read_csv('status_xref.csv') 

df1 = df1[['Station', 'Point']]
df1['combined'] = df1['Station'] + ',' + df1['Point'] + '  '

results = []
matches = 0
for val in df1['combined']:
    match = df2['Name_Status_Source  '].str.contains(val)
    if match.any():
        key = df2[match]['Key'].iloc[0]
        results.append({'equivalency_station_point': val, 'Key': key})
        matches += 1

df = pd.DataFrame(results)

print(f"Number of matches: {matches}") 
print(df)


# In[103]:


df1 = pd.read_csv('equivalency_station.csv')
df2 = pd.read_csv('status_xref.csv')

df1 = df1[['Station', 'Point', 'IP', 'DNP Point #']]
df1['combined'] = df1['Station'] + ',' + df1['Point'] + '  '

results = []
matches = 0
for val in df1['combined']:
    match = df2['Name_Status_Source  '].str.contains(val)
    if match.any():
        key = df2[match]['Key'].iloc[0]
        results.append({'equivalency_station_point': val, 'Key': key, 'IP': df1[df1['combined'] == val]['IP'].iloc[0], 'DNP Point #': df1[df1['combined'] == val]['DNP Point #'].iloc[0]})
        matches += 1

df_matches = pd.DataFrame(results)
print(f"Number of matches: {matches}")


rtac_scada_ips = pd.read_csv('RTAC SCADA DNP IPs Reordered (1).csv')

#  control_type
df_matches['control_type'] = 6
df_matches.loc[df_matches.duplicated(subset=['IP', 'DNP Point #'], keep=False), 'control_type'] = df_matches[df_matches.duplicated(subset=['IP', 'DNP Point #'], keep=False)].groupby(['IP', 'DNP Point #']).cumcount() + 4

#  point_address
df_matches['point_address'] = df_matches['DNP Point #']

#  pRTU
df_matches['pRTU'] = df_matches['IP'].apply(lambda x: rtac_scada_ips[rtac_scada_ips['RTAC SCADA IP'] == x]['RTAC Number'].iloc[0] if not rtac_scada_ips[rtac_scada_ips['RTAC SCADA IP'] == x].empty else '')


result_df = df_matches[['Key', 'control_type', 'point_address', 'pRTU']]


result_df = result_df.fillna(777)


result_df['control_type'] = result_df['control_type'].astype(int)
result_df['point_address'] = result_df['point_address'].astype(int)
result_df['pRTU'] = result_df['pRTU'].astype(int)
result_df['control_format'] = 1


result_df = result_df.replace(777, '')

print(result_df)


# In[104]:


import numpy as np
index = np.arange(1,len(result_df)+1)
result_df.insert(0, 'idx', index)


# In[105]:


result_df


# Numero de objeto RTU_CONTROL?

# In[106]:


rtu_object_number = 20


# In[107]:


with open("RTU_CONTROL.dat", 'w') as f:
    f.write('* \n')
    f.write(f'\t{rtu_object_number}\tRTU_CONTROL\t1\t2\t4\t6\t13\n')
    f.write('*\tKeySCADA\tcontrol_type\tpoint_address\tpRTU\tcontrol_format\n')

    for index, row in result_df.iterrows():
        f.write("\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                row['idx'] ,row['Key'], row['control_type'], row['point_address'], row['pRTU'],row['control_format']))
    

    f.write(" 0") 


# In[ ]:




