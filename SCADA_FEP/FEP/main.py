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

# In[46]:


import pandas as pd
from datetime import datetime
#libraries


# In[47]:


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


# In[48]:


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

# In[49]:


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




# In[50]:


channel


# # Output : CHANNEL.DAT

# SE LE INCORPORA UNA COLUMNA CON VALORES '1' A CONTINUACION DE LA COLUMNA INDICE

# In[51]:


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

# In[52]:


rtu_data = pd.read_csv('RTAC SCADA DNP IPs Reordered (1).csv')


# In[53]:


df = pd.DataFrame()
rtu_data['Panel'] = rtac_data['Panel'].str.replace('Panel ', '', regex=False)

#CHECK INDICS ******************
df['Indics'] = rtu_data['RTAC Number']

df['pCHANNEL_GROUP'] = rtu_data['RTAC Number']
df['Protocol'] = [8] * len(rtu_data)

df['Name'] = rtu_data['Abreviation'] + '_' + rtu_data['Panel'] + '_RTU'
df['Address'] = [1] * len(rtu_data)

df['SubType'] = [2] * len(rtu_data)


# In[54]:


df


# # OUTPUT : RTU_DATA.DAT

# Se incorpora una columna de '1s' siguiente al indice . 

# In[55]:


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

# In[56]:


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


# In[57]:


channel_group


# Columna siguiente a Indice agregada: 1s. Valores unicamente int 1

# In[58]:


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
# RG 3/11: For each RTAC (each RTAC has a unique IP address) search for the smallest "DNP Point"(all_stations_equivalency.csv) of the Point Type == Status and use that number.
# If an RTAC has the following DNP Point # (9,10,45,59,70) then set start to 9
#    
# 
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

# In[59]:


import pandas as pd

# Cargar los archivos CSV
rtu_data = pd.read_csv('RTAC SCADA DNP IPs Reordered (1).csv')
all_stations_equivalency = pd.read_csv('all_stations_equivalency.csv')
rtu_defn = pd.DataFrame()
rtu_defn['Indics'] = range(1, len(rtu_data) + 1)
rtu_defn['PointType10'] = [1] * len(rtu_data)


# In[60]:


rtu_defn['Start30'] = ''
rtu_defn['Count40'] = ''

encontrados = 0
no_encontrados = 0

for index, row in rtu_data.iterrows():
    rtac_scada_ip = row['RTAC SCADA IP']
    
    filtered_stations = all_stations_equivalency[(all_stations_equivalency['IP Address'] == rtac_scada_ip) & 
                                                 (all_stations_equivalency['Type'] == 'STATUS')]
    
    if not filtered_stations.empty:
        valid_dnp_points = filtered_stations['DNP Point'].dropna()
        valid_dnp_points = valid_dnp_points[valid_dnp_points != 0]
        valid_dnp_points = valid_dnp_points[valid_dnp_points != '']
        
        if not valid_dnp_points.empty:
            min_dnp_point = valid_dnp_points.min()
            max_dnp_point = valid_dnp_points.max()
            
            rtu_defn.at[index, 'Start30'] = int(min_dnp_point)
            rtu_defn.at[index, 'Count40'] = int(max_dnp_point) - int(min_dnp_point) + 1
            
            encontrados += 1
        else:
            rtu_defn.at[index, 'Start30'] = ''
            rtu_defn.at[index, 'Count40'] = ''
            no_encontrados += 1
    else:
        rtu_defn.at[index, 'Start30'] = ''
        rtu_defn.at[index, 'Count40'] = ''
        no_encontrados += 1

rtu_defn['Start30'] = rtu_defn['Start30'].replace('', 771771771)
rtu_defn['Start30'] = rtu_defn['Start30'].astype(int)
rtu_defn['Start30'] = rtu_defn['Start30'].replace(771771771,'')

rtu_defn['Count40'] = rtu_defn['Count40'].replace('', 771771771)
rtu_defn['Count40'] = rtu_defn['Count40'].astype(int)
rtu_defn['Count40'] = rtu_defn['Count40'].replace(771771771,'')

print(f"Valores encontrados: {encontrados}")
print(f"Valores no encontrados: {no_encontrados}")


# In[61]:


rtu_defn['PointType11'] = [4] * len(rtu_data)


# In[62]:


rtu_defn['Start31'] = ''
rtu_defn['Count41'] = ''

encontrados_start31 = 0
no_encontrados_start31 = 0
encontrados_count41 = 0
no_encontrados_count41 = 0

