# Demo scanning guide

Kathleen's campus folder (`data/campus_test`) is not on this machine.
The numbers below are the lab test photos already here, plus three
simulated demo-day changes: a side shadow, dim light, and colored
clutter along the edges. Crumpled campus items were not photographed.

Class order is ImageFolder alphabetical. Index 0 is compost, not paper.
Read `checkpoint["class_names"]`. Do not assume `paper=0`.

Checkpoint: `ml/models/mobilenet_v2.pth`
Photos scored: 453 (skipped unreadable: 0)
Batch size: 16

| condition | mean drop in confidence on the clean prediction |
|---|---:|
| shadow | 1.4% |
| dim | 2.9% |
| clutter | 3.7% |

## Golden demo items

These stayed at or above 90% on the same bin for every condition. The strongest qualifying photo from each bin is taken first, then any open slots are filled by confidence.

“Bring this” is the object in that photo, so a presenter can hold up the same thing.

| bring this | file | bin | clean | shadow | dim | clutter |
|---|---|---|---:|---:|---:|---:|
| basket of fresh vegetables | compost/compost_0150.jpg | compost | 100.0% | 100.0% | 99.9% | 99.9% |
| cardboard shipping box | paper/cardboard37.jpg | paper | 100.0% | 99.9% | 99.9% | 99.7% |
| green glass bottle | glass/glass83.jpg | glass | 99.6% | 99.9% | 99.8% | 99.8% |
| plastic milk jug | plastic/plastic220.jpg | plastic | 99.6% | 99.5% | 99.3% | 98.1% |
| aluminum beverage can | landfill/metal32.jpg | landfill | 99.5% | 99.5% | 99.4% | 99.5% |

Class mix: 1 compost, 1 glass, 1 landfill, 1 paper, 1 plastic.

Every bin has at least one photo at or above 90% under every condition. The threshold was not lowered.

## How to hold the phone

Hold the phone about 8–12 inches away (about a hand's length) on a
plain background. The clutter test paints color on the edges, and
that is the change to avoid at the demo table. Keep the item in the
light. Dim photos lose confidence even when the bin stays the same.
A shadow across half the item does the same. Fill the frame so the
item, not the table, is what the crop sees.

These photos were not rechecked on Caden's or Mong's phones.
