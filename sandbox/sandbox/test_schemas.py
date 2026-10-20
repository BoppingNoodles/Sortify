from backend.app.schemas.classify import ClassifyResponse, DisposalTip
from pydantic import ValidationError

# 1. Test valid model
sample = ClassifyResponse(
    item_name="Aluminium Can",
    category="metal",
    confidence=0.94,
    bin="blue_recycling",
    disposal_tips=DisposalTip(action="Rinse and crush", bin_type="blue_recycling"),
)
print("SUCCESS: Valid model created:", sample.item_name)

# 2. Test invalid confidence (should be caught by Pydantic)
try:
    bad = ClassifyResponse(
        item_name="Bad Item",
        category="plastic",
        confidence=1.5,  # Invalid: cannot exceed 1.0!
        bin="recycle",
        disposal_tips=DisposalTip(action="Rinse", bin_type="recycle"),
    )
except ValidationError as e:
    print("SUCCESS: Pydantic correctly blocked invalid confidence > 1.0!")