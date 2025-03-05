from src.battle.army import ArmyLand, ArmyNaval
from src.ref.ref_techgroup import TechGroup
from src.virtual.agents import Agents
from src.virtual.budget import Budget
from src.ref.ref_culture import Culture
from src.ref.ref_technology import Technology
from src.ref.ref_policy import Policies

from src.db import TDB
from src.virtual.modifiers import Modifiers

db = TDB()

from src.ref.ref_ruler import Ruler
from src.ref.ref_religion import Religion
from src.items.item_province import ProvinceItem


class Country:
    def __init__(self, args ):
        self.name = args.get("name", "Country")
        self.tag = args.get("tag", "TAG")
        techgroup = args.get("techgroup", "latin")
        self.techgroup : TechGroup = db.db_techgroups.get(techgroup)
        self.leader_language = args.get("leader_language", "ENG")
        self.color_name = args.get("color", "white")

        self.flag = db.res_images['flag'].get(self.tag, 'REB')
        self.flag_frame = db.res_images['flag_frame'].get(self.tag, 'REB')
        self.country_modifiers : Modifiers = Modifiers( args.get('modifiers', {} ))

        self.agents : Agents = Agents()
        self.budget : Budget = Budget()
        self.ruler : Ruler = None
        self.state_religion : Religion = None

        self.accepted_cultures_tag : list[str] = []
        self.accepted_cultures : list[Culture] = []

        self.capitol_province : ProvinceItem = None

        self.owned_provinces : dict[int, ProvinceItem] = {}
        self.occupied_provinces : dict[int, ProvinceItem] = {}
        self.national_provinces : dict[int, ProvinceItem] = {}
        self.claim_provinces : dict[int, ProvinceItem] = {}

        self.explored_provinces : dict[int, ProvinceItem] = {}

        self.armies : list[ArmyLand] = []
        self.navies : list[ArmyNaval] = []

        # number of months / turn at war
        self.war_time = 0

        # technology levels in country
        self.technology_levels = {}

        # policy settings in country
        self.policy_sliders = {}

    #
    # technology
    #

    def get_technology_modifiers(self, tech_name):
        if tech_name in self.technology_levels.keys():
            lvl = self.technology_levels[tech_name]
            tech_det = db.db_technologies.get(tech_name).modifiers[lvl]
            return tech_det
        else:
            return None

    def get_technology_details(self, tech_name):
        if tech_name in self.technology_levels.keys():
            lvl = self.technology_levels[tech_name]
            tech_det = db.db_technologies.get(tech_name).levels[lvl]
            return tech_det
        else:
            return None

    #
    #   tech group
    #

    def get_tech_group_modifiers(self):
        if self.techgroup:
            return self.techgroup.modifiers
        return None


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
            new_province = db.provinces.get( new_province)

        # remove old
        if self.capitol_province:
            self.capitol_province.set_province_large_frame(None)
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
            province = db.provinces.get( province)

        self.owned_provinces[province.province_id] = province
        db.country_province_owner_dict[ province.province_id ] = self.tag

    def add_occupied_province(self, province):

        if isinstance(province, int):
            province = db.provinces.get( province)

        self.occupied_provinces[province.province_id] = province
        db.country_province_occupant_dict[province.province_id] = self.tag

    def add_national_province(self, province):

        if isinstance(province, int):
            province = db.provinces.get( province)

        if province:
            self.national_provinces[province.province_id] = province
            db.country_province_national_dict[self.tag].append( province.province_id )

    def add_claim_province(self, province):

        if isinstance(province, int):
            province = db.provinces.get( province)

        if province:
            self.claim_provinces[province.province_id] = province
            db.country_province_claim_dict[self.tag].append( province.province_id )

    #
    #   remove provinces
    #

    def remove_owned_province(self, province):
        if isinstance(province, int):
            province = db.provinces.get( province)

        if province:
            if province.province_id in self.owned_provinces.keys():
                self.owned_provinces.pop( province.province_id )
                db.country_province_owner_dict[ province.province_id ] = None

    def remove_occupied_province(self, province):
        if isinstance(province, int):
            province = db.provinces.get( province)

        if province:
            if province.province_id in self.occupied_provinces.keys():
                self.occupied_provinces.pop( province.province_id )
                db.country_province_occupant_dict[ province.province_id ] = None

    def remove_national_province(self, province):
        if isinstance(province, int):
            province = db.provinces.get( province)

        if province:
            if province.province_id in self.national_provinces.keys():
                self.national_provinces.pop( province.province_id )
                db.country_province_national_dict[self.tag].remove( province.province_id )

    def remove_claim_province(self, province):
        if isinstance(province, int):
            province = db.provinces.get( province)

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