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
import pyttsx
engine=pyttsx.init()

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
        engine.say(s)
        engine.runAndWait()
 
    def readText(self):
        text = self.te.toPlainText()
        print text
        engine.say(text)
        engine.runAndWait()

def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
