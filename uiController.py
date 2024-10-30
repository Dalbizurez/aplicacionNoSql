from PyQt6 import QtWidgets
from articuloDialog import Ui_Dialog 
from mainWindow import Ui_MainWindow

class InsertDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btn_articulo.clicked.connect(self.abrir_dialogo)

    def abrir_dialogo(self):
        print("Botón clickeado. Abriendo el diálogo...")  # Para depuración
        dialogo = InsertDialog(self)
        dialogo.exec()

