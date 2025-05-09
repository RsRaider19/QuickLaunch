import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QGridLayout, QPushButton, QLineEdit,
                             QDialog, QLabel, QDialogButtonBox, QMessageBox,
                             QFrame, QTextEdit)
from PyQt5.QtGui import QClipboard, QColor, QPalette, QIcon
from PyQt5.QtCore import Qt, QTime, QThread, pyqtSignal, pyqtSlot
import os
import subprocess
import json

class EditDialog(QDialog):
    def __init__(self, parent=None, nickname="", path=""):
        super().__init__(parent)
        self.setWindowTitle("Edit Launcher")
        self.setGeometry(800, 450, 300, 200)  # Increased size (approx. 16:9)
        self.nickname_edit = QLineEdit(nickname)
        self.path_edit = QLineEdit(path)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Nickname:"))
        layout.addWidget(self.nickname_edit)
        layout.addWidget(QLabel("Path:"))
        layout.addWidget(self.path_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)
        self.apply_stylesheet()
        self.apply_background_color()

    def apply_background_color(self):
        """Applies a light gray background to the edit dialog."""
        palette = self.palette()
        #palette.setColor(QPalette.Background, QColor("#f0f0f0"))  # Light gray
        #self.central_widget.setStyleSheet('background-color: #000000;')
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def apply_stylesheet(self):
        stylesheet = """
            QDialog {
                color: #333;
                font-family: "Segoe UI", sans-serif;
                font-size: 10pt;
            }
            QLabel {
                color: #FFFFFF;
            }
            QLineEdit {
                background: white;
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 5px;
                color: #333;
            }
            QDialogButtonBox QPushButton {
                background: #e0e0e0;
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 5px 10px;
                color: #333;
                font-weight: normal;
            }
            QDialogButtonBox QPushButton:hover {
                background: #d8d8d8;
            }
        """
        self.setStyleSheet(stylesheet)

    def get_values(self):
        return self.nickname_edit.text().strip(), self.path_edit.text().strip()

class LauncherWidget(QWidget):
    def __init__(self, nickname, path, main_window):
        super().__init__()
        self.nickname = nickname
        self.path = path
        self.main_window = main_window

        layout = QHBoxLayout(self)

        self.open_button = QPushButton(nickname)
        self.open_button.clicked.connect(self.open_path)
        self.set_button_enabled_state(path)
        layout.addWidget(self.open_button)

        self.copy_button = QPushButton("\u2398")  # Unicode for copy
        self.copy_button.setObjectName("copyButton")
        self.copy_button.clicked.connect(self.copy_path)
        self.copy_button.setToolTip("Copy path to clipboard")
        layout.addWidget(self.copy_button)

        self.edit_button = QPushButton("\u270E")  # Unicode for edit
        self.edit_button.setObjectName("editButton")
        self.edit_button.clicked.connect(self.edit_launcher)
        self.edit_button.setToolTip("Edit nickname and path")
        layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("X")
        self.delete_button.setObjectName("deleteButton")
        self.delete_button.clicked.connect(self.delete_launcher)
        self.delete_button.setToolTip("Remove nickname and path")
        layout.addWidget(self.delete_button)

        self.setStyleSheet("""
            QWidget {
                
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #f0f0f0, stop:1 #e0e0e0);
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 6px;
                color: #000000;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #e8e8e8, stop:1 #d8d8d8);
            }
            QPushButton:disabled {
                color: #808080;
                background: #d3d3d3;
            }
            QPushButton#copyButton, QPushButton#editButton, QPushButton#deleteButton {
                border: none;
                border-radius: 12px;
                min-width: 25px;
                max-width: 25px;
                min-height: 25px;
                max-height: 25px;
                color: white;
                font-size: 10pt;
                padding: 0;
                margin-left: 2px;
            }
            QPushButton#copyButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #a5d6a7, stop:1 #81c784);
            }
            QPushButton#copyButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #90ee90, stop:1 #66bb6a);
            }
            QPushButton#editButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #ce93d8, stop:1 #ba68c8);
            }
            QPushButton#editButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #e1bee7, stop:1 #ab47bc);
            }
            QPushButton#deleteButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #ef5350, stop:1 #e53935); /* Red */
            }
            QPushButton#deleteButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #f44336, stop:1 #d32f2f);
            }
        """)

    def set_button_enabled_state(self, path):
        self.open_button.setEnabled(bool(path))

    def open_path(self):
        #main_window.show_info_message("In Process", "Executing...")
        self.main_window.open_path_in_explorer(self.path)

    def copy_path(self):
        self.main_window.copy_to_clipboard(self.path)

    def edit_launcher(self):
        self.main_window.edit_launcher(self.nickname, self.path, self)

    def delete_launcher(self):
        self.main_window.delete_launcher(self.nickname)

