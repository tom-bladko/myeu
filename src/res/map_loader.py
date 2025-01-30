
'''

MAP LOADER

Loads all resources files and process them

'''

import os

import yaml
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageQt import ImageQt
from PySide6.QtCore import QPoint
from PySide6.QtGui import QPixmap, QColor, QPen, QBrush, QPainter, Qt

from game.area import GeoArea
from game.climate import Climate
from game.continent import GeoContinent
from game.culture import Culture
from game.goods import Goods
from game.region import GeoRegion
from game.religion import Religion
from game.terrain import Terrains
from src.db import TDB
db = TDB()

from eng.map_loader import TILE_SIZE


def load_mod():
    print('Load mod details')

    load_colors_from_yaml()
    load_color_sets_from_yaml()

    create_pixmaps_from_colors()
    create_pixmaps_with_weather_effect()
    create_pixmaps_with_terrain_effect()
    create_pixmaps_with_pattern_effect()

    # load images
    load_images_from_gfx_folder()
    prepare_country_flag_in_frame()

    # convert map PDN to PNGs
    load_pdn_map_file()

    # process auto-tiles
    load_and_process_autotiles()

    # process rivers
    load_rivers_map_from_image()
    load_river_autotiles()

    # load CSV with province ID vs RGB
    load_province_color_mapping()

    # load from image prov id defs
    load_province_ids_from_image()
    calculate_borders_map()
    load_cities_from_image()

    # TODO load terrain icons
    print("Load terrains icons TODO ")

    calculate_province_river_values()

    create_color_rectangles_image()

    make_font_numbers()

    load_countries_from_yaml()
    load_terrains_from_yaml()
    load_cultures_from_yaml()
    load_religions_from_yaml()
    load_goods_from_yaml()
    load_climates_from_yaml()
    load_continents_from_yaml()
    load_regions_from_yaml()
    load_areas_from_yaml()
    load_cot_colors_from_yaml()

    # save data about province colors to text file
    save_province_colors_to_csv()

    dump_all_map_data_to_files()

    load_provinces_from_prov_id_map()
    load_provinces_def_from_csv()

    calculate_province_city_and_names_positions()
    calculate_province_neighbours()
    calculate_borders_and_roads()

    # remap_province_colors()


def load_province_color_mapping():
    import csv
    print("  Load province color definition")
    csv_path = db.path_map / 'prov_mapping.txt'

    # Load the province colors from the CSV file
    province_colors = {}
    province_colors_hex = {}
    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            province_id, r, g, b, h, c = row
            province_colors[(int(r), int(g), int(b))] = int(province_id)
            province_colors_hex[ h ] = int(province_id)

    db.province_mapping_color = province_colors
    db.province_mapping_color_hex = province_colors_hex


def load_province_ids_from_image( ):
    print("  Load province id map")

    from PIL import Image

    prov_id_map_path = db.path_map_province
    prov_id_defs = db.province_mapping_color

    # Load the image
    image = Image.open(prov_id_map_path)
    pixels = image.load()

    # Create a 2D array of province IDs
    width, height = image.size

    db.map_width = width
    db.map_height = height

    province_ids = [[0 for _ in range(db.map_width)] for _ in range(db.map_height)]
    province_border_map = {}
    province_tile_list = {}

    # find which tiles to which province ID
    for y in range(db.map_height):
        for x in range(db.map_width):
            r, g, b = pixels[x, y][:3]  # Get RGB values

            # set this tile has province ID
            province_id = prov_id_defs.get((r, g, b), 0)  # Default to 0 if not found
            if province_id == 0 and (r,g,b) != (0,0,0):
                print("Province not found", r, g, b)
            province_ids[y][x] = province_id

            # set province ID has these tiles
            if province_id not in province_tile_list.keys():
                province_tile_list[province_id] = []
                province_border_map[ province_id ] = {}
            province_tile_list[ province_id ].append( (x, y) )

    db.province_tile_list = province_tile_list
    db.province_id_map = province_ids


