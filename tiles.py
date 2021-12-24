import actions
import audio
import enemies
import items
import world


class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def intro_text(self):
        raise NotImplementedError()

    def modify_player(self, player):
        raise NotImplementedError()

    def adjacent_moves(self):
        """Returns all move actions for adjacent tiles."""
        moves = []
        if world.tile_exists(self.x + 1, self.y):
            moves.append(actions.MoveEast())
        if world.tile_exists(self.x - 1, self.y):
            moves.append(actions.MoveWest())
        if world.tile_exists(self.x, self.y - 1):
            moves.append(actions.MoveNorth())
        if world.tile_exists(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        return moves

    def available_actions(self):
        """Returns all of the available actions in this room."""
        moves = self.adjacent_moves()
        moves.append(actions.ViewInventory())
        moves.append(actions.Status())
        moves.append(actions.Heal())
        moves.append(actions.BGM_Play())
        moves.append(actions.BGM_Pause())
        moves.append(actions.Equip())

        return moves


class CaptiveRoom(MapTile):
    # override the intro_text method in the superclass
    def intro_text(self):
        audio.intro('play')
        return """
        
████████╗██╗░░██╗███████╗  ██╗░░██╗░█████╗░██████╗░██████╗░███████╗██████╗░  ████████╗██╗░░██╗███████╗██╗░░░██╗
╚══██╔══╝██║░░██║██╔════╝  ██║░░██║██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗  ╚══██╔══╝██║░░██║██╔════╝╚██╗░██╔╝
░░░██║░░░███████║█████╗░░  ███████║███████║██████╔╝██║░░██║█████╗░░██████╔╝  ░░░██║░░░███████║█████╗░░░╚████╔╝░
░░░██║░░░██╔══██║██╔══╝░░  ██╔══██║██╔══██║██╔══██╗██║░░██║██╔══╝░░██╔══██╗  ░░░██║░░░██╔══██║██╔══╝░░░░╚██╔╝░░
░░░██║░░░██║░░██║███████╗  ██║░░██║██║░░██║██║░░██║██████╔╝███████╗██║░░██║  ░░░██║░░░██║░░██║███████╗░░░██║░░░
░░░╚═╝░░░╚═╝░░╚═╝╚══════╝  ╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚══════╝╚═╝░░╚═╝  ░░░╚═╝░░░╚═╝░░╚═╝╚══════╝░░░╚═╝░░░

███████╗░█████╗░██╗░░░░░██╗░░░░░
██╔════╝██╔══██╗██║░░░░░██║░░░░░
█████╗░░███████║██║░░░░░██║░░░░░
██╔══╝░░██╔══██║██║░░░░░██║░░░░░
██║░░░░░██║░░██║███████╗███████╗
╚═╝░░░░░╚═╝░░╚═╝╚══════╝╚══════╝

Story : 

        11-year-old Nat Love is eating dinner with his parents when Rufus Buck and his associate Cortez arrive. 
        Buck guns down Nat's parents and then carves a cross into his forehead.After slaughtering Nat's Parents, Buck and his gang arrive in their stronghold of Redwood City,
        Twenty years later, Love finds and kills Cortez. Love travels to meet his former lover Mary Fields, who runs a chain of saloons.
        Mary Fields, In a pursuit to expand her business, arrives in Redwood. Knowing that Fields is Nat loves former Lover, Buck takes her prisoner and beats her. Love's gang arrives in redwood,
        and Love joins Fields in captivity to save her life. Love has to escape from captivity, take revenge on Rufus Buck and Leave Redwood to start New Life

        """

    def modify_player(self, player):
        # Room has no action on player
        pass


class Store(MapTile):
    def __init__(self, x, y, item):
        self.item = item
        super().__init__(x, y)

    def add_loot(self, player):
        player.inventory.append(self.item)

    def modify_player(self, player):
        self.add_loot(player)


class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)

    def modify_player(self, the_player):
        if self.enemy.is_alive():
            the_player.hp = the_player.hp - self.enemy.damage
            print("Enemy does {} damage. You have {} HP remaining.".format(self.enemy.damage, the_player.hp))

    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy)]
        else:
            return self.adjacent_moves()


class EmptyTownRoad(MapTile):
    def intro_text(self):
        return """
        Empty part of Town. You must forge onwards.
        """

    def modify_player(self, player):
        # Room has no action on player
        pass


