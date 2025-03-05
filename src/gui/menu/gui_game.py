# ----------------------------------
#
#   MENU TO PLAY GAME
#
# ----------------------------------


from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from src.gui.gui_game_top_panel import GUI_GameTopPanel
from src.gui.game_panel.gui_game_left_panel import GameLeftSideWidgets


class GUI_GameWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Main game scene
        from src.game_scene import GameScene
        self.game_scene = GameScene(self)
        self.game_scene.game_view.setContentsMargins(0, 0, 0, 0)

        # left panel menu with all interaction with end user
        self.game_left_side_widgets = GameLeftSideWidgets(self)
        self.game_left_side_widgets.setFixedWidth(300)
        self.game_left_side_widgets.setContentsMargins(0, 0, 0, 0)

        # Add the top widget to the game scene
        self.top_widget = GUI_GameTopPanel(self)
        self.top_widget.setContentsMargins(0, 0, 0, 0)

        # Create a horizontal layout
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setContentsMargins(0, 0, 0, 0)
        horizontal_layout.setSpacing(0)
        horizontal_layout.addWidget(self.game_left_side_widgets)

        # Create a vertical layout
        vertical_layout = QVBoxLayout()
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        vertical_layout.setSpacing(0)
        vertical_layout.addWidget(self.top_widget)
        vertical_layout.addWidget(self.game_scene.game_view)

        horizontal_layout.addLayout(vertical_layout)

        # Set the main layout
        self.setLayout(horizontal_layout)


    def showEvent(self, event):
        from PySide6.QtCore import QTimer
        QTimer.singleShot(100, self.game_scene.switch_to_country_by_tag)  # 500 seconds = 500000 milliseconds
        super().showEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            import random
            random_index = random.randint(0, self.game_left_side_widgets.count() - 1)
            self.game_left_side_widgets.switch_panel(random_index)

        super().keyPressEvent(event)