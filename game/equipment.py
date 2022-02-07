from dataclasses import dataclass
from random import uniform
from typing import List


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self) -> float:
        return round(uniform(self.min_damage, self.max_damage), 1)


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class EquipmentData:
    weapons: List[Weapon]
    armors: List[Armor]

    def get_weapon(self, weapon_name: str) -> Weapon:
        for weapon in self.weapons:
            if weapon == weapon_name:
                return weapon
        raise NameError

    def get_armor(self, armor_name: str) -> Armor:
        for armor in self.armors:
            if armor == armor_name:
                return armor
        raise NameError

    @property
    def get_weapon_names(self) -> List[str]:
        return list(item.name for item in self.weapons)

    @property
    def get_armor_names(self) -> List[str]:
        return list(item.name for item in self.armors)
