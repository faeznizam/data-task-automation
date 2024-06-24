# import module from subfolder
from task_code import compare_paydollar_sf, month_2_to_6, one_time_conversion, burnt, onhold, reactivation, response_leads, task_token, winback_nfp, winback_onhold
from task_code import task_data_cleaning, task_set_reject_burnt_status
from task_code import upgrade_part1, upgrade_part2


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit, QFileDialog, QComboBox, QTableWidget, QTableWidgetItem, QHBoxLayout
import logging

processed_file_info = []

def get_row_count(original_df, updated_df, new_file_name, processed_file_info):
    # Append row count for before and after to list in dictionary.
    processed_file_info.append({
        'File Name': new_file_name,
        'Before Clean': len(original_df),
        'After Clean': len(updated_df),
    })

def browse_folder():
    folder_path = QFileDialog.getExistingDirectory(window, 'Select Folder', '.') 
    if folder_path:

        selected_processing_option = processing_options.currentText()
        output_box.append("\nSelected processing option: " + selected_processing_option)
        
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

        elif selected_processing_option == "Token":
            task_token.task_token_main(folder_path)

        elif selected_processing_option == "Compare Paydollar and SF":
            compare_paydollar_sf.task_compare_paydollarsf(folder_path)

        elif selected_processing_option == "Data Cleaning":
            task_data_cleaning.task_data_cleaning_main(folder_path)
            
        elif selected_processing_option == "To Set Burnt and Reject":
            task_set_reject_burnt_status.task_set_reject_burnt(folder_path)

        # Update the table with new processed file info
        update_table(processed_file_info)
            
# Custom logging handler to redirect log messages to a QTextEdit widget
class TextEditHandler(logging.Handler):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def emit(self, record):
        msg = self.format(record)
        self.widget.append(msg)

def update_table(processed_file_info):
    headers = ["File Name", "Before Clean", "After Clean"]
    table_widget.setRowCount(len(processed_file_info))
    table_widget.setColumnCount(len(headers))
    table_widget.setHorizontalHeaderLabels(headers)

    for row_idx, info in enumerate(processed_file_info):
        table_widget.setItem(row_idx, 0, QTableWidgetItem(info['File Name']))
        table_widget.setItem(row_idx, 1, QTableWidgetItem(str(info['Before Clean'])))
        table_widget.setItem(row_idx, 2, QTableWidgetItem(str(info['After Clean'])))

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
    processing_options.addItem("Token")
    processing_options.addItem("Compare Paydollar and SF")
    processing_options.addItem("Data Cleaning")
    processing_options.addItem("To Set Burnt and Reject")

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

    # Create a QTableWidget for displaying processed file info
    table_widget = QTableWidget()
    layout.addWidget(table_widget)

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
