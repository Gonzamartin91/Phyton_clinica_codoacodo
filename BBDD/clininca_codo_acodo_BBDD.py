#-------------------- LIBRERIAS -------------------------------

#Importamos las librerias para trabajar
import pandas as pd
import sqlite3 as sq3
import sys

#-------------------- CARGA TABLAS A BBDD ----------------------
"""
#Genero coneccion y creo la BBDD clinica_codo_a_codo y la TABLA clinica_cont mediante archivo de EXCEL
#IMPORTANTE ------- SOLO EJECUTA UNA VEZ PARA SUBIR LA BBDD - SI LA TABLA YA EXISTE LA REEMPLAZA!!
#ingresar la ruta el excel con todo y archivo lo mismo con la BD
xls = pd.ExcelFile('contacto_data.xlsx')
db_conn = sq3.connect('clinica_codo_a_codo.db')

df=xls.parse('contacto_data', parse_dates=True) # en este caso "contacto_data" es el nombre de la hoja de excel
df.to_sql('clinica_cont', db_conn, if_exists='replace', index=False) # "clinica_cont" es el nombre de la tabla, no es necesario que tenga el mismo nombre que la hoja de excel

db_conn.commit()
db_conn.close()


#Genero coneccion y creo la TABLA clinica_socio mediante archivo de EXCEL
#IMPORTANTE ------- SOLO EJECUTA UNA VEZ PARA SUBIR LA BBDD - SI LA TABLA YA EXISTE LA REEMPLAZA!!
#ingresar la ruta el excel con todo y archivo lo mismo con la BD
xls = pd.ExcelFile('socio_data.xlsx')
db_conn = sq3.connect('clinica_codo_a_codo.db')

df=xls.parse('socio_data', parse_dates=True) # en este caso "socio_data" es el nombre de la hoja de excel
df.to_sql('clinica_socio', db_conn, if_exists='replace', index=False) # "clinica_socio" es el nombre de la tabla, no es necesario que tenga el mismo nombre que la hoja de excel

db_conn.commit()
db_conn.close()


#Genero coneccion y creo la TABLA clinica_socio mediante archivo de EXCEL
#IMPORTANTE ------- SOLO EJECUTA UNA VEZ PARA SUBIR LA BBDD - SI LA TABLA YA EXISTE LA REEMPLAZA!!
#ingresar la ruta el excel con todo y archivo lo mismo con la BD
xls = pd.ExcelFile('turno_data.xlsx')
db_conn = sq3.connect('clinica_codo_a_codo.db')

df=xls.parse('turno_data', parse_dates=True) # en este caso "turno_data" es el nombre de la hoja de excel
df.to_sql('clinica_turno', db_conn, if_exists='replace', index=False) # "clinica_turno" es el nombre de la tabla, no es necesario que tenga el mismo nombre que la hoja de excel

db_conn.commit()
db_conn.close()
"""

#----------------- GENERACION DE INDICES EN LAS TABLAS ----------
"""
#Genero el INDICE en la tabla clinica_cont si es que no existe
# Esto ya queda dentro de la BBDD NO SERIA necesario correrlo nuevamente
conexion=sq3.connect('clinica_codo_a_codo.db')
cursor=conexion.execute('CREATE UNIQUE INDEX IF NOT EXISTS "id_cont" ON clinica_cont("id_cont")');
conexion.close()

#Genero el INDICE en la tabla clinica_cont si es que no existe
# Esto ya queda dentro de la BBDD NO SERIA necesario correrlo nuevamente
conexion=sq3.connect('clinica_codo_a_codo.db')
cursor=conexion.execute('CREATE UNIQUE INDEX IF NOT EXISTS "id_socio" ON clinica_socio("id_socio")');
conexion.close()

#Genero el INDICE en la tabla clinica_turno si es que no existe
# Esto ya queda dentro de la BBDD NO SERIA necesario correrlo nuevamente
conexion=sq3.connect('clinica_codo_a_codo.db')
cursor=conexion.execute('CREATE UNIQUE INDEX IF NOT EXISTS "id_turno" ON clinica_turno("id_turno")');
conexion.close()
"""
