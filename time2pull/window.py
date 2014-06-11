"""
This module contains the main window implementation.
"""
import os
from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimedia
from time2pull import __version__
from time2pull.constants import RemoteStatus
from time2pull.icons import get_status_icon, get_app_icon
from time2pull.forms.main_window_ui import Ui_MainWindow
from time2pull.settings import Settings
from time2pull.worker import WorkerThread


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self._user_warned_about_tray = False
        # configure refresh timer
        self.timer = QtCore.QTimer()
        self.timer.setInterval(60000)
        self.setupUi(self)
        # setup worker thread
        self.worker_thread = WorkerThread()
        self.worker_thread.start()
        self.worker_thread.finished.connect(self.on_refresh_finished)
        self.worker_thread.status_available.connect(self.on_status_available)
        # load repositories
        self.listWidgetRepos.clear()
        settings = Settings()
        for file in settings.repositories:
            item = QtWidgets.QListWidgetItem()
            item.setText(file)
            item.setIcon(get_status_icon())
            item.setData(QtCore.Qt.UserRole, (False, RemoteStatus.up_to_date))
            self.listWidgetRepos.addItem(item)
        # refresh ui
        self.pushButtonRemove.setEnabled(
            bool(len(self.listWidgetRepos.selectedItems())))
        self.pushButtonRefresh.setEnabled(bool(self.listWidgetRepos.count()))
        # run status refresh
        self.on_refresh_requested()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        # window properties
        icon = QtGui.QIcon(':/time2pull/icons/git-light.png')
        self.setWindowIcon(icon)
        self.setWindowTitle("Time2Pull")
        # refresh label movie
        self.movie = QtGui.QMovie(':/time2pull/icons/loader.gif')
        self.labelRefresh.setMovie(self.movie)
        # Tray icon
        self.tray_icon_menu = QtWidgets.QMenu(self)
        self.tray_icon_menu.addAction(self.actionAbout)
        self.tray_icon_menu.addSeparator()
        self.tray_icon_menu.addAction(self.actionQuit)
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(get_app_icon(False))
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.messageClicked.connect(self.on_message_clicked)
        self.tray_icon.activated.connect(self.on_icon_activated)
        self.tray_icon.show()
        self.actionQuit.triggered.connect(
            QtWidgets.QApplication.instance().quit)
        # connect slots to signals
        self.timer.timeout.connect(self.on_refresh_requested)
        self.pushButtonRefresh.clicked.connect(self.on_refresh_requested)
        self.listWidgetRepos.itemSelectionChanged.connect(
            self.on_selection_changed)

    def closeEvent(self, event):
        if self.tray_icon.isVisible():
            if not self._user_warned_about_tray:
                QtWidgets.QMessageBox.information(
                    self, "Time2Pull",
                    "The program will keep running in the system tray.\n"
                    "To terminate the program, choose Quit in the context menu"
                    " of the system tray entry.")
                self._user_warned_about_tray = True
            self.hide()
            event.ignore()

    def _get_repositories_to_refresh(self):
        return Settings().repositories

    @QtCore.pyqtSlot()
    def on_refresh_requested(self):
        repos = self._get_repositories_to_refresh()
        if repos:
            self.timer.stop()
            self.pushButtonRefresh.setEnabled(False)
            self.pushButtonAdd.setEnabled(False)
            self.pushButtonRemove.setEnabled(False)
            self.listWidgetRepos.setEnabled(False)
            self.labelRefresh.setVisible(True)
            self.movie.start()
            self.worker_thread.set_repositories_to_refresh(repos)
            self.worker_thread.wake_up()

    @QtCore.pyqtSlot()
    def on_refresh_finished(self):
        self.timer.start()
        self.pushButtonRefresh.setEnabled(bool(self.listWidgetRepos.count()))
        self.pushButtonAdd.setEnabled(True)
        self.pushButtonRemove.setEnabled(
            bool(len(self.listWidgetRepos.selectedItems())))
        self.listWidgetRepos.setEnabled(True)
        self.labelRefresh.setVisible(False)
        self.movie.stop()
        for i in range(self.listWidgetRepos.count()):
            item = self.listWidgetRepos.item(i)
            _, remote_status = item.data(QtCore.Qt.UserRole)
            if remote_status == RemoteStatus.behind:
                self.tray_icon.setIcon(get_app_icon(True))
                return
        self.tray_icon.setIcon(get_app_icon(False))

    @QtCore.pyqtSlot()
    def on_pushButtonAdd_clicked(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Select a repository')
        settings = Settings()
        if path and path not in settings.repositories:
            if os.path.exists(os.path.join(path, '.git')):
                repos = settings.repositories
                repos.append(path)
                settings.repositories = repos
                item = QtWidgets.QListWidgetItem()
                item.setText(path)
                item.setIcon(get_status_icon())
                item.setData(QtCore.Qt.UserRole, (False, RemoteStatus.up_to_date))
                self.listWidgetRepos.addItem(item)
                self.on_refresh_requested()
            else:
                QtWidgets.QMessageBox.warning(
                    self, 'Not a git repository',
                    'The chosen directory is not a git repository')

    @QtCore.pyqtSlot()
    def on_pushButtonRemove_clicked(self):
        repo = self.listWidgetRepos.currentItem().text()
        self.listWidgetRepos.takeItem(self.listWidgetRepos.currentRow())
        settings = Settings()
        repos = settings.repositories
        try:
            repos.remove(repo)
        except ValueError:
            pass
        settings.repositories = repos

    @QtCore.pyqtSlot()
    def on_selection_changed(self):
        self.pushButtonRemove.setEnabled(
            bool(len(self.listWidgetRepos.selectedItems())))

    def alert(self, repo):
        repo_name = QtCore.QFileInfo(repo).fileName()
        self.tray_icon.showMessage(
            repo_name,
            "Remote repository has been updated. It's time to pull!")
        QtMultimedia.QSound.play(':/time2pull/sounds/sonar.ogg')

    @QtCore.pyqtSlot(str, bool, object)
    def on_status_available(self, repo, dirty, remote_status):
        for i in range(self.listWidgetRepos.count()):
            item = self.listWidgetRepos.item(i)
            if item.text() == repo:
                item.setIcon(get_status_icon(dirty, remote_status))
                old_dirty_flg, old_remote_status = item.data(
                    QtCore.Qt.UserRole)
                item.setData(QtCore.Qt.UserRole, (dirty, remote_status))
                if(remote_status == RemoteStatus.behind and
                        old_remote_status != RemoteStatus.behind):
                    self.alert(repo)

    @QtCore.pyqtSlot(object)
    def on_icon_activated(self, reason):
        if reason in (QtWidgets.QSystemTrayIcon.Trigger,
                      QtWidgets.QSystemTrayIcon.DoubleClick):
            self.show()
            QtWidgets.QApplication.instance().setActiveWindow(self)
        elif reason == QtWidgets.QSystemTrayIcon.MiddleClick:
            self.showMessage()

    @QtCore.pyqtSlot()
    def on_message_clicked(self):
        self.show()
        QtWidgets.QApplication.instance().setActiveWindow(self)

    @QtCore.pyqtSlot()
    def on_actionAbout_triggered(self):
        QtWidgets.QMessageBox.about(
            self, 'About Time2Pull',
            'Time2Pull is small application that monitors your local git '
            'repositories and warns you when a remote got updated.'
            '\n'
            '\n'
            'Time2Pull is a free open source software licensed under the GPL '
            'v3. The application is written in Python using the PyQt5 GUI '
            'toolkit.'
            '\n'
            '\n'
            'Author: Colin Duquesnoy\n'
            'Version: %s' % __version__)