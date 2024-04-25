import sys
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == '__main__': 
    app = QApplication(sys.argv)
    window = QWidget()
    # set title window
    window.setWindowTitle('Testing pyqt app') 
    # set position and size of window
    window.setGeometry(100,100,400,300)
    # display window on screen






    
    window.show()
    # enter loop
    sys.exit(app.exec_())
