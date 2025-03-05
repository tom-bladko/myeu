import random
from PIL import Image, ImageDraw, ImageFont

class HexTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []
        self.is_block = False
        self.value = 0

    def __repr__(self):
        return f"HexTile({self.x}, {self.y}, Block={self.is_block}, Value={self.value})"

class HexMap:
    def __init__(self, width=15, height=10, tile_size=40):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.battle_tiles = [[HexTile(x, y) for x in range(width)] for y in range(height)]
        self.fog_of_war = {'A': [[True for _ in range(width)] for _ in range(height)],
                           'B': [[True for _ in range(width)] for _ in range(height)]}
        self.initialize_neighbors()
        random.seed(1983)
        self.initialize_random_blocks(40)
        self.initialize_tile_values()

    #
    def initialize_neighbors(self):
        directions_even = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1)]
        directions_odd = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, 1)]

        for y in range(self.height):
            for x in range(self.width):
                tile = self.battle_tiles[y][x]
                directions = directions_even if x % 2 == 0 else directions_odd
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        tile.neighbors.append(self.battle_tiles[ny][nx])

    #
    def initialize_random_blocks(self, num_blocks):
        for _ in range(num_blocks):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.battle_tiles[y][x].is_block = True
            self.battle_tiles[y][x].value = 0

    #
    def initialize_tile_values(self):
        for y in range(self.height):
            for x in range(self.width):
                if not self.battle_tiles[y][x].is_block:
                    self.battle_tiles[y][x].value = random.choice([0.5, 1, 1.5, 2])

    #
    def hide_all_tiles_under_fog_of_war(self):
        for side in self.fog_of_war:
            for y in range(self.height):
                for x in range(self.width):
                    self.fog_of_war[side][y][x] = True

    #
    def reveal_tiles(self, start_tile, range_distance, side):
        tiles_in_range = self.get_tiles_in_range(start_tile, range_distance)
        for tile in tiles_in_range:
            self.fog_of_war[side][tile.y][tile.x] = False

    def get_tiles_in_range(self, start_tile, range_distance):
        visited = set()
        to_visit = [(start_tile, 0)]
        result = []

        while to_visit:
            current_tile, distance = to_visit.pop(0)
            if distance > range_distance:
                continue
            if current_tile not in visited:
                visited.add(current_tile)
                result.append(current_tile)
                for neighbor in current_tile.neighbors:
                    to_visit.append((neighbor, distance + 1))

        return result

    def get_movable_tiles(self, start_tile, range_distance):
        visited = set()
        to_visit = [(start_tile, 0)]
        result = []

        while to_visit:
            current_tile, distance = to_visit.pop(0)
            if distance > range_distance:
                continue
            if current_tile not in visited and not current_tile.is_block:
                visited.add(current_tile)
                result.append(current_tile)
                for neighbor in current_tile.neighbors:
                    to_visit.append((neighbor, distance + neighbor.value))

        return result

    def calculate_distance(self, start_tile, end_tile):
        dx = end_tile.x - start_tile.x
        dy = end_tile.y - start_tile.y
        return max(abs(dx), abs(dy), abs(dx + dy))

    def find_path(self, start_tile, end_tile):
        from heapq import heappop, heappush
        import itertools

        counter = itertools.count()  # unique sequence count
        queue = [(0, next(counter), start_tile, [start_tile])]
        visited = set()

        while queue:
            cost, _, current_tile, path = heappop(queue)
            if current_tile == end_tile:
                return path
            if current_tile not in visited:
                visited.add(current_tile)
                for neighbor in current_tile.neighbors:
                    if neighbor not in visited and not neighbor.is_block:
                        heappush(queue, (cost + neighbor.value, next(counter), neighbor, path + [neighbor]))

        return []

    def is_direct_line_clear(self, tile_a, tile_b):
        dx = tile_b.x - tile_a.x
        dy = tile_b.y - tile_a.y
        steps = max(abs(dx), abs(dy))
        for step in range(1, steps):
            x = tile_a.x + step * dx // steps
            y = tile_a.y + step * dy // steps
            if self.battle_tiles[y][x].is_block:
                return False
        return True

    def visualize(self, start_tile, end_tile, path, filename='hexmap.png'):
        img_width = self.width * self.tile_size
        img_height = self.height * self.tile_size + self.tile_size // 2
        image = Image.new('RGB', (img_width, img_height), 'black')
        draw = ImageDraw.Draw(image)

        #self.draw_movable_tiles(draw, start_tile, 4)
        #self.draw_path(draw, path)
        self.draw_dot(draw, start_tile, 'red')
        self.draw_dot(draw, end_tile, 'blue')
        self.draw_tiles(draw)
        self.draw_range(draw, start_tile, 4  )
        image.save(filename)

    def draw_movable_tiles(self, draw, start_tile, range_distance):
        movable_tiles = self.get_movable_tiles(start_tile, range_distance)
        for tile in movable_tiles:
            draw_x = tile.x * self.tile_size
            draw_y = tile.y * self.tile_size + (self.tile_size // 2 if tile.x % 2 == 1 else 0)
            draw.rectangle([draw_x, draw_y, draw_x + self.tile_size, draw_y + self.tile_size], fill='green', outline='black')

    def draw_tiles(self, draw):
        font = ImageFont.load_default()

        for y in range(self.height):
            for x in range(self.width):
                tile = self.battle_tiles[y][x]
                draw_x = x * self.tile_size
                draw_y = y * self.tile_size + (self.tile_size // 2 if x % 2 == 1 else 0)
                color = 'gray' if tile.is_block else 'white'
                if self.fog_of_war[y][x]:
                    color = 'black'
                draw.rectangle([draw_x, draw_y, draw_x + self.tile_size, draw_y + self.tile_size], fill=color, outline='black')
                if not self.fog_of_war[y][x]:
                    text_x = draw_x + self.tile_size // 2
                    text_y = draw_y + self.tile_size // 2
                    draw.text((text_x, text_y), str(tile.value), fill='black', font=font, anchor='mm')

    def draw_range(self, draw, start_tile, range_distance):
        tiles_in_range = self.get_tiles_in_range(start_tile, range_distance)
        for tile in tiles_in_range:
            draw_x = tile.x * self.tile_size
            draw_y = tile.y * self.tile_size + (self.tile_size // 2 if tile.x % 2 == 1 else 0)
            draw.rectangle([draw_x, draw_y, draw_x + self.tile_size, draw_y + self.tile_size], fill='yellow', outline='black')

    def draw_dot(self, draw, tile, color):
        draw_x = tile.x * self.tile_size + self.tile_size // 2
        draw_y = tile.y * self.tile_size + (self.tile_size // 2 if tile.x % 2 == 1 else 0) + self.tile_size // 2
        radius = 5
        draw.ellipse([draw_x - radius, draw_y - radius, draw_x + radius, draw_y + radius], fill=color, outline=color)

    def draw_path(self, draw, path):
        for tile in path:
            draw_x = tile.x * self.tile_size
            draw_y = tile.y * self.tile_size + (self.tile_size // 2 if tile.x % 2 == 1 else 0)
            draw.rectangle([draw_x, draw_y, draw_x + self.tile_size, draw_y + self.tile_size], fill='blue', outline='black')

    def draw_distance(self, draw, end_tile):
        draw_x = end_tile.x * self.tile_size
        draw_y = end_tile.y * self.tile_size + (self.tile_size // 2 if end_tile.x % 2 == 1 else 0)
        draw.rectangle([draw_x, draw_y, draw_x + self.tile_size, draw_y + self.tile_size], fill='red', outline='black')

# Example usage
hex_map = HexMap()
start_tile = hex_map.battle_tiles[7][3]
end_tile = hex_map.battle_tiles[4][8]
path = hex_map.find_path(start_tile, end_tile)
hex_map.visualize(start_tile, end_tile, path)

# Check if the direct line is clear between start_tile and end_tile
is_clear = hex_map.is_direct_line_clear(start_tile, end_tile)
print(f"Is direct line clear: {is_clear}")