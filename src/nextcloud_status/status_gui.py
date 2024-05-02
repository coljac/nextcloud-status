import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QComboBox,
                             QVBoxLayout, QPushButton, QApplication, QListWidget, QListWidgetItem, QGridLayout)
from PyQt5.QtCore import Qt, QVariant, QSize, QCoreApplication
from PyQt5.QtGui import QFont
from .nextcloud_status import StatusEnum, set_status
from pkg_resources import resource_filename
import json


class EmojiPicker(QWidget):
    def __init__(self, emojis, callback):
        super().__init__()
        self.callback = callback
        self.initUI(emojis)

    def initUI(self, emojis):
        self.gridLayout = QGridLayout(self)
        # self.verticalLayout = QVBoxLayout(self)
        self.search = QLineEdit(self)
        self.search.textChanged.connect(self.updateList)
        self.gridLayout.addWidget(self.search, 0, 0, 1, 4)  # Span across 4 columns
        # self.verticalLayout.addWidget(self.search)

        self.listWidget = QListWidget(self)
        self.listWidget.setViewMode(QListWidget.IconMode)
        self.listWidget.setResizeMode(QListWidget.Adjust)
        self.listWidget.setLayoutMode(QListWidget.Batched)
        self.listWidget.setGridSize(QSize(40, 40))
        self.listWidget.setSpacing(5)
        self.gridLayout.addWidget(self.listWidget, 1, 0, 4, 4)  # Span multiple rows and columns

        # gridLayout.addWidget(self.listWidget, 1, 0, 4, 4)  # Span multiple rows and columns
        # self.listWidget = QListWidget(self)
        # self.verticalLayout.addWidget(self.listWidget)
        # self.listWidget.itemClicked.connect(self.itemSelected)
        # self.listWidget.setGridSize(Qt.QSize(50, 50))

        emoji_font = QFont("Segoe UI Emoji", 16)  # Specify the font and size you want
        self.listWidget.setFont(emoji_font)

        self.emojis = emojis
        self.filtered_emojis = list(emojis.keys())
        self.updateList()
        self.listWidget.itemClicked.connect(self.itemSelected)

    def updateList_old(self):
        search_text = self.search.text().lower()
        self.listWidget.clear()
        for emoji, description in self.emojis.items():
            if search_text in description:
                item = QListWidgetItem(emoji, self.listWidget)
                item.setData(Qt.UserRole, description)

    def updateList(self):
        search_text = self.search.text().lower()
        self.listWidget.clear()
        for emoji in self.emojis:
            if search_text in self.emojis[emoji]:
                item = QListWidgetItem(emoji, self.listWidget)
                item.setSizeHint(QSize(45, 45))

    def itemSelected(self, item):
        self.callback(item.text())  # `text()` here directly returns the emoji
        self.hide()

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.icon = None

    def get_emojis(self):
        with open(resource_filename("nextcloud_status", "gh_emoji.json"), "r") as f:
            emoji_map = json.loads(f.read())
            emoji_map = dict((v,k) for k,v in emoji_map.items())
        return emoji_map


    def initUI(self):
        self.setWindowTitle('Simple GUI')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        layout = QVBoxLayout()

        # Status Label and ComboBox
        self.status_label = QLabel('Status:', self)
        layout.addWidget(self.status_label)
        self.status = QComboBox(self)
        self.status.addItems(StatusEnum)#["online", "away", "dnd", "busy", "offline"])
        layout.addWidget(self.status)
        # self.status.currentIndexChanged.connect(self.setStatus)

        # Message Label and LineEdit
        self.message_label = QLabel('Message:', self)
        layout.addWidget(self.message_label)
        self.message = QLineEdit(self)
        layout.addWidget(self.message)

        # Emoji Label and Button
        self.emoji_label = QLabel('Icon: None', self)
        emoji_font = QFont("Segoe UI Emoji", 12)  # Set the font for emoji display
        self.emoji_label.setFont(emoji_font)
        layout.addWidget(self.emoji_label)
        self.emoji_button = QPushButton('Choose Emoji', self)
        self.emoji_button.clicked.connect(self.openEmojiPicker)
        layout.addWidget(self.emoji_button)

        # Send Button
        self.send_button = QPushButton('Send', self)
        self.send_button.clicked.connect(self.setStatus)
        layout.addWidget(self.send_button)

        self.setLayout(layout)
        self.emoji_picker = EmojiPicker(emojis=self.get_emojis(), callback=self.setEmoji)

        self.resize(300, 200)

    def openEmojiPicker(self):
        self.emoji_picker.show()

    def setEmoji(self, emoji):
        if emoji:
            self.emoji_label.setText(f"Icon: {emoji}")
            self.icon = emoji
        else:
            self.emoji_label.setText("Icon: None")

    def setStatus(self):
        status = self.status.currentText()
        message = self.message.text()
        icon = self.icon
        set_status(status, message = message, icon=icon)
        QCoreApplication.instance().quit()

def show():
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    show()
