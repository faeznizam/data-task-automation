# import module from subfolder
from task_code import task_onetimeconversion, task_month2_6, task_burnt, task_response_leads, task_token
from task_code import task_winbacknfp


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit, QFileDialog, QComboBox
import logging


def browse_folder():
    folder_path = QFileDialog.getExistingDirectory(window, 'Select Folder', '.') 
    if folder_path:

        selected_processing_option = processing_options.currentText()
        output_box.append("Selected processing option: " + selected_processing_option)
        
        if selected_processing_option == "TM One Time Conversion To Pledge":
            task_onetimeconversion.task_onetimeconversion_main(folder_path)
        elif selected_processing_option == "TM On Hold Hard and Soft Reject":
            pass
        elif selected_processing_option == "TM Winback No First Payment":
            task_winbacknfp.task_winbacknfp_main(folder_path)
        elif selected_processing_option == "TM Winback On Hold":
            pass
        elif selected_processing_option == "TM Month 2 - 6":
            task_month2_6.task_month2_to_6_main(folder_path)
        elif selected_processing_option == "TM Burnt":
            task_burnt.task_burnt_main(folder_path)
        elif selected_processing_option == "TM Reactivation":
            pass
        elif selected_processing_option == "TM Upgrade":
            pass
        elif selected_processing_option == "Response Leads":
            task_response_leads.task_response_leads_main(folder_path)
        elif selected_processing_option == "Token":
            task_token.task_token_main(folder_path)

# Custom logging handler to redirect log messages to a QTextEdit widget
class TextEditHandler(logging.Handler):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def emit(self, record):
        msg = self.format(record)
        self.widget.append(msg)

if __name__ == '__main__': 
    app = QApplication(sys.argv)
    window = QWidget()

    # Set window title
    window.setWindowTitle('Testing pyqt app')

    # Set position and size of window
    window.setGeometry(100, 100, 600, 400)

    # Create a layout
    layout = QVBoxLayout()

    # Create a QComboBox for selecting processing options
    processing_options = QComboBox()
    processing_options.addItem("Select Process To Start")
    processing_options.addItem("TM One Time Conversion To Pledge")
    processing_options.addItem("TM On Hold Hard and Soft Reject")
    processing_options.addItem("TM Winback No First Payment")
    processing_options.addItem("TM Winback On Hold")
    processing_options.addItem("TM Month 2 - 6")
    processing_options.addItem("TM Burnt")
    processing_options.addItem("TM Reactivation")
    processing_options.addItem("TM Upgrade")
    processing_options.addItem("Response Leads")
    processing_options.addItem("Token")
    # Add more processing options as needed
    layout.addWidget(processing_options)

    # Create a button for browsing folder
    browse_button = QPushButton('Browse Folder')
    browse_button.clicked.connect(browse_folder)

    # Add the button to the layout
    layout.addWidget(browse_button)

    # Create a QTextEdit widget for displaying output
    output_box = QTextEdit()
    output_box.setReadOnly(True)  # Make the output box read-only
    layout.addWidget(output_box)

    # Set the layout of the window
    window.setLayout(layout)

     # Custom logging handler to redirect log messages to a QTextEdit widget
    handler = TextEditHandler(output_box)
    handler.setFormatter(logging.Formatter('%(message)s'))

    # Get the root logger and add the custom handler
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)

    # Display window on screen
    window.show()

    # Enter event loop
    sys.exit(app.exec_())
