# import files and functions needed for process

# import XXXX
# from XXXX import XXXX

# True if process need a folder path, False if process need a file
IS_FOLDER = True

# if IS_FOLDER = False, files extension wanted for the process
# WARNING: only in lowercase, uppercase is automatic
# example ".pdf"
FILES_EXTENSION = [".mp4", ".m4v", ".avi"]




def process(path_element, list_elements):
    """process that will be applied on each file in the folder, or in the file
    
    Attrs:
        - path_element (str): path of the selected element in the ui
        path of a folder if IS_FOLDER = True, else path of a file
        - list_elements (list(str)) : if IS_FOLDER = True, list of every file in the folder, just name of the file, without full path
                                       else, list_elements = None
    """

    # put here functions of code of the process








    # end of process function






# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
#
# CODE OF UI, DON'T GO FURTHER IF YOU JUST WANT TO USE THE PROJECT FOR A PROCESS
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------




# -------------------- Import Lib Standard -------------------
import sys
import os

# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLineEdit
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QDir, QObject, QThread

# -------------------- Import Lib User -------------------
from Ui_ihm import Ui_MainWindow


# -------------------- Constant -------------------



FILES_EXTENSION_UPPERCASE = [x.upper() for x in FILES_EXTENSION]


# -------------------- Class -------------------

# -------------------------------------------------------------------#
#                          CLASS WORKER                              #
# -------------------------------------------------------------------#
class Worker(QObject):
    """Class for thread
    put the process in a thread and send a signal when the process
    is finished
    """
    command = pyqtSignal(str, list)
    signal_process_done = pyqtSignal()

    def __init__(self):
        super().__init__()

    @pyqtSlot(str, list)
    def thread_process(self, path_and_folder_name, list_elements=None):
        
        process(path_and_folder_name, list_elements)

        self.signal_process_done.emit()


# -------------------------------------------------------------------#
#                          CLASS FILEEDIT                            #
# -------------------------------------------------------------------#
class FileEdit(QLineEdit):
    """QlineEdit class with drag and drop added"""
    def __init__(self, parent):
        super(FileEdit, self).__init__(parent)

        self.setDragEnabled(True)

    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if (urls and urls[0].scheme() == 'folder'):
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if (urls and urls[0].scheme() == 'folder'):
            event.acceptProposedAction()

    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if (urls and urls[0].scheme() == 'folder'):
            filepath = str(urls[0].path())[1:]
            self.setText(filepath)


# -------------------------------------------------------------------#
#                         CLASS MAINWINDOW                           #
# -------------------------------------------------------------------#
class MainWindow(QMainWindow):
    """class of the window"""
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.label_done.hide()
        self.ui.label_process.hide()

        self.m_thread = QThread()
        self.m_thread.start()
        self.m_worker = Worker()
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

    def adapt_const_extention_filter(self):
        """adapt extension put in FILES_EXTENSION to the format of the filter of GetOpenFileName"""
        filter = "Files ("
        for element in FILES_EXTENSION:
            filter = filter + "*" + element
        filter = filter + ")"
        return filter

    @pyqtSlot()
    def find_element(self):
        """open the finder windows,
        put the path in the fileEdit
        """
        if IS_FOLDER:
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
        if IS_FOLDER:
            folder = self.ui.fileEdit_path.text()
            if os.path.isdir(folder):
                data = [f for f in os.listdir(folder) if f.endswith(tuple(FILES_EXTENSION + FILES_EXTENSION_UPPERCASE))]
                if len(data) !=0:
                    self.disable_ui()
                    self.m_worker.command.emit(folder, data)
        else:
            file = self.ui.fileEdit_path.text()
            if file.endswith(tuple(FILES_EXTENSION + FILES_EXTENSION_UPPERCASE)) and os.path.exists(file):
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


# -------------------- Main code -------------------
if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec())
