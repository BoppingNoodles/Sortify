"""Verification script to test valid and invalid schema instantiations."""

import sys
from pathlib import Path

# Ensure repository root is in python path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from pydantic import ValidationError

from backend.app.models.schemas import (
    ClassificationAlternative,
    ClassifyResponse,
    RuleResponse,
    ScanRecord,
)


def verify_valid_instantiations():
    print("[1/2] Verifying valid models...")
    # 1. Valid ClassifyResponse
    classify = ClassifyResponse(
        item_name="Almond Milk Carton",
        category="compost",
        confidence=0.92,
        location="berkeley",
        alternatives=[ClassificationAlternative(category="landfill", confidence=0.08)],
    )
    assert classify.category == "compost"
    assert classify.bin_color == "Green"
    assert classify.bin == "Green Compost Bin"
    assert classify.disposal_tips is not None
    assert classify.disposal_tips.bin_type == "green"
    print("  [OK] ClassifyResponse valid instantiation verified")

    # 2. Valid RuleResponse
    rule = RuleResponse(
        city="berkeley",
        rules={
            "compost": "Food scraps and food-soiled paper",
            "plastic": "Clean rigid plastics only",
        },
        source_url="https://berkeleyca.gov/city-services/trash-recycling",
    )
    assert rule.city == "berkeley"
    print("  [OK] RuleResponse valid instantiation verified")

    # 3. Valid ScanRecord
    scan = ScanRecord(
        scan_id="scan-001",
        user_id="user-123",
        timestamp="2026-10-07T12:00:00Z",
        category="plastic",
        item_name="Water Bottle",
        confidence=0.98,
    )
    assert scan.category == "plastic"
    assert scan.bin_color == "Blue"
    print("  [OK] ScanRecord valid instantiation verified")


def verify_invalid_instantiations():
    print("[2/2] Verifying invalid models trigger ValidationError...")

    # Case 1: Confidence > 1.0
    try:
        ClassifyResponse(
            item_name="Soda Can",
            category="plastic",
            confidence=1.5,
        )
        raise AssertionError(
            "Failed: Confidence > 1.0 should have raised ValidationError"
        )
    except ValidationError:
        print("  [OK] Confidence > 1.0 rejected as expected")

    # Case 2: Negative confidence
    try:
        ClassifyResponse(
            item_name="Soda Can",
            category="plastic",
            confidence=-0.1,
        )
        raise AssertionError(
            "Failed: Negative confidence should have raised ValidationError"
        )
    except ValidationError:
        print("  [OK] Negative confidence rejected as expected")

    # Case 3: Invalid category not in 5 allowed bins
    try:
        ClassifyResponse(
            item_name="Nuclear Waste",
            category="radioactive",
            confidence=0.99,
        )
        raise AssertionError(
            "Failed: Invalid category should have raised ValidationError"
        )
    except ValidationError:
        print("  [OK] Invalid category rejected as expected")

    # Case 4: Invalid alternative category
    try:
        ClassificationAlternative(category="hazardous", confidence=0.5)
        raise AssertionError(
            "Failed: Invalid alternative category should have raised ValidationError"
        )
    except ValidationError:
        print("  [OK] Invalid alternative category rejected as expected")

    # Case 5: Empty city in RuleResponse
    try:
        RuleResponse(city="   ", rules={}, source_url="http://example.com")
        raise AssertionError("Failed: Empty city should have raised ValidationError")
    except ValidationError:
        print("  [OK] Empty city rejected as expected")


if __name__ == "__main__":
    verify_valid_instantiations()
    verify_invalid_instantiations()
    print("\nAll schema verification checks passed successfully!")