class Church(MapTile):
    def intro_text(self):
        return """
        Another unremarkable part of the cave. You must forge onwards.
        """

    def modify_player(self, player):
        player.hp = player.maxHp
        print(" You have gained {} HP due to gods grace.".format(player.hp))



class Salon(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Gunslinger())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            One of Rufus Buck's Outlaw attacks you
            """
        else:
            return """
            The outlaw that you,ve killed can be found lying on the floor.
            """
    # def __init__(self, x, y):
    #     super().__init__(x, y, items.GoldTequila())

class Ranch(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Outlaw())

    def __init__(self, x, y):
        super().__init__(x, y, enemies.Rodeo())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            One of Rufus Buck's Outlaw attacks you
            """
        else:
            return """
            The outlaw that you,ve killed can be found lying on the floor.
            """


class Barn(EnemyRoom):
    # def __init__(self, x, y):
    #     super().__init__(x, y, items.Winchester())
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Hawk())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            One of Rufus Buck's Outlaw attacks you
            """
        else:
            return """
            The outlaw that you,ve killed can be found lying on the floor.
            """


class Hotel(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Gaucho())

    def intro_text(self):
        if self.enemy.is_alive():

            return """
            One of Rufus Buck's Outlaw attacks you
            """

        else:
            return """
            The outlaw that you,ve killed can be found lying on the floor.
            """
    # def __init__(self, x, y):
    #     super().__init__(x, y, items.SilverTequila())


class Post(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Hitman())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            One of Rufus Buck's Outlaw attacks you
            """
        else:
            return """
            The outlaw that you,ve killed can be found lying on the floor.
            """
    # def __init__(self, x, y):
    #     super().__init__(x, y, items.Remington())


class Bank(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Gunslinger())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            One of Rufus Buck's Outlaw attacks you
            """
        else:
            return """
            The outlaw that you,ve killed can be found lying on the floor.
            """


class Stable(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Chief())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            One of Rufus Buck's Outlaw attacks you
            """
        else:
            return """
            The outlaw that you,ve killed can be found lying on the floor.
            """


