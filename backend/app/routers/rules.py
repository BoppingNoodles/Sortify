"""Rules and municipal waste sorting guidelines router."""

from fastapi import APIRouter, HTTPException, status

from backend.app.models.schemas import RuleResponse

router = APIRouter()

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


@router.get("/rules", response_model=dict)
def get_all_rules():
    """Retrieve supported municipalities for disposal rules."""
    return {
        "supported_cities": list(MUNICIPAL_RULES.keys()),
        "default_city": "berkeley",
    }


@router.get("/rules/{city}", response_model=RuleResponse)
def get_city_rules(city: str):
    """Retrieve waste sorting rules for a specific municipality."""
    city_key = city.strip().lower()
    if city_key not in MUNICIPAL_RULES:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City '{city}' not found. Supported cities: {list(MUNICIPAL_RULES.keys())}",
        )

    city_data = MUNICIPAL_RULES[city_key]
    return RuleResponse(
        city=city_key,
        rules=city_data["rules"],
        source_url=city_data["source_url"],
    )
