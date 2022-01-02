# Room-Booking System

## Environment

python version: 3.8.0

install the packages:
```bash
pip install -r requirements.txt
```

## Run

Execute the file `main.py` in the root directory:

```bash
python main.py
```

Or you could run this program in the IDE like `pyCharm` by execute the file `main.py`

The default login information is following:

- username: admin
- password: 123456

And you also could add the login information you would like to the file `/cache/admin.csv`, which store  all users' login information of this system.

## Instruction

When first running this system, there will be a login window. input the username and password and click the OK button to log in.

After login is successful, you could see the main window. 

In the center is a table showing all rooms' details. Click any row of this table you could see the bookings of that room.

At the bottom is a text box that could output some notice. 

There are some text editors at the top of the window, you could input some conditions and click the Search button to filter the rooms. 

There are some control buttons at the right of the window, controlling the change of the table and the data.

## File Structure

The file structure of this project is following: 

```
.
│  main.py
│  README.md
│  requirements.txt
│  
├─cache
│  │  admin.csv
│  │  room_list.csv
│  │  room_manager.pkl
│  │  token
│  └─room_booking
│
├─DataManager
│    RoomManager.py
│          
├─Gui
│    admin.ui
│    app.py
│    confirm.ui
│    login.ui
│          
└─log
     roombooking.log
```

- `main.py` is the main script in this project, you can run this system by executing this file.
- `README.md` is some useful information about this project.
- `requirements.txt` is the files that record the packages information used in this project.
- `cache` is a directory including files storing temp data, and the csv files exported from the system are also store in this directory
- `cache/room_booking` is a directory including all the csv files which record the exported room's bookings
- `DataManager` is a directory including the python script about data management of room.
- `Gui` is a directory including the python script about the graph user interface and the files about page layouts.
- `log` is a directory recording the running log. 

## Author

- WU XIUPING
- douerwxp@gmail.com