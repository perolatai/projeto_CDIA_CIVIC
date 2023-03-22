import mysql.connector
from settings import *

mydb = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

mycursor = mydb.cursor()

import pandas as pd

arquivo = 'exemplodb'

df = pd.read_csv(arquivo + '.tsv', sep='\t')

df.fillna('o', inplace=True)

tam = len(df.dtypes)
headers = df.columns
dtypes_list = df.dtypes.tolist()

mycursor.execute("CREATE TABLE " + arquivo + " (id INT AUTO_INCREMENT PRIMARY KEY)")

for i in range(0, tam):
    if dtypes_list[i] == 'int64':
        mycursor.execute("ALTER TABLE " + arquivo + " ADD COLUMN " + headers[i] + " INT")
    elif dtypes_list[i] == 'float64':
        mycursor.execute("ALTER TABLE " + arquivo + " ADD COLUMN " + headers[i] + " FLOAT")
    elif dtypes_list[i] == 'object':
        if '_id' in headers[i]:
            mycursor.execute("ALTER TABLE " + arquivo + " ADD COLUMN " + headers[i] + " INT")
        else:
            mycursor.execute("ALTER TABLE " + arquivo + " ADD COLUMN " + headers[i] + " VARCHAR(255)")
    elif dtypes_list[i] == 'bool':
        mycursor.execute("ALTER TABLE " + arquivo + " ADD COLUMN " + headers[i] + " BOOLEAN")
    else:
        print('Pronto!')

for i,row in df.iterrows():
    sql = "INSERT INTO exemplodb VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    row = pd.concat([pd.Series([0]), row])
    val = tuple(row)
    mycursor.execute(sql, val)
    mydb.commit()
    print(i)