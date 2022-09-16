#importation des modules
import unicodedata
from design.main_ui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
import time,threading,os,sqlite3,random
import locale,xlwt
import win32com.client as win32

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
        self.ui.stock.setValidator(self.onlyInt)


        


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
        self.ui.valider_12.clicked.connect(self.operation)

        self.ui.annuler.clicked.connect(self.renit)
        self.ui.suprimer.clicked.connect(lambda: self.supprimer("employes",self.id_employe))
        self.ui.modifier.clicked.connect(lambda: self.modifier("employes",self.id_employe))

        self.ui.table.clicked.connect(lambda : self.on_click("employe"))

        self.ui.table_client_3.clicked.connect(lambda : self.on_click("equipement"))
        self.ui.valider_6.clicked.connect(lambda: self.supprimer("equipement",self.id_equipement))
        self.ui.valider_7.clicked.connect(lambda: self.modifier("equipement",self.id_equipement))
        self.ui.valider_8.clicked.connect(self.renit)

        
        self.ui.supprimer4.clicked.connect(lambda: self.supprimer("operation",self.id_operation))
        self.ui.modifier4.clicked.connect(lambda: self.modifier("operation",self.id_operation))
        self.ui.table_client_4.clicked.connect(lambda : self.on_click("operation"))
        self.ui.annuler4.clicked.connect(self.renit)

       
        self.ui.exporter.clicked.connect(self.exportEmployeToExcel)
        self.ui.exporter2.clicked.connect(self.exportEquipementToExcel)
        self.ui.exporter3.clicked.connect(self.exportexportationToExcel)
        self.ui.exporter1.clicked.connect(self.exportpresenceToExcel)
        

        
        #threading.Thread(target=lambda : self.time()).start()
        
        #affiche la date actuel dans le QDateEdit
        #self.ui.date.setDateTime(QtCore.QDateTime.currentDateTime())
        
        self.init()
        self.fin=""
       
        self.border_right = "border-right: 2px solid rgb(255, 121, 198);"
        self.renit()

    def operation(self):
        try:
            materiel= self.ui.comboBox_2.currentText()
            type_operation = self.ui.comboBox.currentText()
            
            quantite = self.ui.spinBox.value()                
            date = self.ui.date_2.date() 
            date_py = date.toPyDate()
            date_string = date_py.strftime("%d/%m/%Y")
            cur=self.base.cursor()
        
            self.cur.execute("SELECT stock FROM equipement WHERE libelle = ?",(materiel,))
            stock_avant = self.cur.fetchone()
            self.base.commit()
            stock_initial = int(stock_avant[0])
            if (type_operation == "entrée"):
                stock_après = stock_initial+quantite
            elif (type_operation == "Sortie"):
                stock_après = stock_initial-quantite
                
            #try:
                
            data=(date_string,materiel,quantite,type_operation,stock_initial,stock_après)
            self.cur.execute("INSERT INTO operation( date , materiel , quantite , type_ope , stock_avant , stock_après )VALUES(?,?,?,?,?,?)",data)
                
            
            self.affichage_operation()
            new=(stock_après,materiel)
            self.cur.execute("UPDATE equipement SET stock = ? WHERE libelle = ? ",new)
            self.base.commit()
            """except:
            QMessageBox.warning(self,"erreur","<p style='color:black'>erreur</p>")"""
        except:
            msg = QMessageBox()
            msg.setWindowTitle("info")
            msg.setText("erreur, veuillez vérifier les champs")
            x = msg.exec_()

    def affichage_operation(self):
        try:
            self.cur.execute('SELECT date , materiel , quantite , type_ope , stock_avant , stock_après FROM operation')
            result = self.cur.fetchall()
            print(result)
            self.ui.table_client_4.setRowCount(0)
            for row_number, row_data in enumerate(result):
                    self.ui.table_client_4.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.ui.table_client_4.setItem(row_number, column_number,QTableWidgetItem(str(data)))
        except e:
                print(e)

    
            
            
        
            
    ## ses deux fonctions permettent d'exporter les tableview dans des fichiers excels
    def exportEmployeToExcel(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '', ".xls(*.xls)") 
        print(filename[0])
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
        self.add2(sheet)
        wbk.save(filename[0])

    def add2(self, sheet):
        for j in range(self.ui.table.model().columnCount()) :
            sheet.write(0,j,self.ui.table.horizontalHeaderItem(j).text())
        for currentColumn in range(self.ui.table.columnCount()):
            for currentRow in range(self.ui.table.rowCount()):
                teext = str(self.ui.table.item(currentRow, currentColumn).text())
                sheet.write(currentRow+1, currentColumn, teext)

    #exportation pour equipement


    def exportEquipementToExcel(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '', ".xls(*.xls)") 
        print(filename[0])
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
        self.add3(sheet)
        wbk.save(filename[0])

    def add3(self, sheet):
        for j in range(self.ui.table_client_3.model().columnCount()) :
            sheet.write(0,j,self.ui.table_client_3.horizontalHeaderItem(j).text())
        for currentColumn in range(self.ui.table_client_3.columnCount()):
            for currentRow in range(self.ui.table_client_3.rowCount()):
                teext = str(self.ui.table_client_3.item(currentRow, currentColumn).text())
                sheet.write(currentRow+1, currentColumn, teext)

    #export exportation

    def exportexportationToExcel(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '', ".xls(*.xls)") 
        print(filename[0])
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
        self.add4(sheet)
        wbk.save(filename[0])

    def add4(self, sheet):
        for j in range(self.ui.table_client_4.model().columnCount()) :
            sheet.write(0,j,self.ui.table_client_4.horizontalHeaderItem(j).text())
        for currentColumn in range(self.ui.table_client_4.columnCount()):
            for currentRow in range(self.ui.table_client_4.rowCount()):
                teext = str(self.ui.table_client_4.item(currentRow, currentColumn).text())
                sheet.write(currentRow+1, currentColumn, teext)

    #export presence
    def exportpresenceToExcel(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '', ".xls(*.xls)") 
        print(filename[0])
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
        self.add5(sheet)
        wbk.save(filename[0])

    def add5(self, sheet):
        for j in range(self.ui.table_client_5.model().columnCount()) :
            sheet.write(0,j,self.ui.table_client_5.horizontalHeaderItem(j).text())
        for currentColumn in range(self.ui.table_client_5.columnCount()):
            for currentRow in range(self.ui.table_client_5.rowCount()):
                teext = str(self.ui.table_client_5.item(currentRow, currentColumn).text())
                sheet.write(currentRow+1, currentColumn, teext)
        


    
                
    

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

        self.ui.valider_6.setEnabled(False)
        self.ui.valider_6.setStyleSheet(font)
        self.ui.valider_8.setEnabled(False)
        self.ui.valider_8.setStyleSheet(font)
        self.ui.valider_7.setEnabled(False)
        self.ui.valider_7.setStyleSheet(font)
        self.ui.libelle.setText("")
        self.ui.unite.setText("")
        self.ui.stock.setText("")

        self.ui.annuler4.setEnabled(False)
        self.ui.annuler4.setStyleSheet(font)
        self.ui.supprimer4.setEnabled(False)
        self.ui.supprimer4.setStyleSheet(font)
        self.ui.modifier4.setEnabled(False)
        self.ui.modifier4.setStyleSheet(font)

        self.ui.valider_13.setEnabled(False)
        self.ui.valider_13.setStyleSheet(font)
        self.ui.valider_16.setEnabled(False)
        self.ui.valider_16.setStyleSheet(font)
        self.ui.valider_15.setEnabled(False)
        self.ui.valider_15.setStyleSheet(font)
        
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
        self.cur.execute("""CREATE TABLE IF NOT EXISTS operation(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, date TEXT, materiel TEXT, quantite TEXT, type_ope TEXT, stock_avant TEXT, stock_après TEXT)""")
        self.base.commit()
        
        if not os.path.isfile("client"):
            with open("client","w") as f : f.write("{}")
        
        with open("client","r") as f :self.dico_client=eval(f.read())
        

        today = QtCore.QDate.currentDate()
        self.ui.date_2.setDate(today)
        self.acceuil()
        self.affichage_operation()
        
        #self.annule()
        self.ui.table.setStyleSheet("QTableView::item:selected { color:white; background:#000000; font-weight:900;}"
                           "QTableCornerButton::section { background-color:#232326; }"
                           "QTableView::item{ color:white;}"
                           "QHeaderView::section { color:white; background-color:#232326; }")
        self.ui.table_client_3.setStyleSheet("QTableView::item:selected { color:white; background:#000000; font-weight:900;}"
                           "QTableCornerButton::section { background-color:#232326; }"
                           "QTableView::item{ color:white;}"
                           "QHeaderView::section { color:white; background-color:#232326; }")
        self.ui.table_client_4.setStyleSheet("QTableView::item:selected { color:white; background:#000000; font-weight:900;}"
                           "QTableCornerButton::section { background-color:#232326; }"
                           "QTableView::item{ color:white;}"
                           "QHeaderView::section { color:white; background-color:#232326; }")
        self.ui.table_client_5.setStyleSheet("QTableView::item:selected { color:white; background:#000000; font-weight:900;}"
                           "QTableCornerButton::section { background-color:#232326; }"
                           "QTableView::item{ color:white;}"
                           "QHeaderView::section { color:white; background-color:#232326; }")

    
    

    

  
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
        libbele = self.ui.libelle.text()
        unite = self.ui.unite.text()
        stock=self.ui.stock.text()
        
        if libbele =="" or unite=="" or stock== "" :
            msg = QMessageBox()
            msg.setWindowTitle("info")
            msg.setText("veuillez remplir tous les champs")
            x = msg.exec_()
            return
        if self.modif != True :
            info = (libbele,unite,stock)
            self.insert_bd("equipement",info)
            self.affichage_equipement()
        else :
            info = (libbele,unite,stock,self.id_equipement)
            self.modif_bd("equipement",info)
            self.affichage_equipement()
            self.renit()
        self.renit()

    def enregistrement_presence(self):
        date= self.ui.date_3.currentText()
        noms= self.ui.comboBox_3.currentText()
        jours= self.ui.comboBox_4.currentText()
        pres=self.ui.comboBox_5.currentText()
        if self.modif != True :
            
                info = (date,noms,jours,pres)
                self.insert_bd("presence",info)
                self.affichage_presence()
                
        else:
                info = (date,noms,jours,pres)
                self.modif_bd("presence",info)
                self.affichage_presence()
                self.renit()
        self.renit()
        
        
            
            
            
    def enregistrement_employe(self):
        nom = self.ui.nom.text()
        prenoms = self.ui.prenoms.text()
        specialite = self.ui.specialite.text()
        salaire = self.ui.salaire.text()
        if nom=="" or prenoms=="" or specialite=="" or salaire=="" :
            msg = QMessageBox()
            msg.setWindowTitle("info")
            msg.setText("veuillez remplir tous les champs")
            x = msg.exec_()
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
                
                msg = QMessageBox()
                msg.setWindowTitle("info")
                msg.setText("succes")
                x = msg.exec_()
            elif table=="equipement":
                print("oo")
                
                self.cur.execute("INSERT INTO equipement(libelle,unite,stock) VALUES (?,?,?)",ligne)
                print("oo")
                self.base.commit()
               
                msg = QMessageBox()
                msg.setWindowTitle("info")
                msg.setText("succes")
                x = msg.exec_()
            elif table=="presence":
                print("oo")
                self.cur.execute("INSERT INTO presence(id ,semaine , nom , jour, presences) VALUES (?,?,?,?)",ligne)
                print("oo")
                self.base.commit()
                
            else:
                
                
                QMessageBox.information(self,"succes","enregistrement non effectué\n")
                
                
        except :
                print("e")
                msg = QMessageBox()
                msg.setWindowTitle("info")
                msg.setText("erreur, veuillez réssayer")
                x = msg.exec_()
                

    def modif_bd(self,table,ligne):
        
        try:
           
            if table=="employes":
                print("oo")
                self.cur.execute("UPDATE employes SET nom=?, prenoms=?, specialite=? , salaire=? WHERE id=?",ligne)
                print("oo")
                self.base.commit()
                
                msg = QMessageBox()
                msg.setWindowTitle("info")
                msg.setText("succes")
                x = msg.exec_()
            elif table=="equipement":
                print("oo")
                self.cur.execute("UPDATE equipement SET libelle=?, unite=?, stock=? WHERE id=?",ligne)
                print("oo")
                self.base.commit()
                
                msg = QMessageBox()
                msg.setWindowTitle("info")
                msg.setText("succes")
                x = msg.exec_()
            elif table=="operation":
                print("oo")
                self.cur.execute("UPDATE operation SET date=?, materiel=?, quantite=?,type_ope  WHERE id=?",ligne)
                print("oo")
                self.base.commit()
                msg = QMessageBox()
                msg.setWindowTitle("info")
                msg.setText("succes")
                x = msg.exec_()
            
                
            else:
                
                
                QMessageBox.information(self,"succes","enregistrement non effectué\n")
                
                
        except :
                print("e")
                msg = QMessageBox()
                msg.setWindowTitle("info")
                msg.setText("veuillez réssayer")
                x = msg.exec_()
                
    def affichage_presence(self):
        try:
            date= self.ui.date_3.currentText()
            self.cur.execute('SELECT * FROM presence WHERE semaine = ?',date)
            result = self.cur.fetchall()
            print(result)
            self.ui.table_client_5.setRowCount(0)
            for row_number, row_data in enumerate(result):
                    self.ui.table_client_5.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.ui.table_client_5.setItem(row_number, column_number,QTableWidgetItem(str(data)))
        except e:
            print(e)
            
    def affichage_equipement(self):
        try:
            self.cur.execute('SELECT * FROM equipement')
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

            data = ("entrée")
            cur.execute('SELECT materiel FROM operation where type_ope = ?',[data] )
            
            c=len(cur.fetchall())

            dato = ("Sortie")
            cur.execute('SELECT materiel FROM operation where type_ope = ?',[dato] )
            d=len(cur.fetchall())
                

            self.base.commit()
            cur.close()
            self.ui.label_13.setText(str(c))
            self.ui.label_15.setText(str(d))
            self.ui.label_6.setText(str(a))
            self.ui.label_11.setText(str(b))
        except:
            
            msg = QMessageBox()
            msg.setWindowTitle("info")
            msg.setText("succes")
            x = msg.exec_()
            
        

    def on_click(self,p):
        font = """font: 14pt "MS Shell Dlg 2";
                                    color: rgb(255, 255, 255);
                                    border:1px solid rgb(255, 85, 0);
                                    background-color:rgb(255, 85, 0);"""
        if p=="employe":
            self.row = self.ui.table.currentRow()
            self.id_employe=self.ui.table.item(self.row, 0).text()
        elif p=="equipement":
            self.row = self.ui.table_client_3.currentRow()
            self.id_equipement=self.ui.table_client_3.item(self.row, 0).text()
        elif p=="operation":
            self.row = self.ui.table_client_4.currentRow()
            self.id_operation=self.ui.table_client_4.item(self.row, 0).text()
        elif p=="presence":
            self.row = self.ui.table_client_5.currentRow()
            self.id_presence=self.ui.table_client_5.item(self.row, 0).text()
            

        self.ui.modifier.setEnabled(True)
        self.ui.modifier.setStyleSheet(font)
        self.ui.annuler.setEnabled(True)
        self.ui.annuler.setStyleSheet(font)
        self.ui.suprimer.setEnabled(True)
        self.ui.suprimer.setStyleSheet(font)

        self.ui.valider_7.setEnabled(True)
        self.ui.valider_7.setStyleSheet(font)
        self.ui.valider_8.setEnabled(True)
        self.ui.valider_8.setStyleSheet(font)
        self.ui.valider_6.setEnabled(True)
        self.ui.valider_6.setStyleSheet(font)

        self.ui.annuler4.setEnabled(True)
        self.ui.annuler4.setStyleSheet(font)
        self.ui.supprimer4.setEnabled(True)
        self.ui.supprimer4.setStyleSheet(font)
        self.ui.modifier4.setEnabled(True)
        self.ui.modifier4.setStyleSheet(font)

        self.ui.valider_13.setEnabled(True)
        self.ui.valider_13.setStyleSheet(font)
        self.ui.valider_16.setEnabled(True)
        self.ui.valider_16.setStyleSheet(font)
        self.ui.valider_15.setEnabled(True)
        self.ui.valider_15.setStyleSheet(font)
        
        
    def supprimer(self,table,id):
        try:
           
            cur=self.base.cursor()
            cur.execute('DELETE from '+table+' WHERE id=?',(id,))
            self.base.commit()
            self.renit()
            if table=="employes":
                self.affichage_employees()
            elif table == "equipement":
                self.affichage_equipement()
            elif table == "operation":
                self.affichage_operation()
                
                
        except:
            msg = QMessageBox()
            msg.setWindowTitle("info")
            msg.setText("erreur")
            x = msg.exec_()

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
            elif table=="equipement":
                self.cur.execute('SELECT * FROM equipement WHERE id=?',id)
                result = self.cur.fetchone()
                print(result)
                self.ui.libelle.setText(result[1])
                self.ui.unite.setText(result[2])
                self.ui.stock.setText(result[3])
            elif table == "operation":
            
                self.cur.execute('SELECT * FROM operation WHERE id=?',(id,))
                result = self.cur.fetchone()
                print(result)

            """elif table=="presence":
                self.cur.execute('SELECT * FROM presence WHERE id=?',id)
                result = self.cur.fetchone()
                print(result)
                self.ui.nom.setText(result[1])
                self.ui.prenoms.setText(result[2])
                self.ui.specialite.setText(result[3])
                self.ui.salaire.setText(result[4])
                #self.ui.comboBox_2.setCurrentText(result[2])
                #self.ui.spinBox.setValue(result[3])
                #self.ui.comboBox.setCurrentText(result[3])
                
                
                #self.affichage_employees()"""
        except:
            
            msg = QMessageBox()
            msg.setWindowTitle("info")
            msg.setText("succes")
            x = msg.exec_()
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
