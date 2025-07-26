from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow
import sys

# using normal function , problem is you cant play with lebel after click button
def button_clicked():
    print("clicked")

def window():
    app=QApplication(sys.argv)
    win=QMainWindow()
    x_axis=200
    y_axis=200 
    width=500
    heigth=300
    win.setGeometry(x_axis,y_axis,width,heigth)
    win.setWindowTitle("Rocky's code")
    
    
    label=QtWidgets.QLabel(win)
    label.setText("Hey this is new things for me ")
    label.move(150,150)
    
    
    b1=QtWidgets.QPushButton(win)
    b1.setText("Click me")
    b1.clicked.connect(button_clicked)
    
    
    
    win.show()
    
    
    sys.exit(app.exec_())
    
# window()



class myWindow(QMainWindow):
    def __init__(self):
        super(myWindow,self).__init__()
        x_axis=200
        y_axis=200
        width=500
        heigth=300
        self.setGeometry(x_axis,y_axis,width,heigth)
        self.setWindowTitle("Rocky's code")
        self.initUI()
        
    def initUI(self):
        self.label=QtWidgets.QLabel(self)
        self.label.setText("Text from class")
        self.label.move(50,50)
        
        self.b1=QtWidgets.QPushButton(self)
        self.b1.setText("Click me")
        self.b1.clicked.connect(self.button_clicked)

    def button_clicked(self):
        self.label.setText("You pressed the button")
        self.upadate_label_text_size()
        
    def upadate_label_text_size(self):
        self.label.adjustSize()
    
def window2():
    app=QApplication(sys.argv)
    win=myWindow()
    
    win.show()
    sys.exit(app.exec_())
window2()