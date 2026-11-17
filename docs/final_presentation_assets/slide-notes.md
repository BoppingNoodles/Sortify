# Slide-ready notes

| Slide | Copy and visual |
|---|---|
| Sorting by city | A guest photographs a waste item, chooses a city, and gets a suggested bin and preparation guidance. Use the accepted camera and result screenshots. |
| Scan architecture | Expo Camera captures the photo. The app posts the image and city to FastAPI. A bounded worker runs the PyTorch model, and the API combines the prediction with municipal rules. The phone saves successful scan metadata in AsyncStorage. Server guest history is a separate explicit API operation. |
| What the team built | Frontend built the capture, preview, results, and local history flow. Backend built the upload, inference, rules, guest history and stats routes. ML produced trained-checkpoint, calibration, export, and evaluation work. Confirm named credits with the team before final assembly. |
| Evaluation | Show the model identity, dataset name and size, overall and per-class accuracy, and the 300 DPI confusion matrix once the release run is available. If only the historical result is available, title the chart “October 2026 MVP campus evaluation” and describe the historical domain gap. |
| Demo and limits | Play the captioned walkthrough, then explain the app's five categories, the dependence on the city and input image, and the limits of confidence. Keep the local video copy available through the last slide. |

Use the [Week 12 team assignments](../../weekly_assignments/updated_team_weekly_assignments.md#week-12--final-presentation-comprehensive-demo-video--release) and the [asset index](README.md) for final ownership and source links.
