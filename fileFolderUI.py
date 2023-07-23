# -------------------- Import Lib Standard -------------------
import sys
import os
import inspect

# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QProgressBar
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QDir, QObject, QThread, QRect, QSize

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


def _do_nothing1():
    pass

def _do_nothing2(str_var):
    pass

def _do_nothing3(str_var, list_str_var):
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
        self.process_func1 = _do_nothing1
        self.process_func2 = _do_nothing2
        self.process_func3 = _do_nothing3

    @pyqtSlot(str, list)
    def thread_process(self, path_and_folder_name, list_elements=None):
        
        self.process_func1()
        self.process_func2(path_and_folder_name)
        self.process_func3(path_and_folder_name, list_elements)

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

        self.progress_bar = QProgressBar(self.ui.centralwidget)
        self.progress_bar.setRange(0,100)
        self.progress_bar.setValue(0)
        self.progress_bar.setGeometry(QRect(30, 10, 536, 20))
        self.progress_bar.hide()

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

    def define_attribute(self, is_folder, has_lineedit, has_progressbar, files_extension, process_func):
        self.is_folder = is_folder
        self.files_extension = files_extension
        self.files_extension_uppercase = [x.upper() for x in self.files_extension]
        self.has_lineedit = has_lineedit
        self.has_progressbar = has_progressbar
        num_args = len(inspect.getfullargspec(process_func).args)
        if num_args == 0:
            self.m_worker.process_func1 = process_func
            self.m_worker.process_func2 = _do_nothing2
            self.m_worker.process_func3 = _do_nothing3
        if num_args == 1:
            self.m_worker.process_func2 = process_func
            self.m_worker.process_func1 = _do_nothing1
            self.m_worker.process_func3 = _do_nothing3
        if num_args == 2:
            self.m_worker.process_func3 = process_func
            self.m_worker.process_func1 = _do_nothing1
            self.m_worker.process_func2 = _do_nothing2


    def update_ui(self):
        if self.has_progressbar:
            self.progress_bar.show()
        if not self.has_lineedit:
            self.ui.fileEdit_path.hide()
        if self.has_lineedit and self.has_progressbar:
            self.setMinimumSize(QSize(642, 116))
            self.setMaximumSize(QSize(642, 116))
            self.progress_bar.setGeometry(QRect(30, 45, 536, 20))
            self.ui.pushButton_process.setGeometry(QRect(240, 70, 75, 23))
            self.ui.label_done.setGeometry(QRect(330, 70, 51, 20))
            self.ui.label_process.setGeometry(QRect(330, 70, 131, 21))


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
        
        self.has_lineedit = True
        self.has_progressbar = False
        self.is_folder = True
        self.files_extension = FileExtensions.DOCUMENTS
        self.process_func = _do_nothing1
        self.window.define_attribute(self.is_folder, self.has_lineedit, self.has_progressbar, self.files_extension, self.process_func)

    def run(self):
        self.window.define_attribute(self.is_folder, self.has_lineedit, self.has_progressbar, self.files_extension, self.process_func)
        self.window.update_ui()
        self.window.show()
        sys.exit(self.app.exec())

    
    def change_value_progressbar(self, value):
        self.window.progress_bar.setValue(value)

