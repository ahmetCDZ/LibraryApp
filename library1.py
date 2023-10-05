import sys 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
import addbook
import addmember,givebook

con=sqlite3.connect('library.db')
cur=con.cursor()

class MyLibrary(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Big Library")
        self.setWindowIcon(QIcon('/Users/ahmetzincir/Desktop/PythonProjects/My Library/icons/icon.ico'))
        self.setGeometry(450,150,1350,750)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.toolbar()
        self.designs()
        self.getBooks()
        self.getMembers()
        self.getStatistics()

    def toolbar(self):
        self.tb=self.addToolBar(('Tool Bar'))
        self.tb.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.add_book=QAction(QIcon('/Users/ahmetzincir/Desktop/PythonProjects/My Library/icons/add_book.png'),"Add Book",self)
        self.add_book.triggered.connect(self.addBook)
        self.tb.addAction(self.add_book)
        self.tb.addSeparator()

        self.add_member=QAction(QIcon('/Users/ahmetzincir/Desktop/PythonProjects/My Library/icons/users.png'),"Add Member",self)
        self.tb.addAction(self.add_member)
        self.add_member.triggered.connect(self.addMembers)
        self.tb.addSeparator()

        self.give_book=QAction(QIcon('/Users/ahmetzincir/Desktop/PythonProjects/My Library/icons/givebook.png'),"Lend Book",self)
        self.give_book.triggered.connect(self.giveBook)
        self.tb.addAction(self.give_book)
        self.tb.addSeparator()
    def designs(self):

        main_layout=QHBoxLayout()
        main_left_layout=QVBoxLayout()
        main_right_layout=QVBoxLayout()
        main_layout.addLayout(main_left_layout,65)
        main_layout.addLayout(main_right_layout,35)

        self.tabs=QTabWidget(self)
        self.setCentralWidget(self.tabs)
        self.tabs.blockSignals(True)
        self.tabs.currentChanged.connect(self.tabChanged)
        self.tab1=QWidget()
        self.tab2=QWidget()
        self.tab3=QWidget()
        self.tabs.addTab(self.tab1,"Books")
        self.tabs.addTab(self.tab2,"Members")
        self.tabs.addTab(self.tab3,"Statistics")

        self.books_table=QTableWidget()
        self.books_table.setColumnCount(6)
        self.books_table.setColumnHidden(0,True)
        self.books_table.setHorizontalHeaderItem(0,QTableWidgetItem("Book Id"))
        self.books_table.setHorizontalHeaderItem(1,QTableWidgetItem("Book Name"))
        self.books_table.setHorizontalHeaderItem(2,QTableWidgetItem("Book Author"))
        self.books_table.setHorizontalHeaderItem(3,QTableWidgetItem("Book Page"))
        self.books_table.setHorizontalHeaderItem(4,QTableWidgetItem("Book Language"))
        self.books_table.setHorizontalHeaderItem(5,QTableWidgetItem("Book Status"))
        self.books_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.books_table.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)
        self.books_table.horizontalHeader().setSectionResizeMode(2,QHeaderView.Stretch)
        main_left_layout.addWidget(self.books_table)

        right_top_frame=QGroupBox(self)
        right_top_frame.setTitle('Search Box')
        right_top_frame.setObjectName('Main')
        right_top_frame.setStyleSheet('#Main{background-color:#fcc324;font: 15 pt Times Bold; color:white; border-radius:10px solid gray}')
        right_top_frame_box=QHBoxLayout(right_top_frame)
        right_top_frame_box.addStretch()
        lbl_search=QLabel("Search",right_top_frame)
        lbl_search.setStyleSheet('font: 13pt Times Bold; color::white')
        self.search_entry=QLineEdit(right_top_frame)
        search_button=QPushButton("Search",right_top_frame)
        search_button.clicked.connect(self.searchBooks)
        right_top_frame_box.addWidget(lbl_search)
        right_top_frame_box.addWidget(self.search_entry)
        right_top_frame_box.addWidget(search_button)
        right_top_frame_box.addStretch()
        main_right_layout.addWidget(right_top_frame)

        right_middle_frame=QGroupBox('List Books',self)
        right_middle_frame.setObjectName('Main')
        right_middle_frame.setStyleSheet('#Main{background-color:#fcc324;font: 15 pt Times Bold; color:white; border-radius:10px solid gray}')
        self.radio_btn1=QRadioButton("All Books",right_middle_frame)
        self.radio_btn2=QRadioButton("Avaiable Books",right_middle_frame)
        self.radio_btn3=QRadioButton("Borrowed Books",right_middle_frame)
        self.btn_list=QPushButton('List',right_middle_frame)
        self.btn_list.clicked.connect(self.listBooks)
        right_middle_box=QHBoxLayout(right_middle_frame)
        right_middle_box.addWidget(self.radio_btn1)
        right_middle_box.addWidget(self.radio_btn2)
        right_middle_box.addWidget(self.radio_btn3)
        right_middle_box.addWidget(self.btn_list)
        main_right_layout.addWidget(right_middle_frame)

        label=QLabel('Welcome to Big Library',self)
        label.setFont(QFont('Times',20))
        label.setContentsMargins(80,0,0,0)
        main_right_layout.addWidget(label)
        library_picture=QLabel(self)
        pixmap=QPixmap('/Users/ahmetzincir/Desktop/PythonProjects/My Library/icons/library.jpg')
        library_picture.setPixmap(pixmap)
        main_right_layout.addWidget(library_picture)
        self.tab1.setLayout(main_layout)

        member_main_layout=QHBoxLayout()
        member_left_layout=QHBoxLayout()
        member_right_layout=QVBoxLayout()
        member_main_layout.addLayout(member_left_layout,65)
        member_main_layout.addLayout(member_right_layout,35)
        self.member_table=QTableWidget()
        self.member_table.setColumnCount(3)
        self.member_table.setHorizontalHeaderItem(0,QTableWidgetItem("Member ID"))
        self.member_table.setHorizontalHeaderItem(1,QTableWidgetItem("Member Name"))
        self.member_table.setHorizontalHeaderItem(2,QTableWidgetItem("Member Phone Number"))
        self.member_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.member_table.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)
        self.member_table.horizontalHeader().setSectionResizeMode(2,QHeaderView.Stretch)
        member_left_layout.addWidget(self.member_table)
        self.tab2.setLayout(member_main_layout)

        member_search_group=QGroupBox("Search For Members")
        member_search_group.setObjectName('Main')
        member_search_group.setStyleSheet('#Main{background-color:#fcc324;font: 15 pt Times Bold; color:white; border-radius:10px solid gray}')
        member_right_layout_top=QHBoxLayout(member_search_group)
        lbl_member=QLabel("Search")
        self.entry_member_search=QLineEdit()
        button_member_search=QPushButton("Search")
        button_member_search.clicked.connect(self.searchMembers)
        member_right_layout_top.addWidget(lbl_member)
        member_right_layout_top.addWidget(self.entry_member_search)
        member_right_layout_top.addWidget(button_member_search)
        member_right_layout.addWidget(member_search_group)
        member_right_layout.addLayout(member_right_layout_top)
        
        statistics_main_layout=QVBoxLayout()
        self.statistic_group=QGroupBox("Statistic")
        self.statistic_form_layout=QFormLayout()
        self.total_books=QLabel("")
        self.total_members=QLabel("")
        self.taken_books=QLabel("")
        self.avaiable_books=QLabel("")
        self.statistic_form_layout.addChildWidget(self.statistic_group)
        self.statistic_form_layout.addRow(QLabel("Total Books:"),self.total_books)
        self.statistic_form_layout.addRow(QLabel("Total Members:"),self.total_members)
        self.statistic_form_layout.addRow(QLabel("Taken Books:"),self.taken_books)
        self.statistic_form_layout.addRow(QLabel("Avaiable Books:"),self.avaiable_books)
        self.statistic_group.setLayout(self.statistic_form_layout)
        statistics_main_layout.addWidget(self.statistic_group)
        self.tab3.setLayout(statistics_main_layout)
        self.tabs.blockSignals(False)
        
    

    def tabChanged(self,i):
         self.getMembers()
         self.getStatistics()
         self.getBooks()
         
    def addBook(self):
        self.addbook=addbook.AddBook()
    def addMembers(self):
         self.addmember=addmember.AddMember()
    def giveBook(self):
         self.givebook=givebook.GiveBook()
    def searchMembers(self):
         value=self.entry_member_search.text()
         if value=="":
              QMessageBox.information(self,"Uyarı","This line can not empty!")
         else:
              self.entry_member_search.setText("")
              query=cur.execute("select * from members where member_name like ?", ('%'+value+'%',)).fetchall()
             
              if query==[]:
                   QMessageBox.information(self,"Uyarı","There is no such a member !")
              else:
                    for i in reversed(range(self.member_table.rowCount())):
                         self.member_table.removeRow(i)
                    for row_data in query:
                        row_number=self.member_table.rowCount()
                        self.member_table.insertRow(row_number)
                        for column_number, data in enumerate(row_data):
                             self.member_table.setItem(row_number,column_number,QTableWidgetItem(str(data)))

                   
    def getStatistics(self):
         count_books=cur.execute("SELECT count(book_id) FROM books").fetchall()
         count_members=cur.execute("SELECT count(member_id) FROM members").fetchall()
         taken_books=cur.execute("SELECT count(book_status) FROM books WHERE book_status='Not Avaiable'").fetchall()
         avaiable_books=cur.execute("SELECT count(book_status) FROM books WHERE book_status='Avaiable'").fetchall()
         self.total_books.setText(str(count_books[0][0]))
         self.total_members.setText(str(count_members[0][0]))
         self.taken_books.setText(str(taken_books[0][0]))
         self.avaiable_books.setText(str(avaiable_books[0][0]))
    
    def getBooks(self):
        query=cur.execute("SELECT book_id,book_name,book_author,book_page,book_language,book_status FROM books")
        for row_data in query:
            row_number=self.books_table.rowCount()
            self.books_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.books_table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        
        self.books_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.books_table.doubleClicked.connect(self.selectedBook)
    
    def getMembers(self):
         for i in reversed(range(self.member_table.rowCount())):
              self.member_table.removeRow(i)
         query=cur.execute("select * from members")
         for row_data in query:
              row_number=self.member_table.rowCount()
              self.member_table.insertRow(row_number)

              for column_number, data in enumerate(row_data):
                   self.member_table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
         self.member_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
         self.member_table.doubleClicked.connect(self.selectedMember)
         
    def searchBooks(self):
        value=self.search_entry.text()
        if value=="":
            QMessageBox.information(self,"Uyarı","Lütfen aradığınız kitap hakkında bir bilgi giriniz..")
        else:
            query=cur.execute("SELECT book_id,book_name,book_author,book_page,book_language,book_status FROM books "
                              "WHERE book_name LIKE ? or book_author LIKE ?",
                              ('%'+value+'%','%'+value+'%')).fetchall()
            if query==[]:
                QMessageBox.information(self,"Uyarı","Böyle bir kitap yada yazar yok")
            else:
                for i in reversed(range(self.books_table.rowCount())):
                    self.books_table.removeRow(i)
                for row_data in query:
                    row_number=self.books_table.rowCount()
                    self.books_table.insertRow(row_number)
                    for column_number,data in enumerate(row_data):
                        self.books_table.setItem(row_number,column_number,QTableWidgetItem(str(data))) 

    def listBooks(self):
        if self.radio_btn1.isChecked()==True:
            query=cur.execute("SELECT book_id,book_name,book_author,book_page,book_language,book_status FROM books")
            for i in reversed(range(self.books_table.rowCount())):
                    self.books_table.removeRow(i)
            for row_data in query:
                    row_number=self.books_table.rowCount()
                    self.books_table.insertRow(row_number)
                    for column_number,data in enumerate(row_data):
                        self.books_table.setItem(row_number,column_number,QTableWidgetItem(str(data))) 

        elif self.radio_btn2.isChecked()==True:
            query=cur.execute("SELECT book_id,book_name,book_author,book_page,book_language,book_status FROM books WHERE book_status ='Avaiable'")
            for i in reversed(range(self.books_table.rowCount())):
                    self.books_table.removeRow(i)
            for row_data in query:
                    row_number=self.books_table.rowCount()
                    self.books_table.insertRow(row_number)
                    for column_number,data in enumerate(row_data):
                        self.books_table.setItem(row_number,column_number,QTableWidgetItem(str(data)))

        elif self.radio_btn3.isChecked()==True:
            query=cur.execute("SELECT book_id,book_name,book_author,book_page,book_language,book_status FROM books WHERE book_status ='Not Avaiable'")
            for i in reversed(range(self.books_table.rowCount())):
                    self.books_table.removeRow(i)
            for row_data in query:
                    row_number=self.books_table.rowCount()
                    self.books_table.insertRow(row_number)
                    for column_number,data in enumerate(row_data):
                        self.books_table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
    def selectedBook(self):
         global book_id
         book_list=[]
         for i in range(0,6):
              book_list.append(self.books_table.item(self.books_table.currentRow(),i).text())
         book_id=book_list[0]
         print(book_list)
         self.displaybook=DisplayBook()
         self.displaybook.show()
    def selectedMember(self):
         global member_id
         member_list=[]
         for i in range(0,3):
              member_list.append(self.member_table.item(self.member_table.currentRow(),i).text())
         member_id=member_list[0]
         self.displaymember=DisplayMember()
         self.displaymember.show()
