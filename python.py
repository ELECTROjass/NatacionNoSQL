import tkinter as tk
from tkinter import messagebox
import pymongo

# Conexión a MongoDB
MONGO_HOST = "localhost"
MONGO_PUERTO = "27017"
MONGO_URL = f"mongodb://{MONGO_HOST}:{MONGO_PUERTO}/"
MONGO_BASEDATOS = "Competencia"
coleccionNombre = "Deportistas"  # Esta puede cambiar dependiendo de la selección

# Conexión con la base de datos
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

# Función para crear un documento en MongoDB


def CrearColeccion(db, collection):
    coleccion = db[coleccionNombre]
    resultado = coleccion.insert_one(collection)
    return resultado.inserted_id

# Función para ver los documentos en MongoDB


def VerColeccion(db):
    coleccion = db[coleccionNombre]
    return [doc for doc in coleccion.find()]

# Función para actualizar un documento en MongoDB


def ActualizarColeccion(db, filtro, nuevos_valores):
    coleccion = db[coleccionNombre]
    resultado = coleccion.update_one(filtro, {"$set": nuevos_valores})
    return resultado.modified_count

# Función para eliminar un documento en MongoDB


def EliminarColeccion(db, filtro):
    coleccion = db[coleccionNombre]
    resultado = coleccion.delete_one(filtro)
    return resultado.deleted_count


# Interfaz gráfica con Tkinter
ventana = tk.Tk()
ventana.title("Editor de Colecciones")

# Variables globales
campo_entries = []
coleccion_var = tk.StringVar(value=coleccionNombre)

# Actualizar campos en función de la colección seleccionada


def actualizar_campos():
    global campo_entries
    for entry in campo_entries:
        entry["label"].destroy()
        entry["entry"].destroy()
    campo_entries = []

    coleccion = coleccion_var.get()
    if coleccion == "Arbitros":
        datos = {"nombre": "", "apellido": "",
                 "edad": "", "numeroDePartidosTomados": ""}
    elif coleccion == "Entrenadores":
        datos = {"nombre": "", "apellido": "",
                 "edad": "", "departamento": "", "equipo": ""}
    elif coleccion == "Deportistas":
        datos = {"nombre": "", "apellido": "", "edad": "",
                 "departamento": "", "entrenador": "", "equipo": ""}

    row = 1
    for campo, valor in datos.items():
        label = tk.Label(ventana, text=campo.capitalize() + ":")
        label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        entry = tk.Entry(ventana)
        entry.grid(row=row, column=1, padx=10, pady=5)
        entry.insert(0, valor)
        campo_entries.append({"label": label, "entry": entry, "campo": campo})
        row += 1

# Guardar datos en MongoDB


def guardar_datos():
    coleccion = coleccion_var.get()
    datos = {}
    for entry in campo_entries:
        campo = entry["campo"]
        nuevo_valor = entry["entry"].get()
        datos[campo] = nuevo_valor

    # Guardar en MongoDB
    insert_id = CrearColeccion(db, datos)
    messagebox.showinfo(
        "Guardado", f"Datos guardados correctamente con ID: {insert_id}")

# Ver documentos de la colección


def ver_coleccion():
    documentos = VerColeccion(db)
    print(f"Documentos en la colección {coleccion_var.get()}:")
    for doc in documentos:
        print(doc)

# Eliminar documentos de la colección


def eliminar_documento():
    datos_eliminar = {}
    for entry in campo_entries:
        campo = entry["campo"]
        nuevo_valor = entry["entry"].get()
        datos_eliminar[campo] = nuevo_valor

    documentos_eliminados = EliminarColeccion(db, datos_eliminar)
    messagebox.showinfo(
        "Eliminado", f"Documentos eliminados: {documentos_eliminados}")

# Actualizar documentos de la colección


def actualizar_documento():
    datos_actualizar = {}
    for entry in campo_entries:
        campo = entry["campo"]
        nuevo_valor = entry["entry"].get()
        datos_actualizar[campo] = nuevo_valor

    filtro = {"nombre": datos_actualizar["nombre"]}  # ejemplo de filtro
    modificados = ActualizarColeccion(db, filtro, datos_actualizar)
    messagebox.showinfo(
        "Actualización", f"Documentos actualizados: {modificados}")


# Crear la interfaz
tk.Label(ventana, text="Seleccionar colección:").grid(
    row=0, column=0, padx=10, pady=5)
coleccion_menu = tk.OptionMenu(ventana, coleccion_var, "Arbitros",
                               "Entrenadores", "Deportistas", command=lambda _: actualizar_campos())
coleccion_menu.grid(row=0, column=1, padx=10, pady=5)

# Botones de operaciones
tk.Button(ventana, text="Guardar Datos", command=guardar_datos).grid(
    row=100, column=0, columnspan=2, pady=10)
tk.Button(ventana, text="Ver Colección", command=ver_coleccion).grid(
    row=101, column=0, columnspan=2, pady=10)
tk.Button(ventana, text="Eliminar Documento", command=eliminar_documento).grid(
    row=102, column=0, columnspan=2, pady=10)
tk.Button(ventana, text="Actualizar Documento", command=actualizar_documento).grid(
    row=103, column=0, columnspan=2, pady=10)

# Inicializar campos
actualizar_campos()

# Ejecutar la interfaz
ventana.mainloop()
