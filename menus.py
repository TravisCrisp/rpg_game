import characters
Characters = characters.Characters

def main_menu():
    """The main menu function is called after any game event.

    Allows user to perform a variety of actions, such as check stats,
    use items, or equip armor."""
    
    while True:
        print("\nWhat will you do?")
        choice = input("\nEquip (e), Use Item (i), Check Something (c), done (d): ")
        if choice.lower() == "e":
            equip_menu()
        elif choice.lower() == "i":
            item_menu()
        elif choice.lower() == "c":
            check_menu()
        elif choice.lower() == "d":
            return

def equip_menu():
    char_list = [char for char in Characters.party.keys()]
    while True:
        print("\nWhich character will you equip?")
        print("\n{}".format("     ".join(char_list)))
        choice = input("\nEnter the name of the character. Check Characters (c), Back (b): ")
        if choice in Characters.party:
            who = Characters.party[choice]
            while True:
                print(f"\nWhat will {who.name} do?")       
                choice = input("\nEquip (e), Unequip (u), Back (b): ")
                if choice.lower() == "e":
                    while True:
                        print(f"\nWhat equipment will {who.name} equip?")
                        choice = input("\nEnter the name of the equipment. Check Equipment (c), Back (b): ")
                        if choice.title() in Characters.armory:
                            print()
                            what = Characters.armory[choice.title()][0]
                            who.equip(what)
                            while True:
                                choice = input("\nCheck Character? Yes (y), Continue (c), Done Equipping (d): ")
                                if choice.lower() == "y":
                                    print()
                                    who.check_member()
                                    break
                                elif choice.lower() == "c":
                                    break
                                elif choice.lower() == "d":
        	                        return
                                continue
                            continue
                        elif choice.lower() == "c":
                            print()
                            Characters.check_armory()
                            continue
                        elif choice.lower() == "b":
                            break
                        print("\nYou don't have any to equip.")
                elif choice.lower() == "u":
                    while True:
                        print(f"\nWhich piece of equipment will {who.name} unequip?")
                        choice = input("\nWeapon (w), Armor (a), Accessory (y), All (l), Back (b): ")
                        if choice.lower() in "way":
                            choices = {"w": "Weapon", "a": "Armor", "y": "Accessory"}
                            print()
                            who.unequip(choices[choice])
                            while True:
                                choice = input("\nCheck Character? Yes (y), Continue (c), Done Equipping (d): ")
                                if choice.lower() == "y":
                                    print()
                                    who.check_member()
                                    break
                                elif choice.lower() == "c":
                                    break
                                elif choice.lower() == "d":
                                    return
                        elif choice.lower() == "l":
                            print()
                            who.unequip_character()
                            while True:
                                choice = input("\nCheck Character? Yes (y), Continue (c), Done Equipping (d): ")
                                if choice.lower() == "y":
                                    print()
                                    who.check_member()
                                    break
                                elif choice.lower() == "c":
                                    break
                                elif choice.lower() == "d":
                                    return
                        elif choice.lower() == "b":
                            break
                elif choice.lower() == "b":
                    break
            continue
        elif choice.lower() == "c":
            Characters.check_members()
            continue
        elif choice.lower() == "b":
             break
        print("\nI don't know who that is.")


def item_menu():
    char_list = [char for char in Characters.party.keys()]
    while True:
        print("\nWhich item will you use?")
        choice = input("\nEnter the item name. Check Items (c), Back (b): ")
        if choice.title() in Characters.inventory:
            what = Characters.inventory[choice.title()][0] 
            if what.targets == "Single":
                while True:
                    print("\nWhich character will use {}?".format(what.name))
                    print("\n{}".format("     ".join(char_list)))
                    choice = input("\nEnter the name of the character. Check Characters (c), Back (b): ")
                    if choice in Characters.party:
                        who = Characters.party[choice]
                        print()
                        who.use_item(what)
                        while True:
                            choice = input("\nCheck Character? Yes (y), Continue (c), Done Using Items (d): ")
                            if choice.lower() == "y":
                                print()
                                who.check_member()
                                break
                            elif choice.lower() == "c":
                                break
                            elif choice.lower() == "d":
                                return
                        break
                    elif choice.lower() == "c":
                        Characters.check_members()
                        continue
                    elif choice.lower() == "b":
                        break
                    print("\nI don't know who that is.")
            else:
                Characters.party_item(what)
            continue
        elif choice.lower() == "c":
            print()
            Characters.check_items()
            continue
        elif choice.lower() == "b":
            break
        print("\nYou don't have any to use!")

def check_menu():
    while True:
        print("\nWhat would you like to check?")
        choice = input("\nCharacters (c), GP (g), Equipment (e), Items (i), Back (b): ")
        if choice.lower() in "cgei":
            print()
            check(choice)
        elif choice.lower() == "b":
            break

def check(choice):
    if choice == "c":
        Characters.check_members()
    if choice == "g":
        Characters.check_gp()
    if choice == "e":
        Characters.check_armory()
    if choice == "i":
        Characters.check_items()
    return  

def prompt():
    prompt = input() 
    return

def get_name():
    while True:
        name = input("\nChoose a name for your character: ")
        if len(name) < 1 or name in "  ":
            print("\nYou have to give your character a name!")
            continue
        elif name not in Characters.party:
            return name
        print("\nYou already have a character with that name!")