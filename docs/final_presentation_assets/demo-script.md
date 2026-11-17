# Two-minute walkthrough

Record after the candidate passes the [device plan](../../plan/01-device-testing-and-triage.md). Match the video to the candidate's app SHA, verified model checksum, and API environment. The [demo scanning guide](../ml/demo_scanning_guide.md) suggests a cardboard shipping box, green glass bottle, or plastic milk jug. Rehearse the actual item on the release device in even light and check that the selected city's guidance makes sense. The guide's earlier controlled tests are historical.

| Time | Action and narration |
|---|---|
| 0:00–0:15 | Open Sortify as a guest. “Sortify helps me decide which bin to use and shows guidance for my city.” Show Home only after its displayed metrics are verified. |
| 0:15–0:35 | Open Scan, show the city selector, and choose the rehearsed city. “I’m sorting this here, so I’ll use the guidance for this city.” |
| 0:35–0:55 | Frame the rehearsed physical object, capture it, and confirm the preview. Tap Identify Bin once and show the resulting classification. |
| 0:55–1:20 | Point out the actual suggested bin and read the disposal guidance displayed on the device. “The app combines the image prediction with local sorting rules.” |
| 1:20–1:45 | Dismiss the result and open History. Match the new row to the object and timestamp. If guest stats are accepted, show the measured change from the known test baseline. |
| 1:45–2:00 | “We rehearsed this example on this build. The app can misclassify other items, including unfamiliar objects. Check local rules when a suggestion looks wrong.” Use only verified metrics with traceable dataset or guest evidence. |

Add readable captions and keep an offline-playable `Sortify_Demo.mp4` on the presentation machine. Play the full recording disconnected, resume the deck at the ending slide, and rehearse the transition. If a live attempt stalls or returns unsuitable guidance, switch to the verified recording and tell the audience it was recorded on the tested candidate.
