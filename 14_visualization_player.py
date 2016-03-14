#! /usr/bin/python

from PyQt4 import QtCore
from PyQt4 import QtGui

import sys
import math
import struct
import wave

class SoundWidget(QtGui.QWidget):
    margin = 10

    white = QtGui.QColor(255, 255, 255)
    grey = QtGui.QColor(50, 50, 50)
    data_color = QtGui.QColor(0, 0, 250)

    def __init__(self, sound, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.drag = 0
        self.sound = sound
        # 
        self.preprocess(sound)
        # 
        self.render(sound)

    def dt(self):
        return self.tend - self.tbegin

    def time_of(self, x):
        return self.tbegin + (self.dt() * x)/self.width()

    def to_samples(self, rawdata):
        ampls = []
        bytes_per_sample = self.sound.getsampwidth()
        if bytes_per_sample == 1:
            for i in range(len(rawdata)):
                ampls.append( struct.unpack(" self.soundlen:
            self.tend = self.soundlen

        # prepare image
        self.image = QtGui.QImage(self.width(), self.height(), QtGui.QImage.Format_RGB32)
        self.image.fill(self.white.rgb())

        painter = QtGui.QPainter(self.image)
        painter.setPen(QtGui.QPen(self.data_color))

        # lines or regions
        sound.setpos(int(self.tbegin * sound.getframerate()))
        nsamples = int(self.dt() * sound.getframerate())
        data = self.to_samples( sound.readframes(nsamples) )

        #if nsamples < self.width():
        #    pass
        #else:
        for x in range(self.width()):
            start_sample = int(x * nsamples / float(self.width()))
            # get [min; max] amplitude over pixel interval
            min_ampl = 0
            max_ampl = 0
            for i in range(int(nsamples/float(self.width()))):
                try:
                    if data[start_sample + i] < min_ampl:
                        min_ampl = data[start_sample + i]
                    if data[start_sample + i] > max_ampl:
                        max_ampl = data[start_sample + i]
                except IndexError: pass

            # draw it
            y1 = int(self.height() * (1 - max_ampl)/2.0)
            y2 = int(self.height() * (1 - min_ampl)/2.0)
            painter.drawLine(x, y1, x, y2)
                

    def drawGrid(self, painter):
        painter.setPen(QtGui.QPen(self.grey))

        ### draw vertical lines
        # get magnitude of deltaT
        if self.dt() == 0: bt
        if self.dt() < 1:
            magn = 0.1
            while self.dt()/magn < 1: magn /= 10.0
        else:
            magn = 1
            while self.dt()/(magn + 1) > 1: magn *= 10.0;
        # draw
        tfrom = magn * int(self.tbegin/magn)
        for i in range(10):
            ti = tfrom + i * magn
            x = self.width() * (ti - self.tbegin)/self.dt()
            painter.drawLine(x, self.margin, x, self.height() - 2 * self.margin)       
            # text
            painter.drawText(x, self.height() - self.margin, str(ti))
        ### draw horisontal lines
        step = 0.25
        for i in range(int(2.0/step) - 1):
            ry = -0.75 + i * step
            y = int(self.height() * (1 - ry) /2)
            painter.drawLine(self.margin, y, self.width() - self.margin, y)
            painter.drawText(self.margin, y, str(ry))
        
    def paintEvent(self, event):
        pntr = QtGui.QPainter(self)
        pntr.drawImage(self.image.rect(), self.image, self.image.rect())
        self.drawGrid(pntr)

    def resizeEvent(self, event):
        #print('soundwidget.width == %d x %d' % (self.width(), self.height()))
        self.render(self.sound)
        self.repaint()

    def wheelEvent(self, event):
        #print('wheel event, delta = %f at x=%d' % (event.delta(), event.x()))
        
        x = event.x()
        t = self.tbegin + (self.dt() * x)/self.width()

        k = math.exp(event.delta() / 2000.0)
        self.tbegin = t - (t - self.tbegin) * k
        self.tend = t + (self.tend - t) * k
   
        self.render(self.sound)
        self.repaint()

    def mousePressEvent(self, event):
        self.drag = self.time_of(event.x())
        
    def mouseReleaseEvent(self, event):
        self.drag = 0

    def mouseMoveEvent(self, event):
        if self.drag:
            new_t = self.time_of(event.x())
            self.tbegin += (self.drag - new_t)
            self.tend += (self.drag - new_t)  
            self.drag = new_t
        
            self.render(self.sound)
            self.repaint()
              
class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        ltMain = QtGui.QVBoxLayout()
        
        if len(sys.argv) < 2: fname = "ma3.wav"
        else: fname = sys.argv[1]
        
        wsound = SoundWidget(wave.open(fname), self)

        tabSound = QtGui.QTabWidget()
        tabSound.addTab(wsound, 'A(t)')

        ltMain.addWidget(tabSound)
        self.setLayout(ltMain)

        wsound.resize(self.width() - 4, self.height() - 4)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = Window()
    w.resize(700, 300)
    w.show()
    app.exec_()
