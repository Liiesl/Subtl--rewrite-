# launcher.py

import sys, subprocess, os
# QSettings is from QtCore, which is a base module and less "heavy" than QtWidgets.
# It is needed to read the configuration to decide which path to take.
from PySide6.QtCore import QSettings

def launch_main_app(python_path, script_path, file_to_open=None):
    """
    Launches the main.py script.
    In case of an error, it will dynamically import PySide6.QtWidgets to show an
    error message box.
    """
    def show_error(title, message):
        """
        Utility to show a critical error message.
        This function is only called on error, so heavy GUI imports are
        deferred until they are actually needed.
        """
        try:
            from PySide6.QtWidgets import QApplication, QMessageBox
            
            # An application instance is required to show a GUI element.
            app = QApplication.instance() or QApplication(sys.argv)
            
            error_box = QMessageBox()
            error_box.setIcon(QMessageBox.Icon.Critical)
            error_box.setText(title)
            error_box.setInformativeText(message)
            error_box.setWindowTitle("Launcher Error")
            error_box.exec()
        except ImportError:
            # Fallback for environments where PySide6 might be missing or broken.
            print(f"LAUNCHER ERROR: {title}\n{message}", file=sys.stderr)
        except Exception as e:
            print(f"LAUNCHER CRITICAL: Failed to display GUI error: {e}", file=sys.stderr)
            print(f"Original Error: {title}\n{message}", file=sys.stderr)


    if not os.path.exists(python_path):
        show_error("Configuration Error", f"Python interpreter not found at:\n{python_path}")
        return

    if not os.path.exists(script_path):
        show_error("Configuration Error", f"Main script not found at:\n{script_path}")
        return

    command = [python_path, script_path]
    if file_to_open:
        command.append(file_to_open)

    try:
        # Use Popen for non-blocking execution. The launcher can exit
        # immediately after spawning the main application.
        subprocess.Popen(command, cwd=os.path.dirname(script_path))
    except Exception as e:
        show_error("Launch Error", f"Failed to start the application:\n{e}")

def main():
    """
    Main entry point for the launcher.
    It checks if a direct launch is possible to avoid loading GUI components
    unnecessarily. If direct launch isn't possible (e.g., no file to open,
    or not configured), it shows the configuration GUI.
    """
    settings = QSettings("Subtle", "SubtleLauncher")

    python_path = settings.value("python_path", "")
    script_path = settings.value("script_path", "")

    # A file argument is expected for the "fast path" (e.g., double-clicking a file).
    file_argument = sys.argv[1] if len(sys.argv) > 1 else None

    # Fast Path: If a file is provided and settings are configured, launch immediately.
    # On this path, no heavy GUI modules are imported unless a launch error occurs.
    if file_argument and python_path and script_path:
        launch_main_app(python_path, script_path, file_argument)
    else:
        # Slow Path: Show the configuration GUI.
        # This is the point where the heavy GUI modules are imported because they
        # are now necessary to show the preloader window.
        from PySide6.QtWidgets import QApplication
        from preloader import PreloaderWindow

        app = QApplication(sys.argv)
        preloader = PreloaderWindow()
        preloader.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    main()