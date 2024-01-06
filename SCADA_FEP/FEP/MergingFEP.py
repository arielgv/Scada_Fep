#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os


# In[2]:


file_names = [
    'FEP.dat',
    'CHANNEL.dat',
    'RTU_DATA.dat',
    'CHANNEL_GROUP.dat',
    'RTU_DEFN.dat',
    'CHANNEL_GROUP_DEFN.dat'
]

#read and concatenate each file
compiled_content = ''
for file_name in file_names:
    with open(file_name, 'r') as file:
        content = file.read()
        compiled_content += content + '\n'


compiled_content = '32 FEP.DB\n' + compiled_content


compiled_content += '0'


final_file_name = 'FEP_Compiled_5-Jan.dat'
with open(final_file_name, 'w') as final_file:
    final_file.write(compiled_content)

print(f"Archivo {final_file_name} generado correctamente.")


# In[ ]:




