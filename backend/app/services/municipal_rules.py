"""Municipal waste-sorting rules shared by the rules and classify routers."""

DEFAULT_CITY = "berkeley"

MUNICIPAL_RULES: dict[str, dict] = {
    "berkeley": {
        "rules": {
            "compost": "Food scraps, soiled paper, plant trimmings, BPI-certified packaging.",
            "plastic": "Rigid plastics #1-#7, bottles, jugs, tubs. Empty and rinse.",
            "paper": "Clean paper, cardboard, newsprint, magazines.",
            "glass": "Glass bottles and jars only. Rinse clean.",
            "landfill": "Styrofoam, plastic wrap, chip bags, composite packaging.",
        },
        "source_url": "https://berkeleyca.gov/city-services/trash-recycling",
    },
    "san-francisco": {
        "rules": {
            "compost": "Food scraps, plant debris, soiled paper products.",
            "plastic": "Clean rigid plastics, containers, bottles.",
            "paper": "Clean paper, boxes, unsoiled cartons.",
            "glass": "Bottles and jars (any color).",
            "landfill": "Non-recyclable plastics, foil wrap, treated items.",
        },
        "source_url": "https://sfenvironment.org/zero-waste",
    },
    "oakland": {
        "rules": {
            "compost": "Food waste, paper plates, yard trimmings.",
            "plastic": "Plastic bottles, tubs, and jugs.",
            "paper": "Clean mixed paper and cardboard.",
            "glass": "Food and beverage glass containers.",
            "landfill": "Wrappers, styrofoam, non-conforming items.",
        },
        "source_url": "https://www.oaklandrecycles.com/",
    },
}


def normalize_city(city: str | None) -> str:
    """Normalize user input to canonical city slug."""
    if not city or not isinstance(city, str):
        return ""
    # Map both 'san_francisco' and 'San Francisco' to canonical 'san-francisco'
    return city.strip().lower().replace("_", "-").replace(" ", "-")


def list_cities() -> list[str]:
    return list(MUNICIPAL_RULES)


def get_city(city: str) -> dict | None:
    """Return a city's rules and source URL, or None if the city isn't supported."""
    return MUNICIPAL_RULES.get(normalize_city(city))


def get_category_rule(category: str, city: str) -> str | None:
    """Return the city's rule sentence for one category, or None if there isn't one."""
    city_data = get_city(city)
    if city_data is None:
        return None
    return city_data["rules"].get(category)