for index, row in rtu_data.iterrows():
    rtac_scada_ip = row['RTAC SCADA IP']
    
    filtered_stations = all_stations_equivalency[(all_stations_equivalency['IP Address'] == rtac_scada_ip) & 
                                                 (all_stations_equivalency['Type'] == 'ANALOG')]
    
    if not filtered_stations.empty:
        valid_dnp_points = filtered_stations['DNP Point'].dropna()
        valid_dnp_points = valid_dnp_points[valid_dnp_points != 0]
        valid_dnp_points = valid_dnp_points[valid_dnp_points != '']
        
        if not valid_dnp_points.empty:
            min_dnp_point = valid_dnp_points.min()
            max_dnp_point = valid_dnp_points.max()
            
            rtu_defn.at[index, 'Start31'] = int(min_dnp_point)
            rtu_defn.at[index, 'Count41'] = int(max_dnp_point) - int(min_dnp_point) + 1
            
            encontrados_start31 += 1
            encontrados_count41 += 1
        else:
            rtu_defn.at[index, 'Start31'] = ''
            rtu_defn.at[index, 'Count41'] = ''
            no_encontrados_start31 += 1
            no_encontrados_count41 += 1
    else:
        rtu_defn.at[index, 'Start31'] = ''
        rtu_defn.at[index, 'Count41'] = ''
        no_encontrados_start31 += 1
        no_encontrados_count41 += 1

rtu_defn['Start31'] = rtu_defn['Start31'].replace('', 771771771)
rtu_defn['Start31'] = rtu_defn['Start31'].astype(int)
rtu_defn['Start31'] = rtu_defn['Start31'].replace(771771771,'')

rtu_defn['Count41'] = rtu_defn['Count41'].replace('', 771771771)
rtu_defn['Count41'] = rtu_defn['Count41'].astype(int)
rtu_defn['Count41'] = rtu_defn['Count41'].replace(771771771,'')

print(f"Valores encontrados : {encontrados_start31}")
print(f"Valores no encontrados : {no_encontrados_start31}")
#print(f"Valores encontrados para Count41: {encontrados_count41}")
#print(f"Valores no encontrados para Count41: {no_encontrados_count41}")


# In[63]:


rtu_defn


# In[64]:


rtu_defn = rtu_defn.astype(str).replace('', '""')


# In[65]:


rtu_defn.to_csv("borrarrtudefn.csv", index=False)


# In[66]:


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


# # SCAN_DATA OBJECT

# cargando y tratando los datos en type status 

# dependencies
# 
# status xref
# 
# rtac scada
# 
# 
# allstation equivalency
# 

# In[67]:


import pandas as pd


rtu_data = pd.read_csv('RTAC SCADA DNP IPs Reordered (1).csv')
all_stations_equivalency = pd.read_csv('all_stations_equivalency.csv')
all_stations_equivalency = all_stations_equivalency[all_stations_equivalency['Type'].isin(['STATUS', 'ANALOG'])]

all_stations_equivalency = all_stations_equivalency[all_stations_equivalency['DNP Point'].notna()]
all_stations_equivalency = all_stations_equivalency[all_stations_equivalency['DNP Point'].astype(str) != '']

all_stations_equivalency['DNP Point'] = all_stations_equivalency['DNP Point'].astype(int)

ip_addresses = rtu_data['RTAC SCADA IP'].unique()
scan_data = all_stations_equivalency[all_stations_equivalency['IP Address'].isin(ip_addresses)]

scan_data['Order'] = scan_data['Type'].map({'STATUS': 0, 'ANALOG': 1})

scan_data = scan_data.sort_values(['IP Address', 'Order', 'DNP Point'])

scan_data = scan_data.reset_index(drop=True)

scan_data['SCAN_DATA_Record'] = 0

last_scan_data_record = {}
last_point_type = {}

for index, row in scan_data.iterrows():
    ip_address = row['IP Address']
    point_type = row['Type']
    dnp_point = row['DNP Point']
    if point_type == 'STATUS':
  
        scan_data.at[index, 'SCAN_DATA_Record'] = dnp_point + 1
        last_scan_data_record[ip_address] = scan_data.at[index, 'SCAN_DATA_Record']
    else:
   
        if ip_address not in last_point_type or last_point_type[ip_address] != 'ANALOG':
 
            scan_data.at[index, 'SCAN_DATA_Record'] = last_scan_data_record[ip_address] + 1
        else:
       
            prev_index = index - 1
            prev_dnp_point = scan_data.at[prev_index, 'DNP Point']
            diff = dnp_point - prev_dnp_point
            scan_data.at[index, 'SCAN_DATA_Record'] = last_scan_data_record[ip_address] + diff

        last_scan_data_record[ip_address] = scan_data.at[index, 'SCAN_DATA_Record']

    last_point_type[ip_address] = point_type

scan_data = scan_data.drop('Order', axis=1)


# In[68]:


status_xref = pd.read_csv('status_xref.csv')