class MansionHouse(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.RufusBuck())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
             You are in front of Rufus buck to avenge your parents murder
             """
        else:
            return """
             Rufus Buck can be found lying dead on the Floor.
             """


class Sheriff(Store):
    def __init__(self, x, y):
        super().__init__(x, y, items.Colt())
        super().__init__(x, y, items.Winchester())
        super().__init__(x, y, items.GoldTequila())
        super().__init__(x, y, items.SilverTequila())
        # super().__init__(x, y, items.Tequila())





    def intro_text(self):
        return """
        ░▐█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█▄☆
        ░███████████████████████████████████     	You notice a Shiny Colt Revolver on the Table of the Sheriff.
        ░▓▓▓▓▓▓▓▓▓▓▓▓██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓◤		It's a COLT! You pick it up.
        ╬▀░▐▓▓▓▓▓▓▌▀█░░░█▀░
        ▒░░▓▓▓▓▓▓█▄▄▄▄▄█▀╬░
        ░░█▓▓▓▓▓▌░▒▒▒▒▒▒▒▒▒
        ░▐█▓▓▓▓▓░░▒▒▒▒▒▒▒▒▒
        ░▐██████▌╬░▒▒▒▒▒▒▒▒

        ,______________________________________       
        |_________________,----------._ [____]  ""-,__  __....-----=====
                       (_(||||||||||||)___________/   ""                |
                          `----------'        [ ))"-,  Remington        |
                                               ""    `,  _,--....___    |
                                                    `/           
                                                    
                            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▓▓
                      ██████░░░░██  ░░░░░░░░░░░░░░  ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  ██
                  ████░░░░▒▒▒▒▒▒██░░░░░░░░░░░░░░░░░░██████████████████████████████████████████████████████████████████████████████
              ████░░▒▒▒▒▒▒▒▒▒▒▒▒██▒▒██████▒▒██████▒▒██▒▒▒▒▒▒▒▒░░░░░░▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██  
          ██▓▓▒▒▒▒░░▒▒▒▒▒▒▒▒▒▒▒▒██▒▒▓▓▓▓▓▓▒▒▓▓▓▓▓▓▒▒██▒▒▒▒▒▒▒▒░░░░░░██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██  
        ██░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██████████████████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓                                                            
      ██░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒████  ██        ██        ██████████████                                                              
    ██░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓██████              ██                                                                                    
  ██▒▒░░▒▒▒▒▒▒▒▒▒▒▒▒██▓▓      ▓▓▓▓▓▓▓▓▓▓▓▓██                                                                                      
  ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒██                                                                                                              
  ██▒▒▒▒▒▒▒▒▒▒▒▒██                                                                                                                
    ██▒▒▒▒▒▒▒▒▒▒██                                                                                                                
    ░░▓▓▓▓▓▓▓▓▓▓░░          
    
    
                                                                                                          

        """


class LeaveTown(MapTile):
    def intro_text(self):
        return """
        You feel happiness as you have took revenge upon the person whom you have killed...
        ... at the same moment you feel anger and sadness for Rufus Buck is your own Brother which is revealed by himself before his death.
        ... you can leave the town with Fields and begin a new life in a new town.
_________¶¶¶¶_____________________________________
________¶¶¶¶¶¶1___________________________________
________¶¶¶¶¶¶¶_¶¶¶1______________________________
________¶¶¶¶¶¶¶¶¶¶¶¶¶_____________________________
________¶¶¶¶¶¶_1¶¶¶¶¶¶____________________________
________¶¶¶¶¶¶1¶¶¶¶¶¶¶1___________________________
________¶¶¶¶¶1_¶¶¶¶¶¶¶¶1__________________________
______1¶¶¶¶_1__¶¶¶¶¶¶¶¶¶__________________________
_____¶¶¶¶¶¶1____1¶¶¶¶¶¶¶1_________________________
_____¶¶¶¶¶¶¶1____¶¶¶¶¶¶¶¶_________________________
____1¶¶¶¶¶¶¶¶___¶¶¶¶¶¶¶¶¶_________________________
____1¶¶¶¶¶¶¶¶¶_¶¶¶¶¶¶¶¶¶¶_________________________
_____¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_________________________
_____¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶__________________________
_____¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶1____________________________
______¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_____________________________
______1¶¶¶¶¶¶¶¶¶¶¶¶¶¶_____________________________
_______¶¶¶¶¶¶¶¶¶¶¶¶¶1_____________________________
_______1¶¶¶¶¶¶¶¶¶¶¶¶______________________________
________¶¶¶¶¶¶¶¶¶¶¶¶1_____________________________
_________¶¶¶¶¶¶¶¶¶¶¶¶¶11__________________________
_________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶1________________________
_________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_______________________
_________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶1_____________________
_________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶1___________________
_________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶11________________
_________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_______________
________1¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶1___________
________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶1_________
________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶__1¶¶¶¶¶¶________
_______¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶1______1¶¶¶¶11¶¶___
_______¶¶¶¶¶¶_1¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶__________1¶¶¶¶¶¶__
______¶¶¶¶¶¶1__¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_____________1¶¶¶¶1_
______¶¶¶¶¶¶___1¶¶¶¶¶¶¶¶¶¶¶¶¶¶1______________1¶¶¶¶
_____1¶¶¶¶¶_____¶¶¶¶¶¶¶¶¶¶_¶¶¶¶¶_______________¶¶¶
_____¶¶¶¶¶1_____¶¶¶¶¶¶¶¶1___1¶¶¶¶________________¶
____¶¶¶¶¶¶______¶¶¶¶¶¶1_______¶¶¶1________________
___1¶¶¶¶¶1_____1¶¶¶¶¶_________¶¶¶¶________________
___¶¶¶¶¶¶______¶¶¶¶¶1__________¶¶¶1_______________
___¶¶¶¶¶_______¶¶¶¶¶____________¶¶¶_______________
__1¶¶¶¶¶_______¶¶¶¶¶____________1¶¶_______________
__¶¶¶¶¶________¶¶¶¶¶_____________¶¶1______________
__¶¶¶¶1_______1¶¶¶¶1______________¶¶11____________
_1¶¶¶¶________1¶¶¶¶¶______________¶¶¶¶1___________
_¶¶¶¶¶________1¶¶¶¶1______________1¶¶¶1___________
_¶¶¶¶1________¶¶¶¶¶¶_______________¶¶_1___________

        Victory is yours! and your new life begins
        """

    def modify_player(self, player):
        player.victory = True
