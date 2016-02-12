__author__ = 'Evan'


class BaseItem:
    def __init__(self, resource_requirements):
        self.resource_requirements = dict(resource_requirements)


class Weapon(BaseItem):
    def __init__(self, resource_requirements):
        BaseItem.__init__(self, resource_requirements)


class Ammo(BaseItem):
    def __init__(self, resource_requirements):
        BaseItem.__init__(self, resource_requirements)


class Spear(Weapon):
    def __init__(self):
        resource_requirements = {"Stone": 2, "Wood": 3}
        Weapon.__init__(self, resource_requirements)


class Sword(Weapon):
    def __init__(self):
        resource_requirements = {"Stone": 2, "Wood": 3}
        Weapon.__init__(self, resource_requirements)


class GreatSword(Weapon):
    def __init__(self):
        resource_requirements = {"Stone": 2, "Wood": 3}
        Weapon.__init__(self, resource_requirements)


class Katana(Weapon):
    def __init__(self):
        resource_requirements = {"Stone": 2, "Wood": 3}
        Weapon.__init__(self, resource_requirements)


class Bow(Weapon):
    def __init__(self):
        resource_requirements = {"Stone": 2, "Wood": 3}
        Weapon.__init__(self, resource_requirements)


class Crossbow(Weapon):
    def __init__(self):
        resource_requirements = {"Stone": 2, "Wood": 3}
        Weapon.__init__(self,  resource_requirements)


class Arrow(Ammo):
    def __init__(self):
        resource_requirements = {"Stone": 2, "Wood": 3}
        Ammo.__init__(self, resource_requirements)


class Bucket(BaseItem):
    def __init__(self):
        resource_requirements = {"Stone": 2, "Wood": 3}
        BaseItem.__init__(self, resource_requirements)
