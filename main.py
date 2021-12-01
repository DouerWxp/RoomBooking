from PyQt5.QtWidgets import QApplication
import sys

from DataManager.RoomManager import Room,RoomManager
from Gui.app import MainWindow

app=QApplication(sys.argv)
w=MainWindow()
w.show()
sys.exit(app.exec_())