from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QPushButton, QSizePolicy

from src.db import TDB
db = TDB()

class GUI_GameTopPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(32)
        self.setStyleSheet("background-color: #333; color: white; font-size: 14px;")
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        layout.addStretch()

        # Add gold, stability, fame
        self.add_icon_with_text(layout, "gold", "1000", "Gold tooltip")
        layout.addStretch()
        self.add_icon_with_text(layout, "stability", "+3", "Stability tooltip")
        self.add_icon_with_text(layout, "fame", "-12", "Fame tooltip")
        self.add_icon_with_text(layout, "manpower", "10", "Manpower tooltip")
        layout.addStretch()

        # Add agents
        agents = ["merchant", "diplomat", "explorer", "engineer", "inventor", "advisor", "general", "missionary"]
        for agent in agents:
            self.add_icon_with_text(layout, agent, f"12", f"{agent.capitalize()} tooltip")

        # Add current date
        self.date_label = QLabel("Dec\n1560")
        self.date_label.setStyleSheet("background-color: transparent; font-size: 14px;")
        layout.addStretch()
        layout.addWidget(self.date_label)

        # Add end turn button
        self.end_turn_button = QPushButton("End Turn")
        self.end_turn_button.setFixedSize(80,30)

        layout.addWidget(self.end_turn_button)
        self.end_turn_button.clicked.connect(self.end_turn)
        layout.addStretch()

        self.setLayout(layout)

    def end_turn(self):
        print("End Turn button clicked")

    def add_icon_with_text(self, layout, icon_name, text, tooltip):
        icon_label = QLabel()

        icon_label.setPixmap(QPixmap( f'data/ftg/gfx/agents/{icon_name}.png'))
        icon_label.setToolTip(tooltip)
        icon_label.setStyleSheet("background-color: transparent; font-size: 14px;")
        layout.addWidget(icon_label)

        text_label = QLabel(text)
        text_label.setStyleSheet("background-color: transparent; font-size: 14px;")
        layout.addWidget(text_label)

