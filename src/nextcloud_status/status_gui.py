import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QComboBox,
                             QVBoxLayout, QPushButton, QApplication, QListWidget,
                             QListWidgetItem)
from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtGui import QFont
from nextcloud_status import *
from pkg_resources import resource_filename



class EmojiPicker(QWidget):
    def __init__(self, emojis, callback):
        super().__init__()
        self.callback = callback
        self.initUI(emojis)

    def initUI(self, emojis):
        self.verticalLayout = QVBoxLayout(self)
        self.search = QLineEdit(self)
        self.search.textChanged.connect(self.updateList)
        self.verticalLayout.addWidget(self.search)

        self.listWidget = QListWidget(self)
        self.verticalLayout.addWidget(self.listWidget)
        self.listWidget.itemClicked.connect(self.itemSelected)

        emoji_font = QFont("Segoe UI Emoji", 12)  # Specify the font and size you want
        self.listWidget.setFont(emoji_font)

        self.emojis = emojis
        self.filtered_emojis = list(emojis.keys())
        self.updateList()

    def updateList(self):
        search_text = self.search.text().lower()
        self.listWidget.clear()
        for emoji, description in self.emojis.items():
            if search_text in description:
                item = QListWidgetItem(emoji, self.listWidget)
                item.setData(Qt.UserRole, description)

    def itemSelected(self, item):
        self.callback(item.text())  # `text()` here directly returns the emoji
        self.hide()

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

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
        self.status.addItems(["online", "away", "dnd", "offline"])
        layout.addWidget(self.status)

        # Message Label and LineEdit
        self.message_label = QLabel('Message:', self)
        layout.addWidget(self.message_label)
        self.message = QLineEdit(self)
        layout.addWidget(self.message)

        # Emoji Label and Button
        self.emoji_label = QLabel('Icon: None', self)
        layout.addWidget(self.emoji_label)
        self.emoji_button = QPushButton('Choose Emoji', self)
        self.emoji_button.clicked.connect(self.openEmojiPicker)
        layout.addWidget(self.emoji_button)

        # Send Button
        self.send_button = QPushButton('Send', self)
        layout.addWidget(self.send_button)

        self.setLayout(layout)
        self.emoji_picker = EmojiPicker(emojis=self.get_emojis(), callback=self.setEmoji)

        self.resize(300, 200)

    def openEmojiPicker(self):
        self.emoji_picker.show()

    def setEmoji(self, emoji):
        if emoji:
            self.emoji_label.setText(f"Icon: {emoji}")
        else:
            self.emoji_label.setText("Icon: None")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())

