#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QTabWidget, QMenuBar, QLineEdit, QSlider, QLabel
from simulation import *
import multiprocessing
import signal

from PyQt5.QtGui import QIcon

class Form(QMainWindow):
    def __init__(self):
        super(Form, self).__init__()
        self.initialize()
        self.t = None

    def start_simulation(self):
        s = Simulation(Buffer(Pattern([1, -1])))
        self.t = multiprocessing.Process(target=s.run)
        self.t.daemon = True
        self.t.start()

    def restart_simulation(self):
        if self.t.is_alive():
            os.kill(self.t.pid, signal.SIGINT)
        #the simulation should be restarted here
        #self.start_simulation()

    def initialize(self):
        tab_widget = QTabWidget()
        tab1 = QWidget()
        tab2 = QWidget()

        juggle_button = QPushButton("Juggle")
        restart_button = QPushButton("Restart")
        juggle_button.clicked.connect(self.start_simulation)
        restart_button.clicked.connect(self.restart_simulation)

        hbox = QHBoxLayout()
        hbox3 = QVBoxLayout()
        min_throw = QLineEdit(self)
        max_throw = QLineEdit(self)
        number_of_balls = QLineEdit(self)
        min_label = QLabel(self)
        max_label = QLabel(self)
        number_of_balls_label = QLabel(self)


        min_label.setText("min throw")
        max_label.setText("max throw")
        number_of_balls_label.setText("number of balls")

        hbox3.addWidget(min_label)
        hbox3.addWidget(min_throw)
        hbox3.addStretch(1)
        hbox3.addWidget(max_label)
        hbox3.addWidget(max_throw)
        hbox3.addWidget(number_of_balls_label)
        hbox3.addWidget(number_of_balls)

        hbox.addStretch(1)
        hbox.addWidget(restart_button)
        hbox.addWidget(juggle_button)

        vbox = QVBoxLayout(tab1)

        vbox.addLayout(hbox3)
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
