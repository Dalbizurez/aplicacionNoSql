from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
    
    client.admin.command("ping")
    print("Conexión exitosa a MongoDB")
    
    db = client["articulos"]
    collection = db["articulo"]

    documentos = collection.find_one()  
    if documentos:
        print("Conexión y acceso a la colección exitosa.")
    else:
        print("Conexión exitosa, pero la colección está vacía.")
        
except ConnectionFailure:
    print("Error: No se pudo conectar a MongoDB")


def getUsuario(id_estudiante:str):
    collection = db["estudiante"]
    return collection.find_one({"id":id_estudiante})

def getArticulos(id_estudiante:str):
    return collection.find({"id_estudiante":id_estudiante})