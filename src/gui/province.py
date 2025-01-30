from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget, QGridLayout, QTableWidget, QTableWidgetItem, \
    QHBoxLayout, QSizePolicy, QHeaderView


class ProvincePanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(4, 4, 4, 4)
        self.setFixedWidth(300)
        self.init_ui()

    def init_ui(self):

        print("  GUI - province info panel")

        # Add province name label
        main_label = QLabel("<b>PROVINCE DETAILS</b>")
        main_label.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(main_label)

        # Add province name label
        province_label = QLabel("Province:  Pomerania")
        province_label.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(province_label)

        # Add images
        image_layout = QHBoxLayout()
        owner_image = QLabel("Owner Image")
        province_image = QLabel("Province Image")
        occupier_image = QLabel("Occupier Image")
        image_layout.addWidget(owner_image)
        image_layout.addWidget(province_image)
        image_layout.addWidget(occupier_image)
        self.layout().addLayout(image_layout)

        # Add statistics label
        statistics_label = QLabel("<b>Statistics</b>")
        statistics_label.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(statistics_label)

        # Add table grid with data
        data_table = QTableWidget(15, 2)
        data_table.setContentsMargins(0, 0, 0, 0)
        data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        data_table.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        data_table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        data_table.setHorizontalHeaderLabels(["Name", "Value"])
        data_table.setSelectionMode(QTableWidget.NoSelection)
        data_table.setEditTriggers(QTableWidget.NoEditTriggers)
        data_table.verticalHeader().setVisible(False)
        data_table.setColumnWidth(0, 170)
        data_table.setColumnWidth(1, 120)

        def add_table_item(data_table, row, name, value, tooltip):
            name_item = QTableWidgetItem(name)
            value_item = QTableWidgetItem(value)
            value_item.setToolTip(tooltip)
            data_table.setItem(row, 0, name_item)
            data_table.setItem(row, 1, value_item)

        add_table_item(data_table, 0, "Population", '7.54', "The current population level of the province")
        add_table_item(data_table, 1, "Growth", '+4.2%', "The growth rate of the population")
        add_table_item(data_table, 2, "Income", '32', "Income generated from production")
        add_table_item(data_table, 3, "Trade Value", '23', "The value of trade in the province")
        add_table_item(data_table, 4, "Manpower", '0.32', "The available manpower for military purposes")
        add_table_item(data_table, 5, "Revolt risk", '0%', "The risk of revolt in the province")
        add_table_item(data_table, 6, "Movement speed", '75%', "Speed modifier for armies and specialists")
        add_table_item(data_table, 7, "Fort Level", '1 - minimal', "The level of fortifications in the province")
        add_table_item(data_table, 8, "Supplies", 'None', "The level of supplies available in the province")
        add_table_item(data_table, 9, "Terrain Type", 'plains', "The type of terrain in the province")
        add_table_item(data_table, 10, "Climate Type", 'arid', "The type of climate in the province")
        add_table_item(data_table, 11, "Religion", 'pagan', "The predominant religion in the province")
        add_table_item(data_table, 12, "Culture", 'polish', "The predominant culture in the province")
        add_table_item(data_table, 13, "Center of Trade", 'Gdansk', "Indicates if the province is a center of trade")

        self.layout().addWidget(data_table)

        # Add actions label
        buildings_label = QLabel("<b>Improve infrastructure</b>")
        buildings_label.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(buildings_label)

        def create_button(text, row, col, layout):
            button = QPushButton(text)
            button.setFixedSize(95, 40)
            layout.addWidget(button, row, col)
            button.setContentsMargins(0, 0, 0, 0)

            return button

        # Add action buttons to Infrastructure and Military sections
        button_layout = QGridLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(0)
        button_layout.setAlignment(Qt.AlignTop)
        self.layout().addLayout(button_layout)

        # Add buttons in a 3-column grid for Infrastructure Improvements
        infra_actions = [
            "Farmland", "Forts", "Roads",
            "Barracks", "Shipyard", "Workshop",
            "Library", "Temple", "Market"
        ]

        for index, action in enumerate(infra_actions):
            row = index // 3
            col = index % 3
            create_button(action, row, col, button_layout)

        # Add military operations label
        military_label = QLabel("<b>Military Operations</b>")
        military_label.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(military_label)

        # Add action buttons to Infrastructure and Military sections
        button_layout2 = QGridLayout()
        button_layout2.setContentsMargins(0, 0, 0, 0)
        button_layout2.setSpacing(0)
        button_layout2.setAlignment(Qt.AlignTop)
        self.layout().addLayout(button_layout2)

        # Add buttons in a 3-column grid for Military Operations
        military_actions = [
            "Build Army", "Train Army", "Mercenaries",
            "Build Navy", "Train Navy", "Pirates"
        ]

        for index, action in enumerate(military_actions):
            row = (index + len(infra_actions)) // 3
            col = (index + len(infra_actions)) % 3
            create_button(action, row, col, button_layout2)


        # Add empty panel to fill empty space
        empty_panel = QWidget()
        empty_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout().addWidget(empty_panel)

