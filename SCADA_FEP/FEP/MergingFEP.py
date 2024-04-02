import pandas as pd
import os
import datetime
file_names = [
    'CHANNEL.dat',
    'RTU_DATA.dat',
    'CHANNEL_GROUP.dat',
    'RTU_DEFN.dat',
    'CHANNEL_GROUP_DEFN.dat',
    'RTU_CONTROL.dat'
]


#read and concatenate each file
compiled_content = ''
for file_name in file_names:
    with open(file_name, 'r') as file:
        content = file.read()
        compiled_content += content + '\n'

now = datetime.datetime.now()
date_string = now.strftime("%d%m%y")


final_file_name = f'FEP_Compiled_{date_string}.dat'


compiled_content = '32 FEP.DB\n' + compiled_content


compiled_content += '0'


#final_file_name = 'FEP_Compiled_15-Jan.dat'
with open(final_file_name, 'w') as final_file:
    final_file.write(compiled_content)

print(f"File {final_file_name} created.")
