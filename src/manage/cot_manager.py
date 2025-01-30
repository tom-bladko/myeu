import time

from game.country import Country
from other import pathengine

from src.db import TDB
db = TDB()

class CenterTradeManager:

    def __init__(self, args):

        from src.trade.center_trade import CenterOfTrade
        self.center_of_trades : dict[str, CenterOfTrade] = {}

        for key, val in args.items():
            cot = CenterOfTrade( val )
            self.center_of_trades[key] = cot

    def calculate_range_of_cots(self):

        print( "Processing COT Manager")

        for _, cot in self.center_of_trades.items():
            cot.location_province = db.province_manager.provinces.get(cot.location_province_id)

        # this is calculated only for explored provinces, otherwise you don't know path
        distances = {province_id: float('inf') for province_id in db.province_manager.provinces}
        previous_nodes = {province_id: None for province_id in db.province_manager.provinces}

        # for each province
        import threading

        def process_province(province, center_of_trades, distances, previous_nodes):
            if province.is_land and province.country_owner_tag:
                prov_x, prov_y = province.city_position
                min_distance = float('inf')
                closest_cot = None
                close_cots = []

                # Find the 4 closest COTs based on Euclidean distance
                for _, cot in center_of_trades.items():
                    cot_x, cot_y = cot.location_province.city_position
                    d = (cot_x - prov_x) ** 2 + (cot_y - prov_y) ** 2
                    if d <= 125 * 125:
                        close_cots.append((d, cot))

                # Sort the COTs by distance and take the closest 3-4
                close_cots.sort(key=lambda x: x[0])
                close_cots = close_cots[:4]

                for _, cot in close_cots:
                    path, distance = pathengine.shortest_path(province.province_id,
                                                              cot.location_province_id,
                                                              None, 'merchant',
                                                              distances, previous_nodes)
                    if distance < min_distance:
                        min_distance = distance
                        closest_cot = cot

                province.center_of_trade = closest_cot

        from concurrent.futures import ThreadPoolExecutor

        provinces = list(db.province_manager.provinces.items())
        section_size = len(provinces) // 8

        def process_section(section):
            for _, province in section:
                process_province(province, self.center_of_trades, distances, previous_nodes)

        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(process_section, provinces[i * section_size: (i + 1) * section_size]) for i in
                       range(8)]
            for future in futures:
                future.result()

    def process_before_all(self):
        print("  Country manager before processing")

        # create all countries
        for id, country_data in db.db_countries.items():
            country_data['tag'] = id
            country = Country(country_data)
            db.country_manager.countries[id] = country

        # Process countries
        for id, country in db.country_manager.countries.items():
            country.process_before_all()

