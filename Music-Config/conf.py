# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
import os,json

App_name='Vk-Music-Tg'

def openFileNameDialog(self, path):
    fileName, _ = QFileDialog.getOpenFileName(self, 'Choose "chrome.exe"', path,"Chrome (chrome.exe)")
    if fileName:
        return (fileName)

class Ui_Form(QtWidgets.QWidget):
    def setupUi(self):
        self.setObjectName("Form")
        self.resize(395, 141)
        self.setMinimumSize(QtCore.QSize(395, 141))
        self.setMaximumSize(QtCore.QSize(395, 141))
        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 381, 140))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.tokenStr = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.tokenStr.setAcceptDrops(False)
        self.tokenStr.setAutoFillBackground(False)
        self.tokenStr.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.tokenStr.setObjectName("tokenStr")
        self.horizontalLayout.addWidget(self.tokenStr)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.IdStr = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.IdStr.setObjectName("IdStr")
        self.horizontalLayout_2.addWidget(self.IdStr)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.chStr = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.chStr.setObjectName("chStr")
        self.gridLayout.addWidget(self.chStr, 0, 0, 1, 1)
        self.fileOpen = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.fileOpen.setObjectName("fileOpen")
        self.gridLayout.addWidget(self.fileOpen, 0, 2, 1, 1)
        self.horizontalLayout_3.addLayout(self.gridLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.closeBut = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.closeBut.setObjectName("closeBut")
        self.horizontalLayout_4.addWidget(self.closeBut)
        self.SaveBut = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.SaveBut.setEnabled(True)
        self.SaveBut.setObjectName("SaveBut")
        self.horizontalLayout_4.addWidget(self.SaveBut)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Config Generator [Created by @dingo3]"))
        self.label.setText(_translate("Form", "Token:"))
        self.tokenStr.setInputMask(_translate("Form", "999999999:NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN"))
        self.label_2.setText(_translate("Form", "White_List Id:"))
        self.label_3.setText(_translate("Form", "Chrome Path:"))
        self.chStr.setText(_translate("Form", "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"))
        self.fileOpen.setText(_translate("Form", "..."))
        self.closeBut.setText(_translate("Form", "Close"))
        self.SaveBut.setText(_translate("Form", "Save"))
    def setup(self):
        self.show()
        self.setWindowIcon(QtGui.QIcon('music.png'))
        self.finished_ch_path=False
        self.finished_id=False
        self.finished_token=False
        if os.path.isfile(self.chStr.text()): self.finished_ch_path=True
        self.last_token=''

    def checker_error(self):
        if not self.finished_token: return 'Token is empty'
        if not self.finished_id: return 'Id is empty'
        if not self.finished_ch_path: return 'Wrong Chrome Path'
        return ''
    def on_closeBut_pressed(self):
        QApplication.quit()
    def on_SaveBut_pressed(self):

        text='Saved'
        detail='Successfully!'
        icon_msg=QMessageBox.Information
        res=self.checker_error()
        if res:
            icon_msg=QMessageBox.Warning
            detail='Error!'
            text=res
        else:
            temp=self.IdStr.text().split(',')
            ids=[]
            for i in temp:
                if i.strip().isdigit(): ids.append(int(i.strip()))
            if not ids:
                icon_msg = QMessageBox.Warning
                detail = 'Error!'
                text = 'Ids List ID Error'
            else:
                config={'Token':self.tokenStr.text(),'ids':ids, 'ch_path': self.chStr.text()}
                cache_path = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.ConfigLocation)
                if cache_path.endswith('/python'): cache_path = cache_path[:len(cache_path)- 7]
                cache_path = cache_path + os.path.sep + App_name
                if not os.path.isdir(cache_path): os.mkdir(cache_path)
                config=json.dumps(config, ensure_ascii=False)
                print(cache_path+os.path.sep+'config.ini')
                open(cache_path+os.path.sep+'config.ini','w').write(config)
        msg = QMessageBox()
        msg.setIcon(icon_msg)
        msg.setText(text)
        msg.setWindowTitle(detail)
        msg.setWindowIcon(QtGui.QIcon('music.png'))
        msg.exec_()

    def on_fileOpen_pressed(self):
        ch_path=openFileNameDialog(self, self.chStr.text())
        if ch_path:self.chStr.setText(ch_path)
    def on_tokenStr_editingFinished(self):
        self.finished_token=True
        self.last_token=self.tokenStr.text()
    def on_tokenStr_textChanged(self, m):
        if self.finished_token and self.last_token!=m:self.finished_token=False
    def on_IdStr_textChanged(self,m):
        if m:self.finished_id=True
        else:self.finished_id=False
    def on_chStr_textChanged(self,m):
        self.finished_ch_path = os.path.isfile(m)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Form()
    ui.setupUi()
    ui.setup()
    sys.exit(app.exec_())

