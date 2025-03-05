import os
import pathlib

import toml
import yaml


from src.manager import manager_province, manager_cot
from src.db import TDB

db = TDB()


class Scenario:

    def __init__(self, kwargs = {}):
        self.name = kwargs.get('name')

        # start / end date
        self.start_date = kwargs.get('start_date')
        self.end_date = kwargs.get('end_date')
        self.description = kwargs.get('description', None)

        # list of available countries
        self.countries_available = kwargs.get('countries')

        # details per country
        self.countries_details : dict = {}
        self.leaders_details : dict = {}
        self.rulers_details : dict = {}
        self.events_details : dict = {}

        # global discoveries already done
        self.discoveries = kwargs.get('discoveries')

        # existing wars and alliance
        self.wars = kwargs.get('wars')
        self.alliances = kwargs.get('alliances')

        # defined center of trades
        self.cots = kwargs.get('cots')

        manager_cot.create_center_of_trades(self.cots)

        # all events already done
        self.events_done = kwargs.get('events')

        # modification of existing provinces
        self.provinces = kwargs.get('provinces')

        # additional files countries
        paths_data = kwargs.get('paths', {})
        self.file_countries = paths_data.get('file_countries', [])
        self.file_leaders = paths_data.get('file_leaders', [])
        self.file_events = paths_data.get('file_events', [])
        self.file_rulers = paths_data.get('file_rulers', [])
        self.file_ideas = paths_data.get('file_ideas', [])

    def process_cots(self, cots):
        manager_cot.create_center_of_trades(cots)

    def process_countries(self, country):
        key = country.get('tag')
        self.countries_details[key] = country

    def process_leaders(self, leaders):
        for key, val in leaders.items():
            self.leaders_details[key] = val

    def process_rulers(self, rulers):
        for key, val in rulers.items():
            self.rulers_details[key] = val

    def process_events(self, events):
        for key, val in events.items():
            self.events_details[key] = val

    def load_content(self):

        for country_tag, val in self.countries_details.items():

            country = db.countries.get(country_tag)

            # geography

            geography = val.get('geography', {})

            # owned provinces
            owned_provinces = geography.get('ownedprovinces', [])
            for prov_id in owned_provinces:
                manager_province.change_province_owner(prov_id, country_tag)

            # occupied provinces
            controlled_provinces = geography.get('controlledprovinces', [])
            for prov_id in controlled_provinces:
                manager_province.change_province_occupant(prov_id, country_tag)

            # national provinces
            national__provinces = geography.get('nationalprovinces', [])
            for prov_id in national__provinces:
                country.add_national_province( prov_id)

            # claimed provinces
            claimed_provinces = geography.get('claimedprovinces', [])
            for prov_id in claimed_provinces:
                country.add_claim_province( prov_id)

            # known provinces & regions
            known_provs = geography.get("knownprovinces")
            knwon_regions = geography.get("knownregions")
            manager_province.explore_province_by_geography(country_tag,
                                                           names=knwon_regions,
                                                           prov_ids=known_provs)

            # technologies

            technologies = val.get('technology', {})
            if technologies:
                country.technology_levels = technologies

            # policies

            policies = val.get('policies', {})
            if policies:
                country.policy_sliders = policies

            # social

            social = val.get('social', {})
            religion = social.get('religion')
            if religion:
                country.change_religion(religion)

            cultures = social.get("cultures")
            if cultures:
                country.add_culture( cultures )

            # armies and navies

            from src.battle.army import ArmyLand, ArmyNaval
            landunits = val.get('armies', [])
            for army in landunits:
                army['owner'] = country_tag
                a = ArmyLand( army )
                prov = db.provinces.get( a.province_id)
                if prov:
                    prov.armies.append(a)
                    country.armies.append(a)

            navalunits = val.get('navies', [])
            for navy in navalunits:
                navy['owner'] = country_tag
                a = ArmyNaval(navy)
                prov = db.provinces.get( a.province_id)
                if prov:
                    prov.navies.append(a)
                    country.navies.append(a)

            # load cities

            cities = val.get('cities', {})
            for city in cities:
                prov_id = city.get('location', 0)
                prov = db.provinces.get(prov_id)
                if prov:

                    # load population
                    prov.manpower_max = city.get('population', 0)

                    # set capital
                    if city.get('capital', False):
                        country.change_country_capital_province(prov)

            # load center of trades




class ScenarioLoader:

    def __init__(self, base_path):
        self.base_path = base_path
        self.scenarios : dict[str, Scenario] = {}

    def load_scenarios(self):
        print("Loading all scenarios")
        with open( str(self.base_path) , 'r') as f:
            list_scenarios = toml.load(f)

            # this is list files to scenarios
            if 'scenarios' in list_scenarios:

                base_path = pathlib.Path( self.base_path ).parent

                # load each scenario
                for scenario_path in list_scenarios['scenarios']:
                    with open(str(base_path / scenario_path), 'r') as fs:
                        scenario_data = toml.load(fs)
                        name = scenario_data['id']
                        scenario = Scenario( scenario_data )
                        self.scenarios[ str(name) ] = scenario

    def select_scenario(self, scenario_name):
        print("Loading scenario", scenario_name)
        scenario = self.scenarios.get(scenario_name)

        if scenario:
            final_dir = pathlib.Path(self.base_path).parent / scenario_name

            # COUNTRIES

            for file_name in scenario.file_countries:
                file_path = os.path.join( final_dir, file_name)
                print( "  ", file_name )
                with open(file_path, 'r') as f:
                    content = toml.load(f)
                    scenario.process_countries( content)

            # EVENTS

            for file_name in scenario.file_events:
                file_path = os.path.join(final_dir, file_name)
                with open(file_path, 'r') as f:
                    content = toml.load(f)
                    scenario.process_events( content)

            # RULERS

            for file_name in scenario.file_rulers:
                file_path = os.path.join(final_dir, file_name)
                with open(file_path, 'r') as f:
                    content = toml.load(f)
                    scenario.process_rulers( content)

            # LEADERS

            for file_name in scenario.file_leaders:
                file_path = os.path.join(final_dir, file_name)
                with open(file_path, 'r') as f:
                    content = toml.load(f)
                    scenario.process_leaders( content)


        return scenario