class DisplayMember(QWidget):
      def __init__(self):
        super().__init__()
        self.setWindowTitle("Members Info")
        self.setWindowIcon(QIcon('/Users/ahmetzincir/Desktop/My Library/icons/icon.ico'))
        self.setGeometry(450,150,450,550)
        self.setFixedSize(self.size())
        self.UI()
        self.show()
      def UI(self):
        member=cur.execute("select * from members where member_id=?",(member_id,)).fetchall()
        taken_books=cur.execute("select books.book_name from barrows left join books on books.book_id=barrows.bbook_id where barrows.bmember_id=?",(member_id,)).fetchall()
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
        lbl_title=QLabel("Members Info",topFrame)
        lbl_title.setStyleSheet('color:#003f8a;font:25pt Times Bold')
        top_layout.addWidget(img_book)
        top_layout.addWidget(lbl_title)
        top_layout.addStretch()
        main_layout.addWidget(topFrame)

        self.name_entry=QLineEdit(bottomFrame)
        self.name_entry.setText(member[0][1])
        self.name_entry.setStyleSheet("background-color:white")
        self.phone_entry=QLineEdit(bottomFrame)
        self.phone_entry.setText(member[0][2])
        self.phone_entry.setStyleSheet("background-color:white")
        self.taken_list=QListWidget(bottomFrame)
        self.taken_list.setStyleSheet("background-color:white")
        if taken_books !=[]:
             for book in taken_books:
                  self.taken_list.addItem(book[0])
        else:
             self.taken_list.addItem("There was not taken books!!")
             
        delete_button=QPushButton("Delete",bottomFrame)
        delete_button.clicked.connect(self.deleteMember)
        delete_button.setStyleSheet("background-color:white")
        delete_button.move(200,320)
        
        bottom_layout.addRow(QLabel("Name:"),self.name_entry)
        bottom_layout.addRow(QLabel("Phone Number:"),self.phone_entry)
        bottom_layout.addRow(QLabel("Taken Books:"),self.taken_list)
        bottom_layout.addRow(QLabel(""),delete_button)
        main_layout.addWidget(bottomFrame)
        self.setLayout(main_layout) 

      def deleteMember(self):
        global member_id
        mbox=QMessageBox.question(self,"Warning","Are you sure to delete this Member?",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
        if mbox==QMessageBox.Yes:
            try:
                 cur.execute("delete from members where member_id=?",(member_id,))
                 con.commit()
                 QMessageBox.information(self,"Info","Member has been deleted!")
                 
            except:
                  QMessageBox.information(self,"Info","Member has not been deleted!")
         
class DisplayBook(QWidget):
     def __init__(self):
        super().__init__()
        self.setWindowTitle("Librarry Management")
        self.setWindowIcon(QIcon('/Users/ahmetzincir/Desktop/My Library/icons/icon.ico'))
        self.setGeometry(450,150,450,550)
        self.setFixedSize(self.size())
        self.UI()
        self.show()
     def UI(self):
        book=cur.execute("select * from books where book_id=?",(book_id,)).fetchall()
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
        lbl_title=QLabel("Add Book",topFrame)
        lbl_title.setStyleSheet('color:#003f8a;font:25pt Times Bold')
        top_layout.addWidget(img_book)
        top_layout.addWidget(lbl_title)
        top_layout.addStretch()
        main_layout.addWidget(topFrame)

        self.name_entry=QLineEdit(bottomFrame)
        self.name_entry.setStyleSheet("background-color:white")
        self.name_entry.setText(book[0][1])
        self.author_entry=QLineEdit(bottomFrame)
        self.author_entry.setStyleSheet("background-color:white")
        self.author_entry.setText(book[0][2])
        self.page_entry=QLineEdit(bottomFrame)
        self.page_entry.setStyleSheet("background-color:white")
        self.page_entry.setText(book[0][3])
        self.lan_entry=QLineEdit(bottomFrame)
        self.lan_entry.setStyleSheet("background-color:white")
        self.lan_entry.setText(book[0][5])
        self.description=QTextEdit(bottomFrame)
        self.description.setText(book[0][4])
        add_button=QPushButton("Delete",bottomFrame)
        add_button.clicked.connect(self.deletedBook)
        add_button.setStyleSheet("background-color:white")
        add_button.move(200,320)
        bottom_layout.addRow(QLabel("Name:"),self.name_entry)
        bottom_layout.addRow(QLabel("Author:"),self.author_entry)
        bottom_layout.addRow(QLabel("Page:"),self.page_entry)
        bottom_layout.addRow(QLabel("Language:"),self.lan_entry)
        bottom_layout.addRow(QLabel("Description:"),self.description)
        bottom_layout.addRow(QLabel(""),add_button)
        main_layout.addWidget(bottomFrame)
        self.setLayout(main_layout) 

     def deletedBook(self):
       global book_id
       mbox=QMessageBox.question(self,"Warning","Are you sure to delete this book?",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
       if mbox==QMessageBox.Yes:
            try:
                 cur.execute("delete from books where book_id=?",(book_id,))
                 con.commit()
                 QMessageBox.information(self,"Info","Book has been deleted!")
                 
            except:
                  QMessageBox.information(self,"Info","Book has not been deleted!")
        
def main():
    App=QApplication(sys.argv)
    window=MyLibrary()
    sys.exit(App.exec_())
if __name__=='__main__':
    main()
        
    
