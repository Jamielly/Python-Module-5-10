from abc import ABC, abstractmethod
from typing import Any


class InvalidStrategyError(Exception):
    pass


class BattleStrategy(ABC):

    @abstractmethod
    def is_valid(self, creature: Any) -> bool:
        pass

    @abstractmethod
    def act(self, creature: Any) -> str:
        pass


class NormalStrategy(BattleStrategy):

    def is_valid(self, creature: Any) -> bool:
        return hasattr(creature, "attack")

    def act(self, creature: Any) -> str:
        if not self.is_valid(creature):
            raise InvalidStrategyError(
                f"Invalid Creature '{getattr(creature, 'name', creature)}' "
                f"for normal strategy"
            )
        return creature.attack()


class AggressiveStrategy(BattleStrategy):

    def is_valid(self, creature: Any) -> bool:
        return hasattr(creature, "transform") and hasattr(creature, "revert")

    def act(self, creature: Any) -> str:
        if not self.is_valid(creature):
            name = getattr(creature, "name", str(creature))
            raise InvalidStrategyError(
                f"Invalid Creature '{name}' for this aggressive strategy"
            )
        t_msg = creature.transform()
        a_msg = creature.attack()
        r_msg = creature.revert()
        return f"{t_msg}\n{a_msg}\n{r_msg}"


class DefensiveStrategy(BattleStrategy):

    def is_valid(self, creature: Any) -> bool:
        return hasattr(creature, "heal")

    def act(self, creature: Any) -> str:
        if not self.is_valid(creature):
            name = getattr(creature, "name", str(creature))
            raise InvalidStrategyError(
                f"Invalid Creature '{name}' for this defensive strategy"
            )
        a_msg = creature.attack()
        h_msg = creature.heal()
        return f"{a_msg}\n{h_msg}"
