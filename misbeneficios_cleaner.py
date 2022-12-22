import pandas as pd
import numpy as np
import sqlite3
import os
from datetime import datetime

date = datetime.now().strftime("%d_%m_%Y")

# abre el archivo scrapeado del dia
# si quiero li,iar un dia especifico usar el comentado
#df = pd.read_csv(f"C:/Users/cabre/Desktop/scraping/misbeneficios/data/raw/misbeneficios_08_11_2022.csv")
df = pd.read_csv(f"C:/Users/cabre/Desktop/scraping/misbeneficios/data/raw/misbeneficios_{date}.csv")
print(df)

# formatea las columnas
df['name'] = df['name'].str.replace(r'\n', '').str.strip()
df['price'] = df['price'].str.replace('"','')
df['date'] = datetime.now().strftime("%d-%m-%Y")
#df['date'] = '08-11-2022'
df['sitio'] = 'misbeneficios'
df.drop_duplicates(keep='first', inplace=True)

# guarda la data clean del dia en un .csv
# si quiero li,iar un dia especifico usar el comentado
#df.to_csv(f"C:/Users/cabre/Desktop/scraping/misbeneficios/data/clean/misbeneficios_08_11_2022_clean.csv", index=False)
df.to_csv(f"C:/Users/cabre/Desktop/scraping/misbeneficios/data/clean/misbeneficios_{date}_clean.csv", index=False)

#conectar con sql
conn = sqlite3.connect('misbeneficios_database.db')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS products (name text, price number, date number, sitio text)')
conn.commit()

df.to_sql('products', conn, if_exists='append', index = False)

for row in c.fetchall():
    print (row)
