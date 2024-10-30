from PyQt6 import QtWidgets
from mainWindow import Ui_MainWindow  

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ventana = Ui_MainWindow()
    ventana.show()
    sys.exit(app.exec())
