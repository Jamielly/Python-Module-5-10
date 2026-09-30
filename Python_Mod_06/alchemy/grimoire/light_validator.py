from typing import List, Optional


def validate_ingredients(
    ingredients: str, allowed: Optional[List[str]] = None
) -> str:
    if allowed is None:
        allowed = ["earth", "air", "fire", "water"]

    ing_lower = ingredients.lower()
    for item in allowed:
        if item.lower() in ing_lower:
            return "VALID"
    return "INVALID"
