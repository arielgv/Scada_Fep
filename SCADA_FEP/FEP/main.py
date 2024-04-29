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

# In[1]:


import pandas as pd
from datetime import datetime


# In[2]:


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


# In[3]:


with open('FEP.DAT', 'w') as file:
    file.write('*\n')
    file.write('\t4\tFEP\t0\t2\t4\t5\t11\t17\n')
    file.write('*\tIndic\tMode\tHostname\tName\tNumPorts\tipaddress\n')

    for index, row in FEP.iterrows():
        file.write(f'\t{row["Indic"]}\t{row["Indic"]}\t{row["Mode"]}\t{row["Hostname"]}\t{row["Name"]}\t{row["NumPorts"]}\t{row["ipdaddress"]}\n')

    file.write("0")


# # CHANNEL

# dependencies: 
# RTAC SCADA DNP IPs Reordered.csv   (DF)
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
# Name  19       [RTAC SCADA DNP IPs Reordered.csv] 
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

# In[4]:


rtac_data = pd.read_csv('RTAC SCADA DNP IPs Reordered.csv')
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




# In[5]:


channel


# # Output : CHANNEL.DAT

# SE LE INCORPORA UNA COLUMNA CON VALORES '1' A CONTINUACION DE LA COLUMNA INDICE

# In[6]:


with open("CHANNEL.dat", 'w') as f:
    f.write('* \n')
    f.write('\t5\tCHANNEL\t0\t1\t13\t14\t18\t19\t24\t25\t27\t30\t40\t41\n')
    f.write('*\tIndic\t1s\tpFEP\tCharacter\tStop_Bits\tNoReplyLimit\tName\tChannelResTimeoutMsec\tPhysicalPort\tChannelReqDelay\tHostname\tpChannel_GROUP\tChannelConnTimeout\n')

    for index, row in channel.iterrows():
        f.write("\t{}\t{}\t{}\t{}\t{}\t{}\t\"{}\"\t{}\t{}\t{}\t{}\t{}\n".format(
                row['Indic'],row['Stop_Bits'], row['pFEP'], row['Character'], row['Stop_Bits'], row['NoReplyLimit'],
                row['Name'],  row['ChannelResTimeoutMsec'], 
                row['PhysicalPort'], row['ChannelReqDelay'], row['Hostname'], row['pCHANNEL_GROUP'], row['ChannelConnTimeout']))
      
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

# In[7]:


rtu_data = pd.read_csv('RTAC SCADA DNP IPs Reordered.csv')


# In[8]:


df = pd.DataFrame()
rtu_data['Panel'] = rtac_data['Panel'].str.replace('Panel ', '', regex=False)

#CHECK INDICS ******************
df['Indics'] = rtu_data['RTAC Number']

df['pCHANNEL_GROUP'] = rtu_data['RTAC Number']
df['Protocol'] = [8] * len(rtu_data)

df['Name'] = rtu_data['Abreviation'] + '_' + rtu_data['Panel'] + '_RTU'
df['Address'] = [1] * len(rtu_data)

df['SubType'] = [2] * len(rtu_data)


# In[9]:


df


# # OUTPUT : RTU_DATA.DAT

# Se incorpora una columna de '1s' siguiente al indice . 

# In[10]:


with open("RTU_DATA.dat", 'w') as f:
    f.write('* \n')
    f.write('\t6\tRTU_DATA\t0\t2\t3\t5\t14\t55\n')
    f.write('*\tIndics\t1s\tpCHANNEL_GROUP\tProtocol\tName\tAddress\tSubType\n')

    line_number = 1  

    for index, row in df.iterrows():
        f.write("\t{}\t{}\t{}\t{}\t\"{}\"\t{}\t{}\n".format(
                row['Indics'],row['Address'], row['pCHANNEL_GROUP'], row['Protocol'], 
                row['Name'], row['Address'], row['SubType']))
        line_number += 1 

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

# In[11]:


rtac_data = pd.read_csv('RTAC SCADA DNP IPs Reordered.csv')
rtac_data['Panel'] = rtac_data['Panel'].str.replace('Panel ', '', regex=False)


channel_group = pd.DataFrame()



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


# In[12]:


channel_group


# Columna siguiente a Indice agregada: 1s. Valores unicamente int 1

# In[13]:


