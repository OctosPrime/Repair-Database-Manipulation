# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogo_nuvem.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Save(object):
    def setupUi(self, Save):
        Save.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        Save.setObjectName("Save")
        Save.resize(400, 189)
        self.label = QtWidgets.QLabel(Save)
        self.label.setGeometry(QtCore.QRect(90, 20, 201, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Save)
        self.label_2.setGeometry(QtCore.QRect(20, 110, 361, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Save)
        QtCore.QMetaObject.connectSlotsByName(Save)

    def retranslateUi(self, Save):
        _translate = QtCore.QCoreApplication.translate
        Save.setWindowTitle(_translate("Save", "Aviso"))
        self.label.setText(_translate("Save", "Salvando banco de dados..."))
        self.label_2.setText(_translate("Save", "Isso pode demorar dependendo da conexão com a Internet e o tamanho do banco de dados."))
