import pymongo

MONGO_HOST = "localhost"
MONGO_PUERTO = "27017"
MONGO_URL = f"mongodb://{MONGO_HOST}:{MONGO_PUERTO}/"
MONGO_BASEDATOS = "Competencia"

# SELECCIONAR COLECCION
coleccionNombre = "Deportistas"

# ARBITROS
if coleccionNombre == "Arbitros":
    datos = {"nombre": "i", "apellido": "ii",
             "edad": "iii", "numeroDePartidosTomados": "iiii"}
# ENTRENADORES
elif coleccionNombre == "Entrenadores":
    datos = {"nombre": "IIII", "apellido": "IIIII",
             "edad": "IIIIII", "departamento": "IIIIIII", "equipo": "IIIIIIII"}
# DEPORTISTAS
elif coleccionNombre == "Deportistas":
    datos = {"nombre": "ll", "apellido": "lll",
             "edad": "llll", "departamento": "lllll", "entrenador": "lllllll", "equipo": "llllllll"}

try:
    cliente = pymongo.MongoClient(MONGO_URL, serverSelectionTimeoutMS=2000)
    cliente.server_info()
    print("Conexión exitosa a MongoDB")
except pymongo.errors.ServerSelectionTimeoutError as error_tiempo:
    print("Error de conexión: Tiempo excedido")  # CONECTADO
    exit()
except pymongo.errors.ConnectionFailure as error_conexion:
    print("Error de conexión: Fallo al conectarse")  # ERROR
    exit()

db = cliente[MONGO_BASEDATOS]

# CREAR LA COLECCION


def CrearColeccion(db, equipo):
    coleccion = db[coleccionNombre]
    resultado = coleccion.insert_one(equipo)
    print(f"Coleccion ID: {resultado.inserted_id}")

# VER LA COLECCION


def VerColeccion(db):
    coleccion = db[coleccionNombre]
    print(coleccionNombre + " en la colección:")
    for equipo in coleccion.find():
        print(equipo)

# ELIMINAR UNA COLECCION


def EliminarColeccion(db, filtro):
    coleccion = db[coleccionNombre]
    # Cambia a delete_many si quieres eliminar múltiples
    resultado = coleccion.delete_one(filtro)
    print(f"Documentos eliminados: {resultado.deleted_count}")

# ACTUALIZAR UNA COLECCION


def ActualizarColeccion(db, filtro, nuevos_valores):
    coleccion = db[coleccionNombre]
    # Cambia a update_many si actualizas múltiples
    resultado = coleccion.update_one(filtro, {"$set": nuevos_valores})
    print(f"Documentos actualizados: {resultado.modified_count}")


if __name__ == "__main__":
    # CREAR
    CrearColeccion(db, datos)

    VerColeccion(db)

    # ACTUALIZAR
    # actualizarDatos = {"nombre": "ll", "apellido": "lll",
    #         "edad": "llll", "departamento": "lllll", "entrenador": "lllllll", "equipo": "llllllll"}
    # ActualizarColeccion(db, actualizarDatos, datos)

    # VerColeccion(db)

    # ELIMINAR
    # datosEliminar = {"nombre": "i", "apellido": "ii",
    # "edad": "iii", "numeroDePartidosTomados": "iiii"}
    # EliminarColeccion(db, datosEliminar)

    # VerColeccion(db)