with open("CHANNEL_GROUP.dat", 'w') as f:
    f.write('* \n')
    f.write('\t22\tCHANNEL_GROUP\t0\t3,3\t3,8\t3,9\t4\t6\t8,0\t20\t23\t24\n')
    f.write('*\tIndic\t1s\tMaxAPDU\tConnectionType\tAPDU\tProtocol\tName\tpCHANNEL\tBackupMonDisable\tpAORGroup\tType\n')


    for index, row in channel_group.iterrows():
        f.write("\t{}\t{}\t{}\t{}\t{}\t{}\t\"{}\"\t{}\t{}\t{}\t{}\n".format(
                row['Indic'],row['BackupMonDisable'],row['MaxAPDU'],row['ConnectionType'],row['APDU'], row['Protocol'], 
                row['Name'], row['pCHANNEL'], row['BackupMonDisable'],row['pAORGroup'] ,row['Type']))


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
#  "RG 4/4: For each RTAC (each RTAC has a unique IP address) search for the smallest ""DNP Point #"" of the Point Type == Status and use that number + 1.
# 
# 
# 
# Count 4,0 : Set to 5
# 
# PointType 1,1 : Set to 4
# 
# Start 3,1 : Set to 1
# RG 3/11: For each RTAC (each RTAC has a unique IP address) search for the smallest ""DNP Point #""  of the Point Type == Analog and use that number + 1.
# 
# 
# Count 4,1 : Set to 5
# 
# 
# 

# In[14]:


import pandas as pd


rtu_data = pd.read_csv('RTAC SCADA DNP IPs Reordered.csv')
all_stations_equivalency = pd.read_csv('all_stations_equivalency.csv')
rtu_defn = pd.DataFrame()
rtu_defn['Indics'] = range(1, len(rtu_data) + 1)
rtu_defn['PointType10'] = [1] * len(rtu_data)


# In[15]:


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
            
            rtu_defn.at[index, 'Start30'] = int(min_dnp_point)+1
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

#print(f"Valores encontrados: {encontrados}")
#print(f"Valores no encontrados: {no_encontrados}")


# In[16]:


rtu_defn['PointType11'] = [4] * len(rtu_data)


# In[17]:


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
            
            rtu_defn.at[index, 'Start31'] = int(min_dnp_point)+1
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

#print(f"Valores encontrados : {encontrados_start31}")
#print(f"Valores no encontrados : {no_encontrados_start31}")


# In[18]:


rtu_defn


# In[19]:


rtu_defn = rtu_defn.astype(str).replace('', '""')


# In[20]:


