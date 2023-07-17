from PyQt5.QtWidgets import QLineEdit


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