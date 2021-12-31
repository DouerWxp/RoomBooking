import os
from collections import namedtuple,defaultdict
import datetime
import time
import hashlib
import logging
import dill
import pandas as pd

#log initialization
if not os.path.exists('log'):
    os.mkdir('log')
logging.basicConfig(filename='log/roombooking.log',level=logging.INFO)

#structure three types 
BOOKING=namedtuple('Booking',['booking_id','room_id','user','start_time','end_time'])
CANCEL=namedtuple('Cancel',['cancel_id','booking_id'])
TOKENMEM=namedtuple('TempToken',['expired_time','token','authority'])

#identify a class to store room information
class Room(object):
    def __init__(self,ID:int,Building:str,Name:str,Capacity:int,Type:str,Facilities:str):
        super().__init__()
        
        #init attribute information
        self.ID=int(ID)
        self.Building=Building
        self.Name=Name
        self.Capacity=int(Capacity)
        self.Type=Type
        self.Facilities=Facilities
        
        #init booking information
        self.bookings=defaultdict(BOOKING)
        self.save_dir='cache/room_booking/'
        
    
    #update Room information  
    def update_info(self,ID:int=None,Building:str=None,Name:str=None,Capacity:int=None,Type:str=None,Facilities:str=None):
        if not ID==None:
            self.ID=ID
        if not Building==None:
            self.Building=Building
        if not Name==None:
            self.Name=Name
        if not Capacity==None:
            self.Capacity=Capacity
        if not Type==None:
            self.Type=Type
        if not Facilities==None:
            self.Facilities=Facilities
    
    # booking process
    # input: booking information
    # output: success(True) or error(False)
    def book(self,booking):
        if self.is_available(booking):
            self.bookings[booking.booking_id]=(booking)
            logging.info('booking successful')
            return True
        logging.error('Time clash')
        return False
    
    # cancel booking 
    # input: booking ID
    # output: success(True) or error(False)
    def cancel(self,booking_id):
        if booking_id in self.bookings.keys():
            self.bookings.pop(booking_id)
            return True
        return False
    
    #check if the booking time is available
    def is_available(self,booking):
        available=True
        
        for exist_booking in self.bookings.values():
            if self.str2time(booking.start_time)>=self.str2time(exist_booking.start_time) and self.str2time(booking.start_time)<self.str2time(exist_booking.end_time):
                available=False
            if self.str2time(booking.end_time)>self.str2time(exist_booking.start_time) and self.str2time(booking.end_time)<=self.str2time(exist_booking.end_time):
                available=False
        
        return available
    
    # store the booking information in a csv file
    def booking_to_csv(self):
        df=pd.DataFrame(columns=['user','start_time','end_time'])
        for booking in self.bookings.values():
            booking_data={'user':booking.user,
                          'start_time':booking.start_time,
                          'end_time':booking.end_time}
            df=df.append(booking_data,ignore_index=True)
        df.to_csv(self.save_dir+'room'+str(self.ID)+str(self.Name)+'.csv',index=False)
    
    def str2time(self,time_str):
        return datetime.datetime.strptime(time_str,"%Y-%m-%d %H:%M")


