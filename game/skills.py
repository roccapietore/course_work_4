from dataclasses import dataclass


@dataclass
class Skill:
    name: str
    damage: float
    stamina: float


ferocious_kick = Skill(name="Свирепый пинок", damage=6,  stamina=12)
powerful_thrust = Skill(name="Мощный укол", damage=5, stamina=15)
