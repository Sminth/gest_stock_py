#importation des modules
from design.main_ui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
import time,threading,os,sqlite3,random
import locale
locale.setlocale(locale.LC_TIME,'')

class main(QMainWindow):
    "classe principale"
    def __init__(self):
        super(main, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("itachi-alt.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.onlyInt = QIntValidator()
        self.ui.salaire.setValidator(self.onlyInt)

        
        #signal lors d'un clic sur un bouton

        self.ui.btn_home.clicked.connect(lambda: self.change(0))
        self.ui.btn_emp.clicked.connect(lambda: self.change(1))
        self.ui.btn_pres.clicked.connect(lambda: self.change(2))
        self.ui.btn_equip.clicked.connect(lambda: self.change(3))
        self.ui.btn_op.clicked.connect(lambda: self.change(4))
        self.ui.btn_param.clicked.connect(lambda: self.change(5))

        self.ui.enreg.clicked.connect(self.enregistrement_employe)
        
        #threading.Thread(target=lambda : self.time()).start()
        
        #affiche la date actuel dans le QDateEdit
        #self.ui.date.setDateTime(QtCore.QDateTime.currentDateTime())
        
        self.init()
        self.fin=""
        self.border_right = "border-right: 2px solid rgb(255, 121, 198);"
        
        
    def change(self,index):
        #print(self.styleSheet())
        #self.setStyleSheet(self.styleSheet()+"\n"+"QPushButton{border-right: 4px solid none;}")
        self.renitMenu()
        self.sender().setStyleSheet(self.sender().styleSheet()+"\n"+self.border_right)
        self.ui.stackedWidget.setCurrentIndex(index)


    def renitMenu(self):
        self.ui.btn_home.setStyleSheet(self.ui.btn_home.styleSheet()+"\n"+"border-right:none;")
        self.ui.btn_emp.setStyleSheet(self.ui.btn_emp.styleSheet()+"\n"+"border-right:  none;")

        self.ui.btn_pres.setStyleSheet(self.ui.btn_pres.styleSheet()+"\n"+"border-right:  none;")
        self.ui.btn_equip.setStyleSheet(self.ui.btn_equip.styleSheet()+"\n"+"border-right:  none;")
        self.ui.btn_op.setStyleSheet(self.ui.btn_op.styleSheet()+"\n"+"border-right:  none;")
        self.ui.btn_param.setStyleSheet(self.ui.btn_param.styleSheet()+"\n"+"border-right:  none;")
        
    def init(self):
        
        #print("initial")
        self.op=""

        #creation de la bd et des tables si ceux ci n'existe pas
        self.base = sqlite3.connect("stock.db")
        self.cur = self.base.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS employes(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, nom TEXT, prenoms TEXT, specialite TEXT, salaire TEXT)""")
        self.base.commit()
        
        """if not os.path.isfile("client"):
            with open("client","w") as f : f.write("{}")
        
        with open("client","r") as f :self.dico_client=eval(f.read())
        """
        
        #self.annule()
        self.ui.table.setStyleSheet("QTableView::item:selected { color:white; background:#000000; font-weight:900;}"
                           "QTableCornerButton::section { background-color:#232326; }"
                           "QTableView::item{ color:white;}"
                           "QHeaderView::section { color:white; background-color:#232326; }")


    def enregistrement_employe(self):
        nom = self.ui.nom.text()
        prenoms = self.ui.prenoms.text()
        specialite = self.ui.specialite.text()
     
        salaire = self.ui.salaire.text()
        
        if nom=="" or prenoms=="" or specialite=="" or salaire=="" :
            QMessageBox.warning(self,"erreur","<p style='color:black'>veillez remplir tous les champs svp</p>")

        else:
            info = {nom,prenoms,specialite,salaire}
            self.insert_bd("employes",info)
    def insert_bd(self,table,ligne):
        
        try:
           
            if table=="employes":
                print("oo")
                try:
                    self.cur.execute("INSERT INTO employes(nom, prenoms, specialite , salaire) VALUES (?,?,?,?)",ligne)
                    print("oo")
                    self.base.commit()
                except e:
                    print(e)
                QMessageBox.information(self,"succes","enregistrement effectuer\n")
                
            else:
                
                
                QMessageBox.information(self,"succes","enregistrement non effectué\n")
                
                
        except e:
                print(e)
                QMessageBox.warning(self,"erreur","une erreur est survenu ,enregistrement non effectuer\nmerci de réessayer!")
                
    def time(self):
        self.ui.jour.setText(time.strftime("%A %d %B"))
        while 1:
            self.ui.heure.setText(time.strftime("%H : %M"))
            time.sleep(1)
            if self.fin=="ok" : break
    def closeEvent(self,event):
        self.fin="ok"
        event.accept()
if __name__ == "__main__":
    import sys,os
    app = QtWidgets.QApplication(sys.argv)
    ui = main()
    ui.show()     #lancement de l'application
    sys.exit(app.exec_())
