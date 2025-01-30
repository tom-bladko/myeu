from game.country import Country

from src.db import TDB
db = TDB()

class CountryManager:

    def __init__(self):

        from game.country import Country
        self.countries : dict[str, Country] = {}

        self.countries_data_dict = {}

    def process_before_all(self):
        print("  Country manager before processing")

        # create all countries
        for id, country_data in db.db_countries.items():
            country_data['tag'] = id
            country = Country(country_data)
            self.countries[id] = country

        # Process countries
        for id, country in self.countries.items():
            country.process_before_all()

