class Items:
    
    inventory = {}
    
    def __init__(self, name, does, affects, targets):
        self.name = name
        self.does = does
        self.affects = affects
        self.targets = targets
        Items.inventory[self.name] = self
        
    def __repr__(self):
        return "Items(\"{}\", \"{}\", {}, {})".format(self.name, 
                                                        self.does, 
                                                        self.affects, 
                                                        self.targets)
        
    @classmethod
    def check_inventory(cls):
        for key, val in cls.inventory.items():
            affects = []
            for key2, val2 in val.affects.items():
                affects.append(key2 + ": + " + str(val2))
            print("\n{}: {} | {} | {} Use" 
                  .format(key, val.does, "  ".join(affects), val.targets))

potion = Items("Potion", "Restores HP", 
               {"HP": 100}, "Single")

power_potion = Items("Power Potion", "Restores HP", 
                     {"HP": 1000}, "Single")

x_potion = Items("Mega Potion", "Restores HP", 
                    {"HP": 10000}, "Single")

party_potion = Items("Party Potion", "Restores HP", 
                     {"HP": 1000}, "Party")

mega_potion = Items("Ultima Potion", "Restores Hp", 
                      {"HP": 10000}, "Party")

ether = Items("Ether", "Restores MP", 
              {"MP": 10}, "Single")

power_ether = Items("Power Ether", "Restores MP", 
                    {"MP": 100}, "Single")

x_ether = Items("Mega Ether", "Restores MP", 
                   {"MP": 1000}, "Single")

party_ether = Items("Party Ether", "Restores MP", 
                    {"MP": 100}, "Party")

mega_ether = Items("Ultima Ether", "Restores MP", 
                     {"MP": 10000}, "Party")

elixir = Items("Elixir", "Restores HP and MP", 
               {"HP": 10000, "MP": 1000}, "Single")

megalixir = Items("Megalixir", "Restores HP and MP", 
                  {"HP": 10000, "MP": 1000}, "Party")

pheonix_feather = Items("Pheonix Feathers", "Revives and Restores HP", 
                        {"HP": 100}, "Single")

angel_feather = Items("Angel Kiss", "Revives and Restores HP", 
                      {"HP": 10000}, "Single")

tiger_fang = Items("Tiger Fang", "Increases Power", 
                   {"Power": 1}, "Single")

dragon_scale = Items("Dragon Scale", "Increases Toughness", 
                     {"Toughness": 1}, "Single")

unicorn_horn = Items("Unicorn Horn", "Increases Magic", 
                     {"Magic": 1}, "Single")

cats_paw = Items("Cats Paw", "Increases Luck", 
                 {"Luck": 1}, "Single")

holy_grail = Items("Holy Grail", "Increases All Stats", 
                   {"Power": 1, "Toughness": 1, "Magic": 1, "Luck": 1}, "Party")