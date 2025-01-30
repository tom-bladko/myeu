from game.culture import Culture
from other.modifiers import Modifiers

from src.db import TDB
db = TDB()

from game.monarch import Monarch
from game.religion import Religion
from map.provinceItem import ProvinceItem


class Budget:

    def __init__(self):

        self.gold = 0
        self.stability = 0
        self.inflation = 0

        self.level_tax = 0.5
        self.level_tax_revolt = 2
        self.level_maintenance = 0.5
        self.level_science = 0.5

class Agents:

    def __init__(self):
        self.merchants_max = 12
        self.merchants_growth = 1.0
        self.merchants = 0

        self.general_max = 12
        self.general_growth = 1.0
        self.general = 0

        self.explorer_max = 12
        self.explorer_growth = 1.0
        self.explorer = 0

        self.diplomats_max = 12
        self.diplomats_growth = 1.0
        self.diplomats = 0

        self.engineers_max = 12
        self.engineers_growth = 1.0
        self.engineers = 0

        self.inventors_max = 12
        self.inventors_growth = 1.0
        self.inventors = 0

        self.missionaries_max = 12
        self.missionaries_growth = 1.0
        self.missionaries = 0

        self.advisories_max = 12
        self.advisories_growth = 1.0
        self.advisories = 0

    def get_more_agents(self):
        self.merchants = min(self.merchants + self.merchants_growth, self.merchants_max)
        self.general = min(self.general + self.general_growth, self.general_max)
        self.explorer = min(self.explorer + self.explorer_growth, self.explorer_max)
        self.diplomats = min(self.diplomats + self.diplomats_growth, self.diplomats_max)
        self.engineers = min(self.engineers + self.engineers_growth, self.engineers_max)
        self.inventors = min(self.inventors + self.inventors_growth, self.inventors_max)
        self.missionaries = min(self.missionaries + self.missionaries_growth, self.missionaries_max)
        self.advisories = min(self.advisories + self.advisories_growth, self.advisories_max)


class Technology:

    def __init__(self, args):
        self.name = args.get("name", "Country")
        self.tag = args.get("tag", "TAG")
        self.modifiers = Modifiers()

class Country:
    def __init__(self, args):
        self.name = args.get("name", "Country")
        self.tag = args.get("tag", "TAG")

        self.flag = db.res_images['flag'].get(self.tag, 'REB')
        self.flag_frame = db.res_images['flag_frame'].get(self.tag, 'REB')
        self.color = args.get("color", "white")

        self.techgroup = args.get("techgroup", "latin")

        self.agents : Agents = Agents()

        self.budget : Budget = Budget()
        self.monarch : Monarch = None

        self.state_religion : Religion = None

        self.accepted_cultures_tag : list[str] = []
        self.accepted_cultures : list[Culture] = []

        self.capitol_province : ProvinceItem = None

        self.owned_provinces : dict[int, ProvinceItem] = {}
        self.occupied_provinces : dict[int, ProvinceItem] = {}
        self.national_provinces : dict[int, ProvinceItem] = {}
        self.claim_provinces : dict[int, ProvinceItem] = {}

        self.explored_provinces : dict[int, ProvinceItem] = {}

        # number of months / turn at war
        self.war_time = 0

        self.technology = Technology( {} )

        from game.policy import Policies
        self.policies : list[Policies] = []

    #
    #   change culture and religion
    #

    def change_religion(self, new_religion_tag):
        religion = db.db_religions.get(new_religion_tag)
        if religion:
            self.state_religion = religion

    def add_culture(self, new_cultures):
        if isinstance(new_cultures, list):
            for cult_tag in new_cultures:
                self.accepted_cultures_tag.append(cult_tag)
        else:
           self.accepted_cultures_tag.append(new_cultures)

    def remove_culture(self, cult_tag):
        if cult_tag in self.accepted_cultures_tag:
            self.accepted_cultures_tag.remove(cult_tag)

    #
    #   change country capitol
    #

    def change_country_capital_province(self, new_province ):

        if isinstance(new_province, int):
            new_province = db.province_manager.provinces.get( new_province)

        # remove old
        if self.capitol_province:
            self.capitol_province.set_province_large_frame(NoneNone)
            self.capitol_province.is_country_capitol = False

        # add new
        if new_province:
            new_province.set_province_large_frame(self.budget.stability)
            self.capitol_province = new_province
            self.capitol_province.is_country_capitol = True

    #
    #   add provinces
    #

    def add_owned_province(self, province):

        if isinstance(province, int):
            province = db.province_manager.provinces.get( province)

        self.owned_provinces[province.province_id] = province
        db.country_province_owner_dict[ province.province_id ] = self.tag

    def add_occupied_province(self, province):

        if isinstance(province, int):
            province = db.province_manager.provinces.get( province)

        self.occupied_provinces[province.province_id] = province
        db.country_province_occupant_dict[province.province_id] = self.tag

    def add_national_province(self, province):

        if isinstance(province, int):
            province = db.province_manager.provinces.get( province)

        if province:
            self.national_provinces[province.province_id] = province
            db.country_province_national_dict[self.tag].append( province.province_id )

    def add_claim_province(self, province):

        if isinstance(province, int):
            province = db.province_manager.provinces.get( province)

        if province:
            self.claim_provinces[province.province_id] = province
            db.country_province_claim_dict[self.tag].append( province.province_id )

    #
    #   remove provinces
    #

    def remove_owned_province(self, province):
        if isinstance(province, int):
            province = db.province_manager.provinces.get( province)

        if province:
            if province.province_id in self.owned_provinces.keys():
                self.owned_provinces.pop( province.province_id )
                db.country_province_owner_dict[ province.province_id ] = None

    def remove_occupied_province(self, province):
        if isinstance(province, int):
            province = db.province_manager.provinces.get( province)

        if province:
            if province.province_id in self.occupied_provinces.keys():
                self.occupied_provinces.pop( province.province_id )
                db.country_province_occupant_dict[ province.province_id ] = None

    def remove_national_province(self, province):
        if isinstance(province, int):
            province = db.province_manager.provinces.get( province)

        if province:
            if province.province_id in self.national_provinces.keys():
                self.national_provinces.pop( province.province_id )
                db.country_province_national_dict[self.tag].remove( province.province_id )

    def remove_claim_province(self, province):
        if isinstance(province, int):
            province = db.province_manager.provinces.get( province)

        if province:
            if province.province_id in self.claim_provinces.keys():
                self.claim_provinces.pop( province.province_id )
                db.country_province_claim_dict[self.tag].remove( province.province_id )

    #
    #
    #

    def process_before_all(self):

        # owned provinces
        for prov_id, province in self.owned_provinces.items():
            province.process_all()

        # occupied provinces
        for prov_id, province in self.occupied_provinces.items():
            province.process_all_occupied()