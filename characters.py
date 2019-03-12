import random
import copy

class Characters:
    """Creates a character class.

    Class attributes are used to share objects between characters.
    Class methods are used heavily to perform non instance specific functions.
    Call Characters.check_methods() for a list of all the methods in the class."""

    party = {}
    armory = {}
    inventory = {}
    treasury = 0
    
    def __init__(self, name):
        self.name = name
        self.level = 1
        if len(Characters.party) > 0:
            total = 0
            for member in Characters.party.values():
                total += member.level
            self.level = int(total / len(Characters.party))
        self.exp = 0
        self.exp_count = 0
        self.next_level = (self.level + 1) * 100
        self.exp_needed = self.next_level - self.exp_count
        self.hp = self.level * 100
        self.current_hp = self.hp
        self.mp = self.level * 10
        self.current_mp = self.mp
        self.stats = {"Power": 1,
                      "Toughness": 1,
                      "Magic": 1,
                      "Luck": 1}
        if self.level > 1:
            total = (self.level - 1) * 4
            for num in range(total):
                stat = random.choice([key for key in self.stats])
                for key, val in self.stats.items():
                    if key == stat:
                        self.stats[key] += 1
        self.equipped = {"Weapon": None,
                         "Armor": None,
                         "Accessory": None,}
        self.spells = {"Attack": [],
                       "Restore": [],
                       "Effect": []}
        self.conscious = 1
        self.attack = self.stats["Power"]
        self.defense = self.stats["Toughness"]
        self.magic_defense = self.stats["Magic"] * self.stats["Toughness"]
        Characters.party[self.name] = self
        
    def __repr__(self):
        return f"Characters(\"{self.name}\")"

    def lose_hp(self, hp):
        print("\n{} has lost {} HP!".format(self.name, hp))
        if hp < self.current_hp:
            self.current_hp -= hp
        else:
            self.lose_consciousness()
        
    def restore_hp(self, hp):
        if self.conscious == 1:
            if self.current_hp != self.hp:
                self.current_hp += hp
                if self.current_hp >= self.hp:
                    self.current_hp = self.hp
                    print("\n{}'s HP has been fully restored!".format(self.name))
                else:
                    print("\n{} recovered {} HP!".format(self.name, hp))
            else:
                print(f"\n{self.name} is already at full HP.")
        else:
            print(f"\n{self.name} is unconscious and must first be revived.")
            
    def lose_mp(self, mp):
        print("\n{} used {} MP!".format(self.name, mp))
        self.current_mp -= mp
        if self.current_mp <= 0:
            self.current_mp = 0
            
    def restore_mp(self, mp):
        if self.conscious == 1:
            if self.current_mp != self.mp:
                self.current_mp += mp
                if self.current_mp >= self.mp:
                    self.current_mp = self.mp
                    print("\n{}'s MP has been fully restored!".format(self.name))
                else:
                    print("\n{} recovered {} MP!".format(self.name, mp))
            else:
                print(f"\n{self.name} is already at full MP.")
        else:
            print(f"\n{self.name} is unconscious and must first be revived.")
            
    def lose_consciousness(self):
        if self.conscious == 1:
            self.conscious -= 1
            print("\n{} has lost conscioussness!".format(self.name))
            self.current_hp = 0        
    
    def revive(self):
        if self.conscious == 0:
            print("\n{} has been revived!".format(self.name))
            self.conscious += 1

    def level_up(self):
        self.exp_count -= self.next_level
        self.level += 1        
        self.hp += 100
        self.current_hp += 100
        self.mp += 10
        self.current_mp += 10
        self.next_level = (self.level + 1) * 100
        self.exp_needed = self.next_level - self.exp_count
        print("\n{} has leveled up. Now at level {}".format(self.name, self.level))
        
    def stats_level_up(self):
        choices = []
        stats_picked = []
        num_choices = random.choice(range(4, 5 + int(self.stats["Luck"] / 2)))
        for key, val in self.stats.items():
            if key == "Power":
                choices += [key] * val
            elif key == "Defense":
                choices += [key] * val
            elif key == "Magic":
                choices += [key] * val
            else:
                choices.append(key)
        for num in range(num_choices):
            choice = random.choice(choices)
            stats_picked.append(choice)
            for key, val in self.stats.items():
                if key == choice:
                    self.stats[key] += 1
        if "Power" in stats_picked:
            print("Power + {}".format(stats_picked.count("Power")))
        if "Toughness" in stats_picked:
            print("Toughness + {}".format(stats_picked.count("Toughness")))
        if "Magic" in stats_picked:
            print("Magic + {}".format(stats_picked.count("Magic")))
        if "Luck" in stats_picked:
            print("Luck + {}".format(stats_picked.count("Luck")))
    
    def calculate_attack_defense(self):
        if self.equipped["Weapon"] != None:
            self.attack = self.stats["Power"] * self.equipped["Weapon"].attack
        else: self.attack = self.stats["Power"]
        if self.equipped["Armor"] != None:
            self.defense = self.stats["Toughness"] * self.equipped["Armor"].defense
        else: self.defense = self.stats["Toughness"] 
        self.magic_defense = self.stats["Toughness"] * self.stats["Magic"]
        if self.stats["Power"] < 1:
            if self.equipped["Weapon"] != None:
                self.attack = self.equipped["Weapon"].attack
            else:
                self.attack = 1
        if self.stats["Toughness"] < 1:
            if self.equipped["Armor"] != None:
                self.defense = self.equipped["Armor"].defense
            else:
                self.defense = 1
        if self.stats["Toughness"] < 1 or self.stats["Magic"] < 1:
            self.magic_defense = 1
        
    def add_exp(self, exp):
        self.exp += exp
        self.exp_count += exp
        self.exp_needed = self.next_level - self.exp_count
        while self.exp_count >= self.next_level:
            self.level_up()
            self.stats_level_up()
            self.negative_stats()
            self.calculate_attack_defense()
            
    def equip(self, equipment):
        if equipment.name in Characters.armory:
            if self.equipped[equipment.equip_type] != None:
                self.unequip(equipment.equip_type)
            del self.equipped[equipment.equip_type]
            self.equipped[equipment.equip_type] = equipment
            Characters.armory[equipment.name].remove(equipment)
            if Characters.armory[equipment.name] == []:
                del Characters.armory[equipment.name]
            print("\n{} has equipped {}.".format(self.name, equipment.name))
            for key, val in self.stats.items():
                for key2, val2 in equipment.stats.items():
                    if key == key2:
                        self.stats[key] += equipment.stats[key2]
            pos_stats = {}
            neg_stats = {}
            for k, v in equipment.stats.items():
                if v < 0:
                    neg_stats[k] = abs(v)
                else:
                    pos_stats[k] = v
            stat_list = []
            for k, v in neg_stats.items():
                stat_list.append(k + ": - " + str(v))
            for k, v in pos_stats.items():
                stat_list.append(k + ": + " + str(v))
            stat_list = Characters.stat_sort(stat_list)
            print("\n{}". format("  ".join(stat_list)))
            self.calculate_attack_defense()
            print()
        else:
            print("You don't have any to equip!")

    def full_equip(self, equipment):
        item_stats = {}
        for item in equipment:
            self.equipped[item.equip_type] = item
            Characters.armory[item.name].remove(item)
            if Characters.armory[item.name] == []:
                del Characters.armory[item.name]
            for k, v in item.stats.items():
                if k not in item_stats:
                    item_stats[k] = 0
                item_stats[k] += v
                for key, val in self.stats.items():
                    if k == key:
                        self.stats[key] += v
        equip_list = [v.name for v in list(self.equipped.values())]
        pos_stats = {}
        neg_stats = {}
        for k, v in item_stats.items():
            if v < 0:
                neg_stats[k] = abs(v)
            else:
                pos_stats[k] = v
        stat_list = []
        for k, v in neg_stats.items():
            stat_list.append(k + ": - " + str(v))
        for k, v in pos_stats.items():
            stat_list.append(k + ": + " + str(v))
        stat_list = Characters.stat_sort(stat_list)
        equip_list = [v.name for v in list(self.equipped.values())]
        print("\n{} has equipped the {}, {}, and {}"
              .format(self.name, equip_list[0], equip_list[1], equip_list[2]))
        print("\n{}". format("  ".join(stat_list)))
        self.calculate_attack_defense()
        print()

    def unequip(self, equipment):
        stats_before = copy.copy(self.stats)
        if self.equipped[equipment] != None:
            print("\n{} has unequipped {}.".format(self.name, self.equipped[equipment].name))
            for key, val in self.stats.items():
                for key2, val2 in self.equipped[equipment].stats.items():
                    if key == key2:
                        self.stats[key] -= self.equipped[equipment].stats[key2]
            self.calculate_attack_defense()
            stats_after = copy.copy(self.stats)
            neg_stats = {}
            pos_stats = {}
            for k, v in stats_before.items():
                for key, val in stats_after.items():
                    if k == key and v != val:
                        if v > val:
                            neg_stats[k] = v - val
                        else:
                            pos_stats[k] = val - v
            stat_list = []
            for k, v in neg_stats.items():
                stat_list.append(k + ": - " + str(v))
            for k, v in pos_stats.items():
                stat_list.append(k + ": + " + str(v))
            stat_list = Characters.stat_sort(stat_list)
            print("\n{}".format("  ".join(stat_list)))
            for key, val in self.equipped.items():
                if key == equipment:
                    if val.name not in Characters.armory:
                        Characters.armory[val.name] = []
                    Characters.armory[val.name].append(val)
                    self.equipped[key] = None
            print()
        else:
            print(f"No {equipment} to unequip.")

    def unequip_character(self): 
        stats_before = copy.copy(self.stats)
        print(f"\n{self.name} has been fully unequipped.")
        for key, val in self.equipped.items():
            if val != None:
                if val.name not in Characters.armory:
                    Characters.armory[val.name] = []
                Characters.armory[val.name].append(val)
                self.equipped[key] = None
                for key2, val2 in self.stats.items():
                    for key3, val3 in val.stats.items():
                        if key2 == key3:
                            self.stats[key2] -= val.stats[key3]
        stats_after = copy.copy(self.stats)
        neg_stats = {}
        pos_stats = {}
        for k, v in stats_before.items():
            for key, val in stats_after.items():
                if k == key and v != val:
                    if v > val:
                        neg_stats[k] = v - val
                    else:
                        pos_stats[k] = val - v
        stat_list = []
        for k, v in neg_stats.items():
            stat_list.append(k + ": - " + str(v))
        for k, v in pos_stats.items():
            stat_list.append(k + ": + " + str(v))
        stat_list = Characters.stat_sort(stat_list)
        if len(stat_list) != 0:
            print("\n{}".format("  ".join(stat_list)))
        print()
        self.calculate_attack_defense()
        
    def use_item(self, item):
        if item.name in Characters.inventory:
            Characters.inventory[item.name].remove(item)
            items_left = len(Characters.inventory[item.name])
            print("\n{} used {}.".format(self.name, item.name))
            if "Revives" in item.does:
                self.revive()
            if "Restores" in item.does:
                for key, val in item.affects.items():
                    if key == "HP":
                        self.restore_hp(val)
                    if key == "MP":
                        self.restore_mp(val)
            if "Increases" in item.does:
                stat_list = []
                for key, val in item.affects.items():
                    self.stats[key] += val
                    stat_list.append(key + ": + " + str(val))
                print("\n{}".format("  ".join(stat_list)))
                self.calculate_attack_defense()
            if items_left == 0:
                print(f"\nUsed last {item.name}.")
            elif items_left > 1 and item.name[-1] != "s":
                print("\n{} {}s left.".format(items_left, item.name))
            else:
                print("\n{} {} left.".format(items_left, item.name))
            if Characters.inventory[item.name] == []:
                del Characters.inventory[item.name]
            print()
        else:
            print("You don't have any to use.")
        
    def learn_spell(self, spell):
        pass

    def cast_spell(self, spell):
        pass

    def change_name(self, name):
        print("\n{} changed their name to {}.".format(self.name, name))
        self.name = name

    def check_member(self):
        print(f"\n{self.name}:")
        print("\nLevel {} | {} EXP For Next Level"
            .format(self.level, self.exp_needed))
        conscious = ""
        if self.conscious == 1:
            conscious = "Conscious"
        else:
            conscious = "Unconscious"
        print("\n{} | HP: {}/{} | MP: {}/{}" 
              .format(conscious, self.current_hp, self.hp,
                      self.current_mp, self.mp))
        print("\nPower: {} | Toughness: {} | Magic: {} | Luck: {}"
              .format(self.stats["Power"], self.stats["Toughness"],
                      self.stats["Magic"], self.stats["Luck"]))
        if self.equipped["Weapon"] != None:
            weapon_stats = []
            for key, val in self.equipped["Weapon"].stats.items():
                weapon_stats.append(key + ": " + str(val))
            print("\nWeapon: {} | Attack: {} | {}"
                  .format(self.equipped["Weapon"].name, 
                  self.equipped["Weapon"].attack, "   ".join(weapon_stats)))
        else:
            print("\nWeapon: None")
        if self.equipped["Armor"] != None:
            armor_stats = []
            for key, val in self.equipped["Armor"].stats.items():
                armor_stats.append(key + ": " + str(val))
            print("\nArmor: {} | Defense: {} | Stats: {}"
                  .format(self.equipped["Armor"].name, 
                          self.equipped["Armor"].defense, "   ".join(armor_stats)))
        else:
            print("\nArmor: None")
        if self.equipped["Accessory"] != None:
            accessory_stats = []
            for key, val in self.equipped["Accessory"].stats.items():
                accessory_stats.append(key + ": " + str(val))
            print("\nAccessory: {} | {}"
                   .format(self.equipped["Accessory"].name,
                           "   ".join(accessory_stats)))
        else:
            print("\nAccessory: None")
        print()

    @classmethod
    def distribute_exp(cls, exp):
        print(f"\nGained {exp} EXP.")
        consc_members = [mem for mem in cls.party.values() if mem.conscious == 1]
        for member in consc_members:
            member.add_exp(int(exp / len(consc_members)))

    @classmethod                          
    def add_items(cls, item, num):
        if num > 1:
            if item.name[-1] == "s":
                print("\nRecieved {} {}.".format(num, item.name))
            else:
                print("\nRecieved {} {}s.".format(num, item.name))
        else:
            print("\nRecieved {}.".format(item.name))
        for n in range(num):
            if item.name not in cls.inventory:
                cls.inventory[item.name] = []
            cls.inventory[item.name].append(item)

    @classmethod
    def add_items_list(cls, items):
        print("\nRecieved Items!")
        for item in items:
            if item.name not in cls.inventory:
                cls.inventory[item.name] = []
            cls.inventory[item.name].append(item)
    
    @classmethod       
    def add_equipment(cls, equipment, num):
        if num > 1:
            if equipment.name[-1] == "s":
                print("\nRecieved {} {}.".format(num, equipment.name))
            else:
                print("\nRecieved {} {}s.".format(num, equipment.name))
        else:
            print("\nRecieved {}.".format(equipment.name))
        for n in range(num):
            if equipment.name not in cls.armory:
                cls.armory[equipment.name] = []
            cls.armory[equipment.name].append(equipment)

    @classmethod
    def add_equipment_list(cls, equipment):
        print("\nRecieved Equipment!")
        for item in equipment:
            if item.name not in cls.armory:
                cls.armory[item.name] = []
            cls.armory[item.name].append(item)

    @classmethod
    def add_gp(cls, gp):
        Characters.treasury += gp
        print(f"\nRecieved {gp} GP.")
                              
    @classmethod
    def win_battle(cls, exp, items, equipment, gp):
        cls.distribute_exp(exp)
        cls.add_gp(gp)
        for item in items:
            cls.add_item(item, 1)
        for equip in equipment:
            cls.add_equipment(equip, 1)

    @classmethod
    def unequip_all(cls):
        for member in cls.party.values():
            member.unequip_character()
            
    @classmethod
    def party_item(cls, item):
        if item.name in Characters.inventory:
            cls.inventory[item.name].remove(item)
            if cls.inventory[item.name] == []:
                del cls.inventory[item.name]
            print("\nUsed {}.".format(item.name))
            for member in cls.party.values():
                if "Revives" in item.does:
                    member.revive()
                if "Restores" in item.does:
                    for key, val in item.affects.items():
                        if key == "HP":
                            member.restore_hp(val)
                        if key == "MP":
                            member.restore_mp(val)
                if "Increases" in item.does:
                    for key, val in item.affects.items():
                        member.stats[key] += val
                    member.calculate_attack_defense()
        else:
            print("You don't have any to use.")
        
    @classmethod
    def check_members(cls):
        for member in cls.party.values():
            member.check_member()

    @classmethod
    def check_gp(cls):
        print(f"\nGP: {Characters.treasury}\n")
                
    @classmethod
    def check_weapons(cls):
        print("\nWeapons:")
        weapon_list = []
        for key, val in cls.armory.items():
            if val[0].equip_type == "Weapon":
                weapon_list.append(val)
        weapon_list.sort(key=lambda item: item[0].attack)
        for item in weapon_list:
            neg_stats = {}
            pos_stats = {}
            for k, v in item[0].stats.items():
                if v < 0:
                    neg_stats[k] = abs(v)
                else:
                    pos_stats[k] = v
            stat_list = []
            for k, v in neg_stats.items():
                stat_list.append(k + ": - " + str(v))
            for k, v in pos_stats.items():
                stat_list.append(k + ": + " + str(v))
            stat_list = Characters.stat_sort(stat_list)
            print("\n{}: {} | Attack {} | {}"
                  .format(item[0].name, len(item),
                          item[0].attack, "  ".join(stat_list)))
        if weapon_list == []:
            print("\nNone")
        print()
            
    @classmethod
    def check_armor(cls):
        print("\nArmor:")
        armor_list = []
        for key, val in cls.armory.items():
            if val[0].equip_type == "Armor":
                armor_list.append(val)
        armor_list.sort(key=lambda item: item[0].defense)
        for item in armor_list:
            neg_stats = {}
            pos_stats = {}
            for k, v in item[0].stats.items():
                if v < 0:
                    neg_stats[k] = abs(v)
                else:
                    pos_stats[k] = v
            stat_list = []
            for k, v in neg_stats.items():
                stat_list.append(k + ": - " + str(v))
            for k, v in pos_stats.items():
                stat_list.append(k + ": + " + str(v))
            stat_list = Characters.stat_sort(stat_list)
            print("\n{}: {} | Defense {} | {}"
                  .format(item[0].name, len(item),
                          item[0].defense, "  ".join(stat_list)))
        if armor_list == []:
            print("\nNone")
        print()
    
    @classmethod
    def check_accessories(cls):
        print("\nAccessories:")
        accessory_list = []
        for key, val in cls.armory.items():
            if val[0].equip_type == "Accessory":
                accessory_list.append(copy.copy(val))
        for item in accessory_list:
            weight = 0
            for key, val in item[0].stats.items():
                weight += val
            item.append(weight)
        accessory_list.sort(key=lambda item: item[-1])
        for item in accessory_list:
            neg_stats = {}
            pos_stats = {}
            for k, v in item[0].stats.items():
                if v < 0:
                    neg_stats[k] = abs(v)
                else:
                    pos_stats[k] = v
            stat_list = []
            for k, v in neg_stats.items():
                stat_list.append(k + ": - " + str(v))
            for k, v in pos_stats.items():
                stat_list.append(k + ": + " + str(v))
            stat_list = Characters.stat_sort(stat_list)
            print("\n{}: {} | {}"
                  .format(item[0].name, len(item[:-1]), "  ".join(stat_list)))
        if accessory_list == []:
            print("\nNone")    
        print()
    
    @classmethod
    def check_armory(cls):
        cls.check_weapons()
        cls.check_armor()
        cls.check_accessories()
        
    @classmethod
    def check_items(cls):
        print(f"\nItems:")
        item_list = []
        for key, val in cls.inventory.items():
            item_list.append(copy.copy(val))
        for item in item_list:
            weight = 0
            for key, val in item[0].affects.items():
                weight += val
            item.append(weight)
        item_list.sort(key=lambda item: item[0].does)
        item_list.sort(key=lambda item: item[-1])
        for item in item_list:
            stats = []
            for key, val in item[0].affects.items():
                stats.append(key + ": + " + str(val))
            if len(stats) < 4:
                print("\n{}: {} | {} | {} | {} Use"
                      .format(item[0].name, len(item[:-1]), item[0].does, 
                              "  ".join(stats), item[0].targets))
            else:
                print("\n{}: {} | {} | {}\n{} Use"
                      .format(item[0].name, len(item[:-1]), item[0].does, 
                              "  ".join(stats), item[0].targets))
        if item_list == []:
            print("\nNone")
        print()

    @classmethod
    def check_spellbooks(cls):
        pass
            
    @classmethod
    def check_party(cls):
        cls.check_members()
        cls.check_gp()
        cls.check_armory()
        cls.check_items()
        cls.check_spellbooks()

    @staticmethod
    def stat_sort(lst):
        results = []
        for item in lst:
            if item.startswith("P"):
                results.insert(0, item)
            elif item.startswith("T"):
                results.insert(1, item)
            elif item.startswith("M"):
                results.insert(2, item)
            elif item.startswith("L"):
                results.insert(3, item)
        return results

    @staticmethod
    def check_methods():
        print("\nInstance Methods:")
        print("\nlose_hp(self, hp): Reduces HP")
        print("\nrestore_hp(self, hp): Increases HP")
        print("\nlose_mp(self, mp): Reduces MP")
        print("\nrestore_mp(self, mp): Increases MP")
        print("\nlose_consciousness(self): Causes Unconsciousness")
        print("\nrevive(self): Restores Consciousness")
        print("\nlevel_up(self): Increases Level")
        print("\nstats_level_up(self): Randomly Increases Stats")
        print("\ncalculate_attack_defense(self): Recalculates Attack and Defense")
        print("\nadd_exp(self, exp): Increases EXP and EXP Count")
        print("\nequip(self, equipment): Equips Equipment")
        print("\nfull_equip(self, equipment): Equips a List of Equipment")
        print("\nunequip(self, equipmnet): Unequips Equipment")
        print("\nunequip_character(self): Unequips All Equipment")
        print("\nuse_item(self, item): Uses Item")
        print("\nlearn_spell(self, spell): Adds Spell (in progress)")
        print("\ncast_spell(self, spell): Uses Spell (in prongress)")
        print("\nchange_name(self): Changes Character Name")
        print("\ncheck_member(self): Prints Status of Character\n")
        print("\nClass Methods:")
        print("\ndistribute_exp(cls, exp): Distributes EXP to Party Members")
        print("\nadd_items(cls, item, num): Adds Items to Inventory")
        print("\nadd_items_list(cls, items): Adds a List of Items to Inventory")
        print("\nadd_equipment(cls, equipment, num): Adds Equipment to Armory")
        print("\nadd_equipmnet_list(cls, euqipment): Adds a List of Equipment to Armory")
        print("\nadd_gp(cls, gp): Adds GP to Treasury")
        print("\nwin_battle(cls, exp, items, equipment, gp): Calls Previous 6 Methods")
        print("\nunequip_all(): Unequips All Party Members")
        print("\nparty_item(cls, item): Party Uses an Item")
        print("\ncheck_members(cls): Prints Status of Party")
        print("\ncheck_gp(cls): Prints Amount of GF")
        print("\ncheck_weapons(cls): Prints Weapons")
        print("\ncheck_armor(cls): Prints Armor")
        print("\ncheck_accessories(cls): Prints Accessories")
        print("\ncheck_armory(cls): Prints Complete Armory")
        print("\ncheck_items(cls): Prints Inventory")
        print("\ncheck_spellbook(cls): Prints Spell Books")
        print("\ncheck_party(cls): Calls Previous 8 Methods\n")
        print("\nStatic Methods:")
        print("\nstat_sort(): Used to Sort Stats for Display")         