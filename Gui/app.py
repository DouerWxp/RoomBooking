from collections import defaultdict
import os
import sys
from PyQt5.QtWidgets import QMainWindow,QDialog,QLineEdit,QHeaderView,QTableWidgetItem,QAbstractItemView, QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5.uic import loadUi

from DataManager.RoomManager import BOOKING, RoomManager,Room

# ui files
login_ui_file='Gui/login.ui'
admin_ui_file='Gui/admin.ui'
confirm_ui_file='Gui/confirm.ui'

# data files
manager_file='cache/room_manager.pkl'
admin_file='cache/admin.csv'
room_list_file='cache/room_list.csv'
token_file='cache/token'

class LoginWindow(QDialog):
    
    # signal connect to the main window
    login_signal=pyqtSignal(dict)
    
    def __init__(self,parent=None):
        super(LoginWindow,self).__init__(parent)
        loadUi(login_ui_file,self)
        self.login_button.accepted.connect(self.login)
        self.login_button.rejected.connect(self.close)
        self.login_password.setEchoMode(QLineEdit.Password)
    
    # send the username and password to the main window checking if correct
    def login(self):
        username=self.login_username.text()
        password=self.login_password.text()
        remember=self.login_remember.isChecked()
        
        content={'username':username,
                 'password':password,
                 'remember':remember}
        # delivery the login info to the main window
        self.login_signal.emit(content)
    
    # if close the login window, then exit the whole program
    def closeEvent(self,event):
        sys.exit(0)

class ConfirmWindow(QDialog):
    
    confirm_signal=pyqtSignal(dict)
    
    def __init__(self,parent=None):
        super(ConfirmWindow,self).__init__(parent)
        loadUi(confirm_ui_file,self)
        
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)
    
    # set the text in the text box
    def set_text(self,text):
        self.textBrowser.setText(text)
    
    def accept(self):
        content={'accepted':True}
        self.confirm_signal.emit(content)
        self.buttonBox.accepted.disconnect(self.accept)
        self.close()
    
    def reject(self):
        self.close()
    
    def closeEvent(self,event):
        event.accept()
            
    
        

class MainWindow(QWidget):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        self.resize(1,1)
        
        self.manager=RoomManager(manager_file).load()
        self.manager.admin_from_csv(admin_file)
        
        self.token=None
        self.auth=None
        self.check_login()
        
        if self.auth==0:
            window=AdminWindow(self.manager,self.token,self)
            window.show()
            
        
    def login(self,content):
        username=content['username']
        password=content['password']
        remember=content['remember']
        self.token=self.manager.login(username,password)
        if self.token == False:
            self.check_login()
            return
        
        self.auth=self.manager.check_token(self.token)
        self.user=self.manager.get_user(self.token)
        if remember:
            with open(token_file,'w+',encoding='utf-8') as f:
                f.write(self.token)
        
    def check_login(self):
        if os.path.exists(token_file):
            with open(token_file,'r+',encoding='utf-8') as f:
                self.token=f.read()
            if self.manager.check_token(self.token)!=-1:
                self.auth=self.manager.check_token(self.token)
                self.user=self.manager.get_user(self.token)
                return True
        
        login_window=LoginWindow(self)
        login_window.login_signal.connect(self.login)
        login_window.exec_()
    
    def closeEvent(self,event):
        pass


