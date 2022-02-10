from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type, Optional
from game.characters import Character
from game.equipment import Weapon, Armor
import random

base_stamina_per_round: float = 0.4


class Hero(ABC):
    def __init__(self, name: str, player_class: Type[Character], weapon=Weapon, armor=Armor):
        self.name = name
        self.player_class = player_class
        self._stamina = player_class.max_stamina
        self._hp = player_class.max_health
        self.weapon = weapon
        self.armor = armor
        self.used_skill: bool = False

    @property
    def hp(self):
        """
        Округление очков здоровья
        """
        return round(self._hp, 1)

    @hp.setter
    def hp(self, value):
        self._hp = value

    @property
    def stamina(self):
        """
        Округление очков выносливости
        """
        return round(self._stamina, 1)

    @stamina.setter
    def stamina(self, value):
        self._stamina = value

    @property
    def total_armor(self) -> float:
        """
        Расчет брони цели (= броня игрока * модификатор брони класса ). Если выносливости достаточно для использования
        брони, возвращаем значение брони, если нет - возвращаем 0.
        """
        if self.stamina - self.armor.stamina_per_turn >= 0:
            return self.armor.defence * self.player_class.armor
        return 0

    def _hit(self, target: Hero) -> Optional[float]:
        """
        Метод нанесения удара.
        Если выносливости для удара недостаточно, возвращаем 0 урона.
        Если выносливости достаточно, то рассчитывается урон атакующего(=урон от оружия * модификатор атаки класса),
        а затем общий урон(=урона атакующего - броня цели). Если общий урон меньше 0, возвращаем 0.
        Вычитаем из очков выносливости кол-во выносливости, которое игрок затратил на удар, и возвращаем значение
        общего урона.
        """
        if self.stamina - self.weapon.stamina_per_hit < 0:
            return None
        hero_damage = self.weapon.damage * self.player_class.attack
        total_damage = hero_damage - target.total_armor
        if total_damage < 0:
            return 0
        self.stamina -= self.weapon.stamina_per_hit
        return round(total_damage, 1)

    def take_hit(self, damage: float):
        """
        Метод для вычета урона из очков здоровья (метод не позволяет очкам здоровья быть отрицательным числом)
        """
        self.hp = round(self.hp, 1)
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def use_skill(self) -> Optional[float]:
        """
        Метод для использования навыка.
        Если у атакующего достаточно выносливости и навык не был использован ранее, возвращаем урон от навыка.
        Если выносливости нет, ничего не возвращаем.
        """
        if self.stamina - self.player_class.skill.stamina and not self.used_skill:
            self.used_skill = True
            return round(self.player_class.skill.damage, 1)
        return None

    def regenerate_stamina(self):
        """
        Метод для регенерации выносливости с использованием константы.
        Если очки выносливости имеют максимальное значение, возвращаем максимальное кол-во выносливости.
        Если нет, высчитываем выносливость с помощью константы.
        """
        delta_stamina = base_stamina_per_round * self.player_class.stamina
        if self.stamina + delta_stamina <= self.player_class.max_stamina:
            self.stamina += delta_stamina
        else:
            self.stamina = self.player_class.max_stamina

    @abstractmethod
    def hit(self, target: Hero) -> Optional[float]:
        pass


class Player(Hero):
    """
    Урон Игрока. Возвращаем урон от обычного удара
    """
    def hit(self, target: Hero) -> Optional[float]:
        return self._hit(target)


class Enemy(Hero):
    def hit(self, target: Hero) -> Optional[float]:
        """
        Урон Соперника.
        Если есть 10% шанс и наличие достаточного кол-ва очков выносливости на использование Соперником навыка,
        возвращаем урон от навыка. Если шанса и выносливости нет, возвращаем урон от обычного удара.
        """
        if random.randint(0, 100) < 10 and self.stamina >= self.player_class.skill.stamina and not self.used_skill:
            self.use_skill()
        return self._hit(target)
