import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tableWidget = QTableWidget()
        uic.loadUi('main.ui', self)
        con = sqlite3.connect('films_db.sqlite')
        cur = con.cursor()
        res = cur.execute('select * from coffee').fetchall()
        self.tableWidget.setRowCount(len(res))
        self.tableWidget.setColumnCount(len(res[0]) if res else 0)
        self.tableWidget.setHorizontalHeaderLabels(
            i[0] for i in con.execute('select * from coffee').description)
        for i, line in enumerate(res):
            for j, val in enumerate(line):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.resizeColumnsToContents()
        con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