# identify a class to manage rooms
class RoomManager(object):
    def __init__(self,datafile):
        super().__init__()
        self.datafile=datafile
        self.RoomData=defaultdict(Room)
        self.access_guest_token=defaultdict(str)
        self.access_admin_token=defaultdict(str)
        
        self.token_mem=defaultdict(TOKENMEM)
        self.booking_queue=defaultdict(BOOKING)
        self.booking_count=0
        
        self.cancel_queue=defaultdict()
        self.cancel_count=0
        
        self.load()
    
    # generate token by username and password
    def gen_token(self,username,password):
        return hashlib.sha256(str.encode(str(username)+str(password))).hexdigest()
    
    # check token authorities
    def check_token(self,token):
        username=self.get_user(token)
        if username in self.access_admin_token.keys():
            return 0
        if username in self.access_guest_token.keys():
            return 1
        return -1
    
    # identify user by token 
    def get_user(self,token):
        for username,value in self.token_mem.items():
            if value.token==token:
                return username
        return False
    
    # register a new account checking if the username has been used
    def register(self,username,password):
        
        if username in self.access_guest_token.keys() or username in self.access_admin_token.keys():
            print('This username has been used')
            return False
        
        self.access_guest_token[username]=self.gen_token(username,password) 
        print('Register Successful')
        return True
    
    # import the username and password of managers
    def admin_from_csv(self,filepath):
        df=pd.read_csv(filepath)
        for _,row in df.iterrows():
            username=row['username']
            password=row['password']
            self.access_admin_token[username]=self.gen_token(username,password)
        return
    
    # log in
    # if log in successful return template token otherwise False
    def login(self,username,password):
        login_token=self.gen_token(username,password)
        
        if (username,login_token) in self.access_admin_token.items() or (username,login_token) in self.access_guest_token.items():
            temp_token=self.gen_token(username+str(time.time),password)
            self.token_mem[username]=TOKENMEM((datetime.datetime.now()+datetime.timedelta(days=30)),temp_token,0)
            return temp_token
        
        return False
          
    def load(self):
        if os.path.exists(self.datafile):
            with open(self.datafile,'rb') as f:
                return dill.load(f)
        return self
    
    def save(self):
        with open(self.datafile,'wb') as f:
            self=dill.dump(self,f)

    # bulk import room information 
    def room_list_from_csv(self,filepath):
        if not os.path.exists(filepath):
            return False
        
        df=pd.read_csv(filepath)
        for _,row in df.iterrows():
            if row['ID'] in self.RoomData.keys():
                self.RoomData[row['ID']].update_info(row['ID'],row['Building'],row['Name'],row['Capacity'],row['Type'],row['Facilities'])
            else:
                self.RoomData[row['ID']]=Room(row['ID'],row['Building'],row['Name'],row['Capacity'],row['Type'],row['Facilities'])
        return True
    
    # bulk export room information
    def room_list_to_csv(self,filepath):
        df=pd.DataFrame(columns=['ID','Building','Name','Capacity','Type','Facilities'])
        for room in self.RoomData.values():
            row_data={'ID':room.ID,
                      'Building':room.Building,
                      'Name':room.Name,
                      'Capacity':room.Capacity,
                      'Type':room.Type,
                      'Facilities':room.Facilities}
            df=df.append(row_data,ignore_index=True)
        df.to_csv(filepath,index=False)
        return
    
    # get booking information of all rooms 
    def get_booking_list(self):
        booking_list=defaultdict(BOOKING)
        for room in self.RoomData.values():
            for booking in room.bookings.values():
                booking_list[booking.booking_id]=booking
                
        return booking_list
    
    def search_room(self,**conditions):
        RoomData=self.RoomData.copy()
        # ID filter
        try:
            if 'ID' in conditions.keys() and conditions['ID']!='':
                for room_id in list(RoomData.keys()):
                    if RoomData[room_id].ID !=int(conditions['ID']):
                        RoomData.pop(room_id)
            
            # Building filter
            if 'Building' in conditions.keys() and conditions['Building']!='':
                for room_id in list(RoomData.keys()):
                    if RoomData[room_id].Building.lower() !=conditions['Building'].lower():
                        RoomData.pop(room_id)
                        
            # Name filter
            # if 'Name' in conditions.keys() and conditions['Name']!='':
            #     for room_id,room in RoomData.items():
            #         if RoomData[room_id].Name !=conditions['Name']:
            #             RoomData.pop(room_id)
            
            # Capacity filter
            if 'CapacityMin' in conditions.keys() and conditions['CapacityMin']!='':
                for room_id in list(RoomData.keys()):
                    if RoomData[room_id].Capacity < int(conditions['CapacityMin']):
                        RoomData.pop(room_id)
            if 'CapacityMax' in conditions.keys() and conditions['CapacityMax']!='':
                for room_id in list(RoomData.keys()):
                    if RoomData[room_id].Capacity > int(conditions['CapacityMax']):
                        RoomData.pop(room_id)
            
            # Type filter
            if 'Type' in conditions.keys() and conditions['Type']!='':
                for room_id in list(RoomData.keys()):
                    if RoomData[room_id].Type.lower() !=conditions['Type'].lower():
                        RoomData.pop(room_id)
            
            # Facilities filter
            if 'Facilities' in conditions.keys() and conditions['Facilities']!='':
                for room_id in list(RoomData.keys()):
                    if self.check_facility(conditions['Facilities'],RoomData[room_id].Facilities):
                        RoomData.pop(room_id)
        except (Exception,BaseException) as e:
            return e
        return RoomData
    
    def check_facility(facilities:str,room_facilities:str):
        facilities=facilities.lower()
        facilities=facilities.split()
        room_facilities=room_facilities.lower()
        for facility in facilities:
            if facility not in room_facilities:
                return False
        return True
    
    # the valid operations of admin
    # add room
    def add_room(self,token:str,room:Room):
        if self.check_token(token)==0:
            for exist_room in self.RoomData.values():
                if room.ID==exist_room.ID:
                    print('ID clash: the ID of rooms should be different')
                    return False
            self.RoomData[room.ID]=room
            return True
        return False
    
    # delete room
    def delete_room(self,token,room_id:int):
        if self.check_token(token)==0:
            self.RoomData.pop(room_id)
            return True
        return False 
    
    # add booking 
    def add_booking(self,token,booking:BOOKING):
        if self.check_token(token)==0:
            room_id=int(booking.room_id)
            self.RoomData[room_id].book(booking)
            return True
        return False
    
    # delete booking 
    def delete_booking(self,token,booking_id):
        if self.check_token(token)==0:
            booking_list=self.get_booking_list()
            if booking_id in booking_list.keys():
                room_id=booking_list[booking_id].room_id
                return self.RoomData[room_id].cancel(booking_id)
        return False
    
    # the valid operations of guests
    # add booking operation in the booking queue
    def book_room(self,token,ID,start_time,end_time):
        if self.check_token(token)==-1:
            return False
        user=self.get_user(token)
        if user == None:
            return False
        self.booking_queue[self.booking_count]=BOOKING(self.booking_count,ID,user,start_time,end_time)
        self.booking_count+=1
        return True
    
    # add canceling operation in the canceling queue
    def cancel_book(self,token,booking_id):
        if self.check_token(token)==-1:
            return False
        user=self.get_user(token)
        if user == None:
            return False
        self.cancel_queue[self.cancel_count]=CANCEL(self.cancel_count,booking_id)
        self.cancel_count+=1
        return True

