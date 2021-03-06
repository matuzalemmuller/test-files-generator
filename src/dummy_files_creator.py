import sys
import icon_qt
from about import About
from files_creator import FilesCreator
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QButtonGroup, QCheckBox, QComboBox,  \
    QFileDialog, QGridLayout, QHBoxLayout, QLabel, QLayout, QLineEdit,         \
    QMessageBox, QProgressBar, QPushButton, QRadioButton, QWidget, QAction,    \
    QMenuBar

#------------------------------------------------------------------------------#

class MyWindow(QWidget):
    sig_abort_workers = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dummy Files Creator")
        self.setWindowIcon(QtGui.QIcon(':/icon.png'))
        QThread.currentThread().setObjectName('main')
        self.__threads = []
        self._files_created = []
        self._create_ui()


    # Creates all UI elements
    def _create_ui(self):
        self._window_layout = QGridLayout()
        self._window_layout.setContentsMargins(0,0,0,0)

        self._menu_bar = QMenuBar()
        self._window_layout.addWidget(self._menu_bar)
        self._help_item = self._menu_bar.addMenu('Help')
        self._about_action = QAction("Help", self._menu_bar)
        self._about_action.triggered.connect(self._about_clicked)
        self._help_item.addAction(self._about_action)

        self._options_layout = QGridLayout()
        self._options_layout.setAlignment(QtCore.Qt.AlignCenter)
        self._options_widget = QWidget()
        self._options_widget.setLayout(self._options_layout)

        self._path_label = QLabel()
        self._path_label.setText("Path")
        self._path_label.setAlignment(QtCore.Qt.AlignCenter)

        self._path_textbox = QLineEdit()
        self._path_textbox.resize(320,20)
        self._path_textbox.setMinimumWidth(320)

        self._browse_button = QPushButton("Browse")
        self._browse_button.setFixedWidth(80)
        self._browse_button.clicked.connect(self._browse_clicked)

        self._options_layout.addWidget(self._path_label, 1, 1)
        self._options_layout.addWidget(self._path_textbox, 1, 2)
        self._options_layout.addWidget(self._browse_button, 1, 3,
                                      QtCore.Qt.AlignCenter)

        self._number_files_label = QLabel()
        self._number_files_label.setText("Number of Files")
        self._number_files_label.setAlignment(QtCore.Qt.AlignCenter)

        self._number_validator=QtCore.QRegExp("[0-9]+")
        self._validator = QtGui.QRegExpValidator(self._number_validator)

        self._number_files_textbox = QLineEdit()
        self._number_files_textbox.resize(320,20)
        self._number_files_textbox.setMinimumWidth(320)
        self._number_files_textbox.setValidator(self._validator)

        self._options_layout.addWidget(self._number_files_label, 2, 1)
        self._options_layout.addWidget(self._number_files_textbox, 2, 2)

        self._size_files_label = QLabel()
        self._size_files_label.setText("Size of File(s)")
        self._size_files_label.setAlignment(QtCore.Qt.AlignCenter)

        self._size_files_textbox = QLineEdit()
        self._size_files_textbox.resize(320,20)
        self._size_files_textbox.setMinimumWidth(320)
        self._size_files_textbox.setValidator(self._validator)

        self._radio_button_layout = QHBoxLayout()
        self._radio_button_layout.setSpacing(5)
        self._radio_widget = QWidget() 
        self._radio_widget.setLayout(self._radio_button_layout)
        self._kb_button = QRadioButton("KiB")
        self._kb_button.setChecked(False)
        self._mb_button = QRadioButton("MiB")
        self._mb_button.setChecked(True)
        self._gb_button = QRadioButton("GiB")
        self._gb_button.setChecked(False)

        self._radio_button_layout.addWidget(self._kb_button, 1)
        self._radio_button_layout.addWidget(self._mb_button, 2)
        self._radio_button_layout.addWidget(self._gb_button, 3)

        self._options_layout.addWidget(self._size_files_label, 3, 1)
        self._options_layout.addWidget(self._size_files_textbox, 3, 2)
        self._options_layout.addWidget(self._radio_widget, 3, 3,
                                      QtCore.Qt.AlignLeft)

        self._advanced_layout = QGridLayout()
        self._advanced_layout.setContentsMargins(0,0,0,0)
        self._advanced_widget = QWidget()
        self._advanced_widget.setLayout(self._advanced_layout)
        self._options_layout.addWidget(self._advanced_widget, 4, 2)

        self._debug_label = QLabel()
        self._debug_label.setText("Debug")
        self._debug_label.setMaximumHeight(17)
        self._debug_label.setAlignment(QtCore.Qt.AlignRight)
        self._advanced_layout.addWidget(self._debug_label, 1, 1)

        self._debug_checkbox = QCheckBox()
        self._debug_checkbox.setChecked(False)
        self._debug_checkbox.setToolTip("Impacts performance")
        self._advanced_layout.addWidget(self._debug_checkbox, 1, 2,
                                        QtCore.Qt.AlignLeft)

        self._chunksize_label = QLabel()
        self._chunksize_label.setText("Chunk Size")
        self._chunksize_label.setMaximumHeight(17)
        self._chunksize_label.setAlignment(QtCore.Qt.AlignRight)
        self._advanced_layout.addWidget(self._chunksize_label, 1, 3)

        self._chunksize_textbox = QLineEdit()
        self._chunksize_textbox.setText("1024")
        self._chunksize_textbox.resize(50,20)
        self._chunksize_textbox.setMaximumWidth(50)
        self._chunksize_textbox.setValidator(self._validator)
        self._advanced_layout.addWidget(self._chunksize_textbox, 1, 4,
                                        QtCore.Qt.AlignCenter)
        
        self._chunksize_combobox = QComboBox()
        self._chunksize_combobox.addItems(["KiB", "MiB", "GiB"])
        self._advanced_layout.addWidget(self._chunksize_combobox, 1, 5,
                                        QtCore.Qt.AlignCenter)

        self._create_close_layout = QHBoxLayout()
        self._create_close_widget = QWidget() 
        self._create_close_widget.setLayout(self._create_close_layout)

        self._create_button = QPushButton("Create")
        self._create_button.setFixedWidth(80)
        self._create_button.clicked.connect(self._create_clicked)

        self._close_button = QPushButton("Close")
        self._close_button.setFixedWidth(80)
        self._close_button.clicked.connect(self._close_clicked)

        self._create_close_layout.addWidget(self._create_button, 1)
        self._create_close_layout.addWidget(self._close_button, 1)
        self._options_layout.addWidget(self._create_close_widget, 5, 2)

        self._window_layout.addWidget(self._options_widget)
        self._window_layout.setSizeConstraint(QLayout.SetFixedSize)

        self._debug_progress_bar = QProgressBar()
        self._debug_progress_bar.setContentsMargins(0,0,0,0)
        self._debug_progress_label = QLabel()
        self._debug_progress_label.setAlignment(QtCore.Qt.AlignCenter)
        self._debug_progress_label.setContentsMargins(0,0,0,0)

        self._overall_progress_bar = QProgressBar()
        self._overall_progress_bar.setContentsMargins(0,0,0,0)
        self._overall_progress_label = QLabel()
        self._overall_progress_label.setAlignment(QtCore.Qt.AlignCenter)
        self._overall_progress_label.setContentsMargins(0,0,0,0)

        self.setLayout(self._window_layout)


    # Opens About window when Help is choosen in top menu
    def _about_clicked(self):
        About()


    # Open native folder dialog to select where test files will be created
    def _browse_clicked(self):
        dialog = QFileDialog()
        path = str(QFileDialog.getExistingDirectory(dialog,
                                                         "Select Directory"))
        self._path_textbox.setText(path)    
   

    # Action to button Create
    def _create_clicked(self):
        if self._path_textbox.text() == "" or \
        self._number_files_textbox.text() == "" or \
        self._size_files_textbox.text() == "":
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText("You must fill all options to "\
                                       "create files")
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setStyleSheet("QLabel{min-width: 100px;}")
                msg.exec_()
        elif int(self._number_files_textbox.text()) == 0 or \
             int(self._size_files_textbox.text()) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText("Number of files/File size cannot be zero")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setStyleSheet("QLabel{min-width: 100px;}")
            msg.exec_()
        else:
            if self._kb_button.isChecked(): size_unit = 0
            elif self._mb_button.isChecked(): size_unit = 1
            else: size_unit = 2
            self.Files = FilesCreator(self._path_textbox.text(),
                                      self._number_files_textbox.text(),
                                      self._size_files_textbox.text(),
                                      size_unit,
                                      self._chunksize_textbox.text(),
                                      self._chunksize_combobox.currentIndex(),
                                      self._debug_checkbox.isChecked())
            self.thread = QThread()
            self.__threads.append((self.thread, self.Files))
            self.Files.moveToThread(self.thread)
            self.Files.sig_step_overall.connect(self._step_overall)
            self.Files.sig_step_file.connect(self._step_file)
            self.Files.sig_done.connect(self._done)  
            self.Files.sig_abort.connect(self._abort)
            self.thread.started.connect(self.Files.work)
            self.thread.start()
            self._change_layout('Running')


    # Action to button Close/Quit
    def _close_clicked(self):
        if self._close_button.text() == "Quit":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Quit")
            msg.setText("Are you sure you want to quit?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            quit_code = msg.exec_()
            if quit_code == QMessageBox.Yes:
                sys.exit(0)
        else:
            sys.exit(0)


    # Action to button Cancel
    def _cancel_clicked(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Confirmation")
        msg.setText("Are you sure?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        cancel_code = msg.exec_()
        if cancel_code == QMessageBox.Yes:
            self.Files.abort()
            self._change_layout('Stopped')


    # Changes layout when app is creating files / idle
    def _change_layout(self, status):
        if status == 'Running':
            self._files_created.clear()
            disabled_style = "background-color: rgb(210,210,210); border: gray"
            self._path_textbox.setStyleSheet(disabled_style)
            self._number_files_textbox.setStyleSheet(disabled_style)
            self._size_files_textbox.setStyleSheet(disabled_style)
            self._path_textbox.setDisabled(True)
            self._browse_button.setDisabled(True)
            self._number_files_textbox.setDisabled(True)
            self._size_files_textbox.setDisabled(True)
            self._kb_button.setDisabled(True)
            self._mb_button.setDisabled(True)
            self._gb_button.setDisabled(True)
            self._debug_checkbox.setDisabled(True)
            self._chunksize_textbox.setDisabled(True)
            self._chunksize_combobox.setDisabled(True)
            self._create_button.setText("Cancel")
            self._create_button.clicked.disconnect()
            self._create_button.clicked.connect(self._cancel_clicked)
            self._close_button.setText("Quit")
            self._close_button.clicked.disconnect()
            self._close_button.clicked.connect(self._close_clicked)

            self._debug_progress_label.setText("")
            self._debug_progress_bar.setValue(0)
            if self._debug_checkbox.isChecked():
                self._debug_progress_bar.show()
                self._debug_progress_label.show()
                self._debug_progress_bar.setContentsMargins(0,0,0,0)
                self._window_layout.addWidget(self._debug_progress_label)
                self._window_layout.addWidget(self._debug_progress_bar)

            self._overall_progress_bar.setContentsMargins(0,0,0,0)
            self._overall_progress_bar.setValue(0)
            self._overall_progress_label.setText("0/" + \
                                        str(self.Files._number_files))

            self._window_layout.addWidget(self._overall_progress_label)
            self._window_layout.addWidget(self._overall_progress_bar)

            self.repaint()
        else:
            self._path_textbox.setStyleSheet("")
            self._number_files_textbox.setStyleSheet("")
            self._size_files_textbox.setStyleSheet("")
            self._path_textbox.setDisabled(False)
            self._browse_button.setDisabled(False)
            self._number_files_textbox.setDisabled(False)
            self._size_files_textbox.setDisabled(False)
            self._kb_button.setDisabled(False)
            self._mb_button.setDisabled(False)
            self._gb_button.setDisabled(False)
            self._debug_checkbox.setDisabled(False)
            self._chunksize_textbox.setDisabled(False)
            self._chunksize_combobox.setDisabled(False)
            self._create_button.setText("Create")
            self._create_button.clicked.disconnect()
            self._create_button.clicked.connect(self._create_clicked)
            self._close_button.setText("Close")
            self._close_button.clicked.disconnect()
            self._close_button.clicked.connect(self._close_clicked)

            if self._debug_checkbox.isChecked():
                self._debug_progress_bar.hide()
                self._debug_progress_label.hide()
                self._window_layout.removeWidget(self._debug_progress_label)
                self._window_layout.removeWidget(self._debug_progress_bar)

            self._window_layout.removeWidget(self._overall_progress_label)
            self._window_layout.removeWidget(self._overall_progress_bar)

            self.repaint()


    # Method to treat error during file creation
    @pyqtSlot(str)
    def _abort(self, error: str):
        print(error)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText("Error. See details for more information.")
        msg.setDetailedText(error)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setStyleSheet("QLabel{min-width: 100px;}")
        msg.exec_()
        self._change_layout('Stopped')


    # Method to treat files creation completion
    @pyqtSlot()
    def _done(self):
        self._change_layout('Stopped')
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Info")
        msg.setText("Info")
        msg.setInformativeText("Files created!")
        detailed_text="Files created at " + self._path_textbox.text() + ":\n\n"
        for i in range(0,len(self._files_created)):
            detailed_text = detailed_text + self._files_created[i] + "\n"
        msg.setDetailedText(detailed_text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setStyleSheet("QLabel{min-width: 175px;}")
        msg.exec_()


    # Runs when each file is created to change progress bar UI values
    @pyqtSlot(str, int)
    def _step_overall(self, file_name: str, number_files: int):
        self._overall_progress_label.setText(str(self.Files.created_files) + "/" + \
                                    str(int(self._number_files_textbox.text())))
        value = number_files * 100 / int(self._number_files_textbox.text())
        self._overall_progress_bar.setValue(value)
        self._files_created.append(file_name)


    # Runs when each file chunk is generated to change progress bar UI values
    @pyqtSlot(str, int, int)
    def _step_file(self, file_name: str, chunk_idx: int, total: int):
        self._debug_progress_label.setText("Creating " + file_name + "...")
        value = (chunk_idx * 100) / total
        self._debug_progress_bar.setValue(value)


    # Handles clicking in Exit window button
    def closeEvent(self, event):
        self._close_clicked()

#------------------------------------------------------------------------------#

if __name__ == "__main__":
    app = QApplication([])

    window = MyWindow()
    window.show()

    sys.exit(app.exec_())