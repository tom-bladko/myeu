from src.battle.regiment import Regiment

#
#   BATTLE TILE
#


class BattleTile:
    def __init__(self, terrain: str, x: int, y: int):
        self.terrain = terrain
        self.x = x
        self.y = y
        self.regiment: Regiment = None  # No unit on the tile initially
        self.neighbours = []

    def set_regiment(self, regiment : Regiment):
        self.regiment = regiment

    def set_neighbours(self, data):
        self.neighbours = data