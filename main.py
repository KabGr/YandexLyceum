import sys
from random import randint

from PyQt5 import uic
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI.ui', self)
        self.setFixedSize(400, 430)
        self.f = 0
        self.pushButton.clicked.connect(self.click)

    def click(self):
        self.f = randint(1, 200)
        self.update()

    def paintEvent(self, event):
        if self.f:
            qp = QPainter()
            qp.begin(self)
            qp.translate(200, 230)
            qp.setBrush(QColor(255, 255, 0))
            qp.drawEllipse(-self.f, -self.f, self.f * 2, self.f * 2)
            qp.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