def calculate_borders_map():
    print("  Calculate border per province")

    RECT_SIZE = db.rect_size
    province_ids = db.province_id_map

    width = db.map_width
    height = db.map_height

    province_border_map = {}

    # find borders
    for y in range(height):
        for x in range(width):
            current_province = province_ids[y][x]
            if current_province == 0:
                continue
            neighbors = [
                ((x, y), (x + 1, y)),  # Right
                ((x, y), (x, y + 1)),  # Down
            ]
            for (sx, sy), (ex, ey) in neighbors:
                if 0 <= ex < width and 0 <= ey < height:
                    neighbor_province = province_ids[ey][ex]
                    if neighbor_province == 0:
                        continue
                    if neighbor_province != current_province:
                        start = (sx * RECT_SIZE + RECT_SIZE, sy * RECT_SIZE + RECT_SIZE)
                        end = (ex * RECT_SIZE, ey * RECT_SIZE)
                        if current_province not in province_border_map:
                            province_border_map[current_province] = {}
                        province_border_map[current_province].setdefault(neighbor_province, []).append((start, end))

            # Check left neighbor
            if x > 0 and province_ids[y][x - 1] != current_province:
                if province_ids[y][x - 1] > 0:
                    start = (x * RECT_SIZE, y * RECT_SIZE + RECT_SIZE)
                    end = (x * RECT_SIZE, y * RECT_SIZE)
                    neighbor_province = province_ids[y][x - 1]
                    if current_province not in province_border_map:
                        province_border_map[current_province] = {}
                    province_border_map[current_province].setdefault(neighbor_province, []).append((start, end))

            # Check up neighbor
            if y > 0 and province_ids[y - 1][x] != current_province:
                if province_ids[y - 1][x] > 0:
                    start = (x * RECT_SIZE + RECT_SIZE, y * RECT_SIZE)
                    end = (x * RECT_SIZE, y * RECT_SIZE)
                    neighbor_province = province_ids[y - 1][x]
                    if current_province not in province_border_map:
                        province_border_map[current_province] = {}
                    province_border_map[current_province].setdefault(neighbor_province, []).append((start, end))

    db.province_border_map = province_border_map


def load_cities_from_image():
    print("  Load city id map")
    from PIL import Image

    CAPITAL_LAND = (255,0,255)
    NAME_LOCATION = (0,255,0)
    CAPITAL_SEA = (255,255,255)

    capital_map_path = db.path_map_capital
    province_id_map = db.province_id_map

    # Load the image
    image = Image.open(capital_map_path)
    pixels = image.load()

    # Create a 2D array of province IDs
    height, width = db.map_height, db.map_width
    city_id_map = [[0 for _ in range(width)] for _ in range(height)]
    province_name_map = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y][:3]  # Get RGB values
            if (r, g, b) in [ CAPITAL_LAND, CAPITAL_SEA ]:
                city_id_map[y][x] = province_id_map[y][x]
            if (r,g,b) == NAME_LOCATION:
                province_name_map[y][x] = province_id_map[y][x]

    db.city_id_map = city_id_map
    db.name_id_map = province_name_map


def load_rivers_map_from_image():

    print("  Load rivers from image")
    from PIL import Image

    RIVER = (0,0,255)
    SEA = (0,255,0)
    LAND = (255, 255, 255)
    STRAIT = (255,0,0)

    river_map_path = db.path_map_river

    # Load the image
    image = Image.open(river_map_path)
    pixels = image.load()

    # Create a 2D array of province IDs
    height, width = db.map_height, db.map_width
    rivers_id_map = [[0 for _ in range(width)] for _ in range(height)]

    all_types = [RIVER, SEA]

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y][:3]  # Get RGB values
            rgb = (r, g, b)
            if  rgb == RIVER :
                value = 0
                # Check neighbors
                if x < width - 1 and pixels[x + 1, y][:3] in all_types:  # Right
                    value += 1
                if y < height - 1 and pixels[x, y + 1][:3] in all_types:  # Bottom
                    value += 2
                if x > 0 and pixels[x - 1, y][:3] in all_types:  # Left
                    value += 4
                if y > 0 and pixels[x, y - 1][:3] in all_types:  # Up
                    value += 8
                rivers_id_map[y][x] = value
            elif rgb == SEA:
                continue
            else:
                continue

    db.river_id_map = rivers_id_map


