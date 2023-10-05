import sys
import typing
from PyQt5 import QtCore 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
import library1

from PyQt5.QtWidgets import QWidget
con=sqlite3.connect('library.db')
cur=con.cursor()

class AddMember(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Members Management")
        self.setWindowIcon(QIcon('/Users/ahmetzincir/Desktop/PythonProjects/My Library/icons/icon.ico'))
        self.setGeometry(450,150,450,550)
        self.setFixedSize(self.size())
        self.UI()
        self.show()
    def UI(self):
        self.setStyleSheet('background-color:white')
        main_layout=QVBoxLayout()
        
        topFrame=QFrame(self)
        topFrame.setStyleSheet('background-color:white')
        top_layout=QHBoxLayout(topFrame)
        bottomFrame=QFrame(self)
        bottom_layout=QFormLayout(bottomFrame)
        bottomFrame.setStyleSheet('background-color:#fcc324')

        img_book=QLabel(topFrame)
        img=QPixmap('icons/addbook.png')
        img_book.setPixmap(img)
        top_layout.addStretch()
        lbl_title=QLabel("Add Member",topFrame)
        lbl_title.setStyleSheet('color:#003f8a;font:25pt Times Bold')
        top_layout.addWidget(img_book)
        top_layout.addWidget(lbl_title)
        top_layout.addStretch()
        main_layout.addWidget(topFrame)

        self.name_entry=QLineEdit(bottomFrame)
        self.name_entry.setPlaceholderText('Name of Member')
        self.name_entry.setStyleSheet("background-color:white")
        self.phone_entry=QLineEdit(bottomFrame)
        self.phone_entry.setPlaceholderText('Phone Number of Member')
        self.phone_entry.setStyleSheet("background-color:white")

        add_button=QPushButton("Add",bottomFrame)
        add_button.clicked.connect(self.addMember)
        add_button.setStyleSheet("background-color:white")
        add_button.move(200,320)
        bottom_layout.addRow(QLabel("Name:"),self.name_entry)
        bottom_layout.addRow(QLabel("Phone Number:"),self.phone_entry)
        bottom_layout.addRow(QLabel(""),add_button)
        main_layout.addWidget(bottomFrame)
        
         
        self.setLayout(main_layout) 

    def addMember(self):
        name=self.name_entry.text()
        phone=self.phone_entry.text()

        if(name and phone !=""):
            try:
                query="INSERT INTO 'members' (member_name,member_phone) VALUES(?,?)"
                cur.execute(query, (name, phone))
                con.commit()
                QMessageBox.information(self,"Warning","Member has been added")
            except:
                QMessageBox.information(self,"Warning","Member can't added")
        else:
            QMessageBox.information(self,"Warning","Fields can't empty")
      

       