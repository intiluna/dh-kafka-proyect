import pymongo
from pymongo import MongoClient
from pprint import pprint

# Conexión a MongoDB
try:
    client = MongoClient('mongodb://admin:admin@localhost:27017/')
    db = client["proyecto_inti"]
    maletas_full = db["full_data"]
    print("Conexión a MongoDB establecida correctamente")
except Exception as e:
    print(f"Error al intentar conectar a MongoDB: {e}")
    exit(1)  # Salir si no se puede conectar a MongoDB

# Consultar todos los documentos en la colección "resumen"
try:
    documentos = maletas_full.find()
    print("Documentos en la colección 'full':")
    for doc in documentos:
        pprint(doc)
except Exception as e:
    print(f"Error al consultar los documentos en MongoDB: {e}")
