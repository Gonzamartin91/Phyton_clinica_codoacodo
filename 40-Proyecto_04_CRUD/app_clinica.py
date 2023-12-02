# -------------------------------------------------------
# Importamos extenciones
# -------------------------------------------------------
import mysql.connector
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import time


# -------------------------------------------------------
# Definimos la clase BaseAfiliados
# -------------------------------------------------------
app = Flask(__name__)
CORS(app)                   #Esto habilita CORS para todas las rutas

# -------------------------------------------------------

class BaseAfiliados:
    def __init__(self, host, user, password, database):         #Inicializador con los parametros de ingreso a la BBDD
        self.conn = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database = database
        )
        self.cursor = self.conn.cursor()

        #intentamos seleccionar la BBDD
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
        #Si la BBDD no existe la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CRATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        #Una vez establecida la BBDD creamos SI NO EXISTE la tabla
        self.cursor.execute('''create table if not exists afiliados(
                            dni INT,
                            nombre VARCHAR(50),
                            apellido VARCHAR(50),
                            fecha_nac VARCHAR(10),
                            plan VARCHAR(20),
                            foto VARCHAR(255),
                            prestador INT(3))''')                       
        self.conn.commit()                                              #Le damos confirmacion a la sentencia SQL

        #Cerramos el cursor inicial y abrimos uno nuevo con el parámetro de dictionary = True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

    # ---------------------------------------------------------
    # Metodo para consultar un afiliado a partir de su dni
    # ---------------------------------------------------------
    def consultar_afiliado(self, dni):
        self.cursor.execute(f"SELECT * FROM afiliados WHERE dni = {dni}")   #Busca en la BBD si esta ese DNI)
        return self.cursor.fetchone()                                       #Regresa solo ese afiliado encontrado


    # -------------------------------------------------------
    # Metodo para agregar un afiliado
    # -------------------------------------------------------
    """
    Agregar un afiliado al arreglo de afiliados

    Parámetros:
    - dni: int, dni numérico del afiliado.
    - nombre: str, nombre del afiliado.
    - apellido: str, apellido del afiliado.
    - fecha_nac: date, fecha_nac del afiliado.
    - plan: str, plan del afiliado.
    - foto: str, nombre de la foto del afiliado.
    - prestador: int, dni del prestador.

    Retorna:
    - boolean: True si agrego el afiliado o False si ese afiliado ya existe con el mismo dni
    """


    def agregar_afiliado(self, dni, nombre, apellido, fecha_nac, plan, foto, prestador):
        #Verificamos si el afiliado ya existe en la BBDD
        self.cursor.execute(f"SELECT * FROM afiliados WHERE dni = {dni}")   #Busca en la BBD si esta ese DNI
        afiliado_existe = self.cursor.fetchone()                            #Si el DNI existe lo guarda en variable afiliado_existe

        if afiliado_existe:                                                 #Si existe manda este mensaje
            print(f"AFILIADO {dni} YA EXISTE EN LOS REGISTROS!")
            return False
        
        sql = f"INSERT INTO afiliados \
                (dni, nombre, apellido, fecha_nac, plan, foto, prestador) \
                VALUES \
                ({dni}, '{nombre}', '{apellido}', '{fecha_nac}', '{plan}', '{foto}', {prestador})"  #Si no existe lo agrega a la tabla
        
        self.cursor.execute(sql)                                            #El cursor ejecuta el comando SQL
        self.conn.commit()                                                  #Confirmo la ejecucion
        return True


    # -------------------------------------------------------
    # Metodo para obtener listado de afiliados por pantalla
    # -------------------------------------------------------
    def listar_afiliados(self):
        self.cursor.execute("SELECT * FROM afiliados")
        afiliados = self.cursor.fetchall()
        return afiliados


    # ----------------------------------------------------------------------
    # Metodo para modificar los datos de un afiliado a partir de su dni
    # ----------------------------------------------------------------------
    def modificar_afiliado(self, dni, nuevo_nombre, nuevo_apellido, nueva_fecha_nac, nuevo_plan, nueva_foto, nuevo_prestador):
        sql = "UPDATE afiliados SET nombre = %s, apellido = %s, fecha_nac = %s, plan = %s, foto = %s, prestador = %s WHERE dni = %s"
        valores = (nuevo_nombre, nuevo_apellido, nueva_fecha_nac, nuevo_plan, nueva_foto, nuevo_prestador, dni)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0


    # ---------------------------------------------------------------------
    # Metodo para eliminar los datos de un afiliado a partir de su dni
    # ---------------------------------------------------------------------
    def eliminar_afiliado(self, dni):
        # Eliminamos un producto de la tabla a partir de su código
        self.cursor.execute(f"DELETE FROM afiliados WHERE dni = {dni}")
        self.conn.commit()
        return self.cursor.rowcount > 0


