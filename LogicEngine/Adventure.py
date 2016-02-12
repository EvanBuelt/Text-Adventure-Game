__author__ = 'Evan'
import Item
import Materials


class Game:
    def __init__(self):
        self.copper_ore = Materials.Ore("Copper Ore", 0)
        self.tin_ore = Materials.Ore("Tin Ore", 0)
        self.iron_ore = Materials.Ore("Iron Ore", 0)
        self.silver_ore = Materials.Ore("Silver Ore", 0)
        self.gold_ore = Materials.Ore("Gold Ore", 0)
        self.mithril_ore = Materials.Ore("Mithril Ore", 0)

        self.copper_metal = Materials.Metal("Copper Metal")
        self.bronze_metal = Materials.Metal("Bronze Metal")
        self.iron_metal = Materials.Metal("Iron Metal")
        self.steel_metal = Materials.Metal("Steel Metal")
        self.silver_metal = Materials.Metal("Silver Metal")
        self.gold_metal = Materials.Metal("Gold Metal")
        self.mithril_metal = Materials.Metal("Mithril Metal")