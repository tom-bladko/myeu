'''

MAIN

MAIN GAME UI

'''

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QStackedWidget, QInputDialog
from PySide6.QtWidgets import QVBoxLayout, QWidget


class GameWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        print("Start game")
        self.setToolTipDuration(30000)
        self.setMouseTracking(True)

        self.setWindowTitle("For The Europa")
        self.setGeometry(100, 100, 1280, 960)

        from src.db import TDB
        self.db = TDB()
        self.db.current_zoom_index = 2

        # create scene
        from game_scene import GameScene
        self.game_scene = GameScene()

        # create game logic
        import game_logic
        game_logic.create_managers()

        # setup game logic and game scene to db
        self.db.game_scene = self.game_scene

        # setup mod
        self.db.setup_mod('mods/ftg')

        # load mod
        from src.res import map_loader
        map_loader.load_mod()

        # create all background calculation
        game_logic.process_game_logic_before()

        # here enter GUI
        self.create_gui()

        # Create a top-level widget to hold the layout
        self.global_widget = QWidget()
        self.global_layout = QHBoxLayout(self.global_widget)

        # Add the panel container and game view to the layout
        self.global_layout.addWidget(self.menu_widget)
        self.global_layout.addWidget(self.game_scene.game_view)

        # Set the top-level widget as the central widget
        self.setCentralWidget(self.global_widget)

        # create all map graphics
        self.game_scene.create_graphics()

        # make full screen
        # self.showMaximized()
        self.game_scene.apply_zoom()

        from src.res.scenario import ScenarioLoader
        scenario_loader = ScenarioLoader(self.db.path_mod / "scenarios" / 'world.yml')
        scenario_loader.load_scenarios()
        scenario = scenario_loader.select_scenario('1399')
        scenario.load_content()

        # self.db.center_trade_manager.calculate_range_of_cots()

        tag_to_own = 'POL'
        self.db.province_manager.switch_current_country_tag(tag_to_own)
        self.db.province_manager.switch_map_mode('terrain')

    #
    #   GUI
    #

    def create_gui(self):
        print("GUI Creation" )
        # create menu widget
        self.menu_widget = QStackedWidget()
        self.menu_widget.setFixedWidth(300)

        # Create 10 panels with random widgets

        from src.gui.diplomacy import DiplomacyPanel
        panel_diplomacy = DiplomacyPanel(self.menu_widget)
        self.menu_widget.addWidget(panel_diplomacy)

        from src.gui.province import ProvincePanel
        panel_province = ProvincePanel(self.menu_widget)
        self.menu_widget.addWidget(panel_province)

        from src.gui.policies import DomesticPolicyPanel
        panel_policies = DomesticPolicyPanel(self.menu_widget)
        self.menu_widget.addWidget(panel_policies)

        from src.gui.technology import TechnologyPanel
        panel_technologies = TechnologyPanel(self.menu_widget)
        self.menu_widget.addWidget(panel_technologies)

        from src.gui.budget import BudgetPanel
        panel_budget = BudgetPanel(self.menu_widget)
        self.menu_widget.addWidget(panel_budget)

        from src.gui.recruit_army import RecruitArmyPanel
        panel_recruit_army = RecruitArmyPanel(self.menu_widget)
        self.menu_widget.addWidget(panel_recruit_army)

        from src.gui.battle_land import BattleLandPanel
        panel_battle_land = BattleLandPanel(self.menu_widget)
        self.menu_widget.addWidget(panel_battle_land)

        from src.gui.country import CountryPanel
        panel_country = CountryPanel(self.menu_widget)
        self.menu_widget.addWidget(panel_country)

        from src.gui.cot import CenterOfTradePanel
        panel_cot = CenterOfTradePanel(self.menu_widget)
        self.menu_widget.addWidget(panel_cot)

        from src.gui.religion_culture import ReligionCulturePanel
        panel_religion_culture = ReligionCulturePanel(self.menu_widget)
        self.menu_widget.addWidget(panel_religion_culture)

        from src.gui.editor import EditorPanel
        panel_editor = EditorPanel(self.menu_widget)
        self.menu_widget.addWidget(panel_editor)

        container_layout = QVBoxLayout()
        container_layout.addWidget(self.menu_widget)

        self.menu_widget.setLayout(container_layout)
        self.menu_widget.setParent(self)
        self.menu_widget.move(0, 0)

    def switch_panel(self, index):
        self.menu_widget.setCurrentIndex(index)

    #
    #   KEYBOARD EVENTS GLOBAL
    #
    #
    #   KEYBOARD EVENTS
    #

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Backspace:
            import random
            random_index = random.randint(0, self.menu_widget.count() - 1)
            self.switch_panel(random_index)

        super().keyPressEvent(event)
        self.update()  # Ensure the scene is updated after dragging



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    viewer = GameWindow()
    viewer.show()
    sys.exit(app.exec())