from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from serial import Serial, serialutil
import datetime as dt
from tools import ms_to_time

class SerialWorker(QObject):
    """
    This class provides inetface to serial port
    """
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    
    @pyqtSlot()
    def __init__(self, serial_port):
        super(SerialWorker, self).__init__()
        self._working = True
        self._serial_port = serial_port
    
    def work(self):
        #try:
        '''    serial = Serial()
            serial.port = self._serial_port
            serial.baudrate = 115200
            serial.dtr = True
            serial.rts = False
            serial.open()'''
        with Serial(port=self._serial_port, baudrate=115200) as serial:
            serial.dtr = False
            serial.rts = False
            while self._working:
                try:
                    line = serial.readline().decode('ascii').strip().split(';')[0]
                    line = int(line)
                    
                    self.progress.emit(line)
                except Exception:
                    pass
        '''finally:
            serial.close()'''
        self.finished.emit()