# Sortify — AI / ML Subteam Work Plan (Weeks 6–12)

> **Companion Documents:** [updated_team_weekly_assignments.md](updated_team_weekly_assignments.md) | [Starter Code Scaffold](starter_code/updated_ml-ai_code.md)  
> **Repository:** `Sortify`  
> **Subteam:** AI / Machine Learning (Computer Vision)  
> **Branching Convention:** `<type>/ml/<your-name>/<feature-name>` (e.g., `feat/ml/kathleen/dataset-expansion-v2`, `feat/ml/aarav/int8-quantization`)  
> **Key Milestones:** **Week 4** (Mid-Semester Presentation — Completed) & **Week 12** (Final Presentation / Portfolio Release)  

---

## 👥 AI / ML Team Directory

| Member | Role | Focus Areas |
|---|---|---|
| **Kathleen** | ML Engineer | Dataset Acquisition & Curation, Real-World Campus Test Collection, Empirical Confidence Threshold Calibration, Empirical Benchmark Reporting |
| **Max** | ML Engineer | Domain Gap Analysis, Golden Demo Items Identification, Model Retraining Pipeline (v2), ONNX Export & Validation, Presentation Evolution Visuals |
| **Aarav** | ML Engineer | Model Checkpoint Freeze (v1), Dynamic INT8 Model Quantization, Out-of-Distribution Stress Testing, Production Weights Release Packaging |

*(Note: Tasks are managed via a pull-based GitHub Issue ticket system. Below is the sprint backlog of tickets available to claim).*

---

## 📅 Quick Navigation

