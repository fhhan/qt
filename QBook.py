import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
#import qdarkstyle
from PyQt5.QtSql import QSqlDatabase,QSqlQueryModel

class Qbook(QWidget):
    def __init__(self):
        super(Qbook, self).__init__()

        # 当前页数
        self.pageNum = 1
        # 总页数
        self.pageAll = 0
        # 每页显示记录数
        self.pageRecord = 10
        # 总记录数
        self.Record = 0

        self.initUI()

    def initUI(self):
        self.resize(800, 500)
        self.setWindowTitle('🐂🍺')

        self.layout = QVBoxLayout()
        self.layout1 = QHBoxLayout()
        self.layout2 = QHBoxLayout()
        self.layout3 = QHBoxLayout()

        self.edit = QLineEdit()
        self.searchBtn = QPushButton("查询")
        self.box = QComboBox()
        items = ['按书名🔍', '按书号🔍', '按作者🔍']
        self.box.addItems(items)

        self.layout1.addWidget(self.edit)
        self.layout1.addWidget(self.searchBtn)
        self.layout1.addWidget(self.box)

        self.initModel()

        self.label1 = QLabel('当前页')
        self.edit2 = QLineEdit()
        self.edit2.setText('1')
        self.edit2.setFixedWidth(30)
        self.label2 = QLabel(' /' + str(self.pageAll) + '页')

        self.jumpBtn = QPushButton('跳转')
        self.preBtn = QPushButton('前一页')
        self.preBtn.setFixedWidth(65)  # 按钮变宽
        self.nextBtn = QPushButton('后一页')
        self.nextBtn.setFixedWidth(65)

        self.layout2.addWidget(self.label1)
        self.layout2.addWidget(self.edit2)
        self.layout2.addWidget(self.label2)

        self.layout2.addWidget(self.jumpBtn)
        self.layout2.addWidget(self.preBtn)
        self.layout2.addWidget(self.nextBtn)

        widget = QWidget()
        widget.setLayout(self.layout2)
        widget.setFixedWidth(320)
        self.layout3.addWidget(widget)

        self.layout.addLayout(self.layout1)
        self.layout.addWidget(self.view)
        self.layout.addLayout(self.layout3)
        self.setLayout(self.layout)

        self.jumpBtn.clicked.connect(self.jump)
        self.preBtn.clicked.connect(self.prePage)
        self.nextBtn.clicked.connect(self.nextPage)
        self.edit2.returnPressed.connect(self.jump)

        self.box.currentTextChanged.connect(lambda :self.pageShow(0))
        self.searchBtn.clicked.connect(lambda :self.pageShow(0))
        self.edit.returnPressed.connect(lambda :self.pageShow(0))

        self.btnStatus()

          #  clicked.connect(self.search)

    def initModel(self):
        # 打开数据库
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('./LibraryManagement.db')
        self.db.open()

        self.view = QTableView()

        self.model = QSqlQueryModel()

        # 总页数和总记录数
        self.sqlcode = 'select * from Book'
        self.model.setQuery('select * from Book')
        self.Record = self.model.rowCount()
        self.pageAll = int(self.Record / self.pageRecord) + 1

        # 只显示第一页
        sqlcode = 'select * from book limit %d,%d' % (0, self.pageRecord)
        self.model.setQuery(sqlcode)

        self.model.setHeaderData(0, Qt.Horizontal, "书名")
        self.model.setHeaderData(1, Qt.Horizontal, "书号")
        self.model.setHeaderData(2, Qt.Horizontal, "作者")
        self.model.setHeaderData(3, Qt.Horizontal, "分类")
        self.model.setHeaderData(4, Qt.Horizontal, "出版社")
        self.model.setHeaderData(5, Qt.Horizontal, "出版时间")
        self.model.setHeaderData(6, Qt.Horizontal, "库存")
        self.model.setHeaderData(7, Qt.Horizontal, "剩余可借")
        self.model.setHeaderData(8, Qt.Horizontal, "总借阅次数")

        self.view.setModel(self.model)


        # self.db.close()

    def btnStatus(self):
        if self.edit2.text() == '1':
            self.preBtn.setEnabled(False)
            self.nextBtn.setEnabled(True)
        elif self.edit2.text() == str(self.pageAll):
            self.preBtn.setEnabled(True)
            self.nextBtn.setEnabled(False)
        else:
            self.preBtn.setEnabled(True)
            self.nextBtn.setEnabled(True)

    def jump(self):
        if self.edit2.text().isdigit():
            self.pageNum = int(self.edit2.text())
            pag = self.label2.text()[2]
            if self.pageNum > int(pag):
                #print(self.label2.text())
                self.edit2.setText(pag)
                QMessageBox().warning(self,'Warning','超出页数')
                return
            if self.pageNum < 1:
                self.pageNum = 1
        else:
            self.pageNum = 1
        index = (self.pageNum - 1) * self.pageRecord
        self.pageShow(index)

    def pageShow(self, index):
        if self.box.currentText() == '按书名🔍':
            searchby = 'BookName'
        elif self.box.currentText() == '按书号🔍':
            searchby = 'BookId'
        elif self.box.currentText() == '按作者🔍':
            searchby = 'Auth'
        if self.edit.text() == '':
            #self.edit2.setText('1')
            sqlcode = 'select * from book order by %s limit %d,%d' % (searchby, index, self.pageRecord)
            self.model.setQuery(sqlcode)
            # if index == 0:
            #     self.searchall = int(self.model.rowCount() / self.pageRecord) + 1
            self.label2.setText(' /' + str(self.pageAll) + '页')
            self.btnStatus()
        else:
            input = self.edit.text()
            keywd = '%'
            for i in range(0, len(input)):
                keywd = keywd + input[i] + "%"
            if index == 0:
                sqlcode = "select * from book where %s like '%s' order by %s limit %d,%d" % (searchby, keywd, searchby,index, self.pageRecord)
                self.model.setQuery(sqlcode)
                self.searchall = int(self.model.rowCount() / self.pageRecord) + 1
            else:
                sqlcode = "select * from book where %s like '%s' order by %s limit %d,%d" % (searchby, keywd, searchby, index, self.pageRecord)
                self.model.setQuery(sqlcode)
            if self.model.rowCount()!=0:
                #self.searchall = int(self.model.rowCount() / self.pageRecord) + 1
                self.label2.setText(' /' + str(self.searchall) + '页')
                self.btnStatus()
                if self.edit2.text() == str(self.searchall):
                    self.nextBtn.setEnabled(False)
            else:
                msg = QMessageBox()
                msg.information(self,'Tips','404 Not Found')
                msg.show()
                sqlcode = 'select * from book limit %d,%d' % (0, self.pageRecord)
                self.model.setQuery(sqlcode)
                self.edit2.setText('1')
                self.btnStatus()

    def prePage(self):
        self.pageNum -= 1
        self.edit2.setText(str(self.pageNum))
        index = (self.pageNum - 1) * self.pageRecord
        self.pageShow(index)

    def nextPage(self):
        self.pageNum += 1
        self.edit2.setText(str(self.pageNum))
        index = (self.pageNum - 1) * self.pageRecord
        self.pageShow(index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Qbook()
    #app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    demo.show()
    sys.exit(app.exec_())
