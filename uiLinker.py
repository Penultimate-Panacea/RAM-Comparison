import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from decimal import Decimal

qtcreator_file  = "qt/mainwindow.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.speedLcdNumber.setDigitCount(8)
        self.speedLcdNumber.display("00.00ns")
        self.calculateButton.clicked.connect(self.calculate_speed)

    def calculate_speed(self):
        cas = Decimal(self.casSpinBox.value())
        speed = Decimal(self.freqComboBox.currentText())
        speed *= 1000000  # Convert to hertz
        val1 = speed / 2  # DDR
        val2 = 1 / val1  # Invert of DDR
        time = cas * val2  # Convert clock speed to time Source: https://www.wepc.com/tips/ram-speed/
        time *= 1000000000  # Convert to ns
        disp_time = str(round(time, 2))
        self.speedLcdNumber.display(disp_time)
        return


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

