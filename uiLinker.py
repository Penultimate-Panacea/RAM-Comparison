import sys
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
from decimal import Decimal

qtcreator_file  = "mainwindow.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setWindowTitle('RAM Compare')
        self.setupUi(self)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setHorizontalHeaderLabels(["Name", "Speed"])
        self.tableWidget.setSortingEnabled(True)
        self.speedLcdNumber.setDigitCount(6)
        self.speedLcdNumber.display("00.000")
        self.calculateButton.clicked.connect(self.calculate_speed)
        self.addButton.clicked.connect(self.add_to_compare)

    def calculate_speed(self):
        cas = Decimal(self.casSpinBox.value())
        speed = Decimal(self.freqComboBox.currentText())
        speed *= 1000000  # Convert to hertz
        val1 = speed / 2  # DDR
        val2 = 1 / val1  # Invert of DDR
        time = cas * val2  # Convert clock speed to time Source: https://www.wepc.com/tips/ram-speed/
        time *= 1000000000  # Convert to ns
        disp_time = str(round(time, 3))
        self.speedLcdNumber.display(disp_time)
        return

    def add_to_compare(self):
        self.calculate_speed()
        row = self.tableWidget.rowCount() - 1
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        self.tableWidget.setItem(row, 0, QTableWidgetItem(str(self.nameEntry.text())))
        # self.tableWidget.setItem(row, 1, QTableWidgetItem(self.casSpinBox.value()))
        # self.tableWidget.setItem(row, 2, QTableWidgetItem(self.freqComboBox.currentText()))
        self.tableWidget.setItem(row, 1, QTableWidgetItem(str(self.speedLcdNumber.value())))
        return


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

