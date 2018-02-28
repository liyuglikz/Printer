# -*- coding: utf-8 -*-
import math
import html
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import QPrinter,QPrintDialog
import qrc_resources

DATE_FORMAT = "yyyy.MM.dd"

class Statement(object):
    def __init__(self, hospital, contact, address):
        self.hospital = hospital
        self.contact = contact
        self.address = address
        self.transactions = []  # List of (QDate, float) two-tuples

    def balance(self):
        return sum([amount for date, amount in self.transactions])

# 定义获取病人信息类
class GetpatientInfo(object):
    def __init__(self, name, gender, age, ill_type, ward, bed_no, hospital_no, CT_no):
        self.name = name
        self.gender = gender
        self.age = age
        self.ill_type = ill_type
        self.ward = ward
        self.bed_no = bed_no
        self.hospital_no = hospital_no
        self.CT_no = CT_no

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.printer = QPrinter()
        self.printer.setPageSize(QPrinter.Letter)
        self.generateFakeStatements()
        self.table = QTableWidget()
        self.populateTable()

        htmlButton = QPushButton("打印")
        quitButton = QPushButton("退出")

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(htmlButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(quitButton)
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        htmlButton.clicked.connect(self.printViaHtml)
        quitButton.clicked.connect(self.accept)

        self.setWindowTitle("打印页面")

    def generateFakeStatements(self):
        self.statements = []
        statement = Statement("华中科技大学同济医学院附属协和医院", "CT检查报告书", "234123")
        self.statements.append(statement)

    def populateTable(self):
        headers = ["hospital", "Contact", "Address", "Balance"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(self.statements))
        for row, statement in enumerate(self.statements):
            self.table.setItem(row, 0,
                    QTableWidgetItem(statement.hospital))
            self.table.setItem(row, 1,
                    QTableWidgetItem(statement.contact))
            self.table.setItem(row, 2,
                    QTableWidgetItem(statement.address))
            item = QTableWidgetItem("$ {:,.2f}".format(
                                    statement.balance()))
            item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
            self.table.setItem(row, 3, item)
        self.table.resizeColumnsToContents()

    def printViaHtml(self):
        htmltext = ""
        date = QDate.currentDate().toString(DATE_FORMAT)    # 获取当前时间
        patient = GetpatientInfo("李尼古","男","56岁","内科","113","2","955464","111745")
        htmltext += ("<p align=center><font size='16'>华中科技大学同济医学院附属协和医院</font></p>"
                     "<p align=center><font size='18'><b>CT检查报告书</b></font></p>")
        htmltext += ("<p align=right><font size='4'>CT号：<u>{0}</u></font></p>").format(patient.CT_no)
        htmltext += ("<hr style='color:black'/>")
        htmltext += ("<p align=center><font size='4'>姓名：<u>{0}</u>&nbsp;性别：<u>{1}</u>&nbsp;"
                     "年龄：<u>{2}</u>&nbsp;科别：<u>{3}</u>&nbsp;病房：<u>{4}</u>&nbsp;床号：<u>{5}</u>"
                     "&nbsp;住院号：<u>{6}</u></font></p>").format(patient.name,patient.gender,patient.age,
                    patient.ill_type,patient.ward,patient.bed_no,patient.hospital_no)
        htmltext += ("<p align=justify><font size='5'>&nbsp;&nbsp;左肺瘤第三次化疗"
                     "术后:左肺舌叶可见不规则型团块状软组织密度影,截面约为3.0×4.4cm,CT值约为28-45HU,左侧舌"
                     "叶支气管截断,邻近胸膜可见牵引征,肿块远端见小片状高密度影,左肺下叶外基底段胸膜下可见直"
                     "径约0.7cm小结节影,边界光整。纵隔内可见明显肿大淋巴结,最大者位于主肺动脉窗内,约为4.1×"
                     "3.5cm。扫描所及肝左叶可见点状低密度影,肝脏密度减低。</font></p>")
        htmltext += ("<p align=right><font size='4'>医师签名：</font></p>")
        htmltext += ("<p align=right><font size='4'>报告日期：{0}</font></p>").format(date)
        htmltext += ("<hr style='color:black'/><p align=left><font size='4'><b>(本报告仅供临床医生诊断参考)</b></font></p>")
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            document = QTextDocument()
            document.setHtml(htmltext)
            document.print_(self.printer)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()
