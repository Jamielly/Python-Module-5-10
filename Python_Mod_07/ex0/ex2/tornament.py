#!/usr/bin/env python3

from typing import Any, List, Tuple

from ex0 import AquaFactory, FlameFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory

from ex2 import (
    AggressiveStrategy,
    BattleStrategy,
    DefensiveStrategy,
    InvalidStrategyError,
    NormalStrategy,
)


def run_tournament(
    title: str, opponents: List[Tuple[Any, BattleStrategy]]
) -> None:
    print(f"{title}")
    print(f"*** Tournament *** {len(opponents)} opponents involved")

    competitors = []
    for factory, strategy in opponents:
        creature = factory.create_base()
        competitors.append((creature, strategy))

    for i in range(len(competitors)):
        for j in range(i + 1, len(competitors)):
            c1, strat1 = competitors[i]
            c2, strat2 = competitors[j]

            print("* Battle *")
            print(f"{c1.describe()} vs.")
            print(f"{c2.describe()}")
            print("now fight!")

            try:
                res1 = strat1.act(c1)
                res2 = strat2.act(c2)
                print(res1)
                print(res2)
            except InvalidStrategyError as e:
                print(f"Battle error, aborting tournament: {e}")
                print()
                return

    print()


def main() -> None:
    flame_fact = FlameFactory()
    aqua_fact = AquaFactory()
    heal_fact = HealingCreatureFactory()
    trans_fact = TransformCreatureFactory()

    normal_strat = NormalStrategy()
    aggro_strat = AggressiveStrategy()
    defensive_strat = DefensiveStrategy()

    t0_opponents = [
        (flame_fact, normal_strat),
        (heal_fact, defensive_strat),
    ]
    run_tournament("Tournament 0 (basic)", t0_opponents)

    t1_opponents = [
        (flame_fact, aggro_strat),
        (heal_fact, defensive_strat),
    ]
    run_tournament("Tournament 1 (error)", t1_opponents)

    t2_opponents = [
        (aqua_fact, normal_strat),
        (heal_fact, defensive_strat),
        (trans_fact, aggro_strat),
    ]
    run_tournament("Tournament 2 (multiple)", t2_opponents)


if __name__ == "__main__":
    main()
