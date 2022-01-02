#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Created :   2021/12/01, 22:53:40
@Changed :   2022/01/02 22:46:21
@Author  :   Wu Xiuping (2145265) 
@Contact :   douerwxp@gmail.com
'''

from PyQt5.QtWidgets import QApplication
import sys
from Gui.app import MainWindow

app=QApplication(sys.argv)
w=MainWindow()
w.show()
sys.exit(app.exec_())