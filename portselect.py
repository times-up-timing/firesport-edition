from serial.serialutil import SerialException
from serial.tools import list_ports
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class PortSelectWorker(QObject):

    finished = pyqtSignal()
    intReady = pyqtSignal(list)
    
    @pyqtSlot()
    def __init__(self):
        super(PortSelectWorker, self).__init__()
    
    def work(self):
        ports = list_ports.comports()
        self.intReady.emit(ports)
        # if line != '':
        # self.textEdit_3.append(line)
        self.finished.emit()