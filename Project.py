from PyQt5.QtWidgets import  QApplication,QMainWindow,QFileDialog
from PyQt5.uic import loadUi    
import sys,os
import fitz
from PyQt5.QtWidgets import QMessageBox
from genarative_ai import generate_ai_response,generate_ai_response_for_image
class Main(QMainWindow):
    def __init__(self):
        super(Main,self).__init__()
        loadUi("Project.ui",self)
        
        self.current_path=None
        self.setWindowTitle("Untitled")
        self.pdf_contain=""
        self.prompt=""
        self.image=False
        self.img_file_path=''
        
        ## file
        self.actionNew.triggered.connect(self.new_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave_as.triggered.connect(self.save_as)

        
        ##Edit
        self.actionCopy.triggered.connect(self.Copy_Text)
        self.actionPaste.triggered.connect(self.Paste_text)
        self.actionCut.triggered.connect(self.Cut_text)
        self.actionUndo.triggered.connect(self.Undo_m)
        self.actionRedo.triggered.connect(self.Redu_m)

        #Apperence
        self.actionSet_Dark_Mode.triggered.connect(self.set_Dark_mode)
        self.actionSet_Light_Mode.triggered.connect(self.set_light_mode)
        self.actionSet_Font_Size.triggered.connect(self.font_size)

        #Ai button
        self.atteched_file.clicked.connect(self.atteched_clicked)
        self.send_button.clicked.connect(self.send_button_fun)
        self.clear.clicked.connect(self.clear_text)
        
       ## file  
    def new_file(self):
        if (self.textEdit.toPlainText() == "" and self.windowTitle() == "Untitled") or \
        (self.textEdit.toPlainText() != "" and self.windowTitle() != "Untitled"):
            self.textEdit.clear()
            self.setWindowTitle("Untitled")
            self.current_path = None
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setText("You don't want to save ")
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok )
            msg.buttonClicked.connect(self.button_clicked)
            msg.exec_()
    def button_clicked(self,button):
            self.textEdit.clear()
            self.setWindowTitle("Untitled")
            self.current_path = None
    def save_file(self):
        # print("save file ")
        if self.current_path is not None:
            filetext=self.textEdit.toPlainText()
            with open(self.current_path,'w') as f:
                f.write(filetext)
            
        else:
            self.save_as()
    def   save_as(self):
        file_path= QFileDialog.getSaveFileName(self,'Save File,',r'C:\Users\SOUMODIP\OneDrive\Desktop\PyQt','Text files(*.txt)')
        print(file_path)
        file_text=self.textEdit.toPlainText()
        if file_path[0]:
            with open(file_path[0],'w') as f:
                f.write(file_text)
        else:
            return
        self.current_path=file_path[0]
        self.setWindowTitle(file_path[0])
        
    def open_file(self):
        # print("open file ") 
        fname = QFileDialog.getOpenFileName(self,'Open File',r'C:\Users\SOUMODIP\OneDrive\Desktop\PyQt','Text files(*.txt)')  
        print(fname[0])
        # self.setWindowTitle(fname[0])
        if fname:
            with open(fname[0],'r') as f:
                filetext = f.read()
                self.textEdit.setText(filetext)
                self.current_path=fname[0]
                self.setWindowTitle(self.current_path)
        else:
            return
    ## Edit
    def Copy_Text(self):
        # print("Copy_Text")
        self.textEdit.copy()
    def Paste_text(self):
        # print("Paste_text  ")
        self.textEdit.paste()
    def Cut_text(self):
        self.textEdit.cut() 
    def Undo_m(self):
        # print("Undo_m")
        self.textEdit.undo()
    def Redu_m(self):
        self.textEdit.Redo()    
        
    #Appeerence
    def set_Dark_mode(self):
        # print("Dark")
        self.setStyleSheet('''QWidget{
            background-color: rgb(33,33,33);
            color: #FFFFFF;
            }
            QTextEdit{
            background-color: rgb(46,46,46);
            border: 2px solid #00BFFF;
            }
            QMenuBar::item:selected{
            color: #000000
            } 
            
            QPushButton {
        border: 2px solid #00BFFF;
        border-radius: 5px;
        padding: 5px;
        color: white;
        background-color: rgb(50, 50, 50);
    }


            ''')
    def set_light_mode(self):
        # print("Light")
        self.setStyleSheet("")
    def font_size(self):
        print("font")
    
    
    #AI    
    def atteched_clicked(self):
        # print("Fi")
        file_path=QFileDialog.getOpenFileName(self, "Open PDF File", "",
                                                   "Supported Files (*.pdf *.png *.jpg *.jpeg);;PDF Files (*.pdf);;Image Files (*.png *.jpg *.jpeg)")    
        if file_path:
            extension=os.path.splitext(file_path[0])[1].lower()
            # print(file_path[0])
            self.file_selec_or_not.setText(file_path[0])
            if extension == '.pdf':
                doc=fitz.open(file_path[0])
                text=""
                for page in doc:
                    text+=page.get_text()
                # print("PDF contain : ",text)
                self.pdf_contain=text
                doc.close()
            elif extension in ['.png','.jpg','.jpeg']:
                print("img") 
                self.image=True 
                self.img_file_path=os.path.basename(file_path[0]) 
            else:
                return
        else:
            return
    
    def send_button_fun(self):
        self.Ai_message_display.setText("loading...")
        self.text = self.Ai_send_message.toPlainText()
        

        if self.text != "" and  self.pdf_contain !="":
            self.prompt = f"""{self.text} \n Here is the content of the attached PDF:{self.pdf_contain}\n **If you are unable to understand the PDF content properly, please respond with a message indicating that a valid or proper PDF file is required.**"""
            # print("prompt"+self.prompt)
            result=generate_ai_response(prompt=self.prompt)
            self.Ai_message_display.setText(result)
            self.pdf_contain =""
            self.file_selec_or_not.setText("No file selected")
        elif self.text != "" and  self.pdf_contain =="" and self.image==False:
            self.prompt=self.text
            result=generate_ai_response(prompt=self.prompt)
            self.Ai_message_display.setText(result)
            
        elif self.img_file_path and self.text != "" and self.image:
            print("yes")
            propmt=f"""{self.text}\n **if you are unable to understand image or not found the image path give an error message**"""
            print(propmt,",",self.img_file_path)
            result=generate_ai_response_for_image(propmt,self.img_file_path)
            self.Ai_message_display.setText(result)
            self.image=False
            self.img_file_path=''
            self.file_selec_or_not.setText("No file selected")

        else:
            # print("hi")
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("You did't put any prompt")
            msg.setIcon(QMessageBox.Question)
            msg.exec_()

        self.Ai_send_message.setText("")
          
    def clear_text(self):
        self.Ai_message_display.setText("")
          
if __name__=="__main__":
    app=QApplication(sys.argv)
    ui=Main()
    ui.show()
    app.exec_()