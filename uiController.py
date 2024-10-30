from PyQt6 import QtWidgets
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from articuloDialog import Ui_Dialog 
from mainWindow import Ui_MainWindow

# Configuración de conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")  
db = client["articulos"]
coleccion_articulo = db["articulo"]

class InsertDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
       
        self.btn_guardar_articulo.clicked.connect(self.insertar_articulo)

    def insertar_articulo(self):
        titulo = self.txt_titulo.text()
        contenido = self.txtContenido.toPlainText()
        
        articulo = {
            "_id": ObjectId(), 
            "titulo": titulo,
            "contenido": contenido,
            "fecha": datetime.now().strftime("%Y-%m-%d"),  
            "comentarios": []  
        }

        resultado = coleccion_articulo.insert_one(articulo)
        
        if resultado.inserted_id:
            print("Artículo insertado correctamente:", resultado.inserted_id)
            QtWidgets.QMessageBox.information(self, "Éxito", "El artículo ha sido guardado.")
        else:
            print("Error al insertar el artículo.")
            QtWidgets.QMessageBox.warning(self, "Error", "Hubo un problema al guardar el artículo.")

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.btn_articulo.clicked.connect(lambda:self.abrir_dialogo())

        self.insertDialog = InsertDialog()
        
        self.insertDialog.btn_guardar_articulo.clicked.connect(lambda:self.cargar_articulos)

        self.tbl_articulos.setColumnCount(4)
        self.tbl_articulos.setHorizontalHeaderLabels(["ID", "Título", "Contenido", "Fecha"])

        self.cargar_articulos()

    def abrir_dialogo(self):
        dialogo = InsertDialog(self)
        if dialogo.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            titulo, contenido = dialogo.obtener_datos()
            self.insertar_articulo(titulo, contenido)
            self.cargar_articulos() 


    def cargar_articulos(self):
        self.tbl_articulos.clearContents()

        articulos = db["articulo"].find()

        for row_index, articulo in enumerate(articulos):
            self.tbl_articulos.insertRow(row_index)
        
            id_value = articulo.get("id", "N/A") 
            titulo_value = articulo.get("titulo", "Sin Título")
            contenido_value = articulo.get("contenido", "Sin Contenido")
            fecha_value = articulo.get("fecha", "Fecha No Disponible")
        
            self.tbl_articulos.setItem(row_index, 0, QtWidgets.QTableWidgetItem(id_value))
            self.tbl_articulos.setItem(row_index, 1, QtWidgets.QTableWidgetItem(titulo_value))
            self.tbl_articulos.setItem(row_index, 2, QtWidgets.QTableWidgetItem(contenido_value))
            self.tbl_articulos.setItem(row_index, 3, QtWidgets.QTableWidgetItem(fecha_value))

def run():
    app = QtWidgets.QApplication([])
    ventana = MainWindow()
    ventana.show()
    app.exec()

if __name__ == "__main__":
    run()