from random import random, randint, randrange, uniform
from unittest import result
from unittest.mock import CallableMixin
from PyQt5 import uic,QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSlot, QSortFilterProxyModel
from PyQt5.QtWidgets import QApplication, QWidget, QHeaderView, QAbstractItemView, QPushButton, QTableWidget, QDialog, QAbstractItemView, \
                            QTableWidgetItem, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QStandardItem, QStandardItemModel
import sqlite3
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from aviso_salvar import Ui_Save
from aviso_baixar import Ui_Down
from dialogo_sinc import Ui_Sinc
from Lista import Ui_Lista
from Formulario import Ui_Form
from Editor import Ui_Editor
from dialogo_salvar import Ui_Salvar
from dialogo_exclusao import Ui_Excluir
from Login import Ui_Login
from Visualizar import Ui_View
import sys
from reportlab.pdfgen import canvas

banco = sqlite3.connect('cadastro_clientes.db')
dbcursor = banco.cursor()
dbcursor.execute("CREATE TABLE IF NOT EXISTS clientes (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,n INT(5),nome VARCHAR(35),modelo VARCHAR(60),descricao VARCHAR(250),valor VARCHAR(15),situacao VARCHAR(22),data VARCHAR(12),garantia VARCHAR(24))")
dbcursor.execute("CREATE TABLE IF NOT EXISTS login (nome text, senha text, UNIQUE(nome, senha))")
#dbcursor.execute("INSERT INTO login (nome, senha) VALUES (?,?)", (Usuario, Senha))
dbcursor.execute("INSERT OR IGNORE INTO login(nome, senha) VALUES('infocel', 'inf54321')")
banco.commit()
app2 = QApplication(sys.argv)
app=QtWidgets.QApplication([])

