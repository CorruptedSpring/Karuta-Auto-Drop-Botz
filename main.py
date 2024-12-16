import sys
from PySide6 import QtCore, QtWidgets, QtGui
import subprocess
import signal
import os

def GetData():
        with open("otherdata.data", "r") as file:
            data = file.readlines()
        return data

class MyWidget(QtWidgets.QWidget):
    def __init__(self):

        super().__init__()
        self.bot_process = None
        self.setWindowTitle("DiscordWhatsAppLinker Bot")
        self.setWindowIcon(QtGui.QIcon("Assets/icon.ico"))
        self.NameLabel = QtWidgets.QLabel("Name :")
        self.DiscordTokenLabel = QtWidgets.QLabel("Discord Account Token :")
        self.AddBotButton = QtWidgets.QPushButton("Add Bot")
        self.StartButton = QtWidgets.QPushButton("Start Bot")
        self.NameInput = QtWidgets.QLineEdit()
        self.TokenInput = QtWidgets.QLineEdit()
        self.NameInput.setPlaceholderText("Name")
        self.TokenInput.setPlaceholderText("Discord Account Token")
        self.NameInput.setFixedSize(200, 50)
        self.TokenInput.setFixedSize(200, 50)
        self.StartButton.setStyleSheet(" background-color: #42f569;color: #fff;")
        self.AddBotButton.setStyleSheet("background-color: #4548ff; color: #fff;")
        self.AddBotButton.setFixedSize(100, 50)
        self.StartButton.setFixedSize(100, 50)
        self.NameInput.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.TokenInput.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.StartButton)
        self.button_layout.addStretch()
        
        self.layout = QtWidgets.QVBoxLayout(self)
        input_layout = QtWidgets.QHBoxLayout()
        input_layout.addWidget(self.NameLabel)
        input_layout.addWidget(self.NameInput)
        input_layout.addWidget(self.DiscordTokenLabel)
        input_layout.addWidget(self.TokenInput)
        input_layout.addWidget(self.AddBotButton)
        
        AccountsList_layout = QtWidgets.QVBoxLayout()
        self.AccountsListWidget = QtWidgets.QListWidget()
        self.loadAccountsList()
        
        AccountsList_layout.addWidget(QtWidgets.QLabel("Account List:"))
        AccountsList_layout.addWidget(self.AccountsListWidget)
        self.layout.addLayout(input_layout)
        self.layout.addLayout(AccountsList_layout)
        self.layout.addLayout(self.button_layout)

        self.ChannelIDLabel = QtWidgets.QLabel("Channel ID:")
        self.TimeBetweenDropsLabel = QtWidgets.QLabel("Time Between Drops (s):")
        self.ChannelIDInput = QtWidgets.QLineEdit()
        self.TimeBetweenDropsInput = QtWidgets.QLineEdit()
        self.ConfirmButton = QtWidgets.QPushButton("Confirm")
        
        self.ChannelIDInput.setPlaceholderText(GetData()[0].strip())
        self.TimeBetweenDropsInput.setPlaceholderText(GetData()[1].strip()+" seconds")
        self.ChannelIDInput.setFixedSize(200, 50)
        self.TimeBetweenDropsInput.setFixedSize(200, 50)
        self.ConfirmButton.setFixedSize(100, 50)
        self.ConfirmButton.setStyleSheet("background-color: #42a1f5; color: #fff;")
        
        self.ChannelIDInput.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.TimeBetweenDropsInput.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        self.drop_settings_layout = QtWidgets.QHBoxLayout()
        self.drop_settings_layout.addWidget(self.ChannelIDLabel)
        self.drop_settings_layout.addWidget(self.ChannelIDInput)
        self.drop_settings_layout.addWidget(self.TimeBetweenDropsLabel)
        self.drop_settings_layout.addWidget(self.TimeBetweenDropsInput)
        self.drop_settings_layout.addWidget(self.ConfirmButton)

        self.layout.addLayout(self.drop_settings_layout)

        self.AddBotButton.clicked.connect(self.AddAccountsToList)
        self.ConfirmButton.clicked.connect(self.confirmDropSettings)
        self.StartButton.clicked.connect(self.StartBot)

        
    def loadAccountsList(self):
        try:
            with open("accounts.data", "r") as file:
                lines = file.readlines()[1:]
                for line in lines:
                    account = line.strip().split(":")
                    if len(account) == 2:
                        self.addAccountToWidget(account[0].strip(), account[1].strip())
        except Exception as e:
            confirm_dialog = QtWidgets.QMessageBox(self)
            confirm_dialog.setWindowTitle("Error")
            confirm_dialog.setText(e)
            confirm_dialog.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            confirm_dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            confirm_dialog.exec()

    def addAccountToWidget(self, name, token):
        item = QtWidgets.QListWidgetItem()
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        
        label = QtWidgets.QLabel(f"Name: {name} \t Token: {token}")
        removeBtn = QtWidgets.QPushButton("Remove")
        removeBtn.setStyleSheet("background-color: #f54242; color: #fff;")
        removeBtn.setFixedWidth(70)
        
        layout.addWidget(label)
        layout.addWidget(removeBtn)
        widget.setLayout(layout)
        
        item.setSizeHint(widget.sizeHint())
        self.AccountsListWidget.addItem(item)
        self.AccountsListWidget.setItemWidget(item, widget)
        
        removeBtn.clicked.connect(lambda: self.removeAccount(item, name, token))

    def removeAccount(self, item, name, token):
        try:
            confirm_dialog = QtWidgets.QMessageBox(self)
            confirm_dialog.setWindowTitle("Confirm")
            confirm_dialog.setText(f"Are you sure you want to remove this account?\n Name : '{name}'")
            confirm_dialog.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            confirm_dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            result = confirm_dialog.exec()
            
            if result == QtWidgets.QMessageBox.StandardButton.Yes:
                with open("accounts.data", "r") as file:
                    lines = file.readlines()
                
                with open("accounts.data", "w") as file:
                    file.write(lines[0])
                    for line in lines[1:]:
                        if f"{name}:{token}" not in line:
                            file.write(line)
                
                self.AccountsListWidget.takeItem(self.AccountsListWidget.row(item))
        except Exception as e:
            confirm_dialog = QtWidgets.QMessageBox(self)
            confirm_dialog.setWindowTitle("Error")
            confirm_dialog.setText(e)
            confirm_dialog.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            confirm_dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            confirm_dialog.exec()

    @QtCore.Slot()
    def StartBot(self):
        if self.bot_process is None:
            self.bot_process = subprocess.Popen([sys.executable, "bot_script.py"])
            self.StopButton = QtWidgets.QPushButton("Stop Bot")
            self.StopButton.setStyleSheet("background-color: #f54242; color: #fff;")
            self.StopButton.setFixedSize(100, 50)
            self.StartButton.hide()
            self.button_layout.replaceWidget(self.StartButton, self.StopButton)
            self.StopButton.clicked.connect(self.StopBot)
            
            self.AddBotButton.setDisabled(True)
            self.NameInput.setDisabled(True)
            self.TokenInput.setDisabled(True)
            self.ChannelIDInput.setDisabled(True)
            self.TimeBetweenDropsInput.setDisabled(True)
            self.ConfirmButton.setDisabled(True)
            self.AccountsListWidget.setDisabled(True)

    def StopBot(self):
        if self.bot_process:
            if sys.platform == "win32":
                subprocess.run(['taskkill', '/F', '/T', '/PID', str(self.bot_process.pid)])
            else:
                self.bot_process.send_signal(signal.SIGTERM)
            self.bot_process = None
            
        self.StopButton.hide()
        self.StartButton.show()
        self.button_layout.replaceWidget(self.StopButton, self.StartButton)
        self.StopButton.deleteLater()
        
        self.AddBotButton.setDisabled(False)
        self.NameInput.setDisabled(False)
        self.TokenInput.setDisabled(False)
        self.ChannelIDInput.setDisabled(False)
        self.TimeBetweenDropsInput.setDisabled(False)
        self.ConfirmButton.setDisabled(False)
        self.AccountsListWidget.setDisabled(False)

    def AddAccountsToList(self):
        name = self.NameInput.text().strip()
        token = self.TokenInput.text().strip()
        
        if not name or not token:
            return
            
        try:
            with open("accounts.data", "r") as file:
                lines = file.readlines()
            for line in lines[1:]:
                account = line.strip().split(":")
                if len(account) != 2:
                    continue
                if account[0].strip() == name:
                    
                    error_dialog = QtWidgets.QMessageBox(self)
                    error_dialog.setWindowTitle("Error")
                    error_dialog.setText("Name already exist.")
                    error_dialog.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    error_dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    error_dialog.exec()
                    return
                if account[1].strip() == token:
                    error_dialog = QtWidgets.QMessageBox(self)
                    error_dialog.setWindowTitle("Error")
                    error_dialog.setText("Token already exist.")
                    error_dialog.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    error_dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    error_dialog.exec()
                    return
            
            with open("accounts.data", "w") as file:
                for line in lines:
                    file.write(line)        
                file.write(f"{name}:{token}\n")
            self.addAccountToWidget(name, token)
            self.NameInput.clear()
            self.TokenInput.clear()
                
        except Exception as e:
            confirm_dialog = QtWidgets.QMessageBox(self)
            confirm_dialog.setWindowTitle("Error")
            confirm_dialog.setText(e)
            confirm_dialog.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            confirm_dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            confirm_dialog.exec()

    def confirmDropSettings(self):
        channel_id = self.ChannelIDInput.text().strip()
        time_between_drops = self.TimeBetweenDropsInput.text().strip()
        
        if not channel_id:
            channel_id = self.ChannelIDInput.placeholderText()
        if not time_between_drops:
            time_between_drops = self.TimeBetweenDropsInput.placeholderText().split()[0]
        
        try:
            time_between_drops = int(time_between_drops.split()[0]) if "seconds" in time_between_drops else int(time_between_drops)
            with open("otherdata.data", "w") as file:
                file.write(f"{channel_id}\n{time_between_drops}")
        except ValueError:
            error_dialog = QtWidgets.QMessageBox(self)
            error_dialog.setWindowTitle("Input Error")
            error_dialog.setText("Time Between Drops must be an integer.")
            error_dialog.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            error_dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            error_dialog.exec()
        
        self.ChannelIDInput.clear()
        self.TimeBetweenDropsInput.clear()

if __name__ == "__main__":

    if not os.path.exists("accounts.data"):
        with open("accounts.data", "w") as f:
            f.write("Name\t Token\n")
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())