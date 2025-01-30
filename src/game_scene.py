'''

GAME SCENE

Class related to manage all interaction with user and graphics management


'''
from gui.technology import TechnologyPanel
from map.provinceItem import ProvinceItem
from map.roaditem import RoadItem
from PySide6.QtCore import Qt, QRectF, QPoint
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QToolTip, QInputDialog
from map.borderitem import BorderItem

from src.db import TDB
db = TDB()



#
#   HERE GOES ALL INTERACTION WITH USER
#


class GameScene(QGraphicsScene):

    def __init__(self, parent=None):
        super().__init__(parent)

        print("Create game scene")

        from PySide6.QtWidgets import QApplication
        QApplication.instance().setStyleSheet("""
            QToolTip { background-color: #303030; color: gold; border: 2px solid gold; font-family: Consolas; font-size: 10pt; }
            QWidget { background-color: #202020; color: white; font-family: Consolas; font-size: 10pt; }
            QMainWindow { background-color: #202020; }
            QMenuBar { background-color: #303030; color: white; }
            QMenu { background-color: #303030; color: white; }
            QStatusBar { background-color: #303030; color: white; }
            QPushButton { background-color: #404040; color: white; border: 1px solid gold; }
            QPushButton:hover { background-color: #505050; }
            QLineEdit { background-color: #303030; color: white; border: 1px solid gold; }
            QComboBox { background-color: #303030; color: white; border: 1px solid gold; }
            QCheckBox { color: white; }
            QRadioButton { color: white; }
            QTabWidget::pane { border: 1px solid gold; }
            QTabBar::tab { background: #303030; color: white; border: 1px solid gold; padding: 5px; }
            QTabBar::tab:selected { background: #404040; }
        """)
        self.selected_color = ''

        self.game_view = QGraphicsView(self)

        self.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.setBackgroundBrush(Qt.black)
        self.game_view.setRenderHint(QPainter.Antialiasing, False)
        self.game_view.setRenderHint(QPainter.TextAntialiasing, False)
        self.game_view.setRenderHint(QPainter.SmoothPixmapTransform, False)
        self.game_view.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing, True)
        self.game_view.setCacheMode(QGraphicsView.CacheBackground)
        self.game_view.setDragMode(QGraphicsView.ScrollHandDrag)
        self.game_view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.game_view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.game_view.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.game_view.setCursor(Qt.ArrowCursor)
        self.game_view.setViewportUpdateMode(QGraphicsView.MinimalViewportUpdate)
        self.game_view.setOptimizationFlag(QGraphicsView.DontSavePainterState, True)

        self.current_country_tag_number = 0

        from map.provinceItem import ProvinceItem
        self.selected_province : ProvinceItem = None
        self.selected_province_id = None

    #
    # MOUSE MOVE TOOLTIP
    #

    def mouseMoveEvent(self, event):
        pos = event.scenePos().toPoint()
        province : ProvinceItem = self.get_province_from_position(pos)
        if province:
            if province.is_explored:
                tooltip_text = province.get_province_tooltip( db.province_manager.current_map_mode )
            else:
                tooltip_text = 'Terra Incognita'
            QToolTip.showText(event.screenPos() + QPoint(64, 64), tooltip_text, self.game_view, msecShowTime=20000)
        else:
            QToolTip.hideText()
        super().mouseMoveEvent(event)
        self.game_view.update()  # Ensure the scene is updated after dragging

    #
    #   PROVINCE SELECTION
    #

    def select_province(self, position):
        prov = self.get_province_from_position(position)
        if prov:
            if prov.is_explored:
                self.update_selected_province( prov )
                print('Selected province', prov.province_id, prov.name)

    def select_province_by_id(self, province_id):
        self.selected_province_id = province_id
        self.update_selected_province( None )
        print('Selected province', province_id)

    def update_selected_province(self, prov ):
        # Clear previous selection highlight
        self.clear_selection_highlight()

        self.selected_province_id = prov.province_id
        self.selected_province = prov

        # Highlight the selected province
        self.highlight_province(prov)

    def clear_selection_highlight(self):
        if self.selected_province:
            self.selected_province.deselect_province()

        self.selected_province = None
        self.selected_province_id = 0

    def highlight_province(self, province):
        province.select_province()

    #
    #   MOUSE EVENTS
    #

    def mouseDoubleClickEvent(self, event):
        pos = event.scenePos().toPoint()
        prov = self.get_province_from_position(pos)

        if prov:
            if event.button() == Qt.RightButton:
                self._perform_action_double(event, pos, prov)

        super().mouseDoubleClickEvent(event)
        self.update()  # Ensure the scene is updated after dragging

    def mousePressEvent(self, event):
        pos = event.scenePos().toPoint()
        prov = self.get_province_from_position(pos)

        if prov:
            if event.button() == Qt.LeftButton:
                self.select_province(pos)

            if event.button() == Qt.RightButton:
                self._perform_action(event, pos, prov)

        super().mousePressEvent(event)
        self.update()  # Ensure the scene is updated after dragging

    def _perform_action(self, event, position, prov):

        tag = db.current_country_tag

        if prov:
            if prov.is_explored:
                if event.modifiers() & Qt.ControlModifier:
                    db.province_manager.change_province_owner(prov, tag)
                if event.modifiers() & Qt.AltModifier:
                    db.province_manager.change_province_occupant(prov, tag)

    def _perform_action_double(self, event, position, prov):
        if event.modifiers() & Qt.ControlModifier:
            if prov:
                if prov.is_explored:
                    prov.change_country_capitol_province( )
        else:
            if prov:
                if prov.is_explored:
                    import random
                    for _ in range(10):
                        random_province_id = random.choice(list(db.province_manager.provinces.keys()))
                        db.province_manager.highlight_path_between_provinces(prov.province_id, random_province_id)

    #
    #   PROVINCE SELECTIOn
    #

    def get_province_from_position(self, position):

        rect_size = db.rect_size

        col = int(position.x() // rect_size)
        row = int(position.y() // rect_size)

        if 0 <= row < len(db.province_id_map) and 0 <= col < len(db.province_id_map[0]):
            province_id = db.province_id_map[row][col]

            province = db.province_manager.provinces.get(province_id, None)
            if province:
                return province

        return None

    #
    #   KEYBOARD EVENTS
    #

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_S:
            self.take_screenshot()

        if event.key() == Qt.Key_M:
            from src.res import map_loader
            map_loader.dump_all_map_data_to_files()

        #
        #   explore entire map
        #

        if event.key() == Qt.Key_P:
            db.province_manager.explore_entire_map()

        #
        #   find province dialog
        #

        if event.key() == Qt.Key_Backslash:
            self.show_province_id_input()

        #
        #   next / prev country
        #

        if event.key() == Qt.Key_BracketRight:
            self.switch_to_next_country(1)

        if event.key() == Qt.Key_BracketLeft:
            self.switch_to_next_country(-1)

        #
        #   ZOOM
        #

        if event.key() == Qt.Key_Plus:
            self.increase_zoom()
        if event.key() == Qt.Key_Minus:
            self.decrease_zoom()

        if event.key() == Qt.Key_Space:
            db.province_manager.save_provinces_to_file()

        #
        #   switch zoom modes
        #

        if event.key() == Qt.Key_F1:
            db.province_manager.switch_map_mode('terrain')
        if event.key() == Qt.Key_F2:
            db.province_manager.switch_map_mode('culture')
        if event.key() == Qt.Key_F3:
            db.province_manager.switch_map_mode('religion')
        if event.key() == Qt.Key_F4:
            db.province_manager.switch_map_mode('goods')
        if event.key() == Qt.Key_F5:
            db.province_manager.switch_map_mode('climate')
        if event.key() == Qt.Key_F6:
            db.province_manager.switch_map_mode('politic')
        if event.key() == Qt.Key_F7:
            db.province_manager.switch_map_mode('region')
        if event.key() == Qt.Key_F8:
            db.province_manager.switch_map_mode('manpower')
        if event.key() == Qt.Key_F9:
            db.province_manager.switch_map_mode('trade')

        for province in db.province_manager.provinces.values():
            province.change_details_based_on_zoom_level(db.current_zoom_index)

        super().keyPressEvent(event)
        self.update()  # Ensure the scene is updated after dragging

    #
    #   ZOOM CHANGE
    #

    def increase_zoom(self):
        if db.current_zoom_index < len(db.ZOOM_LEVELS) - 1:
            db.current_zoom_index += 1
        self.apply_zoom()

    def decrease_zoom(self):
        if db.current_zoom_index > 0:
            db.current_zoom_index -= 1
        self.apply_zoom()

    def apply_zoom(self):
        self.game_view.resetTransform()
        self.game_view.scale(db.ZOOM_LEVELS[db.current_zoom_index], db.ZOOM_LEVELS[db.current_zoom_index])

        for province in db.province_manager.provinces.values():
            province.change_details_based_on_zoom_level(db.current_zoom_index)

        self.update()

    #
    #   GRAPHICS
    #

    def enforce_redraw(self):
        self.game_view.update()

    def create_graphics(self):

        print("  Create map objects graphics")

        provinces_data = db.province_tile_list
        borders_data = db.province_border_map

        rect_size = db.rect_size

        print("    Create provinces")

        for province_id, province_info in provinces_data.items():
            tiles = [QRectF(x * rect_size, y * rect_size, rect_size, rect_size) for x, y in province_info]
            province = db.province_manager.provinces.get(province_id)
            if province:
                province.set_tiles(tiles)
                self.addItem(province)
                self.addItem(province.river_path)
                # self.addItem(province.province_fog_of_war)
            else:
                print("ERROR, cannot find province in province manager", province_id)

        print("    Create borders")

        for province_id, province_info in borders_data.items():
            province = db.province_manager.provinces.get(province_id)

            if province:
                for neighbor_id, border_lines in province_info.items():
                    border_key = tuple(sorted((province_id, neighbor_id)))

                    if border_key in db.borders_objs:
                        continue

                    dist = db.province_neighbours_distance.get( border_key, None )

                    if dist is None:
                        print("ERROR, distance is null", province_id, neighbor_id)

                    borders = BorderItem(border_lines, province_id, neighbor_id)
                    db.borders_objs[border_key] = borders
                    province.borderlines[neighbor_id] = borders
                    province.neighbors_distance[neighbor_id] = dist
                    self.addItem(borders)

                    # Add the border to the neighbor province as well
                    neighbor_province = db.province_manager.provinces.get(neighbor_id)
                    if neighbor_province:
                        neighbor_province.borderlines[province_id] = borders
                        neighbor_province.neighbors_distance[province_id] = dist
                        neighbor_province.neighbors[province_id] = province
                        province.neighbors[neighbor_id] = neighbor_province

        print("    Create roads")

        for key, border in db.borders_objs.items():
            border: BorderItem
            province1 = db.province_manager.provinces.get(key[0])
            province2 = db.province_manager.provinces.get(key[1])

            p1_id = province1.province_id
            p2_id = province2.province_id

            if province1 and province2 and province1.city_position and province2.city_position:

                # its coastal but VERY SHORT TODO
                #if len( border.border_lines) <= 2 and border.border_type == 'coastal':
                #    continue

                road = RoadItem(province1, province2)

                province1.roads[ p2_id ] = road
                province2.roads[ p1_id ] = road

                db.roads_objs[ (p1_id, p2_id)] = road
                db.roads_objs[ (p2_id, p1_id)] = road

                self.addItem(road)

        print("    Create province city graphics")

        for province in db.province_manager.provinces.values():
            if province.city_position:
                col, row = province.city_position

                if province.is_land:  # Land provinces
                    province.create_city_pixmap('city', 'city.png', self, col, row)
                    province.create_province_large_frame(self, col, row)
                    province.create_core_pixmap(self, col, row)
                else:  # Sea provinces
                    pass

        print("    Create province name graphics")

        for province in db.province_manager.provinces.values():
            if province.name_text_position:
                if len(province.name_text_position) >= 2:
                    province.set_name_text(self, text = province.name, points = province.name_text_position)
                else:
                    print('ERROR - province does not have proper name position', province.province_id,
                          province.name)

        self.update()

    def center_view_on_province(self, province_id):

        province = db.province_manager.provinces.get(province_id)

        if province:
            if province.is_explored:

                # Get the bounding rectangle of the province
                bounding_rect = province.boundingRect()
                # Calculate the center of the bounding rectangle
                center_point = bounding_rect.center()
                # Center the view on the calculated center point
                self.game_view.centerOn(center_point)


    def switch_to_next_country(self, change):
        self.current_country_tag_number = (self.current_country_tag_number + change) % len(
            db.country_manager.countries)

        cnt = list(db.country_manager.countries.keys())[self.current_country_tag_number]
        db.province_manager.switch_current_country_tag(cnt)
        db.province_manager.switch_map_mode('terrain')

    #
    #   SUPPORT
    #

    def show_province_id_input(self):
        province_id, ok = QInputDialog.getInt(self, "Find Province", "Enter Province ID:")
        if ok:
            self.center_view_on_province(province_id)

    def take_screenshot(self):
        from PySide6.QtGui import QPixmap, QPainter
        print("Taking screenshot....")
        rect = self.itemsBoundingRect()
        image = QPixmap(rect.size().toSize())
        image.fill(Qt.transparent)
        painter = QPainter(image)
        self.render(painter, target=rect)
        painter.end()
        image.save( str(db.path_logs / 'screenshot.png'), 'png')
        print("Screenshot done")