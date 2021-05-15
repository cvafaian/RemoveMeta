import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import subprocess

class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop Image Here \n\n')
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa
            }
        ''')

    def setPixmap(self, image):
        super().setPixmap(image)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.brief = "No changes have been made."
        self.text = "No image has been changed yet.\n\nDrag and drop image into box to remove metadata and generate information."
        self.resize(400, 400)
        self.setAcceptDrops(True)

        mainLayout = QVBoxLayout()

        self.photoViewer = ImageLabel()
        mainLayout.addWidget(self.photoViewer)

        button = QPushButton('Show Metadata', self)
        button.setToolTip('This will show image metadata from before and after it is changed')
        mainLayout.addWidget(button)

        button.clicked.connect(self.clickEvent)

        self.setLayout(mainLayout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.success(file_path)
            event.accept()

        else:
            event.ignore()

    def clickEvent(self):

        # msgBox = ScrollMessageBox(self.text)
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(self.brief)
        msgBox.setDetailedText(self.text)
        msgBox.setWindowTitle("Image Metadata")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()


    def success(self, file_path):
        self.photoViewer.setPixmap(QPixmap("images/success.png"))
        self.removeMeta(file_path)

    def removeMeta(self, file_path):
        text = "-------------------------------------------"
        text += "\n\n Metadata Present Before: \n\n"
        output = subprocess.run(["exiftool",  "-n", file_path], capture_output=True)
        text += output.stdout.decode("utf-8")
        text += "\n\n Metadata Present After: \n\n"
        output = subprocess.run(["exiftool",  "-all=", file_path], capture_output=True)
        text += output.stdout.decode("utf-8")
        self.brief = output.stdout.decode("utf-8")
        text += "\n"
        output = subprocess.run(["exiftool",  "-n", file_path], capture_output=True)
        text += output.stdout.decode("utf-8")
        text += "\n\n-------------------------------------------"
        self.text = text



if __name__ == '__main__':
    app = QApplication(sys.argv)
    run = App()
    run.show()
    sys.exit(app.exec_())
