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


        self.id_employe=0
        self.modif = False
        #signal lors d'un clic sur un bouton

        self.ui.btn_home.clicked.connect(lambda: self.change(0))
        self.ui.btn_emp.clicked.connect(lambda: self.change(1))
        self.ui.btn_pres.clicked.connect(lambda: self.change(2))
        self.ui.btn_equip.clicked.connect(lambda: self.change(3))
        self.ui.btn_op.clicked.connect(lambda: self.change(4))
        self.ui.btn_param.clicked.connect(lambda: self.change(5))
        
        self.ui.enreg.clicked.connect(self.enregistrement_employe)
        self.ui.valider_2.clicked.connect(self.enregistrement_equipement)
        self.ui.valider_14.clicked.connect(self.enregistrement_presence)

        self.ui.annuler.clicked.connect(self.renit)
        self.ui.suprimer.clicked.connect(lambda: self.supprimer("employes",self.id_employe))
        self.ui.modifier.clicked.connect(lambda: self.modifier("employes",self.id_employe))

        self.ui.table.clicked.connect(lambda : self.on_click("employe"))
        #threading.Thread(target=lambda : self.time()).start()
        
        #affiche la date actuel dans le QDateEdit
        #self.ui.date.setDateTime(QtCore.QDateTime.currentDateTime())
        
        self.init()
        self.fin=""
       
        self.border_right = "border-right: 2px solid rgb(255, 121, 198);"
        self.renit()
        
    def change(self,index):
        #print(self.styleSheet())
        #self.setStyleSheet(self.styleSheet()+"\n"+"QPushButton{border-right: 4px solid none;}")
        self.renitMenu()
        self.sender().setStyleSheet(self.sender().styleSheet()+"\n"+self.border_right)
        self.ui.stackedWidget.setCurrentIndex(index)
        print("o")
        if index == 3 : self.affichage_equipement()
        elif index == 1 : self.affichage_employees()
        elif index == 0 : self.acceuil()
        elif index == 2 : self.liste_employes()
        elif index == 4 : self.liste_equipement()


    def renit(self):
      
        font = """font: 14pt "MS Shell Dlg 2";
                                    color: rgb(255, 255, 255);
                                    border:1px solid rgb(163, 163, 163);
                                    background-color: rgb(163, 163, 163);"""
        self.ui.modifier.setEnabled(False)
        self.ui.modifier.setStyleSheet(font)
        self.ui.annuler.setEnabled(False)
        self.ui.annuler.setStyleSheet(font)
        self.ui.suprimer.setEnabled(False)
        self.ui.suprimer.setStyleSheet(font)
        self.ui.nom.setText("")
        self.ui.prenoms.setText("")
        self.ui.specialite.setText("")
        self.ui.salaire.setText("")
        self.modif=False
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
        self.cur.execute("""CREATE TABLE IF NOT EXISTS equipement(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, libelle TEXT, unite TEXT, stock TEXT)""")
        
        self.base.commit()
        
        """if not os.path.isfile("client"):
            with open("client","w") as f : f.write("{}")
        
        with open("client","r") as f :self.dico_client=eval(f.read())
        """

        today = QtCore.QDate.currentDate()
        self.ui.date_2.setDate(today)
        self.acceuil()
        #self.annule()
        self.ui.table.setStyleSheet("QTableView::item:selected { color:white; background:#000000; font-weight:900;}"
                           "QTableCornerButton::section { background-color:#232326; }"
                           "QTableView::item{ color:white;}"
                           "QHeaderView::section { color:white; background-color:#232326; }")

    
    

    def enregistrement_presence(self):
        a=self.ui.comboBox_3.currentText()
        print(a)





        


        """try:
    
            self.cur.execute('SELECT  FROM employes ')
            result = self.cur.fetchall()
            print(result)
            self.ui.table_client_3.setRowCount(0)
            for row_number, row_data in enumerate(result):
                    self.ui.table_client_3.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.ui.table_client_3.setItem(row_number, column_number,QTableWidgetItem(str(data)))
        except e:

                print(e)"""

  
    def liste_employes(self):
        
        cur=self.base.cursor()
        self.ui.comboBox_3.clear()
        cur.execute('SELECT * from employes')
        a=cur.fetchall()
        print(a)
        for i in a:
            noms = i[1]+" "+i[2]
            self.ui.comboBox_3.addItem(noms)

    def liste_equipement(self):

        cur=self.base.cursor()
        self.ui.comboBox_2.clear()
        cur.execute('SELECT * from equipement')
        a=cur.fetchall()
        print(a)
        for i in a:
            equip = i[1]
            self.ui.comboBox_2.addItem(equip)

        


    
    def enregistrement_equipement(self):
        libbele = self.ui.nom_5.text()
        unite = self.ui.nom_6.text()
        
        if libbele =="" or unite==""  :
            QMessageBox.warning(self,"erreur","<p style='color:black'>veillez remplir tous les champs svp</p>")
        else:
            info = (libbele,unite)
            self.insert_bd("equipement",info)

            
            self.affichage_equipement()
            
            
    def enregistrement_employe(self):
        nom = self.ui.nom.text()
        prenoms = self.ui.prenoms.text()
        specialite = self.ui.specialite.text()
        salaire = self.ui.salaire.text()
        if nom=="" or prenoms=="" or specialite=="" or salaire=="" :
            QMessageBox.warning(self,"erreur","<p style='color:black'>veillez remplir tous les champs svp</p>")
            return
        
        if self.modif != True :
            
                info = (nom,prenoms,specialite,salaire)
                self.insert_bd("employes",info)
                self.affichage_employees()
                
        else:
                info = (nom,prenoms,specialite,salaire,self.id_employe)
                self.modif_bd("employes",info)
                self.affichage_employees()
                self.renit()
        self.renit()

        
    def insert_bd(self,table,ligne):
        
        try:
           
            if table=="employes":
                print("oo")
                self.cur.execute("INSERT INTO employes(nom, prenoms, specialite , salaire) VALUES (?,?,?,?)",ligne)
                print("oo")
                self.base.commit()
                
                QMessageBox.information(self,"succes","enregistrement effectuer\n")
            elif table=="equipement":
                print("oo")
                
                self.cur.execute("INSERT INTO equipement(libelle,unite) VALUES (?,?)",ligne)
                print("oo")
                self.base.commit()
               
                QMessageBox.information(self,"succes","enregistrement effectuer\n")
                
            else:
                
                
                QMessageBox.information(self,"succes","enregistrement non effectué\n")
                
                
        except :
                print("e")
                QMessageBox.warning(self,"erreur","une erreur est survenu ,enregistrement non effectuer\nmerci de réessayer!")
                

    def modif_bd(self,table,ligne):
        
        try:
           
            if table=="employes":
                print("oo")
                self.cur.execute("UPDATE employes SET nom=?, prenoms=?, specialite=? , salaire=? WHERE id=?",ligne)
                print("oo")
                self.base.commit()
                
                QMessageBox.information(self,"succes","enregistrement effectuer\n")
            
                
            else:
                
                
                QMessageBox.information(self,"succes","enregistrement non effectué\n")
                
                
        except :
                print("e")
                QMessageBox.warning(self,"erreur","une erreur est survenu ,enregistrement non effectuer\nmerci de réessayer!")
                

    def affichage_equipement(self):
        try:
            self.cur.execute('SELECT libelle,unite FROM equipement')
            result = self.cur.fetchall()
            print(result)
            self.ui.table_client_3.setRowCount(0)
            for row_number, row_data in enumerate(result):
                    self.ui.table_client_3.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.ui.table_client_3.setItem(row_number, column_number,QTableWidgetItem(str(data)))
        except e:

                print(e)

    def affichage_employees(self):
        try:
            self.cur.execute('SELECT * FROM employes')
            result = self.cur.fetchall()
            print(result)
            self.ui.table.setRowCount(0)
            for row_number, row_data in enumerate(result):
                    self.ui.table.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.ui.table.setItem(row_number, column_number,QTableWidgetItem(str(data)))
        except e:
                print(e)
    def acceuil(self):
        try:
           
            cur=self.base.cursor()
            cur.execute('SELECT * from employes')
            a=len( cur.fetchall())
            cur.execute('SELECT * from equipement')
            b=len(cur.fetchall())
            self.base.commit()
            cur.close()
            
            self.ui.label_6.setText(str(a))
            self.ui.label_11.setText(str(b))
        except:
            QMessageBox.warning(self,"erreur","<p style='color:black'>erreur</p>")
        

    def on_click(self,p):
        font = """font: 14pt "MS Shell Dlg 2";
                                    color: rgb(255, 255, 255);
                                    border:1px solid rgb(255, 85, 0);
                                    background-color:rgb(255, 85, 0);"""
        if p=="employe":
            self.row = self.ui.table.currentRow()
            self.id_employe=self.ui.table.item(self.row, 0).text()

        self.ui.modifier.setEnabled(True)
        self.ui.modifier.setStyleSheet(font)
        self.ui.annuler.setEnabled(True)
        self.ui.annuler.setStyleSheet(font)
        self.ui.suprimer.setEnabled(True)
        self.ui.suprimer.setStyleSheet(font)
        
    def supprimer(self,table, id):
        try:
           
            cur=self.base.cursor()
            cur.execute('DELETE from '+table+' WHERE id=?',id)
            self.base.commit()
            self.renit()
            if table=="employes":
                self.affichage_employees()
        except:
            QMessageBox.warning(self,"erreur","<p style='color:black'>erreur</p>")

    def modifier(self,table, id):
        try:
            self.modif = True
            if table=="employes":
                self.cur.execute('SELECT * FROM employes WHERE id=?',id)
                result = self.cur.fetchone()
                print(result)
                self.ui.nom.setText(result[1])
                self.ui.prenoms.setText(result[2])
                self.ui.specialite.setText(result[3])
                self.ui.salaire.setText(result[4])
                #self.affichage_employees()
        except:
            QMessageBox.warning(self,"erreur","<p style='color:black'>erreur</p>")
    def time(self):
        today = QtCore.QDate.currentDate()
        self.ui.jour.setText(today)
        while 1:
            this_moment = QtCore.QTime.currentTime()
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
