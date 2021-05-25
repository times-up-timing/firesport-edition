#!/usr/bin/env python3
from serial import Serial
from serialworker import SerialWorker
from tools import ms_to_time

from form import Ui_Casomira


from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget
)

from PyQt5.QtGui import QIcon, QPixmap

data = None



class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicksCount = 0
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Freezing GUI")
        self.resize(300, 150)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        # Create and connect widgets
        self.clicksLabel = QLabel("Counting: 0 clicks", self)
        self.clicksLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.stepLabel = QLabel("Long-Running Step: 0")
        self.stepLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.countBtn = QPushButton("Click me!", self)
        self.countBtn.clicked.connect(self.countClicks)
        self.longRunningBtn = QPushButton("Long-Running Task!", self)
        self.longRunningBtn.clicked.connect(self.runLongTask)
        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.clicksLabel)
        layout.addWidget(self.countBtn)
        layout.addStretch()
        layout.addWidget(self.stepLabel)
        layout.addWidget(self.longRunningBtn)
        self.centralWidget.setLayout(layout)
    def countClicks(self):
        self.clicksCount += 1
        self.clicksLabel.setText(f"Counting: {self.clicksCount} clicks")

    def reportProgress(self, n):
        #print(ms_to_time(n))
        self.stepLabel.setText(ms_to_time(n))

    def runLongTask(self):
        # Step 2: Create a QThread object        
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = SerialWorker('/dev/cu.usbserial-0001')
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.work)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        self.longRunningBtn.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.longRunningBtn.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: self.stepLabel.setText("Long-Running Step: 0")
        )


app = QApplication(["Time's up - firesport edition",])
app.setWindowIcon(QIcon(QPixmap('icon.png')))
app.setApplicationName("Time's up - firesport edition")
#win = Ui_Casomira()
win = Window()
win.show()
#button = QtWidgets.QLabel("Click to Exit")
#button.setWindowTitle("Goodbye World")
#button.clicked.connect(app.quit)

#button.show()


if __name__ == "__main__":
    CORESVG_VERBOSE = True
    app.exec()

    