with open("RTU_DEFN.dat", 'w') as f:
    f.write('* \n')
    f.write('\t27\tRTU_DEFN\t1,0\t3,0\t4,0\t1,1\t3,1\t4,1\n')
    f.write('*\tIndic\tPointtype(1,0)\tStart(3,0)\tCount(4,0)\tPointType(1,1)\tStart(3,1)\tCount(4,1)\n')



    for index, row in rtu_defn.iterrows():
        f.write("\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                row['Indics'], row['PointType10'], row['Start30'], row['Count40'], row['PointType11'], row['Start31'], row['Count41']))

    

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

# Scan_data_xref.csv will be CSV format. 
# Is created after FEP.dat is created  because some of the inputs come from the object RTU_DEFN. 
# The different files of <station>_equivalency.xlsx will be merged into all_equivalency_stations.csv . The all_equivalency_stations.csv will be used as input to create the scan_data_xref.
# RTAC_SCADA_DNP_IPs_Reordered will also be an input.
# Once the Scan_data_xref is created, SCAN_DATA.dat will be created out of some of the columns of Scan_data_xref.
# 

# The number of records will be the addition of the count values of the object FEP/RTU_DEFN. 
# At this moment April 2024 we only have two values per record of RTU_DEFN, Count (4,0) and Count(4,1). Soon we will have more than two counts. i.e Count(4,2) … count(4,9) . 
# For now lets only focus on Count (4,0) and Count(4,1). 
# The addition of all is equal to 1501. 
# Scan_data_xref.csv will have 1501 records. 
# 

# ### Scan_data_xref

# ### 'Record' Column

# In[21]:


import pandas as pd

def convert_to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0

rtu_defn['Count40'] = rtu_defn['Count40'].apply(convert_to_int)
rtu_defn['Count41'] = rtu_defn['Count41'].apply(convert_to_int)

total_records = rtu_defn['Count40'].sum() + rtu_defn['Count41'].sum()

Scan_Data_xref = pd.DataFrame({'record': range(1, total_records + 1)})

print(f"Se crearon {total_records} records en Scan_Data_xref.")


# In[22]:


Scan_Data_xref


# ____

# ### RTAC_Address

# In[23]:


import pandas as pd


rtu_defn_copy = rtu_defn.copy()


numeric_columns = ['Start30', 'Count40', 'Start31', 'Count41']
rtu_defn_copy = rtu_defn_copy[rtu_defn_copy[numeric_columns].apply(lambda x: pd.to_numeric(x, errors='coerce')).notna().all(axis=1)]


rtu_defn_copy[numeric_columns] = rtu_defn_copy[numeric_columns].apply(pd.to_numeric)

Scan_Data_xref = pd.DataFrame(columns=['record', 'RTAC_Address', 'point_type'])


for _, row in rtu_defn_copy.iterrows():

    start30_records = pd.DataFrame({
        'record': range(len(Scan_Data_xref), len(Scan_Data_xref) + int(row['Count40'])),
        'RTAC_Address': range(int(row['Start30']), int(row['Start30']) + int(row['Count40'])),
        'point_type': int(row['PointType10'])
    })
    Scan_Data_xref = pd.concat([Scan_Data_xref, start30_records], ignore_index=True)
    
    start31_records = pd.DataFrame({
        'record': range(len(Scan_Data_xref), len(Scan_Data_xref) + int(row['Count41'])),
        'RTAC_Address': range(int(row['Start31']), int(row['Start31']) + int(row['Count41'])),
        'point_type': int(row['PointType11'])
    })
    Scan_Data_xref = pd.concat([Scan_Data_xref, start31_records], ignore_index=True)

Scan_Data_xref.reset_index(drop=True, inplace=True)

Scan_Data_xref['record'] = range(1, len(Scan_Data_xref) + 1)


# ____________

# ### RTAC_Number

# In[24]:


rtu_defn_df = rtu_defn


numeric_rows = rtu_defn_df.apply(lambda x: x.astype(str).str.isnumeric().all(), axis=1)

Scan_Data_xref['RTAC_Number'] = ''

start_index = 0

for index, row in rtu_defn_df[numeric_rows].iterrows():
    indics = row['Indics']
    count40 = row['Count40']
    count41 = row['Count41']
    
  
    total_count = count40 + count41

    end_index = start_index + total_count
    Scan_Data_xref.loc[start_index:end_index-1, 'RTAC_Number'] = indics

    start_index = end_index


# ### RTAC_Name , IP , and ABR

# In[25]:


rtac_scada_df = pd.read_csv('RTAC SCADA DNP IPs Reordered.csv')

Scan_Data_xref['RTAC_Number'] = Scan_Data_xref['RTAC_Number'].astype(str)
rtac_scada_df['RTAC Number'] = rtac_scada_df['RTAC Number'].astype(str)
Scan_Data_xref = pd.merge(Scan_Data_xref, rtac_scada_df[['RTAC Number', 'RTAC SCADA IP', 'Site', 'Abreviation']], 
                          left_on='RTAC_Number', right_on='RTAC Number', how='left')
Scan_Data_xref = Scan_Data_xref.rename(columns={'RTAC SCADA IP': 'RTAC IP'})
Scan_Data_xref = Scan_Data_xref.rename(columns={'Site': 'RTAC NAME'})
Scan_Data_xref = Scan_Data_xref.rename(columns={'Abreviation': 'RTAC Abr'})
Scan_Data_xref = Scan_Data_xref.drop('RTAC Number', axis=1)


# ### NAME

# In[26]:


all_station_df = pd.read_csv('all_stations_equivalency.csv')

# Function to find the matching row in all_station_df and return the Name value
def find_name(row):
    if row['point_type'] == 1:
        dnp_point = row['RTAC_Address'] - 1
        mask = (all_station_df['DNP Point'] == dnp_point) & (all_station_df['Type'] == 'STATUS') & (all_station_df['IP Address'] == row['RTAC IP'])
        matching_row = all_station_df[mask]
        if not matching_row.empty:
            return f"{matching_row['Station'].values[0]},{matching_row['Pnuemonic'].values[0]}"
    elif row['point_type'] == 4:
        dnp_point = row['RTAC_Address'] - 1
        mask = (all_station_df['DNP Point'] == dnp_point) & (all_station_df['Type'] == 'ANALOG') & (all_station_df['IP Address'] == row['RTAC IP'])
        matching_row = all_station_df[mask]
        if not matching_row.empty:
            return f"{matching_row['Station'].values[0]},{matching_row['Pnuemonic'].values[0]}"
    return 'none'

# Apply the find_name function to each row of Scan_Data_xref and create the 'Name' column
Scan_Data_xref['Name'] = Scan_Data_xref.apply(find_name, axis=1)

# Print the number of matches found
num_matches = (Scan_Data_xref['Name'] != 'none').sum()
print(f"Number of matches found: {num_matches}")


# 

# In[27]:


Scan_Data_xref['1s'] = 1


# ### DNP POINT

# In[28]:


all_station_df = pd.read_csv('all_stations_equivalency.csv')
def find_name(row):
    if row['point_type'] == 1:
        dnp_point = row['RTAC_Address'] - 1
        mask = (all_station_df['DNP Point'] == dnp_point) & (all_station_df['Type'] == 'STATUS') & (all_station_df['IP Address'] == row['RTAC IP'])
        matching_row = all_station_df[mask]
        if not matching_row.empty:
            return f"{matching_row['Station'].values[0]},{matching_row['Pnuemonic'].values[0]}"
    elif row['point_type'] == 4:
        dnp_point = row['RTAC_Address'] - 1
        mask = (all_station_df['DNP Point'] == dnp_point) & (all_station_df['Type'] == 'ANALOG') & (all_station_df['IP Address'] == row['RTAC IP'])
        matching_row = all_station_df[mask]
        if not matching_row.empty:
            return f"{matching_row['Station'].values[0]},{matching_row['Pnuemonic'].values[0]}"
    return 'none'

def find_dnp_point_address(row):
    if row['point_type'] == 1:
        dnp_point = row['RTAC_Address'] - 1
        mask = (all_station_df['DNP Point'] == dnp_point) & (all_station_df['Type'] == 'STATUS') & (all_station_df['IP Address'] == row['RTAC IP'])
        matching_row = all_station_df[mask]
        if not matching_row.empty:
            return int(matching_row['DNP Point'].values[0])
    elif row['point_type'] == 4:
        dnp_point = row['RTAC_Address'] - 1
        mask = (all_station_df['DNP Point'] == dnp_point) & (all_station_df['Type'] == 'ANALOG') & (all_station_df['IP Address'] == row['RTAC IP'])
        matching_row = all_station_df[mask]
        if not matching_row.empty:
            return int(matching_row['DNP Point'].values[0])
    return 'none'

Scan_Data_xref['Name'] = Scan_Data_xref.apply(find_name, axis=1)
Scan_Data_xref['DNP Point Address'] = Scan_Data_xref.apply(find_dnp_point_address, axis=1)
num_matches = (Scan_Data_xref['Name'] != 'none').sum()
print(f"Number of matches found: {num_matches}")


# In[29]:


source_status_df = pd.read_csv('SOURCE_status.csv')
analog_xref = pd.read_csv('analog_xref.csv')
status_xref = pd.read_csv('status_xref.csv')


source_analog_df = pd.read_csv('SOURCE_analog.csv')


def find_name(row):
    if row['point_type'] == 1:
        dnp_point = row['RTAC_Address'] - 1
        mask = (all_station_df['DNP Point'] == dnp_point) & (all_station_df['Type'] == 'STATUS') & (all_station_df['IP Address'] == row['RTAC IP'])
        matching_row = all_station_df[mask]
        if not matching_row.empty:
            return f"{matching_row['Station'].values[0]},{matching_row['Pnuemonic'].values[0]}"
    elif row['point_type'] == 4:
        dnp_point = row['RTAC_Address'] - 1
        mask = (all_station_df['DNP Point'] == dnp_point) & (all_station_df['Type'] == 'ANALOG') & (all_station_df['IP Address'] == row['RTAC IP'])
        matching_row = all_station_df[mask]
        if not matching_row.empty:
            return f"{matching_row['Station'].values[0]},{matching_row['Pnuemonic'].values[0]}"
    return 'none'


def find_dnp_point_address(row):
    if row['point_type'] == 1:
        dnp_point = row['RTAC_Address'] - 1
        mask = (all_station_df['DNP Point'] == dnp_point) & (all_station_df['Type'] == 'STATUS') & (all_station_df['IP Address'] == row['RTAC IP'])
        matching_row = all_station_df[mask]
        if not matching_row.empty:
            return int(matching_row['DNP Point'].values[0])
    elif row['point_type'] == 4:
        dnp_point = row['RTAC_Address'] - 1
        mask = (all_station_df['DNP Point'] == dnp_point) & (all_station_df['Type'] == 'ANALOG') & (all_station_df['IP Address'] == row['RTAC IP'])
        matching_row = all_station_df[mask]
        if not matching_row.empty:
            return int(matching_row['DNP Point'].values[0])
    return 'none'


def find_destination_key(row):
    mask = (all_station_df['IP Address'] == row['RTAC IP'])
    matching_row = all_station_df[mask]
    if not matching_row.empty:
        if matching_row['Type'].values[0] == 'STATUS':
            station = matching_row['Station'].values[0]
            pneumonic = matching_row['Pnuemonic'].values[0]
            name_to_match = (station + ',' + pneumonic).rstrip()
            
            status_mask = status_xref['name_to_match'].apply(lambda x: x.rstrip() == name_to_match)
            if status_mask.any():
                return status_xref.loc[status_mask, 'Key'].values[0]
        
        elif matching_row['Type'].values[0] == 'ANALOG':
            station = matching_row['Station'].values[0]
            pneumonic = matching_row['Pnuemonic'].values[0]
            name_to_match = (station + ',' + pneumonic).rstrip()
            
            analog_mask = analog_xref['Name_Analog_Source'].apply(lambda x: x.rstrip() == name_to_match)
            if analog_mask.any():
                return analog_xref.loc[analog_mask, 'Key'].values[0]
    
    return '""'


Scan_Data_xref['Name'] = Scan_Data_xref.apply(find_name, axis=1)

Scan_Data_xref['DNP Point Address'] = Scan_Data_xref.apply(find_dnp_point_address, axis=1)


Scan_Data_xref['Destination Key'] = Scan_Data_xref.apply(find_destination_key, axis=1)

num_matches = (Scan_Data_xref['Name'] != 'none').sum()
print(f"Number of matches found: {num_matches}")


# ## DESTINATION KEY

# For each of the points in Equivalency file that have 
# 
# 
# Point Type == STATUS, then grab all_station_equivalency/Station + "." + Pneumonic , and then search for it in the status_xref.csv/Name_Status_Source , Grab the key of the matching record.
# 
# 
# PointType == Analog, then grab all_station_equivalency/Station + "." + Pneumonic , and then search for it in the analog_xref.csv/Name_Analog_Source , Grab the key of the matching record.

# _______

# # OUTPUT SCAN DATA - Not included in merge

# In[30]:


with open("SCAN_DATA XREF.dat", 'w') as f:
    f.write('32 FEP.DB\n')
    f.write('* \n')
    f.write('\t10\tSCAN_DATA\t0\t14\t35\n')
    f.write('*\tRecord\t1s\tRTAC_point_type\tRTAC_address\tRTAC_Number\tRTAC IP\tRTAC NAME\tRTAC Abr\tDNP Point Address\tName\tDestinationKey\n')

    for index, row in Scan_Data_xref.iterrows():
        f.write('\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t"{}"\n'.format(
                row['record'], "1", row['point_type'], row['RTAC_Address'],row['RTAC_Number'],row['RTAC IP'],row['RTAC NAME'], row['RTAC Abr'], row['DNP Point Address'], row['Name'], row['Destination Key']))
    

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

# In[31]:


rtac_data = pd.read_csv('RTAC SCADA DNP IPs Reordered.csv')

channel_group_defn = pd.DataFrame()

#COLUMNS OF CHANNEL_GROUP
channel_group_defn['Indic'] = rtac_data['RTAC Number'] #Este es el indice incremental de a uno
channel_group_defn['ConnectionType'] = [1] * len(rtac_data)
channel_group_defn['APDU'] = [2] * len(rtac_data)

channel_group_defn['MaxApdu'] = [23] * len(rtac_data)
channel_group_defn['MasterAddr'] = [1024] * len(rtac_data)


# In[32]:


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
# & RTAC SCADA DNP IPs Reordered.csv
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
# UPDATE 4/4: 
# all_equivalency_station.csv	"IP
# DNP Point #"	"RG 4/4:  If there are two records with same IP and same DNP Point # then create one record with the KeySCADA, it will have control_type equal to 6.
# 
# UPDATE 4/ 24:
# RG 4/24:  If there are two records with same IP and same DNP Point # then create one record. Merge column of all_station_equivalency Station + "," + Pneumonic and search for it in status_xref, If the point is type 6(R/L) set to type 3 else set to 6 
# 
# 
# 
# 
# 
# 
# 4  =  point_address: Field : "DNP Point #"
# 
# "RG 2/11:  If there are two records with same IP and same DNP Point # then use DNP Point # on each of the two records, 
# If there is only one record with unique IP and unique DNP Point # then use  DNP Point # in its own record."
# 
# "RG 4/4:  If there are two records with same IP and same DNP Point # then use DNP Point # + 1 
# 
# 	RG 4/4: The first control of Melrose will be set to type 6 and address 19
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

# # RTU CONTROL UPDATED:
# ## all_equivalency_station.csv

# 

# columnas existentes de all_equivalency_station.csv:
# Point ID,Station,Pnuemonic,Description,COM,RTU,Pg,Status P,Analog P,Relay P,Value,Scale,Type,Helper Column,IP Address,DNPAddress,DNP Point,,.1
# 
# columnas existentes de status_xref.csv:
# record,name_to_match,OrderNo,Type,Key,Name,Stn,AOR,pState,Norm,AlarmGroup,ICAddress,FeedbackKey,pDeviceInstance,pCtrlState,pScale,HiControlLimit,LoControlLimit,Setpoint_emulation,Name_Status_Source  ,Desc  ,Zones  ,PreSuffx  ,Telem_A  ,Open_A  ,Open_B  ,Close_A  ,Normal_State  
# 
# 
# Crear un Dataframe RTU_CONTROL con las siguientes columnas.
# 1 . KeySCADA :  Si la columna 'Type' de all_equivalency_station.csv es == 'RELAY',  entonces unir el contenido de la columna Station + ',' + el contenido de la columna Pnuemonic. Y buscar ese resultante dentro de la columna 'name_to_match' en el archivo status_xref.csv , y si encuentra coincidencia, tomar el valor de la columna 'Key' de status_xref.csv. ese será el valor de KeyScada para esa fila.
# 
# 2. control_type: (realizar un barrido de todas las filas para conocer si hay casos en los que hayan dos records que tengan el mismo Ip y el mismo DNP Point (en all equivalency station) para los casos en los que existiese dos records con mismo Ip y mismo DNP Point #  , crear un solo record para ambos. unir el contenido de la columna Station + ',' + el contenido de la columna Pnuemonic. Y buscar ese resultante dentro de la columna 'name_to_match' en el archivo status_xref.csv , en el caso de encontrar coincidencia, SI el valor de la columna 'Type' de status_xref.csv es 6 , entonces control_type tomará el valor 3. sino, setearlo a 6.
# 
# 4. point_address : 
# 
# RG 4/4:  If there are two records with same IP and same DNP Point # then point_address =  (DNP Point  + 1 )
# If there is only one record with unique IP and unique DNP Point # then use  the value of DNP Point for point_address
# 
# 6. pRTU : Buscar el valor que figura en la columna IP Address de 'all equivalency station' dentro de la columna 'RTAC SCADA IP' en el archivo RTAC SCADA DNP IPs Reordered.csv, de encontrar coincidencia, tomar el valor de la columna 'RTAC Number' de RTAC SCADA DNP IPs Reordered.csv, ese será el valor de pRTU, si no encuentra coincidencia, el valor será 'none'
# 
# 43. Name : set to station + ',' + Pnuemonic. 
# 
# 
# 

# In[33]:


import pandas as pd


all_equivalency_station = pd.read_csv('all_stations_equivalency.csv')
status_xref = pd.read_csv('status_xref.csv')
rtac_scada_ips = pd.read_csv('RTAC SCADA DNP IPs Reordered.csv')


relay_records = all_equivalency_station[all_equivalency_station['Type'] == 'RELAY'].copy()


relay_records.loc[:, 'combined_key'] = relay_records['Station'] + ',' + relay_records['Pnuemonic']


rtu_control = pd.DataFrame(columns=['KeySCADA', 'control_type', 'point_address', 'pRTU', 'Name'])


for _, row in relay_records.iterrows():
    combined_key = row['combined_key']
    ip_address = row['IP Address']
    dnp_point = row['DNP Point']
    
   
    match = status_xref[status_xref['name_to_match'] == combined_key]
    
    if not match.empty:
        key_scada = match['Key'].iloc[0]
        
      
        duplicate_records = relay_records[(relay_records['IP Address'] == ip_address) & (relay_records['DNP Point'] == dnp_point)]
        
        if len(duplicate_records) == 2:
         
            control_type = 3 if match['Type'].iloc[0] == 6 else 6
            point_address = int(dnp_point + 1)
        else:
  
            control_type = 6
            point_address = dnp_point
        
       
        rtac_match = rtac_scada_ips[rtac_scada_ips['RTAC SCADA IP'] == ip_address]
        
        if not rtac_match.empty:
            prtu = rtac_match['RTAC Number'].iloc[0]
        else:
            prtu = 'none'
        
        name = row['Station'] + ',' + row['Pnuemonic']
        
       
        new_row = pd.DataFrame({
            'KeySCADA': [key_scada],
            'control_type': [control_type],
            'point_address': [point_address],
            'pRTU': [prtu],
            'Name': [name]
        })
        
      
        rtu_control = pd.concat([rtu_control, new_row], ignore_index=True)


print(rtu_control)


# In[34]:


draft_erase = """
df1 = pd.read_csv('all_equivalency_station.csv')
df1 = df1[df1['Type'] == 'RELAY']
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

rtac_scada_ips = pd.read_csv('RTAC SCADA DNP IPs Reordered.csv')



#"RG 4/24:  If there are two records with same IP and same DNP Point # then create one record. Merge column of all_station_equivalency Station + "","" + Pneumonic and search for it in status_xref, If the point is type 6(R/L) set to type 3 else set to 6 

# control_type
df_matches['combined_station_pneumonic'] = df1['Station'] + ',' + df1['Point']
df_matches['combined_station_pneumonic'] = df_matches['combined_station_pneumonic'].str.strip()

status_xref = pd.read_csv('status_xref.csv')
status_xref['name_to_match'] = status_xref['name_to_match'].astype(str)

def get_control_type(row):
    match = status_xref['name_to_match'].str.contains(str(row['combined_station_pneumonic']))
    if match.any():
        point_type = status_xref[match]['Type'].iloc[0]
        if point_type == 6:
            return 3
        else:
            return 6
    return 6

df_matches['control_type'] = df_matches.apply(get_control_type, axis=1)
df_matches.drop_duplicates(subset=['IP', 'DNP Point #'], keep='first', inplace=True)

# point_address
df_matches['point_address'] = df_matches['DNP Point #']
df_matches['duplicate'] = df_matches.duplicated(subset=['IP', 'DNP Point #'], keep=False)
df_matches.loc[df_matches['duplicate'], 'point_address'] += 1

# pRTU
df_matches['pRTU'] = df_matches['IP'].apply(lambda x: rtac_scada_ips[rtac_scada_ips['RTAC SCADA IP'] == x]['RTAC Number'].iloc[0] if not rtac_scada_ips[rtac_scada_ips['RTAC SCADA IP'] == x].empty else '')

result_df = df_matches[['Key', 'control_type', 'point_address', 'pRTU', 'Description']]
result_df = result_df.fillna(777)
result_df['control_type'] = result_df['control_type'].astype(int)
result_df['point_address'] = result_df['point_address'].astype(int)
result_df['pRTU'] = result_df['pRTU'].astype(int)
result_df['control_format'] = 1
result_df['control_bit_params'] = 1
result_df = result_df.replace(777, '')

# Modificar la columna 'Description' en result_df
result_df['Description'] = result_df['Key'].apply(lambda x: df1[(df1['Station'] + ',' + df1['Point'] + ' ') == df_matches[df_matches['Key'] == x]['equivalency_station_point'].iloc[0]]['Station'].iloc[0] + ',' + df1[(df1['Station'] + ',' + df1['Point'] + ' ') == df_matches[df_matches['Key'] == x]['equivalency_station_point'].iloc[0]]['Point'].iloc[0])
result_df['Name'] = '"' + result_df['Description'] + '"'

# Eliminar la columna 'Description'
result_df = result_df.drop('Description', axis=1)

import numpy as np
index = np.arange(1, len(result_df) + 1)
result_df.insert(0, 'idx', index)

print(result_df) """


# In[35]:


result_df = rtu_control


# In[36]:


result_df['control_format'] = 1
result_df['control_bit_params'] = 1
import numpy as np
index = np.arange(1, len(result_df) + 1)
result_df.insert(0, 'idx', index)


# Numero de objeto RTU_CONTROL?

# In[37]:


rtu_object_number = 20


# In[38]:


with open("RTU_CONTROL.dat", 'w') as f:
    f.write('* \n')
    f.write(f'\t{rtu_object_number}\tRTU_CONTROL\t1\t2\t4\t6\t13\t25,1\t43\n')
    f.write('*\tKeySCADA\tcontrol_type\tpoint_address\tpRTU\tcontrol_format\tcontrol_bit_params\tName\n')

    for index, row in result_df.iterrows():
        f.write("\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                row['idx'] ,row['KeySCADA'], row['control_type'], row['point_address']+1, row['pRTU'],row['control_format'],row['control_bit_params'],row['Name']))
    

    f.write(" 0") 


# ________

# # Scan defn (28)

# SCAN_DEFN	1,0	Mode_1	On or Off. 1 or 0 		RTAC SCADA DNP IPs Reordered.xlsx	RTAC Number	RG 4/3: Set to 1	"RG 4/3: The first column of this object is the record number so every row is increasing +1
# The second column of this object is 1s. his object will have a record per RTU, so around 73 records. "
# SCAN_DEFN	1,1	Mode_2	On or Off. 1 or 0 		RTAC SCADA DNP IPs Reordered.xlsx	RTAC Number	RG 4/3: Set to 1	
# SCAN_DEFN	1,2	Mode_3	On or Off. 1 or 0 		RTAC SCADA DNP IPs Reordered.xlsx	RTAC Number	RG 4/3: Set to 1	
# SCAN_DEFN	2,0	GSD_1	pointer to GSD		RTAC SCADA DNP IPs Reordered.xlsx	RTAC Number	RG 4/3: Set to 1	
# SCAN_DEFN	2,1	GSD_2	pointer to GSD		RTAC SCADA DNP IPs Reordered.xlsx	RTAC Number	RG 4/3: Set to 2	
# SCAN_DEFN	2,2	GSD_3	pointer to GSD		RTAC SCADA DNP IPs Reordered.xlsx	RTAC Number	RG 4/3: Set to 3	

# In[39]:


import pandas as pd

df = pd.read_csv('RTAC SCADA DNP IPs Reordered.csv')

num_rows = len(df)

Scan_defn = pd.DataFrame()
Scan_defn['Mode_1'] = range(1, num_rows+1) 
Scan_defn['Mode_2'] = 1
Scan_defn['Mode_3'] = 1
Scan_defn['GSD_1'] = 1 
Scan_defn['GSD_2'] = 2
Scan_defn['GSD_3'] = 3


# In[40]:


with open("SCAN_DEFN.dat", 'w') as f:
    f.write('* \n')
    f.write(f'\t28\tSCAN_DEFN\t1,0\t1,1\t1,2\t2,0\t2,1\t2,2\n')
    f.write('*\tMode_1\tMode_2\tMode_3\tGSD_1\tGSD_2\tGSD_3\n')

    for index, row in Scan_defn.iterrows():
        f.write("\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                row['Mode_1'] ,row['Mode_2'], row['Mode_2'],row['Mode_3'], row['GSD_1'], row['GSD_2'],row['GSD_3']))
    

    f.write(" 0") 


# ________

# # Demand Scan Defn (29)

# DEMAND_SCAN_DEFN	1,0	Mode_1	On or Off. 1 or 0 		RTAC SCADA DNP IPs Reordered.xlsx	RTAC Number	RG 4/3: Set to 1	"RG 4/3: The first column of this object is the record number so every row is increasing +1
# The second column of this object is 1s. his object will have a record per RTU, so around 73 records. "
# DEMAND_SCAN_DEFN	2,0	GSD_1	pointer to GSD		RTAC SCADA DNP IPs Reordered.xlsx	RTAC Number	RG 4/3: Set to 1	

# In[41]:


import pandas as pd

df = pd.read_csv('RTAC SCADA DNP IPs Reordered.csv')

num_rows = len(df)

demand_Scan_defn = pd.DataFrame()
demand_Scan_defn['Mode_1'] = range(1, num_rows+1) 
demand_Scan_defn['GSD_1'] = 1


# In[42]:


with open("DEMAND_SCAN_DEFN.dat", 'w') as f:
    f.write('* \n')
    f.write(f'\t29\tDEMAND_SCAN_DEFN\t1,0\t2,0\n')
    f.write('*\tMode_1\tGSD_1\n')

    for index, row in demand_Scan_defn.iterrows():
        f.write("\t{}\t{}\t{}\n".format(
                row['Mode_1'] ,row['GSD_1'],row['GSD_1']))
    

    f.write(" 0") 


# ___

# # INIT_SCAN_DEFN (30)

# INIT_SCAN_DEFN	1,0	Mode_1	On or Off. 1 or 0 		RTAC SCADA DNP IPs Reordered.xlsx	RTAC Number	RG 4/3: Set to 1	"RG 4/3: The first column of this object is the record number so every row is increasing +1
# The second column of this object is 1s. This object will have a record per RTU, so around 73 records. "
# INIT_SCAN_DEFN	1,1	Mode_2	On or Off. 1 or 0 		RTAC SCADA DNP IPs Reordered.xlsx	RTAC Number	RG 4/3: Set to 1	
# INIT_SCAN_DEFN	1,2	Mode_3	On or Off. 1 or 0 		RTAC SCADA DNP IPs Reordered.xlsx	RTAC Number	RG 4/3: Set to 1	
# INIT_SCAN_DEFN	2,0	GSD_1	pointer to GSD		RTAC SCADA DNP IPs Reordered.xlsx	RTAC Number	RG 4/3: Set to 1	
# INIT_SCAN_DEFN	2,1	GSD_2	pointer to GSD		RTAC SCADA DNP IPs Reordered.xlsx	RTAC Number	RG 4/3: Set to 2	
# INIT_SCAN_DEFN	2,2	GSD_3	pointer to GSD		RTAC SCADA DNP IPs Reordered.xlsx	RTAC Number	RG 4/3: Set to 3	

# In[43]:


import pandas as pd

df = pd.read_csv('RTAC SCADA DNP IPs Reordered.csv')

num_rows = len(df)

init_Scan_defn = pd.DataFrame()
init_Scan_defn['Mode_1'] = range(1, num_rows+1) 
init_Scan_defn['Mode_2'] = 1
init_Scan_defn['Mode_3'] = 1
init_Scan_defn['GSD_1'] = 1 
init_Scan_defn['GSD_2'] = 2
init_Scan_defn['GSD_3'] = 3


# In[44]:


with open("INIT_SCAN_DEFN.dat", 'w') as f:
    f.write('* \n')
    f.write(f'\t30\tINIT_SCAN_DEFN\t1,0\t1,1\t1,2\t2,0\t2,1\t2,2\n')
    f.write('*\tMode_1\tMode_2\tMode_3\tGSD_1\tGSD_2\tGSD_3\n')

    for index, row in Scan_defn.iterrows():
        f.write("\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                row['Mode_1'] ,row['Mode_2'], row['Mode_2'],row['Mode_3'], row['GSD_1'], row['GSD_2'],row['GSD_3']))
    

    f.write(" 0") 


# In[ ]:




