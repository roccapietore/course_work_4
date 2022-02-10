from typing import Optional
from game.hero import Hero


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Game(metaclass=SingletonMeta):
    def __init__(self):
        self.player = None
        self.enemy = None
        self.game_processing = False
        self.game_results = ""

    def run(self, player: Hero, enemy: Hero):
        """
        Запуск игры. Игра идет (game_processing = True)
        """
        self.player = player
        self.enemy = enemy
        self.game_processing = True

    def _check_hp(self) -> Optional[str]:
        """
        Метод, проверяющий очки здоровья.
        Если у Игрока и Соперника не осталось очков здоровья, то никто не выиграл.
        Если у Игрока не осталось очков здоровья, то Игрок проиграл, Соперник выиграл.
        Если у Соперника не осталось очков здоровья, то Игрок выиграл, Соперник проиграл.
        В других случаях - None.
        """
        if self.player.hp <= 0 and self.enemy.hp <= 0:
            return self._end_game(results="Бой окончен, победителя нет")
        elif self.player.hp <= 0:
            return self._end_game(results="Бой окончен, победил Противник!")
        elif self.enemy.hp <= 0:
            return self._end_game(results="Бой окончен, победил Игрок!")
        else:
            return None

    def _end_game(self, results: str) -> str:
        """
        Метод для вывода результатов боя
        """
        self.game_processing = False
        self.game_results = results
        return results

    def next_turn(self) -> str:
        """
        Метод следующего хода.
        Если нет очков здоровья у игроков, выводятся результаты боя, игра заканчивается.
        Если игра не идет, игра заканчивается (game_processing = False), выводятся результаты боя.
        Если есть очки здоровья и игра идет, Игрок принимает удар Соперника, далее регенерируется выносливость игроков,
        выводятся результаты атаки.
        """
        if results := self._check_hp():
            return results
        elif not self.game_processing:
            return self.game_results

        results = self.enemy_hit()
        self._stamina_recovery()
        return results

    def _stamina_recovery(self):
        """
        Метод для регенерации выносливости  Игрока и Соперника (см. hero.py)
        """
        self.player.regenerate_stamina()
        self.enemy.regenerate_stamina()

    def enemy_hit(self) -> str:
        """
        Метод для вывода результатов атаки Соперника
        """
        total_damage: Optional[float] = self.enemy.hit(self.player)
        if total_damage is not None:
            self.player.take_hit(total_damage)
            results = f"{self.enemy.name} наносит {total_damage} урона сопернику."
        else:
            results = f"{self.enemy.name} попытался нанести урон, но у него не хватило выносливости."
        return results

    def player_hit(self) -> str:
        """
        Метод для вывода результатов атаки Игрока
        """
        total_damage: Optional[float] = self.player.hit(self.enemy)
        if total_damage is not None:
            self.enemy.take_hit(total_damage)
            return (f"{self.player.name} наносит {total_damage} урона сопернику."
                    f"{self.next_turn()}")
        return (f"{self.player.name} попытался использовать {self.player.weapon.name}, "
                f"но у него не хватило выносливости."
                f"{self.next_turn()}")

    def use_skill(self) -> str:
        """
        Метод для вывода результатов атаки Игрока с использованием навыка
        """
        total_damage: Optional[float] = self.player.use_skill()
        if total_damage is not None:
            self.enemy.take_hit(total_damage)
            return (f"{self.player.name} наносит {total_damage} урона сопернику."
                    f"{self.next_turn()}")
        return (f"{self.player.name} попытался использовать навык, "
                f"но у него не хватило выносливости. {self.next_turn()}")
