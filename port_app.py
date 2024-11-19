# import module from subfolder
from task_code import compare_paydollar_sf, month_2_to_6, one_time_conversion, burnt, onhold, reactivation, response_leads, task_token, winback_nfp, winback_onhold
from task_code import task_data_cleaning, task_set_reject_burnt_status
from task_code import upgrade_part1, upgrade_part2, task_token_return_file, import_donation_notin_sf, task_import_to_secondary_token

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit, QFileDialog, QComboBox, QProgressBar
import logging

def browse_folder():
    folder_path = QFileDialog.getExistingDirectory(window, 'Select Folder', '.') 
    if folder_path:
        selected_processing_option = processing_options.currentText()
        output_box.append("\nSelected processing option: " + selected_processing_option)

        # Reset progress bar to 0
        progress_bar.setValue(0)

        if selected_processing_option == "TM One Time Conversion To Pledge":
            one_time_conversion.one_time_conversion_flow(folder_path)

        elif selected_processing_option == "TM On Hold Hard and Soft Reject":
            onhold.onhold_flow(folder_path)

        elif selected_processing_option == "TM Winback No First Payment":
            winback_nfp.winback_nfp_flow(folder_path)

        elif selected_processing_option == "TM Winback On Hold":
            winback_onhold.winback_onhold_flow(folder_path)

        elif selected_processing_option == "TM Month 2 - 6":
            month_2_to_6.month_2_to_6_flow(folder_path)

        elif selected_processing_option == "TM Burnt":
            burnt.burnt_flow(folder_path)

        elif selected_processing_option == "TM Reactivation":
            reactivation.reactivation_flow(folder_path)

        elif selected_processing_option == "TM Upgrade: Prepare Files":
            upgrade_part1.task_upgrade_part1_flow(folder_path)

        elif selected_processing_option == "TM Upgrade: Process Files":
            upgrade_part2.upgrade_part2_flow(folder_path)

        elif selected_processing_option == "Response Leads":
            response_leads.response_leads_flow(folder_path)

        elif selected_processing_option == "Token: Send File":
            task_token.task_token_main(folder_path)
        
        elif selected_processing_option == "Token: Return File":
            task_token_return_file.token_return_main(folder_path)

        elif selected_processing_option == "Token: Import To Secondary Token":
            task_import_to_secondary_token.import_to_secondary_token(folder_path)

        elif selected_processing_option == "Compare Paydollar and SF":
            compare_paydollar_sf.task_compare_paydollarsf(folder_path)

        elif selected_processing_option == "Data Cleaning":
            task_data_cleaning.task_data_cleaning_main(folder_path)
            
        elif selected_processing_option == "To Set Burnt and Reject":
            task_set_reject_burnt_status.task_set_reject_burnt(folder_path)

        elif selected_processing_option == "To Import Payment Status Recurring Pledge Donation - Digital":
            import_donation_notin_sf.import_donation_notin_sf_main(folder_path)

        # Simulate progress
        for i in range(101):
            progress_bar.setValue(i)

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
    window.setWindowTitle('Task Simplifier App')

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
    processing_options.addItem("TM Upgrade: Prepare Files")
    processing_options.addItem("TM Upgrade: Process Files")
    processing_options.addItem("Response Leads")
    processing_options.addItem("Token: Send File")
    processing_options.addItem("Token: Return File")
    processing_options.addItem("Token: Import To Secondary Token")
    processing_options.addItem("Compare Paydollar and SF")
    processing_options.addItem("Data Cleaning")
    processing_options.addItem("To Set Burnt and Reject")
    processing_options.addItem("To Import Payment Status Recurring Pledge Donation - Digital")

    # Add more processing options as needed
    layout.addWidget(processing_options)

    # Create a button for browsing folder
    browse_button = QPushButton('Browse Folder')
    browse_button.clicked.connect(browse_folder)

    # Add the button to the layout
    layout.addWidget(browse_button)

    # Create a QProgressBar widget for displaying progress
    progress_bar = QProgressBar()
    layout.addWidget(progress_bar)

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

    # Set the dark mode stylesheet
    dark_stylesheet = """
    QWidget {
        background-color: #2e2e2e;
        color: #ffffff;
    }
    QComboBox, QTextEdit, QProgressBar {
        background-color: #3c3c3c;
        border: 1px solid #555555;
        color: #ffffff;
    }
    QComboBox QAbstractItemView {
        background-color: #3c3c3c;
        color: #ffffff;
        selection-background-color: #555555;
    }
    QComboBox::drop-down {
        border: 0px;
    }
    QComboBox::down-arrow {
        image: url(down_arrow.png); /* Customize as needed */
        width: 14px;
        height: 14px;
    }
    QPushButton {
        background-color: #d9534f;  /* Red color for button */
        border: 1px solid #888888;
        padding: 5px;
        border-radius: 4px;
        color: #ffffff;
    }
    QPushButton:hover {
        background-color: #c9302c;  /* Darker red on hover */
    }
    QTextEdit {
        border: 1px solid #555555;
        border-radius: 4px;
    }
    QProgressBar {
        text-align: center;
    }
    QProgressBar::chunk {
        background-color: #05B8CC;
        width: 20px;
    }
    """

    app.setStyleSheet(dark_stylesheet)

    # Display window on screen
    window.show()

    # Enter event loop
    sys.exit(app.exec_())
