import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from ytComments import yt_manager
from .menu import MenuBar
from .main import MainWindow
from .update import UpdateManager
from .error import run_error
from ..__about__ import __title__, __url__, __author__, __license__, __description__

class App(QMainWindow):
    """Main application class."""
    def __init__(self):
        # Initialize QApplication
        self.qapp = QApplication(sys.argv)
        self.yt = yt_manager()
        self.yt.settings.load()
        
        # Initialize QMainWindow
        super().__init__()
        self.setWindowTitle(__title__)
        self.setGeometry(
            self.yt.settings.window_size[0],
            self.yt.settings.window_size[1],
            self.yt.settings.window_size[2],
            self.yt.settings.window_size[3]
        )
        
        # Create the main window
        self.main_frame = MainWindow(self)
        self.setCentralWidget(self.main_frame)
        
        # Create the menu bar
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)
        
        # Connect the window resize event and move event
        self.resizeEvent = self.on_resize
        self.moveEvent = self.on_move
        
        # Allow the window to accept drag-and-drop events for files
        self.setAcceptDrops(True)
        
    def run(self):
        """Execution of the application."""
        self.show()
        self.check_for_updates()
        sys.exit(self.qapp.exec())
        
    def on_resize(self, event):
        """Execute actions when the main window is resized."""
        self.yt.settings.window_size = (
            self.x(),
            self.y(),
            self.width(), 
            self.height()
            )
        self.yt.settings.save()
        super().resizeEvent(event)
        
    def on_move(self, event):
        """Execute actions when the main window is moved."""
        self.yt.settings.window_size = (
            self.x(),
            self.y(),
            self.width(), 
            self.height()
            )
        self.yt.settings.save()
        super().moveEvent(event)
        
    def dragEnterEvent(self, event):
        """Manage the drag-and-drop event.
        Only accept files."""
        if event.mimeData().hasUrls():
            event.accept()  # Accept the event
        else:
            event.ignore()  # Ignore if it's not a file
    
    def dropEvent(self, event):
        """Manage the drop event and retrieve the dropped file."""
        if event.mimeData().hasUrls():
            # Retrieve the URLs from the mimeData
            urls = event.mimeData().urls()
            # Convert the URLs to a local path
            list_urls = []
            for url in urls:
                file_path = url.toLocalFile()
                list_urls.append(file_path)
            # Set the path in the QLineEdit
            self.main_frame.old_save_input.setText(";".join(list_urls))

    def check_for_updates(self):
        """Check for updates."""
        repo_owner, repo_name = self.menu_bar.about_dialog.extract_repo_info(
            __url__
            )
        updater = UpdateManager(repo_owner, repo_name, self)
        reply = None
        
        # Check for updates
        if updater.check_updates() and self.yt.settings.auto_update:
            msg = "An update is available,"
            msg += "\nwould you like to update the software ?"
            reply = QMessageBox.question(
                None, 
                "Information", 
                msg, 
                QMessageBox.Yes | QMessageBox.No
                )
        
        # Download the update
        if updater.check_updates() and reply == QMessageBox.Yes:
            try:
                updater.update_software()
                updater.show_file_location_message(updater.new_filedir)
                self.close()
                sys.exit()
            except Exception as e:
                msg = "An error occurred during the update"
                run_error(msg, details = e)
                
