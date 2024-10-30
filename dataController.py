import datetime

def saveArticulo(titulo, texto, fecha=datetime.datetime.now().date()):
    # Guardar articulo en base de datos
    print(titulo, texto, fecha)

def getArticulos():
    # Obtener articulos de la base de datos
    # Un arreglo de articulos con titulo, contenido, fecha y usuario que lo aprobo
    pass

def getUsuario(usrId):
    # Obtener usuario de la base de datos
    # Retornar nombreDeUsuario, y los articulos que ha escrito
    pass

