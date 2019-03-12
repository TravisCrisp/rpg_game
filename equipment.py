class Equipment:
    
    armory = {"Weapons": [],
              "Armor": [],
              "Accessories": []}
    
    def __init__(self, name, equip_type, stats):
        self.name = name
        self.equip_type = equip_type
        self.stats = stats
    
    @classmethod
    def check_armory(cls):
        for key, val in cls.armory.items():
            if key == "Weapons":
                print(f"\n{key}:\n________\n")
                for item in val:
                    print(f"{item}")
            elif key == "Armor":
                print(f"\n{key}:\n______\n")
                for item in val:
                    print(f"{item}")
            else:
                print(f"\n{key}:\n____________\n")
                for item in val:
                    print(f"{item}")
                    
class Weapons(Equipment):

    weapons = {}
    
    def __init__(self, name, equip_type, stats, attack):
        super().__init__(name, equip_type, stats)
        self.attack = attack
        Equipment.armory["Weapons"].append(self)
        Weapons.weapons[self.name] = self
        
    def __repr__(self):
        return "Weapons(\"{}\", \"{}\", {}, {})".format(self.name, 
                                                        self.equip_type, 
                                                        self.stats, 
                                                        self.attack)
        
    @classmethod
    def check_weapons(cls):
        for key, val in cls.weapons.items():
            stats = []
            for key2, val2 in val.stats.items():
                stats.append(key2 + ": " + str(val2))
            print("\n{} | Attack: {} | Stats: {}"
                  .format(key, val.attack, "  ".join(stats)))

class Armor(Equipment):
    
    armor = {}
    
    def __init__(self, name, equip_type, stats, defense):
        super().__init__(name, equip_type, stats)
        self.defense = defense
        Equipment.armory["Armor"].append(self)
        Armor.armor[self.name] = self
        
    def __repr__(self):
        return "Armor(\"{}\", \"{}\", {}, {})".format(self.name, 
                                                        self.equip_type, 
                                                        self.stats, 
                                                        self.defense)

    @classmethod
    def check_armor(cls):
        for key, val in cls.armor.items():
            stats = []
            for key2, val2 in val.stats.items():
                stats.append(key2 + ": " + str(val2))
            print("\n{} | Defense: {} | Stats: {}"
                  .format(key, val.defense, "  ".join(stats)))
            
class Accessories(Equipment):
    
    accessories = {}
    
    def __init__(self, name, equip_type, stats):
        super().__init__(name, equip_type, stats)
        Equipment.armory["Accessories"].append(self)
        Accessories.accessories[self.name] = self
        
    def __repr__(self):
        return "Weapons(\"{}\", \"{}\", {})".format(self.name, 
                                                        self.equip_type, 
                                                        self.stats)
        
    @classmethod
    def check_accessories(cls):
        for key, val in cls.accessories.items():
            stats = []
            for key2, val2 in val.stats.items():
                stats.append(key2 + ": " + str(val2))
            print("\n{} | Stats: {}"
                  .format(key, "  ".join(stats)))

broad_sword = Weapons("Broad Sword", "Weapon", {"Power": + 2}, 8)

wood_staff = Weapons("Wood Staff", "Weapon", {"Toughness": + 2, 
                                              "Magic": + 4}, 4)

cat_claws = Weapons("Cat Claws", "Weapon", {"Power": + 1, 
                                            "Toughness": + 1, 
                                            "Magic": + 2,
                                            "Luck": + 2}, 6)

chain_mail = Armor("Chain Mail", "Armor", {"Toughness": + 2}, 8)

magic_robe = Armor("Magic Robe", "Armor", {"Toughness": + 4,
                                           "Magic": + 2}, 4)

cat_fur = Armor("Cat Fur", "Armor", {"Power": + 2, 
                                     "Toughness": + 2, 
                                     "Magic": + 1,
                                     "Luck": + 1}, 6)

gauntlet = Accessories("Gauntlet", "Accessory", {"Power": + 3, 
                                               "Toughness": + 2})

magic_ring = Accessories("Magic Ring", "Accessory", {"Toughness": + 1,
                                                   "Magic": + 2,
                                                   "Luck": + 2})

cat_ears = Accessories("Cat Ears", "Accessory", {"Magic": + 2, 
                                               "Luck": + 3})

cursed_ring = Accessories("Cursed Ring", "Accessory", {"Power": - 10, 
                                                               "Toughness": - 10, 
                                                               "Magic": - 10,
                                                               "Luck": + 10})