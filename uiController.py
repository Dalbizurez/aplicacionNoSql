from PyQt6 import QtWidgets, QtCore
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from articuloDialog import Ui_Dialog 
from mainWindow import Ui_MainWindow

from conexion import getArticulos, getUsuario

# Configuración de conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")  
db = client["articulos"]
coleccion_articulo = db["articulo"]

class InsertDialog(QtWidgets.QDialog, Ui_Dialog):
    articulo_guardado = QtCore.pyqtSignal()

    def __init__(self, parent=None, usuario:str=""):
        super().__init__(parent)
        self.setupUi(self)
        self.btn_guardar_articulo.clicked.connect(lambda:self.insertar_articulo(usuario))
        
    def obtener_datos(self):
        titulo = self.txt_titulo.text()
        contenido = self.txtContenido.toPlainText()
        return titulo, contenido

    def insertar_articulo(self, usuario:str):
        titulo, contenido = self.obtener_datos()

        usuario = getUsuario(usuario)
        id_estudiante = usuario.get("id", "N/A")
        nombre_estudiante = usuario.get("nombre", "N/A")

        
        articulo = {
            "_id": ObjectId(), 
            "titulo": titulo,
            "contenido": contenido,
            "id_estudiante": id_estudiante,
            "nombre_estudiante": nombre_estudiante,
            "id_administrador": "N/A",
            "nombre_administrador": "N/A",
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "comentarios": []
        }

        resultado = coleccion_articulo.insert_one(articulo)
        
        if resultado.inserted_id:
            print("Artículo insertado correctamente:", resultado.inserted_id)
            QtWidgets.QMessageBox.information(self, "Éxito", "El artículo ha sido guardado.")
            self.articulo_guardado.emit()
            self.accept()
        else:
            print("Error al insertar el artículo.")
            QtWidgets.QMessageBox.warning(self, "Error", "Hubo un problema al guardar el artículo.")

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    usuario = ""

    def __init__(self, id_estudiante:str):
        super().__init__()
        self.setupUi(self)
        
        self.btn_articulo.clicked.connect(self.abrir_dialogo)
        self.cargar_articulos()  

#        self.insertDialog = InsertDialog()
#        
#        self.insertDialog.btn_guardar_articulo.clicked.connect(lambda:self.cargar_articulos(self.usuario))
#        self.insertDialog.btn_guardar_articulo.clicked.connect(lambda:self.mostrar_usuario)

        self.tbl_articulos.setColumnCount(5)
        self.tbl_articulos.setHorizontalHeaderLabels(["ID", "Título", "Contenido", "Fecha", "Nombre Administrador"]) 

        self.usuario = id_estudiante
        self.mostrar_usuario()

        self.cargar_articulos()

    def abrir_dialogo(self):
        dialogo = InsertDialog(self, self.usuario)
        dialogo.articulo_guardado.connect(self.cargar_articulos)
        dialogo.articulo_guardado.connect(self.mostrar_usuario)
        dialogo.exec()

    def mostrar_usuario(self):
        usuario = getUsuario(self.usuario)
        if usuario:
            nombre = usuario.get("nombre", "N/A")
            self.lbl_welcome.setText(f"Bienvenido, {nombre}")
        else:
            self.lbl_welcome.setText("Bienvenido N/A")
            self.lb_numero_articulos.setText("0")
        self.lb_numero_articulos.setText(str(coleccion_articulo.count_documents({"id_estudiante":self.usuario})))
        self.lbl_usuario.setText(f"Usuario: {self.usuario}")

    def cargar_articulos(self):
        self.tbl_articulos.setRowCount(0)
        articulos = getArticulos(self.usuario)

        for row_index, articulo in enumerate(articulos):
            self.tbl_articulos.insertRow(row_index)
            id_value = articulo.get("id", "N/A")
            titulo_value = articulo.get("titulo", "Sin Título")
            contenido_value = articulo.get("contenido", "Sin Contenido")
            fecha_value = articulo.get("fecha", "Fecha No Disponible")
            nombre_administrador_value = articulo.get("nombre_administrador", "Sin Administrador")  
            
            # Insertar los valores en las celdas de la tabla
            self.tbl_articulos.setItem(row_index, 0, QtWidgets.QTableWidgetItem(id_value))
            self.tbl_articulos.setItem(row_index, 1, QtWidgets.QTableWidgetItem(titulo_value))
            self.tbl_articulos.setItem(row_index, 2, QtWidgets.QTableWidgetItem(contenido_value))
            self.tbl_articulos.setItem(row_index, 3, QtWidgets.QTableWidgetItem(fecha_value))
            self.tbl_articulos.setItem(row_index, 4, QtWidgets.QTableWidgetItem(nombre_administrador_value))  

def run():
    app = QtWidgets.QApplication([])
    ventana = MainWindow(id_estudiante="estudiante001")
    ventana.show()
    app.exec()

if __name__ == "__main__":
    run()