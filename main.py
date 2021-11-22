import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('films_db.sqlite')
        self.cur = self.con.cursor()
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.edit)
        self.update_table()

    def add(self):
        d = MyDialog(self)
        d.show()

    def edit(self):
        i = set(i.row() for i in self.tableWidget.selectedItems())
        if len(i) == 1:
            i = i.pop()
            d = MyDialog(self, [self.tableWidget.item(i, j).text()
                                for j in range(self.tableWidget.columnCount())])
            d.show()

    def update_table(self):
        res = self.cur.execute('select * from coffee').fetchall()
        self.tableWidget.setRowCount(len(res))
        self.tableWidget.setColumnCount(len(res[0]) if res else 0)
        self.tableWidget.setHorizontalHeaderLabels(
            i[0] for i in self.con.execute('select * from coffee').description)
        for i, line in enumerate(res):
            for j, val in enumerate(line):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.resizeColumnsToContents()

    def closeEvent(self, event):
        self.con.close()


class MyDialog(QDialog):
    def __init__(self, parent, i=None):
        super().__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.setWindowTitle('Изменение записи' if i else 'Создание записи')
        self.pushButton.clicked.connect(self.conf)
        self.pushButton_2.clicked.connect(self.close)
        self.i = i
        if i:
            self.lineEdit.setText(i[1])
            self.lineEdit_2.setText(i[2])
            self.lineEdit_3.setText(i[3])
            self.lineEdit_4.setText(i[4])
            self.lineEdit_5.setText(i[5])
            self.lineEdit_6.setText(i[6])

    def conf(self):
        p = self.parent()
        if self.lineEdit.text() and self.lineEdit_2.text() and self.lineEdit_4.text() \
                and self.lineEdit_5.text().isdigit() and self.lineEdit_6.text().isdigit()\
                and (self.lineEdit_3.text() == '0' or self.lineEdit_3.text() == '1'):
            if self.i:
                p.cur.execute(f"""UPDATE Coffee 
                                  SET name='{self.lineEdit.text()}', roasting='{self.lineEdit_2.text()}', 
                                  ground={self.lineEdit_3.text()}, taste='{self.lineEdit_4.text()}', 
                                  price={self.lineEdit_5.text()}, volume={self.lineEdit_6.text()} 
                                  WHERE id={self.i[0]}""")
            else:
                p.cur.execute(f"""INSERT INTO Coffee(name, roasting, ground, taste, price, volume) 
                                  VALUES ('{self.lineEdit.text()}', '{self.lineEdit_2.text()}', 
                                  {self.lineEdit_3.text()}, '{self.lineEdit_4.text()}', 
                                  {self.lineEdit_5.text()}, {self.lineEdit_6.text()})""")
            p.con.commit()
            p.update_table()
            self.close()
        else:
            self.label_7.setText('Ошибка!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
