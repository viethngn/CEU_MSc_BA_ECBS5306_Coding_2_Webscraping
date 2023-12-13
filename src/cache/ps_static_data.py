class PSStaticData:

    def __init__(self, type_chart, abilities, movedex, items, pokedex, learn_sets):
        self.type_chart = type_chart
        self.abilities = abilities
        self.movedex = movedex
        self.items = items
        self.pokedex = pokedex
        self.learn_sets = learn_sets

    def get_pkm_by_code(self, pkm_code):
        return self.pokedex[pkm_code]