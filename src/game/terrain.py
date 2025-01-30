from other.modifiers import Modifiers


class Terrains:

    def __init__(self, kwargs):
        self.tag = kwargs.get('tag', 'nothing')
        self.name = kwargs.get('name', 'nothing')
        self.effect = kwargs.get('effect', False)
        self.color_name = kwargs.get('color', 'brown')

        self.modifiers = kwargs.get('modifiers', Modifiers())
