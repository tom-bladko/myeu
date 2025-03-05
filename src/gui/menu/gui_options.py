# ----------------------------------
#
#   MENU TO SELECT OPTIONS
#
# ----------------------------------
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QPushButton, QSizePolicy


class GUI_OptionsWidget(QWidget):
	def __init__(self, main_window):
		super().__init__()

		from main import GameWindow
		self.main_window: GameWindow = main_window

		return_button = QPushButton("Back", self)
		return_button.clicked.connect(self.main_window.switch_to_starter_widget)
		return_button.setGeometry(800-120,600-30,120,30)

		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)