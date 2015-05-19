#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QTabWidget, QMenuBar, QLineEdit, QSlider, QLabel, QCheckBox, QComboBox
from simulation import *
from buffer import *
from random_pattern import *
import multiprocessing
import signal

from PyQt5.QtGui import QIcon

class Form(QMainWindow):
    def __init__(self):
        super(Form, self).__init__()
        self.initialize()
        self.t = None

    def start_simulation(self):

        if self.enable_random_cb.isChecked():
            dist_text = self.distribution.currentText()
            dist = "u"
            if dist_text == "Geometric":
                dist = "g"
            if self.number_of_balls.text() == '' or self.max_throw.text() == '' or self.min_throw == '':
                print("invalid input!")
                return
            random_pattern = RandomPattern(int(self.number_of_balls.text()), int(self.min_throw.text()), int(self.max_throw.text()), dist_type=dist)
            buffer = Buffer(random_pattern)
            simulation = Simulation(buffer)
            self.t = multiprocessing.Process(target=simulation.run)
            self.t.daemon = True
            self.t.start()
        else:
            text = str(self.pattern.text())
            if not len(text) > 0:
                return
            p = [int(e) for e in text.split(" ")]
            if p != None:
                s = Pattern(p)
                buffer = Buffer(s)
                simulation = Simulation(buffer)
                self.t = multiprocessing.Process(target=simulation.run)
                self.t.daemon = True
                self.t.start()

    def restart_simulation(self):
        if self.t.is_alive():
            os.kill(self.t.pid, signal.SIGINT)
        #the simulation should be restarted here
        #self.start_simulation()

    def initialize(self):
        self.tab_widget = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.juggle_button = QPushButton("Juggle")
        #restart_button = QPushButton("Restart")
        self.juggle_button.clicked.connect(self.start_simulation)
        #restart_button.clicked.connect(self.restart_simulation)

        self.hbox = QHBoxLayout()
        self.hbox3 = QVBoxLayout()
        self.min_throw = QLineEdit(self)
        self.max_throw = QLineEdit(self)
        self.pattern = QLineEdit(self)
        self.number_of_balls = QLineEdit(self)
        self.min_label = QLabel(self)
        self.max_label = QLabel(self)
        self.pattern_label = QLabel(self)
        self.number_of_balls_label = QLabel(self)
        self.enable_random_cb = QCheckBox("Enable random pattern", self)
        self.distribution = QComboBox(self)
        self.distribution_label = QLabel(self)
        self.distribution.addItem("Uniform")
        self.distribution.addItem("Geometric")

        self.min_label.setText("min throw")
        self.max_label.setText("max throw")
        self.number_of_balls_label.setText("number of balls")
        self.pattern_label.setText("Pattern (only used if random pattern is not enabled)")
        self.distribution_label.setText("Distribution for the random pattern")

        self.hbox3.addWidget(self.min_label)
        self.hbox3.addWidget(self.min_throw)
        self.hbox3.addStretch(1)
        self.hbox3.addWidget(self.max_label)
        self.hbox3.addWidget(self.max_throw)
        self.hbox3.addWidget(self.number_of_balls_label)
        self.hbox3.addWidget(self.number_of_balls)
        self.hbox3.addWidget(self.pattern_label)
        self.hbox3.addWidget(self.pattern)
        self.hbox3.addWidget(self.enable_random_cb)
        self.hbox3.addWidget(self.distribution_label)
        self.hbox3.addWidget(self.distribution)
        self.hbox.addStretch(1)
        #hbox.addWidget(restart_button)
        self.hbox.addWidget(self.juggle_button)

        self.vbox = QVBoxLayout(self.tab1)

        self.vbox.addLayout(self.hbox3)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.hbox)

        self.hbox2 = QHBoxLayout(self.tab2)

        self.tab_widget.addTab(self.tab1, "Main")
        #self.tab_widget.addTab(self.tab2, "Other")

        self.setCentralWidget(self.tab_widget)

        self.menubar = self.menuBar()
        self.file_menu = self.menubar.addMenu('&File')
        self.help_menu = self.menubar.addMenu('&Help')
        self.about = self.help_menu.addMenu('&About')
        self.exit_action = QAction(QIcon('exit.png'), '&Exit', self)
        self.exit_action.triggered.connect(qApp.quit)
        self.file_menu.addAction(self.exit_action)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Juggling Simulator')
        self.show()

def main():

    juggling_app = QApplication(sys.argv)

    win = Form()
    sys.exit(juggling_app.exec_())

main()