class BuildThread(QThread):
    """A thread to run the C code build command."""

    build_finished = pyqtSignal(str, str)  # Signal to send output to the main thread

    def __init__(self, command,command_type = "command"):
        super().__init__()
        self.command = command
        self.command_type = command_type

    def run(self):
        try:
            CREATE_NO_WINDOW = subprocess.CREATE_NO_WINDOW  # Flag to hide the console
            result = subprocess.run(
                self.command,
                shell=True,
                capture_output=True,
                text=True,
                check=True,
                creationflags=CREATE_NO_WINDOW  # Hide console
            )
            self.build_finished.emit("INFO", result.stdout)
        except subprocess.CalledProcessError as e:
            self.build_finished.emit("ERROR", e.stderr)
        except Exception as e:  # Catch any other potential errors
            self.build_finished.emit("ERROR", f"An unexpected error occurred: {str(e)}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quick Launch")
        self.setGeometry(580, 270, 900, 600)  # Increased height to accommodate the terminal
        self.setWindowIcon(QIcon(".\\cmd_icon.ico"))

        self.central_widget = QWidget()
        self.central_widget.setAutoFillBackground(False)
        palette = self.central_widget.palette()
        #palette.setColor(QPalette.Background, QColor("#ffffff"))
        #self.central_widget.setStyleSheet('background-color: #000000;')
        self.central_widget.setPalette(palette)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.grid_layout = QGridLayout()
        self.launchers_data = {"Button 1": "", "Button 2": "",
                               "Button 3": "", "Button 4": "",
                               "Button 5": "", "Button 6": "",
                               "Button 7": "", "Button 8": ""}
        self.launcher_widgets = {}

        self.load_launchers()
        self.create_launcher_grid()

        self.add_button = QPushButton("+ Add New Launcher")
        self.add_button.clicked.connect(self.add_new_launcher)
        self.add_button.setObjectName("addButton")

        self.info_button = QPushButton("About")  # New button for extra info
        self.info_button.setFixedSize(60, 17)
        self.info_button.clicked.connect(self.show_extra_info)
        self.info_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none; /* Removes the border */
                color: #000000; /* Text color */
                font-weight: bold;
            }
            QPushButton:hover {
                color: #ffffff;
            }
        """)

        self.layout.addLayout(self.grid_layout)
        self.layout.addWidget(self.add_button)
        #self.layout.addWidget(self.info_button)

        self.terminal = QTextEdit()  # Create the QTextEdit
        self.terminal.setReadOnly(True)  # Make it read-only
        self.layout.addWidget(self.terminal)  # Add it to the main layout
        
        info_layout = QHBoxLayout()
        info_layout.addWidget(self.info_button)
        info_layout.setAlignment(Qt.AlignCenter) 
        self.layout.addLayout(info_layout)


        self.apply_stylesheet()
        self.setAcceptDrops(True)

    def apply_stylesheet(self):
        stylesheet = """
            QWidget {
                background: #10507f;
                color: #ffffff;
                font-family: "Segoe UI", sans-serif;
                font-size: 11pt;
            }
            QPushButton#info_button {
                background: transparent;
                color: #000000;
                font-weight: bold;
            }
            QPushButton#addButton {
                background: #ffccbc;
                color: #333;
                font-weight: bold;
            }
            QPushButton#addButton:hover {
                background: #ffb380;
            }
            QTextEdit {
            background: #000000; /* White background for terminal */
            color: #ffffff; /* Dark gray text */
            border: 2px solid #cccccc; /* Light gray border */
        }
        """
        self.setStyleSheet(stylesheet)

    def load_launchers(self):
        try:
            with open("launcher_paths.json", "r") as f:
                saved_data = json.load(f)
                if isinstance(saved_data, dict):
                    self.launchers_data = saved_data.get("launchers", self.launchers_data)
                elif isinstance(saved_data, list): # Handle older format if it existed
                    new_data = {}
                    for i, item in enumerate(saved_data):
                        if isinstance(item, dict) and "nickname" in item and "path" in item:
                            new_data[item["nickname"]] = item["path"]
                        else:
                            new_data[f"Empty Path {i+1}"] = ""
                    self.launchers_data = new_data
        except FileNotFoundError:
            pass # Use default initial data

    def save_launchers(self):
        data_to_save = {"launchers": self.launchers_data}
        with open("launcher_paths.json", "w") as f:
            json.dump(data_to_save, f, indent=4)

    def create_launcher_grid(self):
        """Creates the launcher widgets in a dynamic grid based on the order in self.launchers_data."""
        for i, nickname in enumerate(self.launchers_data.keys()):
            path = self.launchers_data[nickname]
            row, col = divmod(i, 2)
            launcher_widget = LauncherWidget(nickname, path, self)
            self.grid_layout.addWidget(launcher_widget, row, col)
            self.launcher_widgets[nickname] = launcher_widget

    def swap_launchers(self, nickname1, nickname2):
        """Swaps the positions of two launchers and saves the order."""
        item1 = self.grid_layout.itemAtPosition(self.grid_layout.indexOf(self.launcher_widgets[nickname1]))
        item2 = self.grid_layout.itemAtPosition(self.grid_layout.indexOf(self.launcher_widgets[nickname2]))

        if item1 and item2:
            row1, col1 = self.grid_layout.getItemPosition(item1)
            row2, col2 = self.grid_layout.getItemPosition(item2)

            self.grid_layout.removeWidget(self.launcher_widgets[nickname1])
            self.grid_layout.removeWidget(self.launcher_widgets[nickname2])

            self.grid_layout.addWidget(self.launcher_widgets[nickname1], row2, col2)
            self.grid_layout.addWidget(self.launcher_widgets[nickname2], row1, col1)

            # Update the order in self.launchers_data
            ordered_nicknames = list(self.launchers_data.keys())
            index1 = ordered_nicknames.index(nickname1)
            index2 = ordered_nicknames.index(nickname2)
            ordered_nicknames[index1], ordered_nicknames[index2] = ordered_nicknames[index2], ordered_nicknames[index1]

            new_launchers_data = {}
            for nick in ordered_nicknames:
                new_launchers_data[nick] = self.launchers_data[nick]
            self.launchers_data = new_launchers_data
            self.save_launchers()
            self.recreate_launcher_grid() # Recreate to reflect new order
            
    @pyqtSlot(str, str)
    def handle_build_finished(self, message_type, message):
        """Handles the signal from the build thread and updates the terminal."""
        self.log_message(message, message_type)
        
    def open_path_in_explorer(self, path):
        if ";" not in path:
            if path:
                try:
                    if os.path.isdir(path) or os.path.isfile(path):
                        subprocess.Popen(['explorer', os.path.normpath(path)])
                    else:
                        self.show_error_message("Could not open path: ", "Directory Not Found" )
                        self.show_info_message("ERROR", "Check Path.\n" + path)
                except FileNotFoundError:
                    self.show_error_message("Path not found:", path)
                except Exception as e:
                    self.show_error_message("Could not open path:", str(e))
            else:
                self.show_info_message("Info", "Path is not set for this launcher.")
        else:
            cmd_command_string = ''
            commands = path.split(";")
            if commands[1] != '':
                cmd_command_string = " && ".join(commands)
            else:
                cmd_command_string = commands[0]
            combined_command = ["cmd.exe", "/c", cmd_command_string]

            self.show_info_message("INFO", "Executing ...")  # Show initial message
            if ".exe" in path:
                command_type = "exe"
            else:
                command_type = "command"
            self.build_thread = BuildThread(combined_command, command_type=command_type)
            self.build_thread.build_finished.connect(self.handle_build_finished)
            self.build_thread.start()
            #self.show_info_message("Info", "Done Execution!")
            

    def copy_to_clipboard(self, path):
        if path:
            clipboard = QApplication.clipboard()
            clipboard.setText(path)
            if ";" in path:
                self.show_info_message("Copied", "Command copied to clipboard!\n" + path)
            else:
                self.show_info_message("Copied", "Path copied to clipboard!\n" + path)
        else:
            self.show_info_message("Info", "Path is not set for this launcher.")

    def edit_launcher(self, nickname, current_path, launcher_widget):
        dialog = EditDialog(self, nickname, current_path)
        if dialog.exec_() == QDialog.Accepted:
            new_nickname, new_path = dialog.get_values()

            if new_nickname != nickname and new_nickname in self.launchers_data:
                # Nickname already exists, rename the existing one to "Empty Path"
                ordered_nicknames = list(self.launchers_data.keys())
                index_to_rename = ordered_nicknames.index(new_nickname)
                nickname_to_rename = ordered_nicknames[index_to_rename]
                self.launchers_data[nickname_to_rename] = ""
                widget_to_rename = self.launcher_widgets.get(nickname_to_rename)
                if widget_to_rename:
                    widget_to_rename.nickname = "Empty Path"
                    widget_to_rename.open_button.setText("Empty Path")
                    widget_to_rename.set_button_enabled_state(False)

            # Update the current launcher
            ordered_nicknames = list(self.launchers_data.keys())
            index_to_update = ordered_nicknames.index(nickname)
            ordered_nicknames[index_to_update] = new_nickname

            new_launchers_data = {}
            for nick in ordered_nicknames:
                if nick == new_nickname:
                    new_launchers_data[nick] = new_path
                else:
                    new_launchers_data[nick] = self.launchers_data.get(nick, "")

            self.launchers_data = new_launchers_data
            launcher_widget.nickname = new_nickname
            launcher_widget.open_button.setText(new_nickname)
            launcher_widget.path = new_path
            launcher_widget.set_button_enabled_state(new_path)
            self.save_launchers()


    def delete_launcher(self, nickname_to_delete):
        if nickname_to_delete in self.launchers_data:
            self.launchers_data[nickname_to_delete] = ""
            widget_to_delete = self.launcher_widgets.get(nickname_to_delete)
            if widget_to_delete:
                widget_to_delete.open_button.setText("Empty Path")
                widget_to_delete.set_button_enabled_state(False)
            self.save_launchers()

    def add_new_launcher(self):
        dialog = EditDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            new_nickname, new_path = dialog.get_values()
            if new_nickname:
                if new_nickname in self.launchers_data:
                    # Nickname already exists, rename the existing one to "Empty Path"
                    old_nickname_widget = self.launcher_widgets.get(new_nickname)
                    if old_nickname_widget:
                        self.launchers_data[new_nickname] = ""
                        old_nickname_widget.nickname = "Empty Path"
                        old_nickname_widget.open_button.setText("Empty Path")
                        old_nickname_widget.set_button_enabled_state(False)
                self.launchers_data[new_nickname] = new_path  # Corrected line: Assign new_path
                self.create_launcher_grid()
                
    def log_message(self, message, message_type="INFO"):
        """Logs a message to the terminal with a timestamp."""
        current_time = QTime.currentTime().toString("hh:mm:ss")
        formatted_message = f"[{current_time}] {message_type}: {message}\n"
        self.terminal.append(formatted_message)
        self.terminal.verticalScrollBar().setValue(self.terminal.verticalScrollBar().maximum())  # Scroll to bottom

                
    def show_error_message(self, title, message):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Critical)
        message_box.setWindowTitle(title)
        message_box.setText(message)
        message_box.exec_()

    # def show_info_message(self, title, message):
    #     message_box = QMessageBox()
    #     message_box.setIcon(QMessageBox.Information)
    #     message_box.setWindowTitle(title)
    #     message_box.setText(message)
    #     message_box.exec_()
    
    def show_info_message(self, title, message):
        self.log_message(f"{message}", title)

    def show_extra_info(self):
        """Displays extra information about the application."""
        QMessageBox.information(
            self,
            "About",
            "Code developed by: RsRaider\n"
            "Application release date: May 9, 2025",
        )
                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
