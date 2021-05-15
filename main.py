import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
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
        self.resize(400, 400)
        self.setAcceptDrops(True)

        mainLayout = QVBoxLayout()

        self.photoViewer = ImageLabel()
        mainLayout.addWidget(self.photoViewer)

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


    def success(self, file_path):
        self.photoViewer.setPixmap(QPixmap("images/success.png"))
        self.removeMeta(file_path)


    def removeMeta(self, file_path):
        # create output text
        text = "-------------------------------------------------------------"
        text += "\n\n Metadata Present Before: \n\n"
        output = subprocess.run(["exiftool",  "-n", file_path], capture_output=True)
        text += output.stdout.decode("utf-8")
        text += "\n\n Metadata Present After: \n\n"
        output = subprocess.run(["exiftool",  "-all=", file_path], capture_output=True)
        text += output.stdout.decode("utf-8")
        text += "\n"
        output = subprocess.run(["exiftool",  "-n", file_path], capture_output=True)
        text += output.stdout.decode("utf-8")
        text += "\n\n-------------------------------------------------------------"
        file = open("output/logs.txt", "w+")
        file.write(text)
        file.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    run = App()
    run.show()
    sys.exit(app.exec_())
