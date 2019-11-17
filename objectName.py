import sys
from PyQt4 import QtGui, QtCore

class testFindChildren(QtGui.QDialog):

        def __init__(self):
                QtGui.QDialog.__init__(self)
                self.setWindowModality(QtCore.Qt.WindowModal)

                self.searchLayout = QtGui.QVBoxLayout(self)

                hLayout = QtGui.QHBoxLayout()
                hLayout.setObjectName('hLayout_0')
                self.searchLayout.addLayout(hLayout)

                print(self.findChild(QtGui.QHBoxLayout,r'hLayout_0'))
                children =self.findChildren(QtGui.QHBoxLayout,QtCore.QRegExp(r'\w*'))
                for c in children:
                        print(c.objectName())
                print(self.findChildren(QtGui.QHBoxLayout,QtCore.QRegExp(r'hLayout_\d')))


def main(args):
        app = QtGui.QApplication(args)
        mainWindow = testFindChildren()

        mainWindow.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
        main(sys.argv)
