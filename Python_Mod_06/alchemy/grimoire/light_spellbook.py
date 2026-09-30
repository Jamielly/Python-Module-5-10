from typing import List
from .light_validator import validate_ingredients


def light_spell_allowed_ingredients() -> List[str]:
    return ["earth", "air", "fire", "water"]


def light_spell_record(spell_name: str, ingredients: str) -> str:
    allowed = light_spell_allowed_ingredients()
    status = validate_ingredients(ingredients, allowed)
    if "VALID" in status:
        return f"Spell recorded: {spell_name} ({ingredients} - VALID)"
    return f"Spell rejected: {spell_name} ({ingredients} - INVALID)"
