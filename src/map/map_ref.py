import toml
from PySide6.QtGui import QColor, QPen, QBrush

from src.ref.ref_mapblock import BattleMapBlock
from src.ref.ref_regiment import RegimentType
from src.ref.ref_unit import UnitType
from src.ref.ref_area import GeoArea
from src.ref.ref_building import Building
from src.ref.ref_climate import Climate
from src.ref.ref_continent import GeoContinent
from src.ref.ref_culture import Culture
from src.ref.ref_formation import BattleFormation
from src.ref.ref_goods import Goods
from src.ref.ref_region import GeoRegion
from src.ref.ref_religion import Religion
from src.ref.ref_techgroup import TechGroup
from src.ref.ref_terrain import Terrains
from src.db import TDB

db = TDB()

def load_countries_from_toml():
    print("  Load country definitions from toml")
    file_path = db.path_db / 'country.toml'

    from src.virtual.country import Country

    with open(file_path, 'r') as file:
        countries = toml.load(file)

    output_countries : dict[str, Country] = {}

    # setup global lists of who owns what
    for key, val in countries.items():

        db.country_province_national_dict[key] = []
        db.country_province_claim_dict[key] = []

        val['tag'] = key
        country = Country(val)
        output_countries[ key] = country

    db.countries = output_countries


def load_terrains_from_toml():
    print("  Load terrains definitions from toml")

    file_path = db.path_db / 'terrain.toml'
    with open(file_path, 'r') as file:
        terrains = toml.load(file)

    c_dict = {}
    for key, val in terrains.items():
        val['tag'] = key
        c_dict[ key ] = Terrains( val )

    db.db_terrains = c_dict

    # load battle tiles codes
    file_path = db.path_db / 'terrain_code.toml'
    with open(file_path, 'r') as file:
        battle_tile_codes = toml.load(file)

    db.battle_tile_codes = battle_tile_codes

    db.db_battle_maps_blocks = {}

    file_path = db.path_db / 'terrain_block.toml'
    with open(file_path, 'r') as file:
        db_battle_maps_blocks = toml.load(file)

    for key, val in db_battle_maps_blocks.items():
        db.db_battle_maps_blocks[key] = []
        for block in val:
            b = BattleMapBlock( block )
            db.db_battle_maps_blocks[key].append( b )


def load_cultures_from_toml():
    print("  Load culture definitions from toml")
    file_path = db.path_db / 'culture.toml'

    with open(file_path, 'r') as file:
        cultures = toml.load(file)

    c_dict = {}
    for key, val in cultures.items():
        val['tag'] = key
        c_dict[ key ] = Culture( val )

    db.db_cultures = c_dict


def load_buildings_from_toml():
    print("  Load building definitions from toml")
    file_path = db.path_db / 'building.toml'

    with open(file_path, 'r') as file:
        buildings = toml.load(file)

    b_dict = {}
    for key, val in buildings.items():
        val['tag'] = key
        b_dict[ key ] = Building( val )

    db.db_buildings = b_dict


def load_religions_from_toml():
    print("  Load religion definitions from toml")
    file_path = db.path_db / 'religion.toml'

    with open(file_path, 'r') as file:
        religions = toml.load(file)

    c_dict = {}
    for key, val in religions.items():
        val['tag'] = key
        c_dict[ key ] = Religion( val )

    db.db_religions = c_dict

def load_climates_from_toml():
    print("  Load climate definitions from toml")
    file_path = db.path_db / 'climate.toml'

    with open(file_path, 'r') as file:
        climates =  toml.load(file)

    c_dict = {}
    for key, val in climates.items():
        val['tag'] = key
        c_dict[ key ] = Climate( val )

    db.db_climates = c_dict


def load_goods_from_toml():
    print("  Load goods definitions from toml")
    file_path = db.path_db / 'good.toml'

    with open(file_path, 'r') as file:
        goods = toml.load(file)

    c_dict = {}
    for key, val in goods.items():
        val['tag'] = key
        c_dict[ key ] = Goods( val )

    db.db_goods = c_dict


def load_regions_from_toml():
    print("  Load regions definitions from toml")
    file_path = db.path_db / 'region.toml'

    with open(file_path, 'r') as file:
        regions = toml.load(file)

    c_dict = {}
    for key, val in regions.items():
        val['tag'] = key
        c_dict[ key ] = GeoRegion( val )

    db.db_regions = c_dict

