import characters
import equipment
import items
import menus

Characters = characters.Characters

initial_equip = [equipment.broad_sword, 
                 equipment.wood_staff, 
                 equipment.cat_claws, 
                 equipment.chain_mail, 
                 equipment.magic_robe, 
                 equipment.cat_fur, 
                 equipment.gauntlet, 
                 equipment.magic_ring, 
                 equipment.cat_ears]

initial_items = [items.potion, 
                 items.potion, 
                 items.potion, 
                 items.potion, 
                 items.potion, 
                 items.ether, 
                 items.ether, 
                 items.ether, 
                 items.ether, 
                 items.ether, 
                 items.pheonix_feather,
                 items.pheonix_feather, 
                 items.pheonix_feather]
 
print("\nSome storyline blah blah blah!")
print("\nIntroducing your first character!")
name = menus.get_name()
char1 = Characters(name)
print("\nSome more storyline blah blah blah!")
print("\nIntroducing your second character!")
name = menus.get_name()
char2 = Characters(name)
print("\nEven more storyline blah blah blah!")
print("\nIntroducing your third character!")
name = menus.get_name()
char3 = Characters(name)
print("\nThe story continues! Time to start the adventure!")
print("\nHere are some things to help you on your quest! ")
menus.prompt()
Characters.add_equipment_list(initial_equip)
Characters.add_items_list(initial_items)
Characters.add_gp(1000)
print("\n\nOh, and here's one more thing you might be able to use. Be careful with it.")
menus.prompt()
Characters.add_equipment(equipment.cursed_ring, 1)
print("\n\nLet's take a look at your party!")
menus.prompt()
print()
Characters.check_members()
while True:
    answer = input("\nWould you like me to help you equip your characters? Yes (y), No (n): ")
    if answer.lower() == "y":
        print()
        char1.full_equip([equipment.broad_sword, equipment.chain_mail, equipment.gauntlet])
        char2.full_equip([equipment.wood_staff, equipment.magic_robe, equipment.magic_ring])
        char3.full_equip([equipment.cat_claws, equipment.cat_fur, equipment.cat_ears])
        print("\nLet's take another look at your party members.")
        menus.prompt()
        print()
        Characters.check_members()
        break
    elif answer.lower() == "n":
        break
    else:
        continue
menus.main_menu()
print("\n\nAnd the characters set off on their adventure!")
print("\nThanks for playing! More coming soon.\n")