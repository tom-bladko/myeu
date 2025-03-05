import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QStackedWidget

import world
from src.gui.menu.gui_starter import GUI_StarterWidget
from src.gui.menu.gui_options import GUI_OptionsWidget
from src.gui.menu.gui_pick_scenario import GUI_PickScenarioWidget
from src.gui.menu.gui_game import GUI_GameWidget

class GameWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        print("Start game")
        self.setToolTipDuration(30000)
        self.setMouseTracking(True)

        self.setGeometry(100, 100, 1280, 960)
        self.setMinimumSize(1280, 960)

        from PySide6.QtWidgets import QApplication
        QApplication.instance().setStyleSheet("""
    QToolTip { background-color: #3A3A3A; color: #FFD700; border: 1px solid #FFD700; font-family: Consolas; font-size: 10pt; border-radius: 10px; }
    QWidget { background-color: #2A2A2A; color: #F0F0F0; font-family: Consolas; font-size: 10pt; }
    QMainWindow { background-color: #2A2A2A; }
    QMenuBar { background-color: #3A3A3A; color: #F0F0F0; }
    QMenu { background-color: #3A3A3A; color: #F0F0F0; }
    QStatusBar { background-color: #3A3A3A; color: #F0F0F0; }
    QPushButton { background-color: #4A4A4A; color: #F0F0F0; border: 1px solid #FFD700; border-radius: 5px; }
    QPushButton:hover { background-color: #5A5A5A; }
    QLineEdit { background-color: #3A3A3A; color: #F0F0F0; border: 1px solid #FFD700; border-radius: 5px; }
    QComboBox { background-color: #3A3A3A; color: #F0F0F0; border: 1px solid #FFD700; border-radius: 5px; }
    QCheckBox { color: #F0F0F0; }
    QLineEdit { background-color: #3A3A3A; color: #F0F0F0; border: 1px solid #FFD700; border-radius: 5px; }
    QListWidget { background-color: #3A3A3A; color: #F0F0F0; border: 1px solid #FFD700; border-radius: 5px; }
    QRadioButton { color: #F0F0F0; }
    QTabWidget::pane { border: 1px solid #FFD700; border-radius: 5px; padding: 1px; }
    QTabBar::tab { background: #3A3A3A; color: #F0F0F0; border: 1px solid #FFD700; padding: 5px; border-radius: 5px; }
    QTabBar::tab:selected { background: #4A4A4A; }
    QTextEdit { background-color: #3A3A3A; color: #F0F0F0; border: 1px solid #FFD700; border-radius: 5px; }
        """)

        # setup icon
        self.setWindowTitle( f"{world.APP_NAME}  ver: {world.APP_VERSION}" )
        ic = QIcon("icon.ico")
        if ic:
            self.setWindowIcon(ic)
        else:
            ic = QIcon("_internal/icon.ico")
            self.setWindowIcon(ic)

        # create main DB object
        from src.db import TDB
        self.db = TDB()
        self.db.current_zoom_index = 2

        # main stacked widget to switch menu

        self.global_stacked_widget = QStackedWidget()
        self.starter_widget = GUI_StarterWidget(self)
        self.pick_scenario_widget = GUI_PickScenarioWidget(self)
        self.option_widget = GUI_OptionsWidget(self)
        self.game_widget = GUI_GameWidget(self)
        self.db.game_scene = self.game_widget.game_scene

        self.global_stacked_widget.addWidget(self.starter_widget)
        self.global_stacked_widget.addWidget(self.pick_scenario_widget)
        self.global_stacked_widget.addWidget(self.option_widget)
        self.global_stacked_widget.addWidget(self.game_widget)

        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(self.global_stacked_widget)

        self.setCentralWidget(central_widget)

    def switch_to_starter_widget(self):
        self.global_stacked_widget.setCurrentWidget(self.starter_widget)

    def switch_to_game_widget(self):
        self.global_stacked_widget.setCurrentWidget(self.game_widget)

    def switch_to_options_widget(self):
        self.global_stacked_widget.setCurrentWidget(self.option_widget)

    def switch_to_pick_scenario_widget(self, selected_mod):

        # setup mod
        self.db.load_mod_data(selected_mod)

        self.global_stacked_widget.setCurrentWidget(self.pick_scenario_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())

import os
from PIL import Image

# Define the directory containing the icons
icon_dir = 'data/ftg/gfx/flag'

# Define the new size
new_size = (32, 32)

# Iterate over all files in the directory
for filename in os.listdir(icon_dir):
    if filename.endswith('.png'):
        # Construct the full file path
        file_path = os.path.join(icon_dir, filename)

        # Open the image
        with Image.open(file_path) as img:
            # Check if the image is 24x24
            if img.size == (24, 24):
                # Resize the image
                img_resized = img.resize(new_size)

                # Save the resized image back to the same path
                img_resized.save(file_path)

print("Rescaling complete.")