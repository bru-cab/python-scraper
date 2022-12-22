import sqlite3
import pandas as pd
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from email.message import EmailMessage

date = datetime.now().strftime("%d_%m_%Y")
conn = sqlite3.connect('misbeneficios_database.db')

#descargar data de hoy
sql_query_today = pd.read_sql_query ('''
                               SELECT
                               *
                               FROM products
                               WHERE date in (strftime('%d-%m-%Y', 'now', 'localtime'));
                               ''', conn)
#sql_query_today = pd.read_sql_query ('''
#                               SELECT
#                               *
#                               FROM products
#                               WHERE date in ('19-11-2022');
#                               ''', conn)


data_0 = pd.DataFrame(sql_query_today, columns = ['name', 'price', 'date', 'sitio'])
data_0.rename(columns={'price': 'price_0', 'date': 'date_0', 'sitio': 'sitio_0'}, inplace=True)
print("data_0")
print(data_0)

for ind in data_0.index:
    sql_query_last = pd.read_sql_query ('''
                               SELECT t1.name as name, t1.price as price, t1.sitio as sitio, max(t2.date) as date_last
                               FROM products t1
                                 JOIN products t2 ON t1.name = t2.name AND t2.date < t1.date
                               GROUP BY t1.name;
                               ''', conn)

#    sql_query_last = pd.read_sql_query ('''
#                               SELECT
#                               name as name, price as price, sitio as sitio, date as date_last
#                               FROM products
#                               WHERE date in ('18-11-2022');
#                               ''', conn)

data_t = pd.DataFrame(sql_query_last, columns = ['name', 'price', 'date_last', 'sitio'])
data_t.rename(columns={'price': 'price_t', 'date_last': 'date_t', 'sitio': 'sitio_t'}, inplace=True)
print("data_t")
print(data_t)

compare = pd.merge(data_0, data_t)
print('compare')
print(compare)
compare.to_csv(f"C:/Users/cabre/Desktop/scraping/misbeneficios/data/price_changes/misbeneficios_{date}_compare_19.csv", index=False)


price_changes=compare.loc[compare['price_0'] != compare['price_t']]
price_changes.to_csv(f"C:/Users/cabre/Desktop/scraping/misbeneficios/data/price_changes/misbeneficios_{date}_pricechanges.csv", index=False)
print("price_changes")
print(price_changes)
#price_changes=compare.loc[compare['date_t'] != '11-11-2022']
cantidad_cambios=(len(price_changes.index))

# buscar productos de interes:
products_interes = ['Smart TV Samsung Frame 55” UHD 4K SAQN55LS03BA','Smart TV LG 55" OLED OLED55C2PSA','Smart TV Sony 55" 4K KD-55X80J']
price_changes_interes=price_changes[price_changes['name'].isin(products_interes)]
price_changes_interes.to_csv(f"C:/Users/cabre/Desktop/scraping/misbeneficios/data/price_changes/misbeneficios_{date}_price_changes_interes.csv", index=False)
print('price_changes_interes')
print(price_changes_interes)
cantidad_cambios_interes=(len(price_changes_interes.index))

# buscar productos de similares a los de interes:
price_changes_interes_simil=price_changes[price_changes['name'].str.contains("Smart")==True]
print('price_changes_interes_simil')
print(price_changes_interes_simil)
price_changes_interes_simil.to_csv(f"C:/Users/cabre/Desktop/scraping/misbeneficios/data/price_changes/misbeneficios_{date}_pricechanges_price_changes_interes_simil.csv", index=False)
print('price_changes_interes_simil')
print(price_changes_interes_simil)
cantidad_cambios_interes_simil=(len(price_changes_interes.index))

# create email para enviar flags de reporte
email_from = '---'
password = '---'
email_to = '---'

# Generate today's date to be included in the email Subject
date_str = pd.Timestamp.today().strftime('%Y-%m-%d')

# Create a MIMEMultipart class, and set up the From, To, Subject fields
email_message = MIMEMultipart()
email_message['From'] = email_from
email_message['To'] = email_to
email_message['Subject'] = f'Report email - {date_str}'

# Define the HTML document
body = """\
<html>
  <head></head>
  <body>
<p>Reporte diario:<br>
<br>
Cantidad de productos al dia de hoy que cambiaron de precio: """ + str(cantidad_cambios) + """.<br>
Cantidad de productos de interes al dia de hoy que cambiaron de precio: """ + str(cantidad_cambios_interes) + """.<br>
 {0}
<br>
    </p>
  </body>
</html>
""".format(price_changes_interes_simil.to_html())

# Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
email_message.attach(MIMEText(body, "html"))
# Convert it as a string
email_string = email_message.as_string()

# Connect to the Gmail SMTP server and Send Email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(email_from, password)
    server.sendmail(email_from, email_to, email_string)
