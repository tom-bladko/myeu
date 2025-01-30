from other.modifiers import Modifiers
from other.requs import Requirements


class Building:

    def __init__(self):
        self.name = ""
        self.image = None

        self.modifiers = Modifiers()
        self.requirements = Requirements()

        self.max_levels = 1
        self.build_cost = 100       # in ducats
        self.build_time = 3         # in turns
