import sys

from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QApplication, QMainWindow
from GUI import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_table_view()

    def setup_table_view(self):
        # Datos de ejemplo
        data = [
            ["Alice", "Engineer", 30],
            ["Bob", "Designer", 24],
            ["Charlie", "Manager", 35]
        ]

        # Crear el modelo
        self.model = QStandardItemModel(len(data), len(data[0]))
        self.model.setHorizontalHeaderLabels(["Name", "Occupation", "Age"])

        # Llenar el modelo con datos
        for row, rowData in enumerate(data):
            for column, value in enumerate(rowData):
                item = QStandardItem(str(value))
                self.model.setItem(row, column, item)

        # Asignar el modelo al QTableView
        self.tableView.setModel(self.model)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
