# Quick Launch (Python Source)
An app to access to frequently used files, folders, and command-line actions
This README provides information for developers or users who wish to run or modify Quick Launch from the Python source code.

## Prerequisites

* Python 3.6+
* PyQt5:  Install using `pip install PyQt5`

## Running from Source

1.  Ensure you have the prerequisites installed.
2.  Clone or download this repository.
3.  Navigate to the directory containing `Quick_Launcher.py` (or the main script) in your terminal.
4.  Run the application: `python Quick_Launcher.py`

## File Structure

* `Quick_Launcher.py` (or similar): The main Python script containing the application's code.
* `launcher_paths.json`:  (If present) Stores saved launcher configurations.

## Code Overview

* **`EditDialog` Class:** Handles the dialog for editing launcher properties.
* **`LauncherWidget` Class:** Represents a single launcher button and its associated functionality.
* **`MainWindow` Class:** The main application window.
* **`open_path_in_explorer` Function:** Opens paths or executes commands.  Handles chained commands.
* **`copy_to_clipboard`, `edit_launcher`, `delete_launcher`, `add_new_launcher` Functions:** Functions for launcher management.
* **`log_message` Function:** Displays messages in the terminal output.
* **PyQt5:** The GUI framework used.
* **`subprocess`:** Used to execute command-line commands.

## Command Chaining Implementation (Important for Developers)

The `open_path_in_explorer` function handles chained commands:

1.  **Semicolon Separation:** Commands in the input string are separated by semicolons (`;`).
2.  **`cmd.exe /c`:** The `subprocess.run` function is used with `cmd.exe /c` to execute commands in the Windows command prompt.
3.  **Output Capture:** `subprocess.run` captures the standard output (stdout) and standard error (stderr) of the executed commands.
4.  **Error Handling:** `subprocess.run` is used with `check=True` to raise an exception if a command fails.  The application displays the output/error messages.

## Creating an Executable (For Developers)

If you wish to create a standalone executable:

1.  Install PyInstaller: `pip install pyinstaller`
2.  Run PyInstaller: `pyinstaller --onefile --name="QuickLaunch" Quick_Launcher.py`
3.  The executable will be in the `dist` directory.

## Contributing

(Your contribution guidelines)

## License

(Your license)

## Author

(Your name or contact information)
