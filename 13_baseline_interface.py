#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial 

In this example, we receive data from
a QtGui.QInputDialog dialog. 

author: Jan Bodnar
website: zetcode.com 
last edited: October 2011
"""

import sys, os
from PyQt4 import QtGui
<<<<<<< HEAD
#import pyttsx
#engine=pyttsx.init()
=======
import pyttsx
engine=pyttsx.init()
>>>>>>> 3b84ff36ea38bc7f74c8aa3a502af5802b8f133a

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()

        
    def initUI(self):      

        self.btn = QtGui.QPushButton('Speak', self)
        self.btn.move(20, 20)
        #self.btn.clicked.connect(self.showDialog)
        self.btn.clicked.connect(self.readText)
        
        self.te = QtGui.QTextEdit(self)
        self.te.move(130, 22)
        
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Text to Speech Demo')
        self.show()
        
    def showDialog(self):
        
        text, ok = QtGui.QInputDialog.getText(self, 'TTS Demo', 
            'Enter the text to read:')
        
        if ok:
            self.le.setText(str(text))
        s = str(text) 
        #cmd = 'espeak ' + s
        #print cmd
        #os.system(cmd) 
<<<<<<< HEAD
        #engine.say(s)
        #engine.runAndWait()
        cmd = 'echo s | festival --tts'
        os.system(cmd) 


    def readText(self):
        text = self.te.toPlainText()
        print text
        #engine.say(text)
        #engine.runAndWait()
        cmd = 'echo ' + str(text) + ' | festival --tts'
        os.system(cmd)
=======
        engine.say(s)
        engine.runAndWait()
 
    def readText(self):
        text = self.te.toPlainText()
        print text
        engine.say(text)
        engine.runAndWait()
>>>>>>> 3b84ff36ea38bc7f74c8aa3a502af5802b8f133a

def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
