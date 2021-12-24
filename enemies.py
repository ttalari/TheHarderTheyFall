class Enemy:
    def __init__(self, name, hp, damage, experience):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.experience = experience

    def is_alive(self):
        return self.hp > 0


class Gunman(Enemy):
    def __init__(self):
        super().__init__(name="Gunman", hp=10, damage=2, experience=10)


class Gunslinger(Enemy):
    def __init__(self):
        super().__init__(name="Gunslinger", hp=20, damage=10, experience=20)


class Hitman(Enemy):
    def __init__(self):
        super().__init__(name="Gunslinger", hp=20, damage=10, experience=20)


class Django(Enemy):
    def __init__(self):
        super().__init__(name="Django", hp=25, damage=12, experience=30)


class Hawk(Enemy):
    def __init__(self):
        super().__init__(name="Hawk", hp=20, damage=35, experience=10)


class Chief(Enemy):
    def __init__(self):
        super().__init__(name="Chief", hp=15, damage=10, experience=30)


class WildRanger(Enemy):
    def __init__(self):
        super().__init__(name="WildRanger", hp=25, damage=20, experience=30)


class Rodeo(Enemy):
    def __init__(self):
        super().__init__(name="Rodeo", hp=50, damage=20, experience=35)


class Gaucho(Enemy):
    def __init__(self):
        super().__init__(name="Gaucho", hp=30, damage=15, experience=30)


class Outlaw(Enemy):
    def __init__(self):
        super().__init__(name="Outlaw", hp=20, damage=10, experience=20)


class RufusBuck(Enemy):
    def __init__(self):
        super().__init__(name="RufusBuck", hp=75, damage=25, experience=35)