def calculate_province_river_values():
    print("  Calculate province river values")
    province_river_values = {}

    for y, row in enumerate(db.province_id_map):
        for x, province_id in enumerate(row):
            if province_id not in province_river_values:
                province_river_values[province_id] = set()
            river_value = db.river_id_map[y][x]
            if river_value > 0:
                province_river_values[province_id].add((x, y, river_value))

    db.province_river_tiles_list = province_river_values


def load_images_from_gfx_folder():
    print('  Load images from gfx folder')

    gfx_folder = db.path_gfx

    images_dict = {}
    for root, dirs, files in os.walk(gfx_folder):
        for subdir in dirs:
            subdir_path = os.path.join(root, subdir)
            images_dict[subdir] = {}
            for file in os.listdir(subdir_path):
                if file.endswith('.png'):
                    file_path = os.path.join(subdir_path, file)
                    pixmap = QPixmap(file_path)
                    images_dict[subdir][file] = pixmap

    db.res_images = images_dict


def prepare_country_flag_in_frame():

    print("  Process country flags into frame")
    from PIL import Image

    # Load the frame image
    frame_path = db.path_gfx / 'city' / 'flag.png'
    frame = Image.open(frame_path).convert("RGBA")

    # Initialize the dictionary to store the images
    db.res_images['flag_frame'] = {}

    # Load all country flags
    flags_folder = db.path_gfx / 'flag'
    for flag_file in os.listdir(flags_folder):
        if flag_file.endswith('.png'):
            country_tag = flag_file.split('.')[0]
            flag_path = flags_folder / flag_file
            country_flag = Image.open(flag_path).convert("RGBA")

            # Create a new image with the same size as the frame
            combined_image = Image.new("RGBA", frame.size, (0, 0, 0, 0))

            # Calculate the position to center the country flag on the frame
            flag_x = (frame.width - country_flag.width) // 2
            flag_y = (frame.height - country_flag.height) // 2

            # Paste the country flag and then the frame over it
            combined_image.paste(country_flag, (flag_x, flag_y), country_flag)
            combined_image.paste(frame, (0, 0), frame)

            # Convert the combined image to QPixmap
            combined_pixmap = QPixmap.fromImage(ImageQt(combined_image))

            # Store the combined pixmap in the dictionary
            db.res_images['flag_frame'][country_tag + '.png'] = combined_pixmap


def load_pdn_map_file():

    print("  Convert map PDN to PNG files")

    import pypdn

    pdn_file_path = db.path_map_pdn

    # Open the .pdn file
    pdn_image = pypdn.read(pdn_file_path)

    # Accessing and saving each layer as a separate PNG file
    for i, layer in enumerate(pdn_image.layers):
        layer_name = layer.name
        layer_image = Image.fromarray(layer.image)
        layer_image.save( db.path_map / f'map_{layer_name}.png')


