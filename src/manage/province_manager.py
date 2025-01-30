'''

PROVINCE MANAGER

Class to manage all provinces in game, part of game logic

'''
from game.culture import Culture
from src.db import TDB

db = TDB()

import random
from other import pathengine

class ProvinceManager:
    def __init__(self):
        from map.provinceItem import ProvinceItem
        self.provinces : dict[int, ProvinceItem] = {}

        self.current_map_mode = 'terrain'
        self.current_map_mode_region = 0

    def find_path_between_provinces(self, prov_from_id, prov_to_id):
        path, distance = pathengine.shortest_path(prov_from_id, prov_to_id)
        print(f"Shortest path from {prov_from_id} to {prov_to_id}: {path} with distance {distance}")

    def find_provs_in_range(self, prov_id, range = 10):
        # Calculate all provinces within a certain range
        provinces_in_range = pathengine.provinces_in_range(prov_id, range)
        print(f"Provinces within {prov_id} distance from {range}: {provinces_in_range}")

    def save_provinces_to_file(self):
        directory_path = str( db.path_mod / 'archive')
        import os
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        for province_id, province in self.provinces.items():
            file_path = os.path.join(directory_path, f"{province_id}.png")
            province.save_to_png(file_path)
            print( file_path )

    #
    #   PROVINCE DATA
    #

    def process_before_all(self):
        print("  Province manager before processing")
        self.provinces = db.db_provinces

    #
    #   SWITCH GAME MAP MODES
    #

    def switch_map_mode(self, new_mode):
        print("Switch map mode to ", new_mode)

        map_mode_switchers = {
            'terrain': self._switch_map_mode_terrain,
            'culture': self._switch_map_mode_culture,
            'religion': self._switch_map_mode_religion,
            'climate': self._switch_map_mode_climate,
            'goods': self._switch_map_mode_goods,
            'politic': self._switch_map_mode_politic,
            'region': self._switch_map_mode_region,
            'manpower': self._switch_map_mode_manpower,
            'trade': self._switch_map_mode_trade,
        }

        if new_mode in map_mode_switchers.keys():
            # cycle on region map
            if self.current_map_mode == 'region' and new_mode == 'region':
                self.current_map_mode_region = (  self.current_map_mode_region + 1 ) % 3
            else:
                self.current_map_mode_region = 0

            self.current_map_mode = new_mode
            for province in db.province_manager.provinces.values():
                if province.is_explored:
                    map_mode_switchers[new_mode](province)

        db.game_scene.update()

    def _switch_map_mode_terrain(self, province):

        # enable fog of war
        # province.enable_fog_of_war()

        country_owner = db.country_manager.countries.get( province.country_owner_tag)

        primary_color = 'basic_water'
        weather_effect = None
        secondary_color = None
        terrain_effect = None

        province.set_province_large_frame(None)
        province.set_core_pixmap(False)
        province.set_city_pixmap()

        # main terrain
        terrain = province.terrain
        if terrain:
            primary_color = terrain.color_name

            # on terrain map secondary color is WEATHER
            # temporary solution
            climate = province.climate
            if climate:
                if province.is_land:
                    if 11 in climate.snow_months:

                        if random.random() > 0.7:
                            weather_effect = 'snow'
                else:
                    if 11 in climate.snow_months:
                        weather_effect = 'ice'

            # get terrain effect
            if terrain.effect:
                terrain_effect = terrain.tag

        # set owner of province
        if province.is_land:
            province.set_city_pixmap('flag_frame', province.country_owner_tag + '.png')

        # set capitol large frame
        if country_owner:
            if province == country_owner.capitol_province:
                province.set_province_large_frame(country_owner.budget.stability)

        province.set_province_background_colors( primary_color = primary_color,
                                                 weather_effect = weather_effect,
                                                 secondary_color = secondary_color,
                                                 terrain_effect = terrain_effect)

    def _switch_map_mode_culture(self, province):

        # no fog of war
        # province.disable_fog_of_war()

        country_owner = db.country_manager.countries.get( province.country_owner_tag)

        primary_color = 'basic_water'
        secondary_color = None
        terrain_effect = None

        province.set_province_large_frame(None)
        province.set_core_pixmap(False)
        province.set_city_pixmap()

        # standard terrain effect
        terrain = province.terrain
        if terrain:
            if terrain.effect:
                terrain_effect = province.terrain.tag

        # get province culture
        culture : Culture = province.culture
        if culture:
            primary_color = culture.color_name

            # if there is a country owner and what is background color
            if country_owner:

                # is country cultures is not matching with province
                cnt_culture_tags = country_owner.accepted_cultures_tag
                if culture.tag not in cnt_culture_tags:
                    secondary_color = 'black'

                # in capitol city show country flag only
                if province == country_owner.capitol_province:
                    province.set_province_large_frame(country_owner.budget.stability)
                    province.set_city_pixmap('flag_frame', province.country_owner_tag + '.png')

        province.set_province_background_colors(primary_color = primary_color,
                                                secondary_color=secondary_color,
                                                terrain_effect= terrain_effect)

    def _switch_map_mode_religion(self, province ):

        # no fog of war
        # province.disable_fog_of_war()

        country_owner = db.country_manager.countries.get( province.country_owner_tag)

        primary_color = 'basic_water'
        secondary_color = None
        terrain_effect = None

        province.set_province_large_frame(None)
        province.set_core_pixmap(False)
        province.set_city_pixmap()

        # standard terrain effect
        terrain = province.terrain
        if terrain:
            if terrain.effect:
                terrain_effect = province.terrain.tag

        # religion province
        prov_religion = province.religion
        if prov_religion:
            primary_color = prov_religion.color_name

        # if there is a country owner and what is background color
        if country_owner:

            # is state religion is NOT as province religion
            state_religion = country_owner.state_religion
            if state_religion.tag != prov_religion.tag:
                secondary_color = state_religion.color_name

            # in capitol city show country religion
            if province == country_owner.capitol_province:
                province.set_city_pixmap('religion', state_religion.tag + '.png')
                province.set_province_large_frame(country_owner.budget.stability)

        province.set_province_background_colors(primary_color = primary_color,
                                                secondary_color= secondary_color,
                                                terrain_effect= terrain_effect)

    def _switch_map_mode_manpower(self, province):

        # no fog of war
        # province.disable_fog_of_war()

        country_owner = db.country_manager.countries.get( province.country_owner_tag)

        province.set_province_large_frame(None)
        province.set_core_pixmap(False)
        province.set_city_pixmap()

        primary_color = 'basic_water'
        secondary_color = None
        terrain_effect = None

        # standard terrain
        terrain = province.terrain
        if terrain:
            if terrain.effect:
                terrain_effect = province.terrain.tag

        # manpower
        manpower = int(province.manpower)
        if manpower > 0:
            primary_color = f"good_0{min( manpower - 1, 9 )}"

        # set capitol large frame
        if country_owner:
            if province == country_owner.capitol_province:
                province.set_province_large_frame(country_owner.budget.stability)
                province.set_city_pixmap('flag_frame', province.country_owner_tag + '.png')

        province.set_province_background_colors(primary_color = primary_color,
                                                terrain_effect= terrain_effect)

    def _switch_map_mode_region(self, province):
        # no fog of war
        # province.disable_fog_of_war()

        country_owner = db.country_manager.countries.get( province.country_owner_tag)

        region_map_mode = self.current_map_mode_region

        primary_color = 'basic_water'
        secondary_color = None
        terrain_effect = None

        province.set_province_large_frame(None)
        province.set_core_pixmap(False)
        province.set_city_pixmap()

        # standard terrain effect
        terrain = province.terrain
        if terrain:
            if terrain.effect:
                terrain_effect = province.terrain.tag

        region_data = {}

        # primary is regions / area / contient
        if region_map_mode == 0:
            region_data = province.region
        elif region_map_mode == 1:
            region_data = province.continent
        elif region_map_mode == 2:
            region_data = province.area

        if region_data:
            primary_color = region_data.color_name

        # if there is a country owner and what is background color
        if country_owner:

            # in capitol city show country flag only
            if province == country_owner.capitol_province:
                province.set_province_large_frame(country_owner.budget.stability)
                province.set_city_pixmap('flag_frame', province.country_owner_tag + '.png')

        province.set_province_background_colors(primary_color = primary_color,
                                                terrain_effect= terrain_effect)

    def _switch_map_mode_climate(self, province):

        # no fog of war
        # province.disable_fog_of_war()

        country_owner = db.country_manager.countries.get( province.country_owner_tag)

        primary_color = 'basic_water'
        secondary_color = None
        terrain_effect = None

        province.set_province_large_frame(None)
        province.set_core_pixmap(False)
        province.set_city_pixmap()

        # standard terrain
        terrain = province.terrain
        if terrain:
            if terrain.effect:
                terrain_effect = province.terrain.tag

        # climate
        climate = province.climate
        if climate:
            primary_color = climate.color_name
            if not province.is_land:
                secondary_color = 'basic_water'

        # if there is a country owner and what is background color
        if country_owner:
            # in capitol city show country flag only
            if province == country_owner.capitol_province:
                province.set_province_large_frame(country_owner.budget.stability)
                province.set_city_pixmap('flag_frame', province.country_owner_tag + '.png')


        province.set_province_background_colors(primary_color = primary_color,
                                                secondary_color= secondary_color,
                                                terrain_effect= terrain_effect)

    def _switch_map_mode_goods(self, province):

        # no fog of war
        # province.disable_fog_of_war()

        country_owner = db.country_manager.countries.get( province.country_owner_tag)

        primary_color = 'basic_water'
        secondary_color = None
        terrain_effect = None

        province.set_province_large_frame(None)
        province.set_core_pixmap(False)
        province.set_city_pixmap()

        # standard effect
        terrain = province.terrain
        if terrain:
            if terrain.effect:
                terrain_effect = province.terrain.tag

        # good are only on land
        if province.is_land:
            province.set_core_pixmap(False)
            goods = province.goods
            if goods:
                province.set_city_pixmap('goods', goods.tag + '.png')
                primary_color = goods.color_name
            else:
                primary_color = 'basic_land'

        # set capitol large frame
        if country_owner:
            if province == country_owner.capitol_province:
                province.set_province_large_frame(country_owner.budget.stability)

        province.set_province_background_colors(primary_color = primary_color,
                                                terrain_effect= terrain_effect)

    def _switch_map_mode_trade(self, province):

        # disable fog of war
        # province.disable_fog_of_war()

        country_owner = db.country_manager.countries.get( province.country_owner_tag)

        primary_color = 'basic_water'
        secondary_color = None
        terrain_effect = None

        province.set_province_large_frame(None)
        province.set_core_pixmap(False)
        province.set_city_pixmap()

        # always show terrain effect
        terrain = province.terrain
        if terrain:
            if terrain.effect:
                terrain_effect = province.terrain.tag

        # trade is only on land
        if province.is_land:
            # province belongs o this center of trade
            cot = province.center_of_trade
            if cot:
                primary_color = cot.color

                # if this is location of center of trade
                if cot.location_province_id == province.province_id:
                    province.set_city_pixmap('flag_frame', province.country_owner_tag + '.png')
                    province.set_province_large_frame(stab_level=cot.stability)
            else:
                # not in COT range
                primary_color = 'basic_land'

        province.set_province_background_colors(primary_color = primary_color,
                                                terrain_effect= terrain_effect)

    def _switch_map_mode_politic(self, province):

        # province.enable_fog_of_war()

        country_owner = db.db_countries.get(province.country_owner_tag, None)
        country_occup = db.db_countries.get(province.country_occupant_tag, None)

        primary_color = 'basic_water'
        secondary_color = None
        terrain_effect = None

        province.set_province_large_frame(None)
        province.set_core_pixmap(False)
        province.set_city_pixmap()

        # standard terrain
        terrain = province.terrain
        if terrain:
            if terrain.effect:
                terrain_effect = province.terrain.tag

        # if there is a country owner and what is background color
        if country_owner:

            if province.is_country_capitol:
                country = db.country_manager.countries.get( province.country_owner_tag )
                if country:
                    province.set_province_large_frame( country.budget.stability )

            # if there is no occupant
            if country_occup == country_owner:
                primary_color = country_owner.get('color', 'gray')
            else:
                # if there is occupant
                if country_occup:
                    primary_color=country_owner.get('color', 'gray')
                    secondary_color=country_occup.get('color', 'gray')
                else:
                    primary_color=country_owner.get('color', 'gray')
                    secondary_color = None
        else:
            if province.is_land:  # no owner
                primary_color = 'basic_land'

        # FOR CURRENT COUNTRY

        # nationals or claimed provs
        current_country = db.country_manager.countries.get( db.current_country_tag )
        if current_country:

            # if province is national province for current player
            nationals = current_country.national_provinces.keys()

            # if province is claim province for current player
            claimed = current_country.claim_provinces.keys()

            # if its national and if not then its claimed or nothing
            if province.province_id in nationals:
                province.set_core_pixmap(True, is_core=True)
            else:
                if province.province_id in claimed:
                    province.set_core_pixmap(True, is_core=False)

        # flag for who is occupying province
        if province.is_land:
            if country_occup:
                province.set_city_pixmap('flag_frame', province.country_occupant_tag + '.png')
            else:
                province.set_city_pixmap('city', 'city.png')
                primary_color = 'basic_land'

        province.set_province_background_colors(primary_color=primary_color,
                                                secondary_color=secondary_color,
                                                terrain_effect= terrain_effect)

    #
    #   SHOW / HIDE PROVINCES
    #

    def get_neighbors_for_province(self, province):

        neighbors = []
        for neighbor_id in province.neighbors_distance.keys():
            neighbor_province = self.provinces.get(neighbor_id)
            if neighbor_province:
                neighbors.append(neighbor_province)
        return neighbors

    #
    #   manage view and explore
    #

    def explore_entire_map(self):
        for prov in self.provinces.values():
            prov.explore_province()

    def unexplore_entire_map(self):
        for prov in self.provinces.values():
            prov.unexplore_province()

    # def view_entire_map(self):
    #     for prov in self.provinces.values():
    #         prov.view_province()

    # def unview_entire_map(self):
    #     for prov in self.provinces.values():
    #         prov.unview_province()

    #
    #   MANAGE OWNER PROVINCE
    #

    def change_province_owner(self, province, tag, change_occupant = False):

        if isinstance(province, int):
            province = self.provinces.get( province)

        province.change_province_owner(tag, change_occupant)
        #province.view_province()

        other_provs = self.get_neighbors_for_province(province)
        # for other in other_provs:
        #     other.view_province()

    def change_province_occupant(self, province, tag):

        if isinstance(province, int):
            province = self.provinces.get( province)

        province.change_province_occupant(tag)
        # province.view_province()

    #
    #   CHANGE CURRENT PLAYER
    #

    def switch_current_country_tag(self, new_tag):

        db.current_country_tag = new_tag
        print("Switched country to ", db.current_country_tag)

        # hide all provinces
        for prov in self.provinces.values():
            # prov.unview_province()
            prov.unexplore_province()
            prov.set_core_pixmap(False)
            prov.set_province_large_frame(None)
            prov.set_city_pixmap()

        country = db.country_manager.countries.get( new_tag )
        if country:

            for prov in country.explored_provinces.values():
                prov.explore_province()
                prov.update()

        # view only mine
        for prov in self.provinces.values():

            # i do own
            if prov.country_owner_tag == new_tag:

                #prov.view_province()
                others = self.get_neighbors_for_province(prov)
                for o in others:
                    o.explore_province()
                    #o.view_province()
                    o.update()

            # i do occupy
            if prov.country_occupant_tag == new_tag:
                prov.explore_province()
                #prov.view_province()
                prov.update()

        # center on this capitol country view
        self.move_viewport_to_capital(new_tag)

    def move_viewport_to_capital(self, country_tag):
        country = db.country_manager.countries.get(country_tag)
        if country and country.capitol_province:
            db.game_scene.center_view_on_province(country.capitol_province.province_id)

    def explore_province_by_geography(self,  country_tag = 'POL', prov_ids = None, names = None):

        country = db.country_manager.countries.get(country_tag)
        if country:
            for prov in self.provinces.values():
                prov.unexplore_province()

            country.explored_provinces.clear()

            if prov_ids:
                for id, prov in self.provinces.items():
                    if id in prov_ids:
                        prov.explore_province()
                        country.explored_provinces[id] = prov

            if names:
                for id, prov in self.provinces.items():
                    if prov.continent.tag in names or prov.region.tag in names or prov.area.tag in names:
                        prov.explore_province()
                        country.explored_provinces[id] = prov

    #
    #   MANAGE ROADS
    #

    def highlight_path_between_provinces(self, prov_from_id, prov_to_id, hide_all_roads = False):

        # Hide all roads
        if hide_all_roads:
            for road in db.roads_objs.values():
                road.hide_road()

        # Calculate the path between the two provinces
        path, distance = self.pathfinding_engine.shortest_path(prov_from_id, prov_to_id, None, 'normal')

        # Show only the roads in the calculated path
        for i in range(len(path) - 1):
            road = db.roads_objs.get((path[i], path[i + 1]))
            if road:
                road.show_road()
