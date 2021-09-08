# importación de librerías y módulos
import pandas as pd # Manejo de los datos
import numpy as np # Posibles operaciones
from bs4 import BeautifulSoup as soup # Web Scraping
from urllib.request import urlopen
import csv
from os.path import exists


# URL que vamos a inspeccionar
url_pagina = 'https://www.bolsamadrid.es/esp/aspx/Mercados/Precios.aspx?indice=ESI100000000'

# Abrimos la página, y guardamos el html
mi_cliente = urlopen(url_pagina)
pag_html = mi_cliente.read()
mi_cliente.close()

# Generamos la página de BeautifulSoup
pag_soup = soup(pag_html, "html.parser")

# Buscamos la tabla que queremos guardar
tabla = pag_soup.find("table", attrs={"id": "ctl00_Contenido_tblAcciones"})

# Recogemos las filas, identificadas por la etiqueta <tr>
filas = tabla.find_all("tr")

# Utilizamos la primera fila para recoger los nombres de las
# columnas
headers = []
for nombre in filas[0].find_all("th"):
    headers.append(nombre.text)
    
# Y retiramos esta fila de la lista de acciones
filas.pop(0)

# Trabajamos el .csv contenedor.
nombre_arx = "ibex_35.csv"

if not exists(nombre_arx):
	# Si no existe, creamos el archivo e iniciamos la cabecera para que pandas
	# pueda leerlo
    f = open(nombre_arx, "a")
    write_csv = csv.writer(f)
    write_csv.writerow(headers)
    f.close()
    df = pd.read_csv(nombre_arx)
else:
	# Si ya existe, simplemente lo pasamos a un DataFrame de pandas
    df = pd.read_csv(nombre_arx)


# Volcamos la info de las acciones en el df (añadiendola)
for fila in filas:
    
    # INTERESANTE! Convertimos dos listas en un dict
    info = {headers[i]: fila.find_all("td")[i].text for i in range(len(headers))}
    df = df.append(info, ignore_index=True)


# Limpiamos registros de la misma acción y el mismo día 
# manteniendo la más actual
df = df.drop_duplicates(['Nombre', 'Fecha'], keep='last')


# Lo escribimos al csv existente.
df.to_csv(r"ibex_35.csv", index = False)