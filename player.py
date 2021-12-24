import random
#from importlib import util

import audio
import items
import world


class Player():
    def __init__(self):
        self.inventory = [items.Gold(15), items.Lasso(), items.Rock(),items.Colt(),items.GoldTequila(),items.SilverTequila]  # Inventory on startup
        self.hp = 100  # Health Points
        self.maxHp = 200
        self.location_x, self.location_y = world.starting_position  # (0, 0)
        self.victory = False  # no victory on start up
        self.experience = 0
        self.level = 1
        self.money = 10
        self.attackPower = 100
        self.nextLevelUp = 10
        self.chosenWpn = None
        self.armor = False
        self.armorHits = 0
        self.currentWpn = self.inventory[1]

    def status(self):
        print("You are level {} \n".format(self.level))
        print(" * Current HP: {} /".format(self.hp), "{}\n".format(self.maxHp))
        print(" * Attack Power: {} \n".format(self.attackPower))
        print(" * Total XP: {} /".format(self.hp), "{}\n".format(self.maxHp))
        print(" * XP until next level up: {} XP\n".format(self.nextLevelUp - self.experience))

    def Music_Play(self):
        audio.intro('play')

    def Music_Pause(self):
        audio.intro('pause')

    def flee(self, tile):
        """Moves the player randomly to an adjacent tile"""
        available_moves = tile.adjacent_moves()
        r = random.randint(0, len(available_moves) - 1)
        self.do_action(available_moves[r])

    # is_alive method
    def is_alive(self):
        return self.hp > 0  # Greater than zero value then you are still alive

    def print_inventory(self):
        for item in self.inventory:
            print(item, '\n')

    def move(self, dx, dy):
        self.location_x += dx
        self.location_y += dy
        print(world.tile_exists(self.location_x, self.location_y).intro_text())

    def move_north(self):
        self.move(dx=0, dy=-1)

    def move_south(self):
        self.move(dx=0, dy=1)

    def move_east(self):
        self.move(dx=1, dy=0)

    def move_west(self):
        self.move(dx=-1, dy=0)

    def attack(self, enemy):
        best_weapon = None
        max_dmg = 0
        for i in self.inventory:
            if isinstance(i, items.Weapon):
                if i.damage > max_dmg:
                    max_dmg = i.damage
                    best_weapon = i

        print("You use {} against {}!".format(best_weapon.name, enemy.name))
        enemy.hp -= best_weapon.damage
        if not enemy.is_alive():
            print("You killed {}!".format(enemy.name))
        else:
            print("{} HP is {}.".format(enemy.name, enemy.hp))

    def do_action(self, action, **kwargs):
        action_method = getattr(self, action.method.__name__)
        if action_method:
            action_method(**kwargs)

    def equip(self):
        print("\n These are the weapons you currently posses.\n")

        weapons_list = []
        for item in self.inventory:
            if isinstance(item, items.Weapon):
                weapons_list.append(item)
        i = 1
        for weapon in weapons_list:
            print(i, ". ", weapon.name, sep='')
            i += 1

        while True:

            itemChoice = int(input("""\n Select the Weapon you want to equip: """)) -1

            if itemChoice not in range(0, len(weapons_list)):
                print("\n Invalid Weapon Choice")
                audio.no()
                continue
            break
        print('\n')
        print(weapons_list[itemChoice].name, "equipped.\n")
        self.currentWpn = weapons_list[itemChoice]

    def heal(self):
        print("\n These are the Tequilas you currently posses.\n")

        potion_list = []
        for potion in self.inventory:
            if isinstance(potion, items.Tequila):
                if potion.amt <= 0:
                    self.inventory.remove(potion)
                else:
                    potion_list.append(potion)
        i = 1
        for potion in potion_list:
            print(i, ". ", potion.name, sep='')
            i += 1

        while True:
            if len(potion_list) == 0:
                print("You have no potions.")
                #pause()
                return None

            itemChoice = int(print("""\n Select a Tequila: """)) - 1

            if itemChoice not in range(0, len(potion_list)):
                print("\n Invalid Choice")
                audio.no()
                continue
            break

        self.healToPlayer(itemChoice, potion_list)

    def healToPlayer(self, itemChoice, potionList):
        chosen_potion = potionList[itemChoice]
        print("\n You Were Healed for {} ".format(chosen_potion.health))
        print("hp. \n")
        self.hp = self.hp + chosen_potion.health
        chosen_potion.amt = chosen_potion.amt - 1
        if chosen_potion.amt == 0:
            self.inventory.remove(chosen_potion)
        audio.drink()
        #util.pause()
        if self.maxHp < self.hp:
            self.hp = self.maxHp