- [Summary of Completed Weeks 1–4 & Current Week 5 Wrap-Up](#summary-of-completed-weeks-14--current-week-5-wrap-up)
- [Sprint 1: Weeks 6–7 — Dataset Expansion, Model v2 & INT8 Quantization](#sprint-1-weeks-67--dataset-expansion-model-v2--int8-quantization)
- [Sprint 2: Weeks 8–9 — Threshold Calibration, ONNX Export & OOD Testing](#sprint-2-weeks-89--threshold-calibration-onnx-export--ood-testing)
- [Sprint 3: Weeks 10–11 — Presentation Figures, Benchmarks & Release Packaging](#sprint-3-weeks-1011--presentation-figures-benchmarks--release-packaging)
- [Week 12 — 🎤 Final Presentation & Model Showcase](#week-12--final-presentation--model-showcase)
- [AI / ML Sprint Ticket Catalog](#ai--ml-sprint-ticket-catalog)

---

# Summary of Completed Weeks 1–4 & Current Week 5 Wrap-Up

> **Context & Baseline:**
> * **Weeks 1–3:** PyTorch transfer learning setup, dataset aggregation and stratified train/val/test splitting (`split_data.py`), baseline ResNet-18 training, and MobileNetV2 architecture benchmarking.
> * **Week 4 (Mid-Semester Presentation):** Team delivered the mid-semester presentation highlighting baseline model performance (74% baseline ResNet-18 vs. 83% fine-tuned) and training curves.
> * **Week 5 (Current Baseline / In Progress):**
>   - Hyperparameter tuning and freezing initial checkpoint `sortify_mvp_v1.pth` with `classes.json`.
>   - Initial campus benchmark photo collection across Moffitt Library and MLK Union.
>   - Domain gap analysis and identification of 5 "golden demo items" (clean cup, soda can, paper napkin) for live demos.

---

# Sprint 1: Weeks 6–7 — Dataset Expansion, Model v2 & INT8 Quantization

> **Sprint Theme:** Expand training data with challenging real-world campus waste, retrain the computer vision model to resolve confusion points, and compress weights using dynamic quantization.

### 🤖 AI / ML Subteam Resources
* [PyTorch Model Training Best Practices](https://pytorch.org/tutorials/beginner/introyt/trainingyt.html)
* [PyTorch Dynamic Quantization Tutorial](https://pytorch.org/tutorials/recipes/quantization.html)
* [Data Augmentation Techniques in Torchvision](https://pytorch.org/vision/stable/transforms.html)

---

### Ticket: Dataset v2 Expansion (Challenging Campus Trash) & Curation
* **Starter Code Scaffold:** [starter_code/updated_ml-ai_code.md#ticket-dataset-v2-curation](starter_code/updated_ml-ai_code.md#ticket-dataset-v2-curation)
* **Goal & Context:** Gather real campus waste images focused on items that confused the v1 model (crushed aluminum cans, clear plastic iced cups vs. glassware, soiled food wrappers).
* **Action Steps:**
  1. Author `ml/scripts/curate_dataset_v2.py`.
  2. Collect and label 100–150 challenging real-world images from UC Berkeley campus waste stations.
  3. Inspect class distributions to ensure no single category dominates the dataset.
  4. Generate stratified train (70%), validation (15%), and test (15%) splits into `data/processed_v2/`.
* **Verification:** Run script; verify images are correctly placed into category folders and image counts match expected splits.
* **Deliverable & Branch:** `feat/ml/<claimant>/dataset-expansion-v2`

---

### Ticket: Model Retraining Pipeline (v2) & Performance Evaluation
* **Starter Code Scaffold:** [starter_code/updated_ml-ai_code.md#ticket-model-retraining-v2](starter_code/updated_ml-ai_code.md#ticket-model-retraining-v2)
* **Goal & Context:** Fine-tune the backbone on the augmented dataset v2 to improve real-world sorting accuracy.
* **Action Steps:**
  1. Author `ml/scripts/train_v2.py` with data augmentations: random resized crops, horizontal flips, slight rotations, and color jitter.
  2. Train model for 15 epochs using AdamW optimizer and cosine annealing learning rate schedule.
  3. Track validation loss progression and automatically save best checkpoint to `ml/models/sortify_v2.pth`.
  4. Run `evaluate.py` to compare per-class accuracy between v1 and v2 checkpoints.
* **Verification:** Confirm that classification accuracy on weak classes (e.g. soiled paper, clear plastics) improves by at least 7%.
* **Deliverable & Branch:** `feat/ml/<claimant>/model-retraining-v2`

---

### Ticket: Dynamic INT8 Model Quantization & Latency Benchmark
* **Starter Code Scaffold:** [starter_code/updated_ml-ai_code.md#ticket-dynamic-int8-quantization](starter_code/updated_ml-ai_code.md#ticket-dynamic-int8-quantization)
* **Goal & Context:** Reduce model memory footprint and accelerate CPU inference latency for web serving.
* **Action Steps:**
  1. Author `ml/scripts/quantize_model.py`.
  2. Apply `torch.quantization.quantize_dynamic` to convert FP32 linear layer weights to INT8.
  3. Compare file sizes between unquantized (`~45MB`) and quantized (`~12MB`) checkpoints.
  4. Measure mean inference latency across 50 simulated forward passes on CPU.
  5. Confirm that validation accuracy loss is strictly under 1.0%.
* **Verification:** Save quantized weights to `ml/models/sortify_quantized.pth` and log latency improvements.
* **Deliverable & Branch:** `feat/ml/<claimant>/int8-quantization`

---

# Sprint 2: Weeks 8–9 — Threshold Calibration, ONNX Export & OOD Testing

> **Sprint Theme:** Calibrate confidence thresholds to reject ambiguous waste, export models to portable ONNX format, and stress-test robustness against non-trash objects.

### 🤖 AI / ML Subteam Resources
* [PyTorch to ONNX Export Guide](https://pytorch.org/tutorials/advanced/super_resolution_with_onnxruntime.html)
* [Softmax Calibration and Out-of-Distribution Detection](https://arxiv.org/abs/1706.04599)
* [ONNX Runtime Python Documentation](https://onnxruntime.ai/docs/get-started/with-python.html)

---

### Ticket: Empirical Confidence Threshold Calibration
* **Starter Code Scaffold:** [starter_code/updated_ml-ai_code.md#ticket-confidence-threshold-calibration](starter_code/updated_ml-ai_code.md#ticket-confidence-threshold-calibration)
* **Goal & Context:** Balance precision vs. rejection rate so ambiguous images safely trigger an "Uncertain" notice.
* **Action Steps:**
  1. Author `ml/scripts/calibrate_threshold.py`.
  2. Evaluate model confidence score distributions across test set images at 0.40, 0.50, and 0.60 cutoffs.
  3. Calculate precision and false rejection rate for each threshold.
  4. Select the optimal threshold (e.g. 0.50) where items with < 50% confidence return `"uncertain": true` with guidance to check physical bin signs.
  5. Hand off threshold parameters to backend team.
* **Verification:** Verify that clear items pass with high confidence while highly ambiguous photos return uncertain flag.
* **Deliverable & Branch:** `feat/ml/<claimant>/threshold-calibration`

---

### Ticket: PyTorch to ONNX Export & Numerical Parity Verification
* **Starter Code Scaffold:** [starter_code/updated_ml-ai_code.md#ticket-onnx-export--parity-check](starter_code/updated_ml-ai_code.md#ticket-onnx-export--parity-check)
* **Goal & Context:** Export model to vendor-neutral ONNX format for accelerated inference across different deployment environments.
* **Action Steps:**
  1. Author `ml/scripts/export_onnx.py`.
  2. Export PyTorch graph to `ml/models/sortify_v2.onnx` with dynamic batch axes.
  3. Validate exported model structure using `onnx.checker.check_model()`.
  4. Run numerical parity check: compare PyTorch tensor output against ONNX Runtime session output; assert difference < `1e-4`.
* **Verification:** Script executes cleanly and reports parity test passed.
* **Deliverable & Branch:** `feat/ml/<claimant>/onnx-export`

---

### Ticket: Out-of-Distribution & Non-Waste Robustness Testing
* **Starter Code Scaffold:** [starter_code/updated_ml-ai_code.md#ticket-out-of-distribution-stress-test](starter_code/updated_ml-ai_code.md#ticket-out-of-distribution-stress-test)
* **Goal & Context:** Confirm model safety against non-trash objects (hands, faces, laptops, furniture) and extreme lighting.
* **Action Steps:**
  1. Curate a test set of 30 challenging non-waste photos (selfies, keyboards, pets, extreme dark).
  2. Pass images through inference and log predicted categories and confidence scores.
  3. Verify that the calibrated confidence threshold correctly flags these images as uncertain rather than falsely identifying them as trash.
  4. Author `docs/ml/robustness_stress_test.md` summarizing findings.
* **Verification:** Ensure 90%+ of non-trash items fall below the confidence cutoff.
* **Deliverable & Branch:** `docs/ml/<claimant>/robustness-stress-test`

---

# Sprint 3: Weeks 10–11 — Presentation Figures, Benchmarks & Release Packaging

> **Sprint Theme:** Prepare publication-quality visual figures for the final presentation, compile campus empirical accuracy statistics, and freeze final production weights.

### 🤖 AI / ML Subteam Resources
* [Creating High-DPI Publication Figures with Matplotlib](https://matplotlib.org/stable/tutorials/introductory/customizing.html)
* [Model Card Governance Guidelines (Hugging Face / Google)](https://huggingface.co/docs/hub/model-cards)

---

### Ticket: High-Resolution Presentation Visualizer & Model Evolution Charts
* **Starter Code Scaffold:** [starter_code/updated_ml-ai_code.md#ticket-presentation-visualizer](starter_code/updated_ml-ai_code.md#ticket-presentation-visualizer)
* **Goal & Context:** Deliver visual charts illustrating the model's evolution for Google Slides.
* **Action Steps:**
  1. Author `ml/scripts/generate_presentation_charts.py`.
  2. Generate 300 DPI figures:
     - Side-by-side confusion matrices (Baseline ResNet-18 vs. Retrained v2).
     - Training and validation loss curves over 15 epochs.
     - Per-class accuracy comparison bar chart.
  3. Save figures in `docs/final_presentation_assets/`.
* **Verification:** Review exported PNG charts; verify all text labels and numbers are crisp and readable.
* **Deliverable & Branch:** `docs/ml/<claimant>/presentation-charts`

---

### Ticket: Campus Real-World Evaluation Benchmark Report
* **Starter Code Scaffold:** [starter_code/updated_ml-ai_code.md#ticket-campus-benchmark-report](starter_code/updated_ml-ai_code.md#ticket-campus-benchmark-report)
* **Goal & Context:** Compile real-world sorting performance statistics across UC Berkeley campus locations.
* **Action Steps:**
  1. Run inference over the complete campus test photo collection using the final model checkpoint.
  2. Author `data/campus_test/CAMPUS_BENCHMARKS.md`:
     - Overall real-world sorting accuracy (e.g. 86.4%).
     - Per-category breakdown (compost, plastic, paper, glass, landfill).
     - Successes and remaining edge cases (e.g. transparent cold cups).
  3. Deliver summary bullet points to presentation lead.
* **Verification:** Confirm all statistics are backed by reproducible evaluation runs.
* **Deliverable & Branch:** `data/campus_test/CAMPUS_BENCHMARKS.md`

---

### Ticket: Production Checkpoint Packaging & ML Reproduction Guide
* **Starter Code Scaffold:** [starter_code/updated_ml-ai_code.md#ticket-release-packaging-script](starter_code/updated_ml-ai_code.md#ticket-release-packaging-script)
* **Goal & Context:** Package release weights and author reproduction instructions for open-source showcase.
* **Action Steps:**
  1. Author `ml/scripts/package_release.py`.
  2. Copy best weights to `ml/models/release_v1/sortify_final.pth` and compute SHA-256 checksum.
  3. Author `ml/README.md`:
     - Dataset description and split numbers.
     - Exact training command: `python ml/scripts/train_v2.py`.
     - Evaluation command: `python ml/scripts/evaluate.py`.
     - Quantization command: `python ml/scripts/quantize_model.py`.
* **Verification:** Clone repository in a fresh directory; verify `ml/README.md` instructions execute cleanly.
* **Deliverable & Branch:** `docs/ml/<claimant>/release-packaging`

---

# Week 12 — 🎤 Final Presentation & Model Showcase

> **All-Hands Effort:** Support final presentation with computer vision metrics and demonstrate live physical scanning.

### Ticket: Final Model Showcase & Metrics Presentation
* **Tasks:**
  1. **Presentation Slides:** Co-author the AI / Computer Vision architecture slides, displaying the confusion matrix, accuracy progression, and campus testing results.
  2. **Golden Demo Items:** Provide physical sample items (clean coffee cup, crumpled napkin, aluminum can) for demo recording and the live presentation.
  3. **Repository Release Review:** Ensure all model weights and docs are properly tracked and merged to `main`.
* **Deliverable:** Final presentation slides, campus benchmark statistics, and clean ML repository release.

---

## 📊 AI / ML Sprint Ticket Catalog

| Sprint | Weeks | Ticket / Task | Focus & Primary Deliverable |
|---|---|---|---|
| **Sprint 1** | Weeks 6–7 | Dataset v2 Expansion (Challenging Trash) | Curated dataset split v2 with balanced weak classes |
| **Sprint 1** | Weeks 6–7 | Model Retraining Pipeline v2 | Fine-tuned `sortify_v2.pth` with error reduction |
| **Sprint 1** | Weeks 6–7 | Dynamic INT8 Model Quantization Experiment | Quantized `sortify_quantized.pth` & benchmark log |
| **Sprint 2** | Weeks 8–9 | Empirical Confidence Threshold Calibration | Calibrated threshold parameter & trade-off analysis |
| **Sprint 2** | Weeks 8–9 | PyTorch to ONNX Export & Parity Verification | Verified `sortify_v2.onnx` artifact & export script |
| **Sprint 2** | Weeks 8–9 | Out-of-Distribution Non-Waste Stress Testing | Robustness test report on non-trash images |
| **Sprint 3** | Weeks 10–11 | Presentation Figures & Loss Curves Visualizer | High-res 300 DPI loss curves & confusion matrices |
| **Sprint 3** | Weeks 10–11 | Campus Real-World Evaluation Benchmark | Empirical campus testing report (`CAMPUS_BENCHMARKS.md`) |
| **Sprint 3** | Weeks 10–11 | Production Weights Packaging & ML README | Frozen weights archive, checksums & reproduction docs |
| **Week 12** | Week 12 | Final Model Showcase & Metrics Presentation | Slides visuals, demo support & final model archive |
