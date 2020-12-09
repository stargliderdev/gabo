import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(800, 600)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        self.draw_something()

    def draw_something(self):
        pen = QtGui.QPen()
        pen.setWidth(4)
        pen.setColor(QtGui.QColor('red'))
        painter = QtGui.QPainter(self.label.pixmap())
        painter.setPen(pen)
        painter.drawLine(4, 300, 4, 00)
        painter.drawLine(20, 200, 20, 60)
        painter.drawLine(30, 200, 30, 100)
        painter.drawLine(4, 300, 300, 150)
        painter.end()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()