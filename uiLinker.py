from ctypes import windll
from decimal import Decimal
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
from sys import exit, argv

myappid = 'fantozzi.ram.1.0'
windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
qtcreator_file  = "mainwindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setWindowTitle('RAM Compare')
        self.setFixedSize(700, 325)
        self.setupUi(self)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setHorizontalHeaderLabels(["Name", "CAS", "MHz", "Speed"])
        self.tableWidget.setColumnWidth(0, 108)
        self.tableWidget.setColumnWidth(1, 1)
        self.tableWidget.setColumnWidth(2, 1)
        self.tableWidget.setColumnWidth(3, 108)
        self.tableWidget.setSortingEnabled(True)
        self.speedLcdNumber.setDigitCount(6)
        self.speedLcdNumber.display("00.000")
        self.addButton.clicked.connect(self.add_to_compare)
        self.removeButton.clicked.connect(self.remove_from_compare)
        self.freqComboBox.currentIndexChanged.connect(self.calculate_speed)
        self.casSpinBox.valueChanged.connect(self.calculate_speed)
        self.clearButton.clicked.connect(self.clear_compare)
        self.calculate_speed()

    def calculate_speed(self):
        cas = Decimal(self.casSpinBox.value())
        speed = Decimal(self.freqComboBox.currentText())
        speed *= 1000000  # Convert to hertz
        val = speed / 2  # DDR
        val = 1 / val  # Invert of DDR
        time = cas * val  # Convert clock speed to time Source: https://www.wepc.com/tips/ram-speed/
        time *= 1000000000  # Convert to ns
        self.speedLcdNumber.display(str(round(time, 3)))
        return

    def remove_from_compare(self):
        self.tableWidget.removeRow(self.tableWidget.currentRow())
        return

    def add_to_compare(self):
        self.calculate_speed()
        row = self.tableWidget.rowCount() - 1
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        self.tableWidget.setItem(row, 0, QTableWidgetItem(str(self.nameEntry.text())))
        self.tableWidget.setItem(row, 1, QTableWidgetItem(str(self.casSpinBox.value())))
        self.tableWidget.setItem(row, 2, QTableWidgetItem(self.freqComboBox.currentText()))
        self.tableWidget.setItem(row, 3, QTableWidgetItem(str(self.speedLcdNumber.value())))
        return

    def clear_compare(self):
        self.tableWidget.clearContents()
        rows = self.tableWidget.rowCount()
        while rows >= 0:
            self.tableWidget.removeRow(rows)
            rows -= 1
        return


if __name__ == "__main__":
    app = QtWidgets.QApplication(argv)
    window = MyWindow()
    window.show()
    exit(app.exec_())

