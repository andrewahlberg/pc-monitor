import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QWidget, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt, QEvent

class TrayApp(QWidget):
    def __init__(self):
        super().__init__()
        self.tray_icon = None
        self.init_ui()
        
        # Install the event filter
        QApplication.instance().installEventFilter(self)

    def init_ui(self):
        self.setWindowTitle('PC Monitor')
        self.setWindowIcon(QIcon('resources/icons/tray.png'))
        
        # Set window dimensions and style
        self.setGeometry(100, 100, 380, 600)
        self.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
        """)
        
        # Set shadow effect to the main window/widget
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 128))
        self.setGraphicsEffect(shadow)
        
        # Set the window to frameless and transparent
        self.setWindowFlags(self.windowFlags() | Qt.Tool | Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.build_ui()

        close_action = QAction("Exit", self)
        close_action.triggered.connect(sys.exit)

        tray_menu = QMenu()
        tray_menu.addAction(close_action)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('resources/icons/tray.png'))
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.setToolTip('PC Monitor')

    def build_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        
        label = QLabel("This is a tray application!")
        layout.addWidget(label)
        
        self.setLayout(layout)

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            # Calculate the position to make the window appear above the tray icon
            tray_position = self.tray_icon.geometry().center()
            self.move(tray_position.x() - self.width() // 2, tray_position.y() - self.height() - 10)

            if self.isVisible():
                self.hide()
            else:
                self.show()
                self.activateWindow()
                self.raise_()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.ApplicationDeactivate:
            self.close()
            return True
        
        return super().eventFilter(obj, event)

    def closeEvent(self, event):
        event.ignore()
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TrayApp()
    window.tray_icon.show()
    sys.exit(app.exec_())