# --------------------------------------------------------------------------------------------------------------------------
# ************************************   Programa Principal   **************************************************************
# --------------------------------------------------------------------------------------------------------------------------
#Nos conectamos a la BBDD
BaseAfiliados = BaseAfiliados(host='localhost', user='root', password='', database='miapp')

"""
# Agregamos afiliados a la tabla afiliados de la BBDD miapp
BaseAfiliados.agregar_afiliado(25542165, "Mariano", "Saratoga", "19/03/1974", "ORO", "25542165.jpg", 101)
BaseAfiliados.agregar_afiliado(35653889, "Amanda", "Tencara", "25/05/1995", "PLATA", "35653889.jpg", 103)
BaseAfiliados.agregar_afiliado(35653889, "Albertito", "Argento", "08/04/1997", "PLATA", "35653889.jpg", 102)
BaseAfiliados.agregar_afiliado(28332779, "Marcela", "Encuentro", "14/08/1980", "BRONCE", "28332779.jpg", 102)
BaseAfiliados.agregar_afiliado(4637999, "Jorgito", "Devoto", "14/03/1943", "Platino", "4637999.jpg", 105)
BaseAfiliados.agregar_afiliado(37199883, "Macarena", "Alegria", "01/09/2000", "PLATA", "37199883.jpg", 101)
"""

# Carpeta para guardar las imagenes.
RUTA_DESTINO = './static/imagenes/'


#--------------------------------------------------------------------
# Agregar un afiliado
#--------------------------------------------------------------------
@app.route("/afiliados", methods=["POST"])
def agregar_afiliado():                     #Capturo los datos que vienen del HTML
    dni = request.form['dni']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    fecha_nac = request.form['fecha_nac']
    plan = request.form['plan']
    foto = request.files['foto']
    prestador = request.form['prestador']  
    nombre_imagen=""

    # Me aseguro que el producto exista
    afiliado = BaseAfiliados.consultar_afiliado(dni)
    if not afiliado: # Si no existe el afiliado...
        # Genero el nombre de la imagen
        nombre_imagen = secure_filename(foto.filename) #Chequea el nombre del archivo de la imagen, asegurándose de que sea seguro para guardar en el sistema de archivos
        nombre_base, extension = os.path.splitext(nombre_imagen) #Separa el nombre del archivo de su extensión.
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}" #Genera un nuevo nombre para la imagen usando un timestamp, para evitar sobreescrituras y conflictos de nombres.
        
        #Se agrega el producto a la base de datos
        if  BaseAfiliados.agregar_afiliado(dni, nombre, apellido, fecha_nac, plan, nombre_imagen, prestador):
            foto.save(os.path.join(RUTA_DESTINO, nombre_imagen))

            #Si el afiliado se agrega con éxito, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 201 (Creado).
            return jsonify({"mensaje": "Afiliado AGREAGADO CORRECTAMENTE!!", "imagen": nombre_imagen}), 201
        else:
            #Si el producto no se puede agregar, se devuelve una respuesta JSON con un mensaje de error y un código de estado HTTP 500 (Internal Server Error).
            return jsonify({"mensaje": "ERROR al agregar el afiliado!!"}), 500

    else:
        #Si el producto ya existe (basado en el código), se devuelve una respuesta JSON con un mensaje de error y un código de estado HTTP 400 (Solicitud Incorrecta).
        return jsonify({"mensaje": "EL afiliado YA EXISTE en el padron!!"}), 400


#--------------------------------------------------------------------
# Modificar un afiliado según su DNI
#--------------------------------------------------------------------
@app.route("/afiliados/<int:dni>", methods=["PUT"])
#La ruta Flask /productos/<int:codigo> con el método HTTP PUT está diseñada para actualizar la información de un producto existente en la base de datos, identificado por su código.
#La función modificar_producto se asocia con esta URL y es invocada cuando se realiza una solicitud PUT a /productos/ seguido de un número (el código del producto).
def modificar_afiliado(dni):
    #Se recuperan los nuevos datos del formulario
    nuevo_nombre = request.form.get("nombre")
    nuevo_apellido = request.form.get("apellido")
    nueva_fecha_nac = request.form.get("fecha_nac")
    nuevo_plan = request.form.get("plan")
    nuevo_prestador = request.form.get("prestador")
    nueva_foto = request.files['foto']

    # Procesamiento de la imagen
    nombre_imagen = secure_filename(nueva_foto.filename) #Chequea el nombre del archivo de la imagen, asegurándose de que sea seguro para guardar en el sistema de archivos
    nombre_base, extension = os.path.splitext(nombre_imagen) #Separa el nombre del archivo de su extensión.
    nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}" #Genera un nuevo nombre para la imagen usando un timestamp, para evitar sobreescrituras y conflictos de nombres.

    # Busco el producto guardado
    afiliado = afiliado = BaseAfiliados.consultar_afiliado(dni)
    if afiliado: # Si existe el producto...
        imagen_vieja = afiliado["foto"]
        # Armo la ruta a la imagen
        ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

        # Y si existe la borro.
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)
    
    # Se llama al método modificar_producto pasando el codigo del producto y los nuevos datos.
    if BaseAfiliados.modificar_afiliado(dni, nuevo_nombre, nuevo_apellido, nueva_fecha_nac, nuevo_plan, nombre_imagen, nuevo_prestador):
        #La imagen se guarda en el servidor.
        nueva_foto.save(os.path.join(RUTA_DESTINO, nombre_imagen))

        #Si la actualización es exitosa, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 200 (OK).
        return jsonify({"mensaje": "Afiliado MODIFICADO EXITOSAMENTE!! 001"}), 200
    else:
        #Si el producto no se encuentra (por ejemplo, si no hay ningún producto con el código dado), se devuelve un mensaje de error con un código de estado HTTP 404 (No Encontrado).
        return jsonify({"mensaje": "Afiliado NO ENCONTRADO!! 002"}), 403