def load_and_process_autotiles():
    print('  Load autotiles graphics')

    from PIL import Image

    file_path = db.path_tiles / 'autotiles.png'

    tiles_names = ['province', 'country', 'coast', 'river', 'sea']

    # Load the tiles.png image
    tiles_image = Image.open(file_path)
    tile_size = 34
    trimmed_tile_size = 32

    # Calculate the number of tiles
    tiles_x = tiles_image.width // tile_size
    tiles_y = 1

    # Function to trim 1 pixel from each side of a tile
    def trim_tile(tile):
        return tile.crop((1, 1, tile.width - 1, tile.height - 1))

    # Function to create autotile set with rotations
    def create_autotile_set(tile):
        autotiles = []
        for i in range(0, 16):
            autotile = Image.new('RGBA', (trimmed_tile_size, trimmed_tile_size))
            if i & 1:  # Right neighbor
                autotile.paste(tile.rotate(0), (0, 0), tile.rotate(0).convert('RGBA'))
            if i & 2:  # top neighbor
                autotile.paste(tile.rotate(-90), (0, 0), tile.rotate(-90).convert('RGBA'))
            if i & 4:  # Left neighbor
                autotile.paste(tile.rotate(-180), (0, 0), tile.rotate(-180).convert('RGBA'))
            if i & 8:  # bottom neighbor
                autotile.paste(tile.rotate(-270), (0, 0), tile.rotate(-270).convert('RGBA'))
            autotiles.append(autotile)
        return autotiles

    # Process each tile
    for x in range(tiles_x):

        # Save each autotile set as a 4x4 array of images
        output_image = Image.new('RGBA', (4 * trimmed_tile_size, 4 * trimmed_tile_size))

        tile = tiles_image.crop((x * tile_size, 0, (x + 1) * tile_size, tile_size))
        trimmed_tile = trim_tile(tile)
        autotile_set = create_autotile_set(trimmed_tile)

        for i, autotile in enumerate(autotile_set):
            row = i // 4
            col = i % 4
            output_image.paste(autotile, (col * trimmed_tile_size, row * trimmed_tile_size))

        output_image.save( db.path_tiles_auto / f'auto_{tiles_names[x]}.png')


