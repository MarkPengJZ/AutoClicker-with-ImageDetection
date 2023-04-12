import sys
import time
import pyautogui
import threading
from PIL import ImageGrab
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap


class App(QtWidgets.QMainWindow):
    decision_flag = False
    stop_while = False
    stop_for = False

    def __init__(self):
        super(App, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 200, 200, 300)
        self.setWindowTitle("Auto Clicker w Image Detection")

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabs.setMovable(True)
        self.helpTab = QtWidgets.QWidget()
        self.captureTab = QtWidgets.QWidget()
        self.selectTab = QtWidgets.QWidget()
        self.startTab = QtWidgets.QWidget()
        self.tabs.addTab(self.helpTab, "Guide")
        self.tabs.addTab(self.captureTab, "Select Screen Area")
        self.tabs.addTab(self.selectTab, "Select Picture to Find")
        self.tabs.addTab(self.startTab, "Start")
        self.helpTabUI()
        self.captureTabUI()
        self.selectTabUI()
        self.startTabUI()
        self.setCentralWidget(self.tabs)

    def helpTabUI(self):
        self.helpTab.layout = QtWidgets.QVBoxLayout()

        self.helpTab.text = QtWidgets.QLabel(self)
        self.helpTab.text.setText("*Instructions*\n1. Select screen area where you want to search for Picture\n2. "
                                  "Select Picture to Find\n3.Decide how many times to repeat Cycle and Start")
        self.helpTab.layout.addWidget(self.helpTab.text)

        self.helpTab.layout.addStretch()
        self.helpTab.setLayout(self.helpTab.layout)


    def startTabUI(self):
        self.startTab.layout1 = QtWidgets.QVBoxLayout()
        self.startTab.layout2 = QtWidgets.QGridLayout()
        self.startTab.layout3 = QtWidgets.QGridLayout()

        self.startTab.t1 = QtWidgets.QLabel("Cycle how many times:")
        self.startTab.l1 = QtWidgets.QLineEdit(self)
        self.startTab.layout2.addWidget(self.startTab.t1, 0, 0)
        self.startTab.layout2.addWidget(self.startTab.l1, 0, 1)

        self.startTab.b1 = QtWidgets.QPushButton(self)
        self.startTab.b1.setText("Start")
        self.startTab.b1.clicked.connect(self.startButton)
        self.startTab.b2 = QtWidgets.QPushButton(self)
        self.startTab.b2.setText("Stop")
        self.startTab.b2.clicked.connect(self.stopClick)
        self.startTab.layout3.addWidget(self.startTab.b1, 0, 0)
        self.startTab.layout3.addWidget(self.startTab.b2, 0, 1)

        self.startTab.layout1.addLayout(self.startTab.layout2)
        self.startTab.layout1.addLayout(self.startTab.layout3)
        self.startTab.layout1.addStretch()
        self.startTab.setLayout(self.startTab.layout1)

    def captureTabUI(self):
        self.captureTab.layout = QtWidgets.QVBoxLayout()

        self.captureTab.b1 = QtWidgets.QPushButton(self)
        self.captureTab.b1.setText("Capture Screen Area")
        self.captureTab.b1.clicked.connect(self.activateSnipping)
        self.captureTab.layout.addWidget(self.captureTab.b1)

        self.captureTab.text = QtWidgets.QLabel(self)
        self.captureTab.text.setText("Preview")
        self.captureTab.layout.addWidget(self.captureTab.text)

        self.captureTab.l1 = QtWidgets.QLabel(self)
        self.captureTab.l1.setFixedSize(200, 300)
        self.captureTab.l1.setStyleSheet("border :3px solid black;")
        self.captureTab.l1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.captureTab.pixmap = QPixmap('preview.jpg')
        self.captureTab.l1.setScaledContents(True)
        self.captureTab.l1.setPixmap(self.captureTab.pixmap)
        self.captureTab.l1.adjustSize()
        self.captureTab.layout.addWidget(self.captureTab.l1)

        self.captureTab.layout.addStretch()
        self.captureTab.setLayout(self.captureTab.layout)

        self.snipper = SnippingWidget()
        self.snipper.closed.connect(self.on_closed)

    def selectTabUI(self):
        self.selectTab.layout = QtWidgets.QVBoxLayout()

        self.selectTab.b1 = QtWidgets.QPushButton(self)
        self.selectTab.b1.setText("Select Image")
        self.selectTab.b1.clicked.connect(self.getfile)
        self.selectTab.layout.addWidget(self.selectTab.b1)

        self.selectTab.text = QtWidgets.QLabel(self)
        self.selectTab.text.setText("Selected Photo")
        self.selectTab.layout.addWidget(self.selectTab.text)

        self.selectTab.l1 = QtWidgets.QLabel(self)
        self.selectTab.l1.setFixedSize(200, 300)
        self.selectTab.l1.setStyleSheet("border :3px solid black;")
        self.selectTab.l1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.selectTab.pixmap = QPixmap('preview.jpg')
        self.selectTab.l1.setScaledContents(True)
        self.selectTab.l1.setPixmap(self.selectTab.pixmap)
        self.selectTab.layout.addWidget(self.selectTab.l1)

        self.selectTab.layout.addStretch()
        self.selectTab.setLayout(self.selectTab.layout)

    def startButton(self):
        threading.Thread(target=self.startClick).start()

    def startClick(self):
        filep = self.file_path
        x1 = self.snipper.startX
        y1 = self.snipper.startY
        x2 = self.snipper.endX
        y2 = self.snipper.endY
        width = x2 - x1
        height = y2 - y1
        cycle = int(self.startTab.l1.text())
        print(cycle, type(cycle))
        for i in range(cycle):
            time.sleep(2)
            if self.stop_for:
                self.stop_for = False
                break
            print("test")
            self.decision_flag = False
            while not self.decision_flag:
                if self.stop_while:
                    self.stop_while = False
                    break
                try:
                    x_centre, y_center = pyautogui.locateCenterOnScreen(filep, region=(x1, y1, width, height),
                                                                        confidence=0.7)
                    time.sleep(2)
                    print(x_centre, y_center)
                    pyautogui.click(x=x_centre, y=y_center, button='left')
                    print("Image found")
                    self.decision_flag = True
                except Exception as e:
                    print(f'image not found, trying again in 10 seconds', e)
                    time.sleep(5)

    def stopClick(self):
        print("stop cycle")
        self.stop_while = True
        self.stop_for = True

    def activateSnipping(self):
        self.snipper.showFullScreen()
        self.hide()

    def getfile(self):
        # Open a file dialog to select an image file
        self.file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image", "",
                                                                  "Image Files (*.png *.jpg *.jpeg "
                                                                  "*.bmp)")

        # Load the selected image file and display it in the QLabel
        if self.file_path:
            self.selectTab.l1.setScaledContents(False)
            self.selectTab.pixmap = QPixmap(self.file_path)
            self.selectTab.l1.setPixmap(self.selectTab.pixmap.scaled(200, 300, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
            self.selectTab.l1.adjustSize()

    def on_closed(self):
        self.snipper.hide()
        self.show()
        self.captureTab.l1.setScaledContents(False)
        self.captureTab.pixmap = QPixmap('./snips/tempImage.png')
        self.captureTab.l1.setPixmap(self.captureTab.pixmap.scaled(200, 300, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        self.captureTab.l1.adjustSize()


class SnippingWidget(QtWidgets.QMainWindow):
    closed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(SnippingWidget, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background:transparent;")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.outsideSquareColor = "red"
        self.squareThickness = 4

        self.startX = None
        self.startY = None
        self.endX = None
        self.endY = None
        self.start_point = QtCore.QPoint()
        self.end_point = QtCore.QPoint()

    def mousePressEvent(self, event):
        self.start_point = event.pos()
        self.end_point = event.pos()
        self.startX, self.startY = pyautogui.position()
        print(self.startX, self.startY)
        self.update()

    def mouseMoveEvent(self, event):
        self.end_point = event.pos()
        self.endX, self.endY = pyautogui.position()
        self.update()

    def mouseReleaseEvent(self, QMouseEvent):
        x1 = min(self.startX, self.endX)
        y1 = min(self.startY, self.endY)
        x2 = max(self.startX, self.endX)
        y2 = max(self.startY, self.endY)
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        img.save("snips/tempImage.png")
        self.closed.emit()

    def paintEvent(self, event):
        trans = QtGui.QColor(255, 255, 255)
        r = QtCore.QRectF(self.start_point, self.end_point).normalized()

        qp = QtGui.QPainter(self)
        trans.setAlphaF(0.2)
        qp.setBrush(trans)
        outer = QtGui.QPainterPath()
        outer.addRect(QtCore.QRectF(self.rect()))
        inner = QtGui.QPainterPath()
        inner.addRect(r)
        r_path = outer - inner
        qp.drawPath(r_path)

        qp.setPen(
            QtGui.QPen(QtGui.QColor(self.outsideSquareColor), self.squareThickness)
        )
        trans.setAlphaF(0)
        qp.setBrush(trans)
        qp.drawRect(r)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    application = App()
    application.show()
    sys.exit(app.exec_())