class AdminWindow(QMainWindow):
    def __init__(self,manager:RoomManager,token,parent=None):
        super(AdminWindow,self).__init__(parent)
        
        self.manager=manager
        self.token=token
        self.user=self.manager.get_user(self.token)
        self.room_prop_count=6
        self.booking_prop_count=5
        # record the type of page shown
        self.page=None
        # record the id of the room operated now
        self.room_now=None
        # record the row selected now
        self.row_selected=None
        
        loadUi(admin_ui_file,self)
        self.back_button.clicked.connect(self.back)
        
        self.edit_button.clicked.connect(self.edit_table)
        self.add_button.clicked.connect(self.add_row)
        self.confirm_button.clicked.connect(self.confirm_change)
        self.delete_button.clicked.connect(self.try_del_row)
        self.search_button.clicked.connect(self.search_room)
        self.export_button.clicked.connect(self.export)
        
        self.room_list_table.cellDoubleClicked.connect(self.entrance_room_booking)
        self.room_list_table.cellClicked.connect(self.record_row)
        self.room_booking_table.cellClicked.connect(self.record_row)
        
        
        self.pages={}
        self.pages['room']=[self.room_list_table]
        self.pages['booking']=[self.room_booking_table]
        
        self.show_room_list(self.manager.RoomData)
        
    # change visible of forms by the content of self.page
    def change_visible(self):
        for key,value in self.pages.items():
            if key==self.page:
                for item in value:
                    item.setVisible(True)
            else:
                for item in value:
                    item.setVisible(False)
    
    # show room list in the table of the main window
    def show_room_list(self,RoomData):
        self.page='room'
        self.change_visible()
        
        table=self.room_list_table
        
        table.setRowCount(len(RoomData))
        table.setColumnCount(self.room_prop_count)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setHorizontalHeaderLabels(['ID','Building','Name','Capacity','Type','Facilities'])
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        row=0
        for room in RoomData.values():
            self.table_set_text(table,row,0,room.ID)
            self.table_set_text(table,row,1,room.Building)
            self.table_set_text(table,row,2,room.Name)
            self.table_set_text(table,row,3,room.Capacity)
            self.table_set_text(table,row,4,room.Type)
            self.table_set_text(table,row,5,room.Facilities)
            row+=1
    
    def entrance_room_booking(self,row,col):
        # get the room_id selected and record it
        room_id=int(self.get_table_text(row,0))
        self.room_now=room_id
        self.show_room_booking(room_id)
    
    # show room bookings in the table of the main window
    def show_room_booking(self,room_id):
        self.page='booking'
        self.change_visible()
        
        room=self.manager.RoomData[room_id]
        bookings=room.bookings
        
        
        table=self.room_booking_table
        table.setRowCount(len(bookings))
        table.setColumnCount(self.booking_prop_count)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setHorizontalHeaderLabels(['booking_id','room_id','user','start_time','end_time'])
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        row=0
        for booking in bookings.values():
            self.table_set_text(table,row,0,booking.booking_id)
            self.table_set_text(table,row,1,booking.room_id)
            self.table_set_text(table,row,2,booking.user)
            self.table_set_text(table,row,3,booking.start_time)
            self.table_set_text(table,row,4,booking.end_time)
            row+=1
    
    # get conditions from the GUI window, filter the rooms and show the valid rooms in the window
    def search_room(self):
        conditions={'ID':self.ID_edit.text(),
                    'Building':self.Building_edit.text(),
                    'CapacityMin':self.CapacityMin_edit.text(),
                    'CapacityMax':self.CapacityMax_edit.text(),
                    'Type':self.Type_edit.text(),
                    'Facilities':self.Facilities_edit.text(),
                    'StartTime':self.StartTime_edit.text(),
                    'EndTime':self.EndTime_edit.text()}
        
        RoomData=self.manager.search_room(**conditions)
        if type(RoomData)!=defaultdict:
            self.log('Please check the valid of search conditions')
            self.log(RoomData)
        else:
            self.show_room_list(RoomData)
            if len(RoomData)==0:
                self.log('There is no room that matches the conditions. Please Change the filter criteria and try again')
        pass
    
    # get the table shown now
    def get_table_shown(self):
        if self.page=='room':
            return self.room_list_table
        if self.page=='booking':
            return self.room_booking_table
        self.log('page error!')
    
    # get the text in a location of table
    def get_table_text(self,row,col):
        table=self.get_table_shown()
        item=table.item(row,col)
        if item==None:
            return None
        return item.text()
    
    # let the table could be edited
    def edit_table(self):
        self.confirm_button.setText('Confirm*')        
        
        table=self.get_table_shown()
        table.setEditTriggers(QAbstractItemView.CurrentChanged)
        self.log('start edit......')
    
    # record the row clicked now
    def record_row(self,row,col):
        self.row_selected=row
    
    # add a new row to the table shown now
    def add_row(self):
        self.confirm_button.setText('Confirm*')
        
        
        table=self.get_table_shown()
        table.setRowCount(table.rowCount()+1)
        self.edit_table()
        if self.page=='booking':
            # generate the booking id
            self.table_set_text(table,table.rowCount()-1,0,self.manager.booking_count)
            self.manager.booking_count+=1
            # generate the room id
            self.table_set_text(table,table.rowCount()-1,1,self.room_now)
            # generate the username
            self.table_set_text(table,table.rowCount()-1,2,self.user)
        if self.page=='room':
            # generate the room id
            self.table_set_text(table,table.rowCount()-1,0,self.manager.room_count)
            self.manager.room_count+=1

    # delete a row and try to delete the data
    def try_del_row(self):
        confirm_window=ConfirmWindow(self)
        confirm_window.confirm_signal.connect(self.delete_row)
        self.manager.reset_count()

        if self.page=='room':
            # get the room id of the room selected
            try:
                room_id=int(self.get_table_text(self.row_selected,0))
                text='Delete the room: '+str(room_id)
                confirm_window.set_text(text)
            except:
                self.log('Error, Please check the row selected')
                return
            
        if self.page=='booking':
            try:
                # get the room id of the room selected
                room_id=self.room_now
                booking_id=int(self.get_table_text(self.row_selected,0))
                text='Delete the booking: '+str(booking_id)+'on the room '+str(room_id)
                confirm_window.set_text(text)
            except:
                self.log('Error, Please check the row selected')
                return
        
        confirm_window.exec_()
    
    # really delete a row data
    def delete_row(self,accepted):
        if not accepted:
            return
        
        try:
            if self.page=='room':
                room_id=int(self.get_table_text(self.row_selected,0))
                # execute the operation of delete room
                status=self.manager.delete_room(self.token,room_id)
                if status:
                    self.log('Delete room '+str(room_id)+' successful')
                else:
                    self.log('Delete failure')
                # flash page
                self.show_room_list(self.manager.RoomData)
            
            if self.page=='booking':
                booking_id=int(self.get_table_text(self.row_selected,0))
                # execute the operation of delete booking
                status=self.manager.delete_booking(self.token,booking_id)
                if status:
                    self.log('Delete booking '+str(booking_id)+' successful')
                else:
                    self.log('Delete failure')
                # flash page
                self.show_room_booking(self.room_now)
                
        except (Exception,BaseException) as e:
            self.log(e)
      
    # save the change of data
    def confirm_change(self):
        self.confirm_button.setText('Confirm')
        self.manager.reset_count()
        
        
        table=self.get_table_shown()
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        rows=table.rowCount()
        cols=table.columnCount()
        if self.page=='room':
            for row in range(rows):
                room_info=[]
                for col in range(cols):
                    item=table.item(row,col)
                    if item==None:
                        self.log('The info in '+str((row,col))+' is None, Please check it')
                        self.show_room_list(self.manager.RoomData)
                        return
                    room_info.append(item.text())
                room_info=tuple(room_info)
                self.manager.add_room(self.token,room_info)
            self.show_room_list(self.manager.RoomData)
        
        if self.page=='booking':
            for row in range(rows):
                booking_info=[]
                for col in range(cols):
                    item=table.item(row,col)
                    if item==None:
                        self.log('Error! The info in '+str((row,col))+' is invalid, Please check it')
                        self.show_room_booking(self.room_now)
                        return
                    booking_info.append(item.text())
                if int(booking_info[1])!=self.room_now:
                    self.log('Error! Please check the room id')
                    self.show_room_booking(self.room_now)
                booking_info[0]=int(booking_info[0])
                booking_info[1]=int(booking_info[1])
                booking_info=BOOKING(*booking_info)
                self.manager.add_booking(self.token,booking_info)
            self.show_room_booking(self.room_now)
        self.log('Confirm table change')
        
    # change the text in the table 
    def table_set_text(self,table,row,col,text):
        item=QTableWidgetItem()
        item.setText(str(text))
        table.setItem(row,col,item)
    
    # export the data to the csv file
    def export(self):
        if self.page=='room':
            self.manager.room_list_to_csv(room_list_file)
            self.log('Export successful, the file is in the path /'+room_list_file)
        
        if self.page=='booking':
            filepath=self.manager.RoomData[self.room_now].booking_to_csv()
            self.log('Export successful, the file is in the path '+filepath)
        
    # back to last page
    def back(self):
        self.manager.reset_count()
        if self.page=='room':
            return
        if self.page=='booking':
            self.show_room_list(self.manager.RoomData)
            return
    
    # print the log to the text box
    def log(self,text):
        self.console_text.append(str(text))
    
    # some command would be execute when the window is closed
    def closeEvent(self,event):
        self.manager.save()
        event.accept()
        sys.exit(0)

