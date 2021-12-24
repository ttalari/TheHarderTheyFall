# Base class for all items
class Item():
    # __init__ is the contructor method
    def __init__(self, name, description, value):
        self.name = name  # attribute of the Item class and any subclasses
        self.description = description  # attribute of the Item class and any subclasses
        self.value = value  # attribute of the Item class and any subclasses

    # __str__ method is used to print the object
    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\n".format(self.name, self.description, self.value)


# Extend the Items class
# Gold class will be a child or subclass of the superclass Item


class Gold(Item):
    # __init__ is the contructor method
    def __init__(self, amt):
        self.amt = amt  # attribute of the Gold class
        super().__init__(name="Gold",
                         description="A round coin with {} stamped on the front.".format(str(self.amt)),
                         value=self.amt)


class Weapon(Item):
    def __init__(self, name, description, value, damage):
        self.damage = damage
        super().__init__(name, description, value)

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\nDamage: {}".format(self.name, self.description, self.value, self.damage)


class Tequila(Item):
    def __init__(self, name, description, value, amt, health):
        self.amt = amt
        self.health = health
        super().__init__(name, description, value)

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\nAmt: {} \nHealth: {}".format(self.name, self.description, self.value,
                                                                       self.amt, self.health)


class BronzeTequila(Tequila):
    def __init__(self):
        super().__init__(name="Small Tequila",
                         description="A small Tequila Bottle which restore 15 HP.",
                         value=5,
                         amt=1,
                         health=25)


class SilverTequila(Tequila):
    def __init__(self):
        super().__init__(name="Medium Tequila",
                         description="A medium Tequila Bottle which restore 25 HP.",
                         value=10,
                         amt=1,
                         health=25)


class GoldTequila(Tequila):
    def __init__(self):
        super().__init__(name="Large Tequila",
                         description="A Large Tequila Bottle which restore 25 HP.",
                         value=15,
                         amt=1,
                         health=50)


class Rock(Weapon):
    def __init__(self):
        super().__init__(name="Rock",
                         description="A fist-sized rock, suitable for bludgeoning.",
                         value=0,
                         damage=5)


class Colt(Weapon):
    def __init__(self):
        super().__init__(name="Colt",
                         description="A famous western revolver which could shoot  bullets without reloading.",
                         value=10,
                         damage=10)


class Lasso(Weapon):
    def __init__(self):
        super().__init__(name="Lasso",
                         description="A lasso is the loop of rope that cowboys use to catch cattle.",
                         value=1,
                         damage=1)


class Remington(Weapon):
    def __init__(self):
        super().__init__(name="Remington",
                         description="A medium range Rifle which deals good damage.",
                         value=20,
                         damage=25)


class Derringer(Weapon):
    def __init__(self):
        super().__init__(name="Derringer",
                         description="A mini shotgun which with low range causing more damage than a colt.",
                         value=15,
                         damage=120)


class Winchester(Weapon):
    def __init__(self):
        super().__init__(name="Winchester",
                         description="A long range Rifle which deals more damage and a rarely found Model",
                         value=30,
                         damage=40)