# Función para buscar el valor en status_xref y obtener la clave correspondiente
def get_destination_key(row):
    search_value = f"{row['Station']},{row['Pnuemonic']}"
    match = status_xref[status_xref['Name_Status_Source  '].str.strip() == search_value.strip()]
    if not match.empty:
        return match['Key'].iloc[0]
    else:
        print(f"No se encontró el valor {search_value} en status_xref")
        return None

# Aplicar la función a cada fila de scan_data para obtener la Destination_key
scan_data['Destination_key'] = scan_data.apply(get_destination_key, axis=1)

# Mostrar el resultado
print("Scan Data con Destination_key:")
print(scan_data.head())


# 

# # OUTPUT SCAN DATA

# In[69]:


with open("SCAN_DATA.dat", 'w') as f:
    f.write('32 FEP.DB\n')
    f.write('* \n')
    f.write('\t10\tSCAN_DATA\t0\t14\t50\n')
    f.write('*\tSCAN_DATA_Record\t1s\tDestinationKey\tName\n')

    for index, row in scan_data.iterrows():
        f.write('\t{}\t{}\t{}\t"{}"\n'.format(
                row['SCAN_DATA_Record'], "1", row['Destination_key'], row['Description']))
    

    f.write(" 0\n")
    f.write(" 0") 


# _____________

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

# In[70]:


rtac_data = pd.read_csv('RTAC SCADA DNP IPs Reordered (1).csv')

channel_group_defn = pd.DataFrame()

#COLUMNS OF CHANNEL_GROUP
channel_group_defn['Indic'] = rtac_data['RTAC Number'] #Este es el indice incremental de a uno
channel_group_defn['ConnectionType'] = [1] * len(rtac_data)
channel_group_defn['APDU'] = [2] * len(rtac_data)

channel_group_defn['MaxApdu'] = [23] * len(rtac_data)
channel_group_defn['MasterAddr'] = [1024] * len(rtac_data)


# In[71]:


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
# ####=!RG 2/11: If ( Point Type == RELAY) then merge column Name+ ',' + Description , and then ####search for it in the output file SCADA.dat object Status. Grab the key of the matching #####record
# 
# # update
# 
# RG 3/24: If ( Point Type == RELAY) then merge column Station+ ',' + Point, and then search for it in the status_xref and grab the key of the matching record.
# 
# 
# 
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
# 
# 43 = Name   Field : Description.  between : ""
# 

# 

# __________

# # OMITIR ESTO ENTRE SEPADRADORES

# In[72]:


#equivalency_station = pd.read_csv('Equivalency_station.csv')


# In[73]:


#equivalency_station = equivalency_station.drop(columns=['Point.1'])


# In[74]:


#equivalency_station


# In[75]:


#RtuControl = pd.DataFrame(index=equivalency_station.index)


#RtuControl['KeySCADA'] = equivalency_station.apply(lambda row: row['Station'] + ',' + row['Point'] if row['Point Type'] == 'RELAY' else '', axis=1)


# In[76]:


#RtuControl


# In[77]:


#source_status = pd.read_csv('status_xref.csv')


#RtuControl['Key2'] = pd.NA


#buscados = 0
#encontrados = 0


#for index, row in RtuControl.iterrows():
 #   if pd.notna(row['KeySCADA']) and row['KeySCADA'] != '': 
  #      buscados += 1
   
  #      match = source_status[source_status['Name_Status_Source  '].str.contains(row['KeySCADA'])]
  #      if not match.empty: 
  #          encontrados += 1
  #          
  #          RtuControl.at[index, 'Key2'] = match['Key'].values[0]

#print(f"Items buscados: {buscados}")
#print(f"Items encontrados: {encontrados}")


# In[78]:


#RtuControl = RtuControl.rename(columns={'KeySCADA': 'equivalency_station_point'})


# In[79]:


#RtuControl = RtuControl.rename(columns={'Key2': 'Key'})


# _________

# In[80]:


comentado = """
import pandas as pd


equivalency_station = pd.read_csv('Equivalency_station.csv')

RtuControl = pd.DataFrame(index=equivalency_station.index)


RtuControl['KeySCADA'] = equivalency_station.apply(lambda row: row['Full Point Name'] + ' ' + row['Description'] if row['Point Type'] == 'RELAY' else '', axis=1)
"""


# In[81]:


comentado = """
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
"""


# In[82]:


comentado = """

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
"""


# In[83]:


