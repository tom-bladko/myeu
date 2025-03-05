# ----------------------------------
#
#   MENU TO PICK SCENARIO OR SAVED GAME
#
# ----------------------------------
import time

import toml
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QTextEdit, QListWidgetItem, \
	QPushButton, QSizePolicy, QScrollArea
from PySide6.QtCore import Qt, QSize

from src.battle.battle import Battle
from src.map.map_scenario import ScenarioLoader
from src.db import TDB

db = TDB()

class GUI_PickScenarioWidget(QWidget):
	def __init__(self, main_window):
		super().__init__()
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		self.scenario_loader : ScenarioLoader

		from main import GameWindow
		self.main_window: GameWindow = main_window

		# main layout

		main_layout = QHBoxLayout()
		main_layout.setAlignment(Qt.AlignCenter)
		main_layout.setContentsMargins(0, 0, 0, 0)

		self.current_country = 'REB'

		from src.db import TDB
		self.db = TDB()

		# Left side layout

		left_layout = QVBoxLayout()
		left_layout.setContentsMargins(0, 0, 0, 0)

		# List of scenarios

		self.scenario_list = QListWidget()
		self.scenario_list.setSelectionMode(QListWidget.SingleSelection)
		self.scenario_list.setFixedWidth(240)
		self.scenario_list.currentItemChanged.connect(self.on_scenario_item_clicked)
		left_layout.addWidget(QLabel("Scenarios"))
		left_layout.addWidget(self.scenario_list)

		# List of game saves

		self.save_list = QListWidget()
		self.save_list.setFixedWidth(240)
		left_layout.addWidget(QLabel("Game Saves"))
		left_layout.addWidget(self.save_list)

		# main layout

		main_layout.addLayout(left_layout)

		# Scenario description

		self.scenario_description = QTextEdit()
		self.scenario_description.setReadOnly(True)
		self.scenario_description.setTextInteractionFlags(Qt.NoTextInteraction)

		scenario_desc_layout = QVBoxLayout()
		scenario_desc_layout.addWidget(QLabel("Scenario Description"))
		scenario_desc_layout.addWidget(self.scenario_description)

		self.scenario_list.clearSelection()
		self.scenario_description.clear()

		# Bottom right layout

		bottom_right_layout = QHBoxLayout()

		# List of countries

		country_list_layout = QVBoxLayout()
		country_list_layout.addWidget(QLabel("Country List"))

		self.country_list = QListWidget()
		self.country_list.currentItemChanged.connect(self.on_country_list_clicked)
		self.country_list.setFixedWidth(240)
		self.country_list.setIconSize(QSize(32, 32))
		country_list_layout.addWidget(self.country_list)

		bottom_right_layout.addLayout(country_list_layout)

		# Country description

		self.country_mini_map = QLabel()
		self.country_mini_map.setAlignment(Qt.AlignCenter)
		self.country_mini_map.setStyleSheet("background-color: transparent; border: 1px solid black;")

		self.scroll_area = QScrollArea()
		self.scroll_area.setWidget(self.country_mini_map)
		self.scroll_area.setWidgetResizable(True)
		self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		country_desc_layout = QVBoxLayout()
		country_desc_layout.addWidget(QLabel("Mini Map"))
		country_desc_layout.addWidget(self.scroll_area)

		bottom_right_layout.addLayout(country_desc_layout)

		# Buttons layout

		buttons_layout = QVBoxLayout()

		self.button1 = QPushButton("Start")
		self.button1.setFixedSize(120, 30)
		self.button1.clicked.connect(self.start_scenario)

		self.button2 = QPushButton("Options")
		self.button2.setFixedSize(120, 30)

		self.button3 = QPushButton("Battle")
		self.button3.setFixedSize(120, 30)
		self.button3.clicked.connect(self.start_battle_simulation)

		self.return_button = QPushButton("Back")
		self.return_button.setFixedSize(120, 30)
		self.return_button.clicked.connect(self.main_window.switch_to_starter_widget)

		buttons_layout.addStretch()
		buttons_layout.addWidget(self.button1)
		buttons_layout.addWidget(self.button2)
		buttons_layout.addWidget(self.button3)
		buttons_layout.addWidget(self.return_button)
		bottom_right_layout.addLayout(buttons_layout)

		# Combine upper and bottom right layouts
		right_layout = QVBoxLayout()
		right_layout.addLayout(scenario_desc_layout, 1)
		right_layout.addLayout(bottom_right_layout, 2)

		main_layout.addLayout(right_layout)
		self.setLayout(main_layout)

	def start_battle_simulation(self):

		path = db.path_battle / 'test_battle.toml'
		with open(path, 'r') as f:
			battle_data = toml.load(f)

		for n in range(20):
			battle = Battle(battle_data)
			battle.prepare_battle(n)

	def start_scenario(self):
		# Add the logic to start the selected scenario
		current_item = self.scenario_list.currentItem()
		if current_item:
			scenario_name = current_item.text()
			print(f"Starting scenario: {scenario_name}")

			scenario = self.scenario_loader.select_scenario(scenario_name)
			scenario.load_content()

			from src.manager import manager_cot
			manager_cot.calculate_range_of_cots()

			# switch to selected country
			self.db.current_country_tag = self.current_country

			# switch to game widget
			self.main_window.switch_to_game_widget()

	def add_scenario_item(self, name, description):
		item = QListWidgetItem(name)
		item.setData(Qt.UserRole, description)
		self.scenario_list.addItem(item)

	def add_country_item(self, name, icon_path):
		item = QListWidgetItem(name)
		item.setIcon(QIcon(icon_path))
		self.country_list.addItem(item)

	def on_scenario_item_clicked(self, item: QListWidgetItem):
		scenario_name = item.text()
		print(f"Scenario clicked: {scenario_name}")

		if item:
			self.scenario_description.setText(item.data(Qt.UserRole))
		else:
			self.scenario_description.clear()

		scenario = self.scenario_loader.select_scenario(scenario_name)
		scenario.load_content()

		self.country_list.clear()
		self.country_mini_map.clear()

		# Add items to the country list
		for n, cnt in scenario.countries_details.items():
			self.add_country_item(f"{n} - {cnt['name']}", f"data/ftg/gfx/flag/{n}.png")

	def on_country_list_clicked(self, item: QListWidgetItem):

		country_name = item.text()
		print(f"Country clicked: {country_name}")

		country_name = country_name.split(" - ")[0]
		self.current_country = country_name

		# Create and display the mini map image
		from src.map.map_graphics import create_mini_map_image
		mini_map_pixmap = create_mini_map_image(country_name)
		self.country_mini_map.setPixmap(mini_map_pixmap)

	def showEvent(self, event):
		super().showEvent(event)
		self.on_widget_displayed()

	def on_widget_displayed(self):

		# load scenarios
		self.scenario_list.clear()
		self.scenario_loader = ScenarioLoader( self.db.path_scenarios / 'scenarios.toml' )
		self.scenario_loader.load_scenarios()
		for name, scen in self.scenario_loader.scenarios.items():
			self.add_scenario_item(name, scen.description)