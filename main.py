# inclure les fichiers ou fonctions qui vont être appelé pour le traitement

# import XXXX
# from XXXX import XXXX

# si on ouvre un dossier, si on veut directement ouvrir un fichier mettre False
EST_DOSSIER = True

# les types de fichiers qu'on veut utiliser, seulement extension en minuscule, avec le point
# exemple ".pdf"
EXTENSIONS_POSSIBLES = [".mp4", ".m4v", ".avi"]




def fonctionsTraitement(path_element, liste_elements):
    """traitement à faire sur les dossier et fichiers
    
    Attrs:
        - path_element (str): chemin de l'élement sélectionné dans l'UI,
        chemin d'un dossier si EST_DOSSIER = True, chemin d'un fichier sinon
        - liste_elements (list(str)) : Si EST_DOSSIER = True, liste de tous les fichiers présent dans le dossier, sans le chemin
                                       sinon, liste_elements = None
    """

    # mettre fonctions ou codes de traitement dans cette fonction








    # fin de la fonction






# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
#
#           CODE DE L'UI DE TRAITEMENT DE FICHIERS ET DOSSIERS
#
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------




# -------------------- Import Lib Standard -------------------
import sys
import os

# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLineEdit
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QDir, QObject, QThread

# -------------------- Import Lib User -------------------
from Ui_ihm import Ui_MainWindow


# -------------------- Constante -------------------



EXTENSIONS_POSSIBLES_MAJ = [x.upper() for x in EXTENSIONS_POSSIBLES]


# -------------------- Classe -------------------

# -------------------------------------------------------------------#
#                          CLASS WORKER                              #
# -------------------------------------------------------------------#
class Worker(QObject):
    """Classe de thread
    S'occupe du traitement
    """
    command = pyqtSignal(str, list)
    signal_traitement_fini = pyqtSignal()

    def __init__(self):
        super().__init__()

    @pyqtSlot(str, list)
    def thread_traitement(self, path_et_nom_dossier, liste_elements=None):
        
        # les fonctions à appeler lors du traitement
        fonctionsTraitement(path_et_nom_dossier, liste_elements)

        self.signal_traitement_fini.emit()

        # faire un truc qui fussionne chaque split si un point dans le nom de fichier


# -------------------------------------------------------------------#
#                          CLASS FILEEDIT                            #
# -------------------------------------------------------------------#
class FileEdit(QLineEdit):
    """Classe redéfinissant QlineEdit
    Ajoute une option de drag & drop de fichier, pour y mettre le path
    """
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
    """La classe de la fenêtre"""
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.label_terminer.hide()
        self.ui.label_traitement.hide()

        self.m_thread = QThread()
        self.m_thread.start()
        self.m_worker = Worker()
        self.m_worker.moveToThread(self.m_thread)

        self.set_up_connect()

    def set_up_connect(self):
        """Connecte tous les signaux"""
        # signaux de l'interface
        self.ui.pushButton_parcourir.clicked.connect(self.choisir_element)
        self.ui.pushButton_traiter.clicked.connect(self.lancer_traitement)
        self.ui.fileEdit_path.textChanged.connect(self.masquer_termine)
        # signaux du thread
        self.m_worker.command.connect(self.m_worker.thread_traitement)
        self.m_worker.signal_traitement_fini.connect(self.activer_interface)

    def adapterConstExtentionFilter(self):
        """adapte les extensions possibles pour le format de str du filtre de GetOpenFileName"""
        filtre = "Fichier ("
        for element in EXTENSIONS_POSSIBLES:
            filtre = filtre + "*" + element
        filtre = filtre + ")"
        return filtre

    @pyqtSlot()
    def choisir_element(self):
        """ouvre le finder windows et permet d'ouvir seulement les fichier,
        met le path dans le fileEdit
        """
        # fonction à modifier, doit prendre en param le type de chose qu'on veut, dossier(s), fichier(s), et si fichier quel type
        if EST_DOSSIER:
            dossier = QFileDialog.getExistingDirectory(self, "Choisir dossier",
                                                    QDir.currentPath(), QFileDialog.ShowDirsOnly)
            self.ui.fileEdit_path.setText(dossier)
        else:

            fichier, _ = QFileDialog.getOpenFileName(self, "Choisir fichier",
                                                     QDir.currentPath(),
                                                     filter=self.adapterConstExtentionFilter())
            self.ui.fileEdit_path.setText(fichier)

    @pyqtSlot()
    def lancer_traitement(self):
        """appel le thread de traitement"""
        if EST_DOSSIER:
            dossier = self.ui.fileEdit_path.text()
            if os.path.isdir(dossier):
                donnees = [f for f in os.listdir(dossier) if f.endswith(tuple(EXTENSIONS_POSSIBLES + EXTENSIONS_POSSIBLES_MAJ))]
                if len(donnees) !=0:
                    self.desactiver_interface()
                    self.m_worker.command.emit(dossier, donnees)
        else:
            fichier = self.ui.fileEdit_path.text()
            if fichier.endswith(tuple(EXTENSIONS_POSSIBLES + EXTENSIONS_POSSIBLES_MAJ)) and os.path.exists(fichier):
                self.desactiver_interface()
                self.m_worker.command.emit(fichier, [])



    @pyqtSlot(str)
    def masquer_termine(self, text):
        """masque le label terminé, appelé quand l'url change

        Attrs:
        - text (str): ne sert pas, mais envoyé par le signal, texte du fileEdit
        """
        self.ui.label_terminer.hide()

    @pyqtSlot()
    def activer_interface(self):
        """active toute l'interface une fois le traitement fini"""
        self.ui.label_traitement.hide()
        self.ui.label_terminer.show()
        self.ui.pushButton_traiter.setEnabled(True)
        self.ui.pushButton_parcourir.setEnabled(True)
        self.ui.fileEdit_path.setEnabled(True)

    def desactiver_interface(self):
        """désactive l'interface pendant le traitement"""
        self.ui.label_traitement.show()
        self.ui.pushButton_traiter.setEnabled(False)
        self.ui.pushButton_parcourir.setEnabled(False)
        self.ui.fileEdit_path.setEnabled(False)


# -------------------- Code principal -------------------
if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec())
