#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QTabWidget, QMenuBar

from PyQt5.QtGui import QIcon

class Form(QMainWindow):
    def __init__(self):
        super(Form, self).__init__()
        self.initialize()

    def start_simulation(self):
        os.system("python2 gfxExample.py")

    def initialize(self):
        tab_widget = QTabWidget()
        tab1 = QWidget()
        tab2 = QWidget()

        juggle_button = QPushButton("Juggle")
        juggle_button.clicked.connect(self.start_simulation)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(juggle_button)

        vbox = QVBoxLayout(tab1)
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        hbox2 = QHBoxLayout(tab2)

        tab_widget.addTab(tab1, "Main")
        tab_widget.addTab(tab2, "Other")

        self.setCentralWidget(tab_widget)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        help_menu = menubar.addMenu('&Help')
        about = help_menu.addMenu('&About')
        exit_action = QAction(QIcon('exit.png'), '&Exit', self)
        exit_action.triggered.connect(qApp.quit)
        file_menu.addAction(exit_action)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Juggling Simulator')
        self.show()

def main():

    juggling_app = QApplication(sys.argv)

    win = Form()
    sys.exit(juggling_app.exec_())

main()
