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