draft = """df1 = pd.read_csv('equivalency_station.csv')
df1 = df1[df1['Point Type'] == 'RELAY']

df2 = pd.read_csv('status_xref.csv')

df1 = df1[['Station', 'Point', 'IP', 'DNP Point #', 'Description']]
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
df_matches['Description'] = df_matches['equivalency_station_point'].apply(lambda x: df1[df1['combined'] == x]['Description'].iloc[0])
print(f"Number of matches: {matches}")


rtac_scada_ips = pd.read_csv('RTAC SCADA DNP IPs Reordered (1).csv')

#  control_type
#df_matches['control_type'] = 6
df_matches.loc[df_matches.duplicated(subset=['IP', 'DNP Point #'], keep=False), 'control_type'] = df_matches[df_matches.duplicated(subset=['IP', 'DNP Point #'], keep=False)].groupby(['IP', 'DNP Point #']).cumcount() + 4
df_matches['control_type'] = df_matches['control_type'].fillna(6)
#  point_address
df_matches['point_address'] = df_matches['DNP Point #']

#  pRTU
df_matches['pRTU'] = df_matches['IP'].apply(lambda x: rtac_scada_ips[rtac_scada_ips['RTAC SCADA IP'] == x]['RTAC Number'].iloc[0] if not rtac_scada_ips[rtac_scada_ips['RTAC SCADA IP'] == x].empty else '')


result_df = df_matches[['Key', 'control_type', 'point_address', 'pRTU', 'Description']]
result_df['Description'] = '"' + result_df['Description'] + '"'



#result_df = df_matches[['Key', 'control_type', 'point_address', 'pRTU']]


result_df = result_df.fillna(777)


result_df['control_type'] = result_df['control_type'].astype(int)
result_df['point_address'] = result_df['point_address'].astype(int)
result_df['pRTU'] = result_df['pRTU'].astype(int)
result_df['control_format'] = 1


result_df = result_df.replace(777, '')

print(result_df)"""


# In[84]:


df1 = pd.read_csv('equivalency_station.csv')
df1 = df1[df1['Point Type'] == 'RELAY']
df2 = pd.read_csv('status_xref.csv')
df1 = df1[['Station', 'Point', 'IP', 'DNP Point #', 'Description']]
df1['combined'] = df1['Station'] + ',' + df1['Point'] + ' '

results = []
matches = 0
for val in df1['combined']:
    match = df2['Name_Status_Source  '].str.contains(val)
    if match.any():
        key = df2[match]['Key'].iloc[0]
        results.append({'equivalency_station_point': val, 'Key': key, 'IP': df1[df1['combined'] == val]['IP'].iloc[0], 'DNP Point #': df1[df1['combined'] == val]['DNP Point #'].iloc[0]})
        matches += 1

df_matches = pd.DataFrame(results)
df_matches['Description'] = df_matches['equivalency_station_point'].apply(lambda x: df1[df1['combined'] == x]['Description'].iloc[0])
print(f"Number of matches: {matches}")

rtac_scada_ips = pd.read_csv('RTAC SCADA DNP IPs Reordered (1).csv')

#control_type
#df_matches['control_type'] = 6
df_matches.loc[df_matches.duplicated(subset=['IP', 'DNP Point #'], keep=False), 'control_type'] = df_matches[df_matches.duplicated(subset=['IP', 'DNP Point #'], keep=False)].groupby(['IP', 'DNP Point #']).cumcount() + 4
df_matches['control_type'] = df_matches['control_type'].fillna(6)

#point_address
df_matches['point_address'] = df_matches['DNP Point #']

#pRTU
df_matches['pRTU'] = df_matches['IP'].apply(lambda x: rtac_scada_ips[rtac_scada_ips['RTAC SCADA IP'] == x]['RTAC Number'].iloc[0] if not rtac_scada_ips[rtac_scada_ips['RTAC SCADA IP'] == x].empty else '')

result_df = df_matches[['Key', 'control_type', 'point_address', 'pRTU', 'Description']]
result_df = result_df.fillna(777)
result_df['control_type'] = result_df['control_type'].astype(int)
result_df['point_address'] = result_df['point_address'].astype(int)
result_df['pRTU'] = result_df['pRTU'].astype(int)
result_df['control_format'] = 1
result_df = result_df.replace(777, '')
result_df['Description'] = '"' + result_df['Description'] + '"'
print(result_df)


# In[85]:


import numpy as np
index = np.arange(1,len(result_df)+1)
result_df.insert(0, 'idx', index)


# In[86]:


result_df


# Numero de objeto RTU_CONTROL?

# In[87]:


rtu_object_number = 20


# In[88]:


with open("RTU_CONTROL.dat", 'w') as f:
    f.write('* \n')
    f.write(f'\t{rtu_object_number}\tRTU_CONTROL\t1\t2\t4\t6\t13\n')
    f.write('*\tKeySCADA\tcontrol_type\tpoint_address\tpRTU\tcontrol_format\n')

    for index, row in result_df.iterrows():
        f.write("\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                row['idx'] ,row['Key'], row['control_type'], row['point_address'], row['pRTU'],row['control_format']))
    

    f.write(" 0") 


# ________

# In[ ]:




