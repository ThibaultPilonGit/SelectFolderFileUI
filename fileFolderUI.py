# -------------------- Import Lib Standard -------------------
import sys
import os

# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QDir, QObject, QThread

# -------------------- Import Lib User -------------------
from Ui_ihm import Ui_MainWindow


# -------------------- Constant -------------------



# -------------------- Class -------------------


class FileExtensions:
    VIDEOS = [".mp4", ".m4v", ".avi", ".mov", ".wmv"]
    PICTURES = [".jpg", ".png", ".bmp", ".gif", ".tiff"]
    DOCUMENTS = [".pdf", ".docx", ".txt", ".rtf"]
    AUDIO = [".mp3", ".wav", ".ogg", ".flac"]
    SPREADSHEETS = [".csv", ".xlsx", ".ods"]
    ARCHIVES = [".zip", ".rar", ".7z", ".tar.gz"]
    PROGRAMS = [".exe", ".msi"]
    SCRIPTS = [".py", ".sh", ".bat"]
    FONT_FILES = [".ttf", ".otf"]
    WEB_FILES = [".html", ".css", ".js"]


# -------------------- Functions -------------------

def _do_nothing(self, str_var, list_str_var):
        pass




# -------------------------------------------------------------------#
#                          CLASS WORKER                              #
# -------------------------------------------------------------------#
class _Worker(QObject):
    """Class for thread
    put the process in a thread and send a signal when the process
    is finished
    """
    command = pyqtSignal(str, list)
    signal_process_done = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.process_func = _do_nothing

    @pyqtSlot(str, list)
    def thread_process(self, path_and_folder_name, list_elements=None):
        
        self.process_func(path_and_folder_name, list_elements)

        self.signal_process_done.emit()





# -------------------------------------------------------------------#
#                         CLASS MAINWINDOW                           #
# -------------------------------------------------------------------#
class _MainWindow(QMainWindow):
    """class of the window"""
    def __init__(self):
        super(_MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.label_done.hide()
        self.ui.label_process.hide()

        self.m_thread = QThread()
        self.m_thread.start()
        self.m_worker = _Worker()
        self.m_worker.moveToThread(self.m_thread)

        self.set_up_connect()

    def set_up_connect(self):
        """Connect every signals"""
        # signals of the ui
        self.ui.pushButton_browse.clicked.connect(self.find_element)
        self.ui.pushButton_process.clicked.connect(self.run_process)
        self.ui.fileEdit_path.textChanged.connect(self.hide_done)
        # signals of the thread
        self.m_worker.command.connect(self.m_worker.thread_process)
        self.m_worker.signal_process_done.connect(self.enable_ui)

    def define_attribute(self, is_folder, files_extension, process_func):
        self.is_folder = is_folder
        self.files_extension = files_extension
        self.files_extension_uppercase = [x.upper() for x in self.files_extension]
        self.m_worker.process_func = process_func

    def adapt_const_extention_filter(self):
        """adapt extension put in files_extension to the format of the filter of GetOpenFileName"""
        filter = "Files ("
        extensions = " ".join(f"*{ext}" for ext in self.files_extension)
        filter = filter + extensions + ")"
        return filter

    @pyqtSlot()
    def find_element(self):
        """open the finder windows,
        put the path in the fileEdit
        """
        if self.is_folder:
            folder = QFileDialog.getExistingDirectory(self, "Choose folder",
                                                    QDir.currentPath(), QFileDialog.ShowDirsOnly)
            self.ui.fileEdit_path.setText(folder)
        else:

            file, _ = QFileDialog.getOpenFileName(self, "Choose file",
                                                     QDir.currentPath(),
                                                     filter=self.adapt_const_extention_filter())
            self.ui.fileEdit_path.setText(file)

    @pyqtSlot()
    def run_process(self):
        """call  the process thread"""
        if self.is_folder:
            folder = self.ui.fileEdit_path.text()
            if os.path.isdir(folder):
                data = [f for f in os.listdir(folder) if f.endswith(tuple(self.files_extension + self.files_extension_uppercase))]
                if len(data) !=0:
                    self.disable_ui()
                    self.m_worker.command.emit(folder, data)
        else:
            file = self.ui.fileEdit_path.text()
            if file.endswith(tuple(self.files_extension + self.files_extension_uppercase)) and os.path.exists(file):
                self.disable_ui()
                self.m_worker.command.emit(file, [])



    @pyqtSlot(str)
    def hide_done(self, text):
        """hide the label "done", call when the path change

        Attrs:
        - text (str): not used, but send by the signal of fileEdit
        """
        self.ui.label_done.hide()

    @pyqtSlot()
    def enable_ui(self):
        """enable ui when process is done"""
        self.ui.label_process.hide()
        self.ui.label_done.show()
        self.ui.pushButton_process.setEnabled(True)
        self.ui.pushButton_browse.setEnabled(True)
        self.ui.fileEdit_path.setEnabled(True)

    def disable_ui(self):
        """disable ui during the process"""
        self.ui.label_process.show()
        self.ui.pushButton_process.setEnabled(False)
        self.ui.pushButton_browse.setEnabled(False)
        self.ui.fileEdit_path.setEnabled(False)


class FileFolderUI():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = _MainWindow()
        
        self.is_folder = True
        self.files_extension = FileExtensions.DOCUMENTS
        self.process_func = _do_nothing
        self.window.define_attribute(self.is_folder, self.files_extension, self.process_func)

    def run(self):
        self.window.define_attribute(self.is_folder, self.files_extension, self.process_func)
        self.window.show()
        sys.exit(self.app.exec())
    