def load_areas_from_toml():
    print("  Load areas definitions from toml")
    file_path = db.path_db / 'area.toml'

    with open(file_path, 'r') as file:
        areas =  toml.load(file)

    c_dict = {}
    for key, val in areas.items():
        val['tag'] = key
        c_dict[ key ] = GeoArea( val )

    db.db_areas = c_dict

def load_continents_from_toml():
    print("  Load continents definitions from toml")
    file_path = db.path_db / 'continent.toml'

    with open(file_path, 'r') as file:
        conts = toml.load(file)

    c_dict = {}
    for key, val in conts.items():
        val['tag'] = key
        c_dict[ key ] = GeoContinent( val )

    db.db_continents = c_dict

def load_cot_colors_from_toml():
    print("  Load cot colors definitions from toml")
    file_path = db.path_db / 'cots.toml'

    with open(file_path, 'r') as file:
        cots = toml.load(file)

    db.db_cot_colors = cots['cot_colors']



def load_units_from_toml():
    print("  Load units definitions from toml")
    file_path = db.path_db / 'units.toml'

    with open(file_path, 'r') as file:
        units = toml.load(file)

    units_obj : dict[str, UnitType] = {}
    for k, val in units.items():
        val['tag'] = k
        u = UnitType( val )
        units_obj[k] = u

    db.db_units = units_obj

def load_regiments_from_toml():
    print("  Load regiment definitions from toml")
    file_path = db.path_db / 'regiments.toml'

    with open(file_path, 'r') as file:
        units = toml.load(file)

    units_obj : dict[str, RegimentType] = {}
    for k, val in units.items():
        val['tag'] = k
        u = RegimentType( val )
        units_obj[k] = u

    db.db_regiments = units_obj

def load_techgroup_from_toml():
    print("  Load technology group definitions from toml")
    file_path = db.path_db / 'technology_group.toml'

    with open(file_path, 'r') as file:
        techgroups = toml.load(file)

    techgroups_obj : dict[str, TechGroup] = {}
    for k, val in techgroups.items():
        val['tag'] = k
        u = TechGroup( val )
        techgroups_obj[k] = u

    db.db_techgroups = techgroups_obj

def load_units_to_regiments_from_toml():
    print("  Load regiment unit to definitions from toml")
    file_path = db.path_db / 'unit_regiment.toml'

    with open(file_path, 'r') as file:
        data = toml.load(file)

    db.db_unit_to_regiments = data


def load_battle_formations_from_toml():
    print("  Load battle region formations from toml")
    file_path = db.path_db / 'battle_formation.toml'

    with open(file_path, 'r') as file:
        data = toml.load(file)

    map = data.get('battle_map').strip().split('\n')

    map_dict = {}
    for y, row in enumerate(map):
        for x, value in enumerate(row.split('\t')):
            for sub_value in value.split('|'):
                if sub_value not in map_dict:
                    map_dict[sub_value] = []
                map_dict[sub_value].append((x, y))

    db.db_battle_map = map_dict
    db.db_battle_regions = data.get('battle_regions')

    form_reg = data.get('battle_formations')

    data_obj : dict[str, BattleFormation] = {}
    for k, val in form_reg.items():
        val['tag'] = k
        u = BattleFormation( val )
        data_obj[k] = u

    db.db_battle_formations = data_obj

def load_colors_from_toml():
    print("  Load colors definitions from format.toml file")
    file_path = db.path_db / 'config' / 'color.toml'

    with open(file_path, 'r') as file:
        colors_data = toml.load(file)
    colors = {}
    for name, hex_value in colors_data['color'].items():
        colors[name] = QColor(hex_value)

    db.db_colors = colors

    # Create QColor, QPen, and QBrush for each color
    db.db_colors_color = {}
    db.db_colors_pen = {}
    db.db_colors_brush = {}

    for name, color in colors.items():
        db.db_colors_color[name] = QColor(color)
        db.db_colors_pen[name] = QPen(color)
        db.db_colors_brush[name] = QBrush(color)

    print("  Load color sets from toml")
    color_sets = colors_data.get('color_sets', {})

    db.db_color_sets = color_sets