#--------------------------------------------------------------------
# Listar todos los afiliados
#--------------------------------------------------------------------
#Esta sentencia es la que se usa con FLASK para poder relacionar la BBDD con HTML y LISTAR TODOS los afiliados
@app.route("/afiliados", methods=["GET"])       #GET es el metodo para obtener respuestas a las peticiones
def listar_afiliados():
    afiliados = BaseAfiliados.listar_afiliados()
    return jsonify(afiliados)


#--------------------------------------------------------------------
# Mostrar un solo afiliado según su DNI
#--------------------------------------------------------------------
#Esta sentencia es la que se usa con FLASK para poder relacionar la BBDD con HTML y CONSULTAR afiliados por DNI
@app.route("/afiliados/<int:dni>", methods=["GET"])
def consultar_afiliado(dni):
    afiliado = BaseAfiliados.consultar_afiliado(dni)
    if afiliado:
        return jsonify(afiliado), 201
    else:
        return "Afiliado NO ENCONTRADO!!", 404


#--------------------------------------------------------------------
# Eliminar un afiliado según su DNI
#--------------------------------------------------------------------
@app.route("/afiliados/<int:dni>", methods=["DELETE"])
#La ruta Flask /productos/<int:codigo> con el método HTTP DELETE está diseñada para eliminar un producto específico de la base de datos, utilizando su código como identificador.
#La función eliminar_producto se asocia con esta URL y es llamada cuando se realiza una solicitud DELETE a /productos/ seguido de un número (el código del producto).
def eliminar_afiliado(dni):
    # Busco el producto en la base de datos
    producto = BaseAfiliados.consultar_afiliado(dni)
    if producto: # Si el producto existe, verifica si hay una imagen asociada en el servidor.
        imagen_vieja = producto["foto"]
        # Armo la ruta a la imagen
        ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

        # Y si existe, la elimina del sistema de archivos.
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

        # Luego, elimina el producto del catálogo
        if BaseAfiliados.eliminar_afiliado(dni):
            #Si el producto se elimina correctamente, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 200 (OK).
            return jsonify({"mensaje": "Afiliado ELIMINADO!!"}), 200
        else:
            #Si ocurre un error durante la eliminación (por ejemplo, si el producto no se puede eliminar de la base de datos por alguna razón), se devuelve un mensaje de error con un código de estado HTTP 500 (Error Interno del Servidor).
            return jsonify({"mensaje": "ERROR al eliminar afiliado!!"}), 500
    else:
        #Si el producto no se encuentra (por ejemplo, si no existe un producto con el codigo proporcionado), se devuelve un mensaje de error con un código de estado HTTP 404 (No Encontrado). 
        return jsonify({"mensaje": "Afiliado NO ENCONTRADO!!"}), 404


# --------------------------------------------------------------------------------------------------------------------------
#Esto es para levantar el servicio y se pueda ejecutar
if __name__ == "__main__":
    app.run(debug=True)


"""
#Consultamos una búsqueda de afiliado por código
dni_afiliado = int(input("Ingrese el DNI del afiliado :"))
afiliado = BaseAfiliados.consultar_afiliado(dni_afiliado)
if afiliado:
    print(f"Afiliado encontrado: {afiliado['dni']} - {afiliado['nombre']} {afiliado['apellido']}")
else:
    print(f"Afiliado {dni_afiliado} NO ENCONTRADO!!")


#Modificamos un registro de afiliado por su DNI
BaseAfiliados.modificar_afiliado(37199883, "Macarena", "Tristeza", "01/09/2000", "Bronce", "37199883.jpg", 103)


#Eliminamos un afiliado por DNI
BaseAfiliados.eliminar_afiliado(35653889)
"""