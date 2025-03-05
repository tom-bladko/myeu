# ----------------------------------
#
#   MENU TO START
#
# ----------------------------------
import toml
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QComboBox, QSizePolicy
from PySide6.QtCore import Qt, QCoreApplication

import world

class GUI_StarterWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()

        from main import GameWindow
        self.main_window : GameWindow = main_window
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # VERSION AND NAME

        game_name_label = QLabel(f"{world.APP_NAME}\nver: {world.APP_VERSION}")
        game_name_label.setFixedWidth(120)
        game_name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(game_name_label)

        # PLAY GAME

        new_game_button = QPushButton("PLAY")
        new_game_button.setFixedSize(120, 30)
        new_game_button.clicked.connect(self.start_new_game)
        layout.addWidget(new_game_button)

        # SELECT MOD

        self.mod_combo_box = QComboBox()
        self.mod_combo_box.setFixedSize(120, 30)
        self.mod_combo_box.setStyleSheet("padding-left: 5px;")

        # load all yaml files
        import yaml
        with open('data/mods.toml', 'r') as file:
            mods_data = toml.load(file)
        for mod in mods_data['mods']:
            self.mod_combo_box.addItem(mod['name'])
        layout.addWidget(self.mod_combo_box)

        # GO TO OPTIONS

        options_button = QPushButton("OPTIONS")
        options_button.clicked.connect(self.main_window.switch_to_options_widget)
        options_button.setFixedSize(120, 30)
        layout.addWidget(options_button)

        # OPEN EDITOR

        editor_button = QPushButton("EDITOR")
        editor_button.setFixedSize(120, 30)
        layout.addWidget(editor_button)

        # GO TO WIKI

        wiki_button = QPushButton("WIKI")
        wiki_button.setFixedSize(120, 30)
        layout.addWidget(wiki_button)

        # QUIT GAME

        quit_game_button = QPushButton("QUIT")
        quit_game_button.setFixedSize(120, 30)
        quit_game_button.clicked.connect(self.quit_game)
        layout.addWidget(quit_game_button)

        self.setLayout(layout)

    def quit_game(self):
        QCoreApplication.instance().quit()

    def start_new_game(self):
        selected_mod = self.mod_combo_box.currentText()
        print("Mod selected", selected_mod)
        self.main_window.switch_to_pick_scenario_widget(selected_mod)


