import glob

import mysql.connector
import pandas as pd

from settings import *

mydb = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)
mycursor = mydb.cursor()

arquivos = glob.glob('*.csv')

dataframes = {}
for i, file in enumerate(arquivos):
    df = pd.read_csv(file)
    df.fillna('NaN', inplace=True)
    dataframes[f'df_{i}'] = df

arquivos_sem = []
arquivos_df = []

for arquivo in arquivos:
    arquivo_sem = arquivo[:-4]
    arquivos_sem.append(arquivo_sem)

headers = [df.columns for df in dataframes.values()]
dtypes_list = [df.dtypes.tolist() for df in dataframes.values()]
lens = [len(dtypes_list[i]) for i in range(0, len(dtypes_list))]

chaves_primaria = []
for n, v in enumerate(arquivos_sem):
    chave_primaria = input(f'Qual a chave primária da tabela {v}?')
    mycursor.execute(f"CREATE TABLE {v} ({chave_primaria} INT PRIMARY KEY)")
    chaves_primaria.append(chave_primaria)

for p in range(0, len(arquivos_sem)):
    for i, z in enumerate(headers[p]):
        if chaves_primaria[p] == headers[p][i]:
            pass
        
        elif dtypes_list[p][i] == 'int64':
            mycursor.execute(
                "ALTER TABLE " + arquivos_sem[p] + " ADD COLUMN " + headers[p][i] + " INT")
        elif dtypes_list[p][i] == 'float64':
            mycursor.execute(
                "ALTER TABLE " + arquivos_sem[p] + " ADD COLUMN " + headers[p][i] + " FLOAT")
        elif dtypes_list[p][i] == 'object':
            if '_id' in headers[p][i]:
                mycursor.execute(
                    "ALTER TABLE " + arquivos_sem[p] + " ADD COLUMN " + headers[p][i] + " INT")
            else:
                mycursor.execute(
                    "ALTER TABLE " + arquivos_sem[p] + " ADD COLUMN " + headers[p][i] + " VARCHAR(255)")
        elif dtypes_list[p][i] == 'bool':
            mycursor.execute(
                "ALTER TABLE " + arquivos_sem[p] + " ADD COLUMN " + headers[p][i] + " BOOLEAN")
        else:
            print('Erro')


def get_sql_placeholder_string(num_values):
    return ','.join(['%s'] * num_values)


for j in range(0, len(arquivos_sem)):
    for i, row in dataframes[f'df_{j}'].iterrows():
        placeholder_string = get_sql_placeholder_string(len(row) + 1)
        sql = f"INSERT INTO {arquivos_sem[j]} VALUES ({placeholder_string})"
        row = pd.concat([pd.Series([0]), row])
        val = tuple(row)
        mycursor.execute(sql, val)
        mydb.commit()
        print(i)
    print(arquivos_sem[j])
