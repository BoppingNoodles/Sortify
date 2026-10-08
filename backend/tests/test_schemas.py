import pytest
from pydantic import ValidationError

from backend.app.schemas import (
    ClassifyResponse,
    RuleResponse,
    ScanRecord,
)


def test_valid_classify_response():
    resp = ClassifyResponse(
        item_name="Cardboard Box",
        category="paper",
        confidence=0.88,
    )
    assert resp.category == "paper"
    assert resp.bin_color == "Brown"
    assert resp.bin == "Brown Paper Bin"
    assert resp.disposal_tips is not None
    assert resp.disposal_tips.bin_type == "brown"


def test_classify_response_confidence_bounds():
    with pytest.raises(ValidationError):
        ClassifyResponse(
            item_name="Cup",
            category="compost",
            confidence=1.05,
        )

    with pytest.raises(ValidationError):
        ClassifyResponse(
            item_name="Cup",
            category="compost",
            confidence=-0.01,
        )


def test_classify_response_invalid_category():
    with pytest.raises(ValidationError):
        ClassifyResponse(
            item_name="Unknown Item",
            category="batteries",
            confidence=0.5,
        )


def test_rule_response_validation():
    rule = RuleResponse(
        city="BERKELEY",
        rules={"compost": "Food scraps only"},
        source_url="https://berkeleyca.gov",
    )
    assert rule.city == "berkeley"

    with pytest.raises(ValidationError):
        RuleResponse(
            city="",
            rules={},
            source_url="https://berkeleyca.gov",
        )


def test_scan_record_validation():
    scan = ScanRecord(
        scan_id="scan-123",
        user_id="user-456",
        timestamp="2026-10-07T12:00:00Z",
        category="glass",
        item_name="Glass Jar",
        confidence=0.95,
    )
    assert scan.category == "glass"
    assert scan.bin_color == "Teal"

    with pytest.raises(ValidationError):
        ScanRecord(
            scan_id="scan-123",
            user_id="user-456",
            timestamp="2026-10-07T12:00:00Z",
            category="e-waste",
            item_name="Old Phone",
            confidence=0.95,
        )
