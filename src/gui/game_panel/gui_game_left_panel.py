from PySide6.QtWidgets import QStackedWidget, QTabWidget, QVBoxLayout, QWidget
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

class GameLeftSideWidgets(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(300)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("""
            QTabBar::tab {
                border-bottom: none;
            }
            QTabBar::tab:selected {
                border: 2px solid gold;
                border-bottom: none;
            }
        """)

        layout = QVBoxLayout(self)
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setTabPosition(QTabWidget.North)
        layout.addWidget(self.tab_widget)

        print("GUI Creation")

        self.stacked_widget = QStackedWidget(self)
        self.tab_widget.addTab(self.stacked_widget,  "🛌")

        from src.gui.game_panel.gui_diplomacy import DiplomacyPanel
        panel_diplomacy = DiplomacyPanel(self)
        self.stacked_widget.addWidget(panel_diplomacy)
        self.tab_widget.addTab(panel_diplomacy,  "🛌")

        from src.gui.game_panel.gui_province import ProvincePanel
        panel_province = ProvincePanel(self)
        self.stacked_widget.addWidget(panel_province)
        self.tab_widget.addTab(panel_province,  "🛌")

        from src.gui.game_panel.gui_policy import DomesticPolicyPanel
        panel_policies = DomesticPolicyPanel(self)
        self.stacked_widget.addWidget(panel_policies)
        self.tab_widget.addTab(panel_policies,   "🛌")

        from src.gui.game_panel.gui_technology import TechnologyPanel
        panel_technologies = TechnologyPanel(self)
        self.stacked_widget.addWidget(panel_technologies)
        self.tab_widget.addTab(panel_technologies,   "🛌")

        from src.gui.game_panel.gui_budget import BudgetPanel
        panel_budget = BudgetPanel(self)
        self.stacked_widget.addWidget(panel_budget)
        self.tab_widget.addTab(panel_budget,  "🛌")

        from src.gui.game_panel.gui_recruit_army import RecruitArmyPanel
        panel_recruit_army = RecruitArmyPanel(self)
        self.stacked_widget.addWidget(panel_recruit_army)
        self.tab_widget.addTab(panel_recruit_army,  "🛌")

        from src.gui.game_panel.gui_battle_land import BattleLandPanel
        panel_battle_land = BattleLandPanel(self)
        self.stacked_widget.addWidget(panel_battle_land)
        self.tab_widget.addTab(panel_battle_land,   "🛌")

        from src.gui.game_panel.gui_country import CountryPanel
        panel_country = CountryPanel(self)
        self.stacked_widget.addWidget(panel_country)
        self.tab_widget.addTab(panel_country,   "🛌")

        from src.gui.game_panel.gui_cot import CenterOfTradePanel
        panel_cot = CenterOfTradePanel(self)
        self.stacked_widget.addWidget(panel_cot)
        self.tab_widget.addTab(panel_cot,   "🛌")

        from src.gui.game_panel.gui_religion_culture import ReligionCulturePanel
        panel_religion_culture = ReligionCulturePanel(self)
        self.stacked_widget.addWidget(panel_religion_culture)
        self.tab_widget.addTab(panel_religion_culture,  "🛌")

    def switch_panel(self, index):
        self.stacked_widget.setCurrentIndex(index)
        self.tab_widget.setCurrentIndex(index)

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    main_window = GameLeftSideWidgets()
    main_window.show()
    sys.exit(app.exec())