def load_river_autotiles():
    print("  Process rivers autotile")
    from PySide6.QtGui import QPixmap

    file_path = db.path_tiles_auto / 'auto_river2.png'

    # Load the auto_river.png image
    river_image = QPixmap(str(file_path))

    # Create a list to store the 16 sub-images
    river_tiles = []

    # Split the image into 16 sub-images
    for y in range(4):
        for x in range(4):
            tile = river_image.copy(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            river_tiles.append(tile)

    db.res_image_river = river_tiles


def load_colors_from_yaml():
    print("  Load colors definitions from yaml file")
    file_path = db.path_db / 'colors.yml'

    with open(file_path, 'r') as file:
        colors_data = yaml.safe_load(file)
    colors = {}
    for name, hex_value in colors_data['colors'].items():
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


def load_color_sets_from_yaml():
    print("  Load color sets from yaml")
    file_path = db.path_db / 'colors.yml'

    with open(file_path, 'r') as file:
        color_sets_data = yaml.safe_load(file)
    color_sets = color_sets_data.get('color_sets', {})

    db.db_color_sets = color_sets


def create_color_rectangles_image():
    print('  Dump all colors to single png file')

    # Define image dimensions
    rect_width = 75
    rect_height = 25
    num_colors = len(db.db_colors_brush)
    image_width = rect_width
    image_height = rect_height * num_colors

    # Create a new image with white background
    image = Image.new('RGB', (image_width, image_height), 'white')
    draw = ImageDraw.Draw(image)

    # Load a font
    font = ImageFont.load_default()

    # Draw each rectangle with the color brush and write the color name
    for i, (name, brush) in enumerate(db.db_colors_brush.items()):
        y0 = i * rect_height
        y1 = y0 + rect_height

        # Draw the rectangle
        draw.rectangle([0, y0, rect_width, y1], fill=brush.color().name())

        # Calculate text position
        text_bbox = draw.textbbox((0, 0), name, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = (rect_width - text_width) // 2
        text_y = y0 + (rect_height - text_height) // 2

        # Draw the text
        draw.text((text_x, text_y), name, fill='black', font=font)

    # Save the image to a PNG file
    output_path = db.path_tiles / 'color_rectangles.png'
    image.save(output_path)


def dump_all_map_data_to_files():
    import csv
    print("  Dump all map data to text files")
    data_maps = {
        'province_id_map': db.province_id_map,
        'city_id_map': db.city_id_map,
        'province_name_map': db.name_id_map,
        'province_river_map': db.river_id_map,
        'province_neighbours_list': db.province_neighbors_list,
        'province_mapping_color': db.province_mapping_color,
        'province_border_map': db.province_border_map
    }

    for map_name, data in data_maps.items():
        with open(db.path_mod_duck / f'{map_name}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            print("  Saving", map_name)
            if isinstance(data, list):
                writer.writerows(data)
            elif isinstance(data, dict):
                for key, value in data.items():
                    writer.writerow([key, value])


def make_font_numbers():
    print("  Generate numbers to png file")
    tile_width, tile_height = 8, 12
    output_path = db.path_gfx / "numbers"

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    def create_numbers_from_base():
        base_image_path = output_path / "base.png"
        base_image = Image.open(base_image_path)
        digits = [base_image.crop((i * tile_width, 0, (i + 1) * tile_width, tile_height)) for i in range(10)]

        atlas = Image.new("RGBA", (tile_width * 20, tile_height * 10), '#404040')
        for number in range(100):
            tens = number // 10
            units = number % 10
            number_image = Image.new("RGBA", (tile_width * 2, tile_height), (0, 0, 0, 0))
            if number < 10:
                number_image.paste(digits[units], (tile_width // 2, 0))
            else:
                number_image.paste(digits[tens], (0, 0))
                number_image.paste(digits[units], (tile_width, 0))

            x = (number % 10) * (tile_width * 2)
            y = (number // 10) * tile_height
            atlas.paste(number_image, (x, y))

        atlas.save(output_path / "numbers_out.png")

    create_numbers_from_base()


def load_countries_from_yaml():
    print("  Load country definitions from yaml")
    file_path = db.path_db / 'countries.yml'

    with open(file_path, 'r') as file:
        countries_data = yaml.safe_load(file)
    countries = countries_data.get('country', {})

    # setup global lists of who owns what
    for key, val in countries.items():
        db.country_province_national_dict[key] = []
        db.country_province_claim_dict[key] = []

    db.db_countries = countries


def load_terrains_from_yaml():
    print("  Load terrains definitions from yaml")
    file_path = db.path_db / 'terrains.yml'

    with open(file_path, 'r') as file:
        terrains_data = yaml.safe_load(file)
    terrains = terrains_data.get('terrains', {})

    c_dict = {}
    for key, val in terrains.items():
        val['tag'] = key
        c_dict[ key ] = Terrains( val )

    db.db_terrains = c_dict


def load_cultures_from_yaml():
    print("  Load culture definitions from yaml")
    file_path = db.path_db / 'culture.yml'

    with open(file_path, 'r') as file:
        cultures_data = yaml.safe_load(file)
    cultures = cultures_data.get('cultures', {})

    c_dict = {}
    for key, val in cultures.items():
        val['tag'] = key
        c_dict[ key ] = Culture( val )

    db.db_cultures = c_dict


def load_religions_from_yaml():
    print("  Load religion definitions from yaml")
    file_path = db.path_db / 'religion.yml'

    with open(file_path, 'r') as file:
        religions_data = yaml.safe_load(file)
    religions = religions_data.get('religions', {})

    c_dict = {}
    for key, val in religions.items():
        val['tag'] = key
        c_dict[ key ] = Religion( val )

    db.db_religions = c_dict

def load_climates_from_yaml():
    print("  Load climate definitions from yaml")
    file_path = db.path_db / 'climate.yml'

    with open(file_path, 'r') as file:
        climates_data = yaml.safe_load(file)
    climates = climates_data.get('climates', {})

    c_dict = {}
    for key, val in climates.items():
        val['tag'] = key
        c_dict[ key ] = Climate( val )

    db.db_climates = c_dict


def load_goods_from_yaml():
    print("  Load goods definitions from yaml")
    file_path = db.path_db / 'goods.yml'

    with open(file_path, 'r') as file:
        goods_data = yaml.safe_load(file)
    goods = goods_data.get('goods', {})

    c_dict = {}
    for key, val in goods.items():
        val['tag'] = key
        c_dict[ key ] = Goods( val )

    db.db_goods = c_dict


def load_regions_from_yaml():
    print("  Load regions definitions from yaml")
    file_path = db.path_db / 'regions.yml'

    with open(file_path, 'r') as file:
        regions_data = yaml.safe_load(file)
    regions = regions_data.get('regions', {})

    c_dict = {}
    for key, val in regions.items():
        val['tag'] = key
        c_dict[ key ] = GeoRegion( val )

    db.db_regions = c_dict

def load_areas_from_yaml():
    print("  Load areas definitions from yaml")
    file_path = db.path_db / 'area.yml'

    with open(file_path, 'r') as file:
        areas_data = yaml.safe_load(file)
    areas = areas_data.get('areas', {})

    c_dict = {}
    for key, val in areas.items():
        val['tag'] = key
        c_dict[ key ] = GeoArea( val )

    db.db_areas = c_dict

def load_continents_from_yaml():
    print("  Load continents definitions from yaml")
    file_path = db.path_db / 'continents.yml'

    with open(file_path, 'r') as file:
        cont_data = yaml.safe_load(file)
    conts = cont_data.get('continents', {})

    c_dict = {}
    for key, val in conts.items():
        val['tag'] = key
        c_dict[ key ] = GeoContinent( val )

    db.db_continents = c_dict

def load_cot_colors_from_yaml():
    print("  Load cot colors definitions from yaml")
    file_path = db.path_db / 'cots.yml'

    with open(file_path, 'r') as file:
        cots_data = yaml.safe_load(file)
    cots = cots_data.get('cots_colors', {})

    db.db_cot_colors = cots

def _create_province_color_mapping():
    colors = {}
    used_colors = set()

    def eu4_color(province_id):
        r = int(province_id * 23.123) % 250  # Full red
        g = int(province_id * 47.456) % 250  # Full green
        b = int(province_id * 71.789) % 250  # Less blue
        return r, g, b

    for province_id in range(1, 4000):
        r, g, b = eu4_color(province_id)
        color = (r, g, b)
        if color not in used_colors:
            used_colors.add(color)
            colors[province_id] = color
        else:
            print("Color province mapping repeated", color)
    return colors


def save_province_colors_to_csv():
    import csv
    print( "  Save province color mapping to CSV")

    def rgb_to_hex(r, g, b):
        return f"#{r:02x}{g:02x}{b:02x}"

    rows = len(db.province_id_map)
    cols = len(db.province_id_map[0])

    colors = _create_province_color_mapping()
    province_size = {}

    for row in range(rows):
        for col in range(cols):
            prov_id = db.province_id_map[row][col]
            if prov_id in province_size.keys():
                province_size[prov_id] += 1
            else:
                province_size[prov_id] = 1

    pathka = db.path_map / 'prov_mapping.txt'

    with open( str(pathka), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "R", "G", "B", "hex", "count"])

        for province_id, (r, g, b) in colors.items():
            hex_color = rgb_to_hex(r, g, b)
            cell_count = province_size.get(province_id, 0)
            writer.writerow([f"{province_id:04}", f"{r:03}", f"{g:03}", f"{b:03}", hex_color, f"{cell_count:04}"])


def create_pixmaps_from_colors():
    print("  Create all graphics for textures")
    db_colors = db.db_colors_color
    grid_size = db.rect_size
    output_dir = db.path_gfx / 'textures'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for color_name, color_value in db_colors.items():
        pixmap = QPixmap(grid_size, grid_size)
        pixmap.fill(color_value)
        pixmap.save(os.path.join(output_dir, f"{color_name}.png"))


def create_pixmaps_with_weather_effect():
    print("  Create all graphics for textures with weather effects")
    weather_effects = db.db_color_sets['weather']

    output_dir = db.path_gfx / 'textures'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for effect in weather_effects:
        effect_image_path = db.path_gfx / 'weather' / f'{effect}.png'
        effect_image = QPixmap(str(effect_image_path))
        grid_size = effect_image.size()

        pixmap = QPixmap(grid_size)
        pixmap.fill(Qt.transparent)  # Ensure the pixmap is transparent
        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)  # Ensure transparency and layering
        painter.drawPixmap(0, 0, effect_image)
        painter.end()

        file_name = f"effect_{effect}"
        db.db_colors_brush[file_name] = QBrush(pixmap)


def create_pixmaps_with_terrain_effect():
    print("  Create all graphics for textures with terrain effects")
    terrains_effects = db.db_color_sets['terrains']

    output_dir = db.path_gfx / 'textures'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for effect in terrains_effects:
        effect_image_path = db.path_gfx / 'terrains' / f'{effect}.png'
        effect_image = QPixmap(str(effect_image_path))
        grid_size = effect_image.size()

        pixmap = QPixmap(grid_size)
        pixmap.fill(Qt.transparent)  # Ensure the pixmap is transparent
        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)  # Ensure transparency and layering
        painter.drawPixmap(0, 0, effect_image)
        painter.end()

        file_name = f"terrain_{effect}"
        db.db_colors_brush[file_name] = QBrush(pixmap)


def create_pixmaps_with_pattern_effect():
    print("  Create all graphics for textures with pattern effects")
    db_color_sets = db.db_color_sets['pattern']
    grid_size = db.rect_size
    output_dir = db.path_gfx / 'textures'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for color_name in db_color_sets:
        color_value = db.db_colors_color.get(color_name)
        if color_value:
            pixmap = QPixmap(grid_size, grid_size)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            painter.setBrush(color_value)
            painter.setPen(Qt.NoPen)
            painter.drawRect(grid_size // 2, 0, grid_size // 2, grid_size)
            painter.end()

            file_name = f"{color_name}_half"
            db.db_colors_brush[file_name] = QBrush(pixmap)


def load_provinces_from_prov_id_map():
    print("    Load provinces from prov id map 2D")
    unique_ids = set()
    for row in  db.province_id_map:
        unique_ids.update(row)

    for province_id in unique_ids:
        prov_data = {
            'ID': province_id,
            'name': 'PROVINCE NAME'
        }
        db.provinces_data_dict[ province_id ] = prov_data

    with open( db.path_db_provinces, 'w') as file:
        yaml.dump({'provinces': db.provinces_data_dict}, file, default_flow_style=False, sort_keys=False)


def load_provinces_def_from_csv():
    print("    Load provinces definitions from csv")
    from map.provinceItem import ProvinceItem
    import csv

    provinces = {}

    with open(db.path_db_provinces_csv, 'r') as file:
        reader = csv.DictReader(file)
        for row_data in reader:
            row_data['id'] = row_data['\ufeffid']
            prov_id = int(row_data['id'])
            terrain = row_data['terrain']
            if prov_id in db.provinces_data_dict.keys():
                row_data['is_land'] = False if terrain in ['sea', 'river', 'lake'] else True
                P = ProvinceItem(row_data)
                provinces[P.province_id] = P

    # setup global lists of who owns what
    for key, val in provinces.items():
        db.country_province_owner_dict[key] = None
        db.country_province_occupant_dict[key] = None

    db.db_provinces = provinces


def calculate_province_city_and_names_positions():
    print("    Calculate position of province city and name")
    map_data =  db.city_id_map
    db_provs = db.db_provinces

    rows = len(map_data)
    cols = len(map_data[0]) if rows > 0 else 0

    for row in range(rows):
        for col in range(cols):
            province_id = map_data[row][col]
            if province_id:
                if province_id in db_provs.keys():
                    prov = db_provs.get(province_id, None)
                    if prov:
                        prov.city_position = (col, row)

    map_data = db.name_id_map

    for key, prov in db_provs.items():
        prov.name_text_position = []

    for row in range(rows):
        for col in range(cols):
            province_id = map_data[row][col]
            if province_id:
                if province_id in db_provs.keys():
                    prov = db_provs.get(province_id, None)
                    if prov:
                        prov.name_text_position.append( (col, row) )


def calculate_province_neighbours():
    print("    Calculate provinces neighbours")
    map_data = db.province_id_map

    db_provs = db.db_provinces

    rows = len(map_data)
    cols = len(map_data[0]) if rows > 0 else 0

    def get_neighbors(data, r, c):
        neighs = []
        if r > 0:
            neighs.append((r - 1, c, data[r - 1][c]))
        if r < len(data) - 1:
            neighs.append((r + 1, c, data[r + 1][c]))
        if c > 0:
            neighs.append((r, c - 1, data[r][c - 1]))
        if c < len(data[0]) - 1:
            neighs.append((r, c + 1, data[r][c + 1]))
        return neighs

    province_neighbors = {}

    for row in range(rows):
        for col in range(cols):
            province_id = map_data[row][col]
            if province_id in db_provs:
                neighbors = get_neighbors(map_data, row, col)
                for neighbor_row, neighbor_col, neighbor_id in neighbors:
                    if neighbor_id != province_id:
                        if neighbor_id > 0:
                            province_neighbors.setdefault(province_id, set()).add(neighbor_id)

    province_neighbors_list = {prov_id: ';'.join(map(str, neighbors)) for prov_id, neighbors in
                               province_neighbors.items()}
    db.province_neighbors = province_neighbors
    db.province_neighbors_list = province_neighbors_list


def calculate_borders_and_roads():

    print("    Calculate boards and roads")
    province_neighbors = db.province_neighbors
    provinces = db.db_provinces

    def calculate_distance(row1, col1, row2, col2):
        return int(((row1 - row2) ** 2 + (col1 - col2) ** 2) ** 0.5)

    # Calculate distance between city positions of neighboring provinces
    province_neighbors_dist = {}

    for province_id, neighbors in province_neighbors.items():
        for neighbor_id in neighbors:
            city_pos1 = provinces[province_id].city_position
            city_pos2 = provinces[neighbor_id].city_position
            if city_pos1 and city_pos2:
                distance = calculate_distance(city_pos1[1], city_pos1[0], city_pos2[1], city_pos2[0])
                province_neighbors_dist[(province_id, neighbor_id)] = distance
                province_neighbors_dist[(neighbor_id, province_id)] = distance
            else:
                print("ERROR, no city found", province_id, neighbor_id)

    db.province_neighbours_distance = province_neighbors_dist


# def remap_province_colors():
#     print("  Remap province colors based on ORG ID")
#
#     import csv
#     from PIL import Image
#
#     # Load province mapping from CSV
#     prov_mapping_path = db.path_map / 'prov_mapping.txt'
#     prov_mapping = {}
#     with open(prov_mapping_path, newline='') as csvfile:
#         reader = csv.reader(csvfile)
#         next(reader)  # Skip the header row
#         for row in reader:
#             province_id, r, g, b, h, c = row
#             prov_mapping[int(province_id)] = (int(r), int(g), int(b))
#
#     # Load provinces data from CSV
#     provinces_csv_path = db.path_db / 'provinces.csv'
#     provinces_data = {}
#     with open(provinces_csv_path, newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             row['id'] = row['\ufeffid']
#             if row['org_id'] == '':
#                 provinces_data[int(row['id'])] = int(row['id'])
#             else:
#                 provinces_data[int(row['id'])] = int(row['org_id'])
#
#     # Load the province ID map image
#     map_provinces_path = db.path_map_province
#     image = Image.open(map_provinces_path)
#     pixels = image.load()
#
#     # Create a new image for the remapped colors
#     remapped_image = Image.new('RGBA', image.size)
#     remapped_pixels = remapped_image.load()
#
#     # Remap the colors based on ORG ID
#     width, height = image.size
#     for y in range(height):
#         for x in range(width):
#             r, g, b = pixels[x, y][:3]
#             province_id = next((pid for pid, color in prov_mapping.items() if color == (r, g, b)), 0)
#             org_id = provinces_data.get(province_id, province_id)
#             remapped_color = prov_mapping.get(org_id, (r, g, b))
#             remapped_pixels[x, y] = (remapped_color[0], remapped_color[1], remapped_color[2], 255)  # Ensure RGBA format
#
#     # Save the remapped image
#     remapped_image_path = db.path_map / 'map_provinces_converted.png'
#     remapped_image.save(remapped_image_path)