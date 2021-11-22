import sys
from random import randint

from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow

from UI import Ui_MainWindow


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(400, 430)
        self.f = []
        self.pushButton.clicked.connect(self.click)

    def click(self):
        self.f = randint(1, 200), [randint(0, 255) for _ in range(3)]
        self.update()

    def paintEvent(self, event):
        if self.f:
            qp = QPainter()
            qp.begin(self)
            qp.translate(200, 230)
            qp.setBrush(QColor(*self.f[1]))
            qp.drawEllipse(-self.f[0], -self.f[0], self.f[0] * 2, self.f[0] * 2)
            qp.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
