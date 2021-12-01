import os
import sys
from PyQt5.QtWidgets import QMainWindow,QDialog,QLineEdit,QHeaderView,QTableWidgetItem
from PyQt5.QtCore import pyqtSignal
from PyQt5.uic import loadUi

from DataManager.RoomManager import RoomManager

login_ui_file='Gui/login.ui'
main_ui_file='Gui/booking.ui'

manager_file='cache/room_manager.pkl'
admin_file='cache/admin.csv'
room_list_file='cache/room_list.csv'
token_file='cache/token'

class LoginWindow(QDialog):
    
    login_signal=pyqtSignal(dict)
    
    def __init__(self,parent=None):
        super(LoginWindow,self).__init__(parent)
        loadUi(login_ui_file,self)
        self.login_button.accepted.connect(self.login)
        self.login_button.rejected.connect(self.close)
        self.login_password.setEchoMode(QLineEdit.Password)
    
    def closeEvent(self,event):
        sys.exit(0)
    
    def login(self):
        username=self.login_username.text()
        password=self.login_password.text()
        remember=self.login_remember.isChecked()
        
        content={'username':username,
                 'password':password,
                 'remember':remember}

        self.login_signal.emit(content)
        

class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        loadUi(main_ui_file,self)
        
        self.manager=RoomManager(manager_file).load()
        self.manager.admin_from_csv(admin_file)
        self.manager.room_list_from_csv(room_list_file)
        
        self.token=None
        self.room_prop_count=6
        
        self.check_login()
        self.show_room_list()
        
    def login(self,content):
        username=content['username']
        password=content['password']
        remember=content['remember']
        self.token=self.manager.login(username,password)
        if self.token == False:
            self.check_login()
            return
        
        if remember:
            with open(token_file,'w+',encoding='utf-8') as f:
                f.write(self.token)
        
    def check_login(self):
        if os.path.exists(token_file):
            with open(token_file,'r+',encoding='utf-8') as f:
                self.token=f.read()
            if self.manager.check_token(self.token)!=-1:
                return True
        
        login_window=LoginWindow(self)
        login_window.login_signal.connect(self.login)
        login_window.exec_()
        
    def show_room_list(self):
        RoomData=self.manager.RoomData
        
        self.room_list.setRowCount(len(RoomData))
        self.room_list.setColumnCount(self.room_prop_count)
        self.room_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.room_list.setHorizontalHeaderLabels(['ID','Building','Name','Capacity','Type','Facilities'])
        row=0
        for room in RoomData.values():
            self.table_set_text(self.room_list,row,0,room.ID)
            self.table_set_text(self.room_list,row,1,room.Building)
            self.table_set_text(self.room_list,row,2,room.Name)
            self.table_set_text(self.room_list,row,3,room.Capacity)
            self.table_set_text(self.room_list,row,4,room.Type)
            self.table_set_text(self.room_list,row,5,room.Facilities)
            row+=1
    
    def table_set_text(self,table,row,col,text):
        item=QTableWidgetItem()
        item.setText(str(text))
        table.setItem(row,col,item)
    
    def closeEvent(self,event):
        self.manager.save()
        event.accept()

