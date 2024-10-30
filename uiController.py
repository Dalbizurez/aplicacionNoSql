from PyQt6 import QtWidgets
from articuloDialog import Ui_Dialog 
from mainWindow import Ui_MainWindow

import dataController

class InsertDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(QtWidgets.QWidget,self ).__init__(parent)
        self.setupUi(self)
        self.btn_guardar_articulo.setEnabled(False)

        self.btn_guardar_articulo.clicked.connect(lambda:dataController.saveArticulo(self.txt_titulo.text(), self.txtContenido.toPlainText()))

        self.txt_titulo.textChanged.connect(lambda:self.btn_guardar_articulo.setEnabled(bool(self.txt_titulo.text())))


        

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btn_articulo.clicked.connect(lambda:self.abrir_dialogo())

        self.insertDialog = InsertDialog()

    def abrir_dialogo(self):
        print("Botón clickeado. Abriendo el diálogo...")  # Para depuración
        self.insertDialog.show()

def run():
    app = QtWidgets.QApplication([])
    ventana = MainWindow()
    ventana.show()
    app.exec()

if __name__ == "__main__":
    run()