class Ui_Visualizar(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_View()
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowIcon(QtGui.QIcon('Icone.ico'))

class ui_login(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        self.ui.lineEdit_2.setFocus(True)
        self.ui.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.lineEdit.setText("infocel")
        self.setWindowIcon(QtGui.QIcon('Icone.ico'))

        self.keyPressEvent = self.keyPressEvent

    def keyPressEvent(self, e):
        print("event", e)
        if e.key()  == Qt.Key_Return :
            print(' return')
            chamar_lista()
        elif e.key() == Qt.Key_Enter :   
            print(' enter')
            chamar_lista()


class Ui_Delete(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_Excluir()
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowIcon(QtGui.QIcon('Icone.ico'))

class Ui_Sincronizar(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_Sinc()
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowIcon(QtGui.QIcon('Icone.ico'))

class Ui_Saves(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_Salvar()
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowIcon(QtGui.QIcon('Icone.ico'))

class Ui_Edit(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_Editor()
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowIcon(QtGui.QIcon('Icone.ico'))

class Ui_Formulario(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowIcon(QtGui.QIcon('Icone.ico'))

class Ui_List(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_Lista()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('Icone.ico'))


class DL_ui(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_Down()
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowIcon(QtGui.QIcon('logo.png'))

class Save_ui(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_Save()
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowIcon(QtGui.QIcon('logo.png'))

Login = ui_login()
visualizar = Ui_Visualizar()
confirmar_sinc = Ui_Sincronizar()
confirmar_salvar = Ui_Saves()
confirmar_exclusao = Ui_Delete()
editor = Ui_Edit()
formulario = Ui_Formulario()
listagem = Ui_List()
DW = DL_ui()
aviso_salvar = Save_ui()


def atualizar():
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM clientes"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    listagem.ui.tableWidget.setRowCount(len(dados_lidos))
    listagem.ui.tableWidget.setColumnCount(9)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 9):
            listagem.ui.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

def Sincronizar():
        QtWidgets.qApp.processEvents()
        gauth = GoogleAuth()           
        drive = GoogleDrive(gauth)
        file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format('1WwdgiiJyhfY3GofjyUPoNItH5Q7idVW7')}).GetList()
        for file in file_list:
            print("Downloading database...")
            file.GetContentFile(file['title'])
            atualizar()
            DW.close()
        


def Update_Backup():
    QtWidgets.qApp.processEvents()
    gauth = GoogleAuth()           
    drive = GoogleDrive(gauth)
    file_id = "1kaq1LMnV_91sPrKfbrXo5m9779unDFol"
    update_file = drive.CreateFile({'id': file_id})
    update_file.SetContentFile('cadastro_clientes.db')
    print("Saving...")
    update_file.Upload()
    aviso_salvar.close()

def Chamar_Download():
    DW.show()
    Sincronizar()
    

def Chamar_Save():
    aviso_salvar.show()
    Update_Backup()
    
    
        


def mostrar_dialogo():
    confirmar_exclusao.show()
    rowcount = listagem.ui.tableWidget.rowCount()
    SelectedRow = listagem.ui.tableWidget.currentRow()

    def Reject():
        SelectedRow == listagem.ui.tableWidget.setCurrentItem(None)

    if rowcount==0:
        print("No Rows To delete!")
        confirmar_exclusao.setWindowTitle("Erro")
        confirmar_exclusao.ui.label.setText("Nenhuma linha disponível para excluir.")
        confirmar_exclusao.ui.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Ok)
    elif SelectedRow == -1:
        confirmar_exclusao.setWindowTitle("Erro")
        confirmar_exclusao.ui.label.setText("Nenhuma linha selecionada.")
        confirmar_exclusao.ui.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Ok)
    else:
        confirmar_exclusao.setWindowTitle("Confirmar")
        confirmar_exclusao.ui.label.setText("Tem certeza de que quer remover este item?")
        confirmar_exclusao.ui.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        confirmar_exclusao.ui.buttonBox.accepted.connect(excluir_dados)
        confirmar_exclusao.ui.buttonBox.rejected.connect(Reject)
        
def excluir_dados():
    index_list = []
    SelectedRow = listagem.ui.tableWidget.selectionModel().selectedRows()
    rowcount = listagem.ui.tableWidget.rowCount()
    for model_index in SelectedRow:
        index = QtCore.QPersistentModelIndex(model_index)         
        index_list.append(index)

    if rowcount==0:
        print("No Rows To delete!")
       

    elif SelectedRow==-1:
        print("No Row selected!")
    else:
        
        SelectedRow = -1
        ix = listagem.ui.tableWidget.model().index(
        SelectedRow, listagem.ui.tableWidget.currentColumn()
    )
        listagem.ui.tableWidget.setCurrentIndex(ix)
        

        for index in index_list:
            listagem.ui.tableWidget.removeRow(index.row())
            cursor = banco.cursor()
            cursor.execute("SELECT id FROM clientes")
            dados_vistos = cursor.fetchall()
            valor_id = dados_vistos[SelectedRow][0]
            cursor.execute("DELETE FROM clientes WHERE id="+ str(valor_id))
            banco.commit()
            print(valor_id)
            print(SelectedRow)

def gerar_pdf():
    cursor = banco.cursor()
    comando_PDF = "SELECT * FROM clientes"
    cursor.execute(comando_PDF)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("cadastro_clientes.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200,800, "Clientes cadastrados:")
    pdf.setFont("Times-Bold", 10)

    pdf.drawString(10,750, "ID")
    pdf.drawString(50,750, "NOME")
    pdf.drawString(150,750, "MODELO")
    #pdf.drawString(150,750, "DESCRIÇÃO")
    pdf.drawString(270,750, "VALOR")
    pdf.drawString(310,750, "SITUAÇÃO")
    pdf.drawString(420,750, "DATA")
    pdf.drawString(470,750, "GARANTIA")

    for i in range (0, len(dados_lidos)):
        y = y + 20
        pdf.drawString(10,750 - y, str(dados_lidos[i][0]))
        pdf.drawString(50,750 - y, str(dados_lidos[i][2]))
        pdf.drawString(150,750 - y, str(dados_lidos[i][4]))
        #pdf.drawString(150,750 - y, str(dados_lidos[i][3]))
        pdf.drawString(270,750 - y, str(dados_lidos[i][5]))
        pdf.drawString(310,750 - y, str(dados_lidos[i][6]))
        pdf.drawString(420,750 - y, str(dados_lidos[i][7]))
        pdf.drawString(470,750 - y, str(dados_lidos[i][8]))

    pdf.save()
    print("PDF FOI GERADO COM SUCESSO!")

codigo_n = 0
clientcode = 0
infoGarantia = ""

def ativar_garantia():
    global infoGarantia
        
    if editor.ui.checkBox.isChecked():
        infoGarantia = editor.ui.dateEdit_2.text()
        editor.ui.label_9.setDisabled(False)
        editor.ui.dateEdit_2.setDisabled(False) 
    else:
        infoGarantia = "Nenhuma Garantia"
        editor.ui.label_9.setDisabled(True)
        editor.ui.dateEdit_2.setDisabled(True)

def visualizar_dados():
    linha = listagem.ui.tableWidget.currentRow()
    print(linha)

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM clientes")
    dados_coletados = cursor.fetchall()
    valor_id = dados_coletados[linha][0]
    cursor.execute("SELECT * FROM clientes WHERE id ="+ str(valor_id))
    cliente = cursor.fetchall()
    
    qdate = QtCore.QDate.fromString(str(cliente[0][7]), "dd/MM/yyyy")
    qdate2 = QtCore.QDate.fromString(str(cliente[0][8]), "dd/MM/yyyy")



    visualizar.ui.lineEdit_2.setText(str(cliente[0][1]))
    visualizar.ui.lineEdit.setText(str(cliente[0][0]))
    visualizar.ui.lineEdit_3.setText(str(cliente[0][2]))
    visualizar.ui.lineEdit_4.setText(str(cliente[0][3]))
    visualizar.ui.textBrowser.setText(str(cliente[0][4]))
    visualizar.ui.lineEdit_5.setText(str(cliente[0][5]))
    visualizar.ui.lineEdit_6.setText(str(cliente[0][6]))
    visualizar.ui.lineEdit_8.setText(str(cliente[0][7]))
    visualizar.ui.lineEdit_7.setText(str(cliente[0][8]))
    visualizar.show()
    visualizar.ui.pushButton.clicked.connect(visualizar.close)
    

def editar_dados():
    editor.ui.checkBox.setChecked(False)
    editor.ui.label_9.setDisabled(True)
    editor.ui.dateEdit_2.setDisabled(True)
    linha = listagem.ui.tableWidget.currentRow()
    global codigo_n
    global clientcode
    global infoGarantia

    rowcount = listagem.ui.tableWidget.rowCount()

    def Reject():
        editor.close()
        linha == listagem.ui.tableWidget.setCurrentItem(None)
    
    editor.ui.pushButton_2.clicked.connect(Reject)



    if rowcount==0:
        print("No Rows To Edit")
        confirmar_exclusao.setWindowTitle("Erro")
        confirmar_exclusao.ui.label.setText("Nenhuma linha disponível para editar.")
        confirmar_exclusao.ui.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        confirmar_exclusao.show()
    elif linha == -1:
        print("Sem dados para editar!")
        confirmar_exclusao.setWindowTitle("Erro")
        confirmar_exclusao.ui.label.setText("Nenhuma linha selecionada.")
        confirmar_exclusao.ui.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        confirmar_exclusao.show()
    else:
        cursor = banco.cursor()
        cursor.execute("SELECT id FROM clientes")
        dados_coletados = cursor.fetchall()
        valor_id = dados_coletados[linha][0]
        cursor.execute("SELECT * FROM clientes WHERE id ="+ str(valor_id))
        cliente = cursor.fetchall()
        editor.show()
    
        codigo_n = valor_id

        Garantia = (str(cliente[0][8]))

        qdate = QtCore.QDate.fromString(str(cliente[0][7]), "dd/MM/yyyy")
        qdate2 = QtCore.QDate.fromString(str(cliente[0][8]), "dd/MM/yyyy")


        if Garantia == "Nenhuma garantia":
            pass
        else:
            editor.ui.checkBox.setChecked(True)

        
        if editor.ui.checkBox.isChecked():
            infoGarantia = editor.ui.dateEdit_2.text()
            editor.ui.label_9.setDisabled(False)
            editor.ui.dateEdit_2.setDisabled(False) 
        else:
            infoGarantia = "Nenhuma garantia"
            editor.ui.label_9.setDisabled(True)
            editor.ui.dateEdit_2.setDisabled(True)



        clientcode = str(cliente[0][1])
        editor.ui.lineEdit.setText(str(cliente[0][0]))
        editor.ui.textEdit_2.setText(str(cliente[0][2]))
        editor.ui.textEdit_3.setText(str(cliente[0][3]))
        editor.ui.textEdit.setText(str(cliente[0][4]))
        editor.ui.lineEdit_2.setText(str(cliente[0][5]))
        editor.ui.lineEdit_3.setText(str(cliente[0][6]))
        editor.ui.dateEdit.setDate(qdate)
        editor.ui.dateEdit_2.setDate(qdate2)

def salvar_edicao():
    global codigo_n
    global clientcode
    global infoGarantia

    nome = editor.ui.textEdit_2.toPlainText()
    modelo = editor.ui.textEdit_3.toPlainText()
    descricao = editor.ui.textEdit.toPlainText()
    valor = editor.ui.lineEdit_2.text()
    situacao = editor.ui.lineEdit_3.text()
    data = editor.ui.dateEdit.text()
    garantia = infoGarantia
    

    
    bancocursor = banco.cursor()
    bancocursor.execute("UPDATE clientes SET nome = '{1}', modelo = '{2}', descricao = '{3}', valor = '{4}', situacao = '{5}', data = '{6}', garantia = '{7}' WHERE n = {0}".format(clientcode,nome,modelo,descricao,valor,situacao,data,garantia,codigo_n))
    banco.commit()
    editor.close()
    atualizar()
    
codigo = 0
codigoTest = 87744

def mostrar_formulario():
    #Gera um código unico, e verifica se o mesmo existe no banco de dados:
    formulario.show()
    codigo_gerado = randrange(10000,99999)
    global codigo
    code = (codigo_gerado,)
    cursor = banco.cursor()
    cursor.execute(
    'SELECT * FROM clientes WHERE n = ? GROUP BY n',
    (codigo_gerado,)
    )

    results = cursor.fetchall()
    
    row_count = cursor.rowcount
    print("number of affected rows: {}".format(row_count))
    if len(results) <= 0:
        print("It Does Not Exist")
        codigo = codigo_gerado
        formulario.ui.lineEdit_4.setText(str(codigo_gerado))
        print(codigo)
    else:
        print("Code exists, changing...")
        codigo_gerado = codigo_gerado + 1
        
        codigo = codigo_gerado
        formulario.ui.lineEdit_4.setText(str(codigo_gerado))
        print(codigo)
        
def chamar_lista():
    Usuario = Login.ui.lineEdit.text()
    Senha = Login.ui.lineEdit_2.text()

    try:
        cursor = banco.cursor()
        cursor.execute("SELECT senha FROM login WHERE nome = '{}'".format(Usuario))
        dbsenha = cursor.fetchall()
        print(dbsenha[0][0])
        #banco.close()
    except:
        print("Login invalido!")
        print(dbsenha)

    if not Usuario and not Senha:
        Login.ui.label_5.setText("Digite um usuário e senha!")
        QtWidgets.qApp.processEvents()
        Login.ui.lineEdit.textChanged.connect(lambda: Login.ui.label_5.setText(""))
        Login.ui.lineEdit_2.textChanged.connect(lambda: Login.ui.label_5.setText(""))
    elif not Usuario:
        Login.ui.label_5.setText("Digite um usuário!")
        QtWidgets.qApp.processEvents()
        Login.ui.lineEdit.textChanged.connect(lambda: Login.ui.label_5.setText(""))
        Login.ui.lineEdit_2.textChanged.connect(lambda: Login.ui.label_5.setText(""))
    elif not Senha:
        Login.ui.label_5.setText("Digite uma senha!")
        QtWidgets.qApp.processEvents()
        Login.ui.lineEdit.textChanged.connect(lambda: Login.ui.label_5.setText(""))
        Login.ui.lineEdit_2.textChanged.connect(lambda: Login.ui.label_5.setText(""))
        return
    elif not dbsenha:
        Login.ui.label_5.setText("Usuário ou senha inválidos!")
        QtWidgets.qApp.processEvents()
        Login.ui.lineEdit.textChanged.connect(lambda: Login.ui.label_5.setText(""))
        Login.ui.lineEdit_2.textChanged.connect(lambda: Login.ui.label_5.setText(""))
    elif Senha == dbsenha[0][0]:
        listagem.show()
        Login.close()
    else:
        Login.ui.label_5.setText("Usuário ou senha inválidos!")
        QtWidgets.qApp.processEvents()
        Login.ui.lineEdit.textChanged.connect(lambda: Login.ui.label_5.setText(""))
        Login.ui.lineEdit_2.textChanged.connect(lambda: Login.ui.label_5.setText(""))
        
def funcao_principal():
    linha1 = formulario.ui.lineEdit.text()
    linha2 = formulario.ui.lineEdit_2.text()
    linha3 = formulario.ui.lineEdit_3.text()
    data = formulario.ui.dateEdit.text()
    descricao = formulario.ui.textEdit.toPlainText()
    infoGarantia = ""
    situacao = ""

    print("Nome: ", linha1)
    print("Modelo: ", linha2)
    print("Data: ", data)
    
    if formulario.ui.checkBox.isChecked():
        data2 = formulario.ui.dateEdit_2.text()
        infoGarantia = data2
        print("Garantia:", data2)
    else:
        infoGarantia = "Nenhuma garantia"
        print("Garantia: Nenhuma")
    
    if formulario.ui.radioButton.isChecked():
       situacao = "Pago|Entregue"
       print("Situação:", situacao)
    elif formulario.ui.radioButton_2.isChecked():
        situacao = "Pagando|Entregue"
        print("Situação:", situacao)
    else:
        situacao = "Não Pago|Não Entregue"
        print("Situação:", situacao)

    formulario.close()

    cursor = banco.cursor()
    dados = (codigo,str(linha1),str(linha2),str(descricao),str(linha3),str(situacao),str(data),infoGarantia)
    cursor.execute("INSERT INTO clientes (n,nome,modelo,descricao,valor,situacao,data,garantia) VALUES (?,?,?,?,?,?,?,?)", dados)
    banco.commit()
    formulario.ui.lineEdit.setText("")
    formulario.ui.lineEdit_2.setText("")
    formulario.ui.lineEdit_3.setText("")
    formulario.ui.textEdit.setPlainText("")

    atualizar()

def mostrar_garantia():
    if formulario.ui.label_6.isEnabled() and formulario.ui.dateEdit_2.isEnabled():
     formulario.ui.label_6.setDisabled(True)
     formulario.ui.dateEdit_2.setDisabled(True)
    else:
     formulario.ui.label_6.setDisabled(False)
     formulario.ui.dateEdit_2.setDisabled(False)



formulario.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
formulario.ui.pushButton.clicked.connect(funcao_principal)
formulario.ui.checkBox.clicked.connect(mostrar_garantia)
formulario.ui.pushButton_2.clicked.connect(formulario.close)

#confirmar_sinc.setWindowFlags()
#confirmar_salvar.setWindowFlags()


confirmar_salvar.ui.buttonBox.accepted.connect(Chamar_Save)
confirmar_sinc.ui.buttonBox.accepted.connect(Chamar_Download)

listagem.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
listagem.ui.pushButton.clicked.connect(mostrar_formulario)
listagem.ui.pushButton_2.clicked.connect(gerar_pdf)
listagem.ui.pushButton_3.clicked.connect(mostrar_dialogo)
listagem.ui.pushButton_4.clicked.connect(editar_dados)
listagem.ui.pushButton_5.clicked.connect(confirmar_salvar.show)
listagem.ui.pushButton_6.clicked.connect(confirmar_sinc.show)
listagem.ui.tableWidget.doubleClicked.connect(visualizar_dados)
editor.ui.pushButton.clicked.connect(salvar_edicao)
editor.ui.checkBox.clicked.connect(ativar_garantia)

Login.show()
Login.ui.pushButton.clicked.connect(chamar_lista)
listagem.ui.tableWidget.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
atualizar()

table = listagem.ui.tableWidget
SelectedItem = None
def search():
    # Clear current selection.
    table.setCurrentItem(None)
    global SelectedItem
    
    if not listagem.ui.lineEdit.text():
        # Empty string, don't search.
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        #SelectedItem.setBackground(brush)
        return

    matching_items = table.findItems(listagem.ui.lineEdit.text(), Qt.MatchContains)
    def changetext():
        listagem.ui.lineEdit.setText("")

    if matching_items:
        # We have found something.
        item = matching_items[0]  # Take the first.
        selected = table.setCurrentItem(item)
        SelectedItem = item
        #table.currentItemChanged.connect(lambda: item == -1)
    else:
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        #SelectedItem.setBackground(brush)
        

listagem.ui.lineEdit.setPlaceholderText("Nº, Nome, Modelo...")
listagem.ui.lineEdit.textChanged.connect(search)
#app.aboutToQuit.connect(Update_Backup)
app.exec()

#Criando Tabela
""" create table clientes (
id INT NOT NULL AUTO_INCREMENT,
n INT(5),
nome VARCHAR(35),
modelo VARCHAR(60),
descricao VARCHAR(250),
valor VARCHAR(15),
situacao VARCHAR(22),
data VARCHAR(12),
garantia VARCHAR(24),
PRIMARY KEY (id) 
); """
# no

""" NSERT INTO clientes (nome,descricao,modelo,data,garantia) VALUES ("Lorena", "Tela Queimada", "J2 Prime", "21/02/2022", "sem garantia"); """