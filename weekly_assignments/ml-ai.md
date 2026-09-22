# Sortify — AI / ML Subteam Weekly Work Plan (Weeks 1–12)

> **Companion Documents:** [IMPLEMENTATION_PLAN.md](../IMPLEMENTATION_PLAN.md) | [TEAM_WEEKLY_ASSIGNMENTS.md](../TEAM_WEEKLY_ASSIGNMENTS.md)  
> **Repository:** `Sortify`  
> **Branching Convention:** `<type>/ml/<your-name>/<feature-name>` (e.g., `feat/ml/aarav/resnet-training`, `feat/ml/kathleen/data-split`)  
> **Key Milestones:** **Week 6** (Mid-Semester Presentation / Recorded Video Demo) & **Week 12** (Final Presentation / Portfolio Release)  

---

## 👥 AI / ML Team Roster & Roles

| Member | Primary Focus Area |
|---|---|
| **Aarav** | Model Architecture (ResNet-18), Transfer Learning Pipeline, Fine-Tuning & Quantization |
| **Kathleen** | Dataset Acquisition, Curation, Data Splitting, Model Logging & Campus Testing Benchmarks |
| **Max** | Image Preprocessing, Baseline Training, ONNX Export, Comparative Model Evaluation |
| **Doil** | Exploratory Data Analysis (EDA), Confusion Matrices, Model Cards, Retraining Docs & Wrap-Up |

---

## 📅 Quick Navigation

- [Week 1 — Setup, Onboarding & Learning Exercises](#week-1--setup-onboarding--learning-exercises)
- [Week 2 — Design, Architecture & Data Preparation](#week-2--design-architecture--data-preparation)
- [Week 3 — Foundation Building & Scaffolding](#week-3--foundation-building--scaffolding)
- [Week 4 — Core MVP Build (Part 1: Model & API Integration)](#week-4--core-mvp-build-part-1-model--api-integration)
- [Week 5 — Core MVP Build (Part 2: Rules Engine & Demo Hardening)](#week-5--core-mvp-build-part-2-rules-engine--demo-hardening)
- [Week 6 — 🎤 Mid-Semester Presentation (Recorded Video Demo)](#week-6--mid-semester-presentation-recorded-video-demo)
- [Week 7 — Authentication & User Accounts](#week-7--authentication--user-accounts)
- [Week 8 — Engagement Tracker, Streaks & Gamification](#week-8--engagement-tracker-streaks--gamification)
- [Week 9 — System Integration Testing & Robustness](#week-9--system-integration-testing--robustness)
- [Week 10 — Production Hardening & UX Polish](#week-10--production-hardening--ux-polish)
- [Week 11 — Stretch Goals & Deployment](#week-11--stretch-goals--deployment)
- [Week 12 — 🎤 Final Presentation & Portfolio Release](#week-12--final-presentation--portfolio-release)
- [Individual 12-Week Trajectory Matrix](#individual-12-week-trajectory-matrix)

---
# Week 1 — Setup, Onboarding & Learning Exercises

> **Theme:** Get everyone on the same page. Install dev tools, configure local environments, and have every member complete their subteam's standardized hands-on learning exercise.
>
> > [!IMPORTANT]
> > **Standardized Learning Exercises:** In Week 1, all members of each subteam complete the **exact same learning exercise** on their personal machines to establish a common baseline of technical confidence before feature specialization begins in Week 2.

---

---

### 🤖 AI / ML Subteam (PyTorch & Transfer Learning)

> **Shared Learning Exercise & Objective:**  
> Work through a PyTorch transfer learning tutorial on sample data:
> 1. Load a pretrained ResNet-18 model from `torchvision.models`.
> 2. Replace the final classification layer to output 5 classes (paper, plastic, glass, compost, landfill).
> 3. Train it on a tiny sample dataset (50 images) for 2–3 epochs.
> 4. Run inference on a single test image and print the predicted class and confidence probability.

**Shared Subteam Resources:**
* [PyTorch Deep Learning 60-Minute Blitz](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html)
* [PyTorch Transfer Learning Tutorial](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)
* [torchvision.models Official Documentation](https://pytorch.org/vision/stable/models.html)
* [PyTorch Training a Classifier (CIFAR-10 Example)](https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html)
* [PyTorch Real-Time Inference Guidelines](https://pytorch.org/tutorials/intermediate/realtime_rpi.html)
* [JupyterLab Documentation](https://jupyterlab.readthedocs.io/en/stable/)

* **Aarav**
  * **Task:** PyTorch environment setup & complete AI/ML Transfer Learning exercise.
  * **Goal & Context:** Establish local GPU/MPS/CPU training capability and understand fine-tuning head replacement.
  * **Action Steps:**
    1. Install Python 3.10+, PyTorch (`torch`), `torchvision`, `torchaudio`, and `jupyterlab`. Check device availability (`torch.cuda.is_available()` or `torch.backends.mps.is_available()`).
    2. Create a Jupyter notebook `notebooks/week1_transfer_learning.ipynb`.
    3. Load pretrained ResNet-18: `weights = torchvision.models.ResNet18_Weights.DEFAULT; model = torchvision.models.resnet18(weights=weights)`.
    4. Freeze backbone parameters: `for param in model.parameters(): param.requires_grad = False`.
    5. Replace `model.fc = nn.Linear(model.fc.in_features, 5)`.
    6. Train on a tiny toy folder of 50 sample images using CrossEntropyLoss and Adam optimizer for 2 epochs.
    7. Run single-image inference and print predicted class and softmax probability.
  * **Verification:** Run notebook end-to-end without errors; attach terminal/notebook screenshot showing decreasing loss and single-image prediction in PR.
  * **Deliverable & Branch:** `feat/ml/aarav/week1-transfer-learning-exercise`.

* **Kathleen**
  * **Task:** PyTorch environment setup & complete AI/ML Transfer Learning exercise.
  * **Goal & Context:** Master PyTorch Dataset/DataLoader pipeline and model fine-tuning mechanics.
  * **Action Steps:**
    1. Set up PyTorch, torchvision, and JupyterLab environment.
    2. Create `notebooks/week1_transfer_learning.ipynb` and implement torchvision ImageFolder dataloader with Resize and ToTensor transforms.
    3. Load ResNet-18, replace fc layer with 5 output units.
    4. Execute training loop for 2 epochs, printing batch loss every 5 steps.
    5. Pass an arbitrary test image through `torch.softmax(model(img), dim=1)` and print top category name.
  * **Verification:** Confirm loss calculation works properly and attach inference test output to PR.
  * **Deliverable & Branch:** `feat/ml/kathleen/week1-transfer-learning-exercise`.

* **Max**
  * **Task:** PyTorch environment setup & complete AI/ML Transfer Learning exercise.
  * **Goal & Context:** Learn PyTorch tensor operations, device handling (CPU vs GPU), and classification evaluation.
  * **Action Steps:**
    1. Set up PyTorch dev environment with JupyterLab.
    2. Implement transfer learning script replacing ResNet-18 classifier head with 5 classes.
    3. Ensure tensors and model are properly moved to target device (`device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')`).
    4. Run training for 2–3 epochs on sample images; verify backpropagation executes cleanly (`loss.backward()` and `optimizer.step()`).
    5. Test inference with a test image and verify output probabilities sum to 1.0.
  * **Verification:** Log epoch training loss and verify softmax probability distribution across the 5 classes.
  * **Deliverable & Branch:** `feat/ml/max/week1-transfer-learning-exercise`.

* **Doil**
  * **Task:** PyTorch environment setup & complete AI/ML Transfer Learning exercise.
  * **Goal & Context:** Familiarize with model inspection, parameter counts, and output classification logits.
  * **Action Steps:**
    1. Set up PyTorch and JupyterLab; verify library versions in terminal.
    2. Load pretrained ResNet-18; inspect layers and print total trainable vs frozen parameters.
    3. Modify final linear layer to output 5 waste categories.
    4. Run 2 training epochs on sample dataset; compute simple training accuracy.
    5. Test single-image prediction and format output as a clean dictionary `{ "predicted_class": "plastic", "confidence": 0.82 }`.
  * **Verification:** Run notebook cleanly from top to bottom; save output showing sample prediction dictionary and commit to branch.
  * **Deliverable & Branch:** `feat/ml/doil/week1-transfer-learning-exercise`.

---
# Week 2 — Design, Architecture & Data Preparation

> **Theme:** High-fidelity UI mockups, API contracts, system architecture, and dataset curation.

---

### 🤖 AI / ML Subteam
* **Aarav**
  * **Task:** Download and assemble composite waste classification dataset.
  * **Goal & Context:** Aggregate real-world waste images from public datasets and map disparate labels to our 5 target classes.
  * **Action Steps:**
    1. Download TrashNet and Kaggle waste datasets into `data/raw/`.
    2. Create `ml/scripts/remap_classes.py` that parses dataset metadata and remaps raw classes (e.g. `cardboard` → `paper`, `organic` → `compost`, `metal` → `landfill/recycling`) into the 5 target categories: **paper, plastic, glass, compost, landfill**.
    3. Inspect corrupted images and remove 0-byte or unreadable files.
    4. Save organized dataset into `data/interim/`.
  * **Verification:** Run script and verify directory contains 5 clean class folders with balanced sample distribution.
  * **Deliverable & Branch:** `feat/ml/aarav/dataset-aggregation`.

* **Kathleen**
  * **Task:** Build train / validation / test partitioning script.
  * **Goal & Context:** Ensure reproducible, stratified data splits across train, validation, and test datasets.
  * **Action Steps:**
    1. Create `ml/scripts/split_data.py` taking `--input_dir` and `--output_dir` arguments.
    2. Split dataset with a strict 70% Train, 15% Validation, 15% Test ratio.
    3. Implement stratified sampling to ensure equal class proportions across all three splits.
    4. Use a fixed deterministic random seed (`seed=42`) for reproducibility.
    5. Organize output directory structure: `data/processed/{train,val,test}/{paper,plastic,glass,compost,landfill}`.
  * **Verification:** Print file counts per class in train, val, and test splits to verify exact 70/15/15 distribution.
  * **Deliverable & Branch:** `feat/ml/kathleen/data-split-script`.

* **Max**
  * **Task:** Build image preprocessing pipeline.
  * **Goal & Context:** Normalize images to prevent training instability and optimize input dimensions for ResNet.
  * **Action Steps:**
    1. Implement `ml/scripts/preprocess.py` using Pillow and torchvision.
    2. Validate image file integrity (check for truncated files using `Image.verify()`).
    3. Resize images to standard 224×224 pixels with bilinear interpolation.
    4. Convert all images (grayscale, RGBA) to standard 3-channel RGB.
    5. Log any skipped or corrupted images with detailed warnings.
  * **Verification:** Run preprocessing on 100 sample images; verify all output images have shape `(224, 224, 3)` and open without warnings.
  * **Deliverable & Branch:** `feat/ml/max/data-preprocessing`.

* **Doil**
  * **Task:** Exploratory Data Analysis (EDA) notebook.
  * **Goal & Context:** Uncover class imbalances, resolution anomalies, and guide augmentation strategies.
  * **Action Steps:**
    1. Create Jupyter notebook `ml/notebooks/exploration.ipynb`.
    2. Load image counts per category and generate a clean Matplotlib/Seaborn bar chart of class distribution.
    3. Calculate image resolution distribution (aspect ratio, width/height variance).
    4. Document potential data biases (e.g. clean studio backgrounds vs cluttered real-world tables).
    5. Recommend specific data augmentations (random rotations, color jitter, horizontal flips) to counteract imbalances.
  * **Verification:** Export notebook visualizations as high-res figures in `docs/ml/eda_summary.png`.
  * **Deliverable & Branch:** `feat/ml/doil/eda-notebook`.

---
# Week 3 — Foundation Building & Scaffolding

> **Theme:** Lay production foundations — camera UI, mock API endpoints, and real model training.

---

### 🤖 AI / ML Subteam
* **Aarav**
  * **Task:** Build end-to-end PyTorch training pipeline script.
  * **Goal & Context:** Create the reproducible training backbone used for all subsequent model experiments.
  * **Action Steps:**
    1. Create `ml/scripts/train.py` with CLI arguments (`--epochs`, `--batch_size`, `--lr`, `--data_dir`, `--output_dir`).
    2. Initialize ResNet-18 with pretrained ImageNet weights; replace final linear layer with 5 output units.
    3. Set up `CrossEntropyLoss()` and `Adam(lr=0.001)` optimizer.
    4. Implement epoch loop calculating training loss and validation accuracy after every epoch.
    5. Save checkpoint `.pth` whenever validation accuracy achieves a new best score.
  * **Verification:** Run `python ml/scripts/train.py --epochs 2 --batch_size 16` on sample dataset; verify loss decreases and checkpoint file is saved.
  * **Deliverable & Branch:** `feat/ml/aarav/training-pipeline`.

* **Kathleen**
  * **Task:** Configure PyTorch DataLoaders with data augmentations.
  * **Goal & Context:** Prevent model overfitting by applying rich visual transformations to training data.
  * **Action Steps:**
    1. Create `ml/scripts/dataset.py` implementing `get_dataloaders(data_dir, batch_size)`.
    2. Define training transform pipeline:
       - `transforms.RandomResizedCrop(224, scale=(0.8, 1.0))`
       - `transforms.RandomHorizontalFlip(p=0.5)`
       - `transforms.RandomRotation(degrees=15)`
       - `transforms.ColorJitter(brightness=0.2, contrast=0.2)`
       - `transforms.ToTensor()`
       - `transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])`
    3. Define validation transform pipeline (Resize to 256, CenterCrop to 224, ToTensor, Normalize).
    4. Configure DataLoader with `shuffle=True`, `batch_size=32`, and `num_workers=2`.
  * **Verification:** Write a script visualizing a batch of 8 augmented training images with Matplotlib to verify augmentations look natural.
  * **Deliverable & Branch:** `feat/ml/kathleen/dataloader-augmentations`.

* **Max**
  * **Task:** Execute ResNet-18 baseline training run.
  * **Goal & Context:** Establish the first real benchmark performance on the composite dataset.
  * **Action Steps:**
    1. Run `ml/scripts/train.py` on the full processed dataset for 10 epochs.
    2. Track training loss, validation loss, and validation accuracy per epoch.
    3. Save final weights to `ml/models/resnet18_baseline.pth`.
    4. Plot training vs validation loss curves and validation accuracy curves.
    5. Save plots to `docs/ml/baseline_loss_curves.png`.
  * **Verification:** Confirm baseline validation accuracy achieves ≥ 75% across the 5 categories.
  * **Deliverable & Branch:** `feat/ml/max/baseline-model-training`.

* **Doil**
  * **Task:** Implement model evaluation & confusion matrix script.
  * **Goal & Context:** Provide deep diagnostic insight into per-class accuracy and category confusions.
  * **Action Steps:**
    1. Create `ml/scripts/evaluate.py` taking `--model_path` and `--test_dir`.
    2. Run inference across the full test split; record true labels and predicted labels.
    3. Calculate overall accuracy, per-class Precision, Recall, and F1-Score using Scikit-learn.
    4. Generate and save a normalized confusion matrix heatmap using Seaborn/Matplotlib.
    5. Output summary metrics table in terminal and save confusion matrix to `docs/ml/baseline_confusion_matrix.png`.
  * **Verification:** Run `python ml/scripts/evaluate.py --model_path ml/models/resnet18_baseline.pth` and review confusion matrix.
  * **Deliverable & Branch:** `feat/ml/doil/evaluation-script`.

---
# Week 4 — Core MVP Build (Part 1: Model & API Integration)

> **Theme:** Connect the real PyTorch model to FastAPI and connect the mobile camera to the live classification endpoint.

---

### 🤖 AI / ML Subteam
* **Aarav**
  * **Task:** Fine-tune ResNet-18 model and optimize learning rate schedule.
  * **Goal & Context:** Improve model generalization and accuracy above the 80% mark on validation data.
  * **Action Steps:**
    1. Unfreeze `layer4` of ResNet-18 in `ml/scripts/train.py` to allow higher-level feature fine-tuning.
    2. Implement `CosineAnnealingLR` scheduler decaying learning rate from `1e-4` down to `1e-6`.
    3. Train for 15 epochs; monitor training loss vs validation loss to avoid overfitting.
    4. Implement early stopping with patience of 3 epochs based on validation loss.
    5. Save best checkpoint to `ml/models/resnet18_finetuned.pth`.
  * **Verification:** Confirm validation accuracy improves over baseline model by at least 5% (targeting ≥ 82%).
  * **Deliverable & Branch:** `feat/ml/aarav/model-finetuning`.

* **Kathleen**
  * **Task:** Build model export and packaging script.
  * **Goal & Context:** Package model weights alongside label maps and metadata for seamless backend integration.
  * **Action Steps:**
    1. Create `ml/scripts/export_model.py`.
    2. Extract model state dictionary (`torch.save(model.state_dict(), ...)`).
    3. Generate companion `classes.json` containing class index mapping:
       `{"0": "paper", "1": "plastic", "2": "glass", "3": "compost", "4": "landfill"}`.
    4. Save model metadata file `metadata.json` documenting: base architecture, training date, final validation accuracy, input resolution (224×224), and normalization constants.
    5. Package files into `ml/models/mvp_package/` and provide drop-in path for backend team.
  * **Verification:** Test loading the exported model package from a standalone Python test script using only `state_dict` and `classes.json`.
  * **Deliverable & Branch:** `feat/ml/kathleen/model-packaging`.

* **Max**
  * **Task:** MobileNetV2 architecture experiment & benchmark.
  * **Goal & Context:** Compare lightweight MobileNet against ResNet-18 for latency and memory advantages.
  * **Action Steps:**
    1. Create `ml/scripts/train_mobilenet.py` using `torchvision.models.mobilenet_v2(pretrained=True)`.
    2. Train MobileNetV2 on the same processed dataset for 10 epochs using identical augmentations.
    3. Benchmark inference latency on CPU across 100 test images (measure mean ms per image).
    4. Compare file sizes: `.pth` weight file of ResNet-18 (~45MB) vs MobileNetV2 (~14MB).
    5. Document comparison in `docs/ml/architecture_comparison.md`.
  * **Verification:** Log accuracy and latency metrics side-by-side; present findings in subteam standup.
  * **Deliverable & Branch:** `docs/ml/max/mobilenet-benchmark`.

* **Doil**
  * **Task:** Detailed error analysis & misclassification breakdown.
  * **Goal & Context:** Identify top failure modes to guide targeted data acquisition and user guidance.
  * **Action Steps:**
    1. Create `ml/scripts/error_analysis.py`.
    2. Run inference across the test split and filter all misclassified samples.
    3. Identify top confused pairs (e.g. clear plastic bottles classified as glass; soiled paper classified as cardboard).
    4. Export a grid image of the top 12 highest-confidence false predictions with labels.
    5. Author `docs/ml/error-analysis-week4.md` detailing root causes (reflections, transparent objects, unusual lighting).
  * **Verification:** Commit error analysis markdown with visual failure grid image to repository.
  * **Deliverable & Branch:** `docs/ml/doil/error-analysis`.

---
# Week 5 — Core MVP Build (Part 2: Rules Engine & Demo Hardening)

> **Theme:** Implement location-specific waste rules, verify the full MVP flow end-to-end, and prepare for the mid-semester presentation.

---

### 🤖 AI / ML Subteam
* **Aarav**
  * **Task:** Hyperparameter optimization & model checkpoint freeze.
  * **Goal & Context:** Lock the official MVP model weights ahead of the mid-semester presentation demo.
  * **Action Steps:**
    1. Conduct final tuning run with optimal batch size (32), learning rate (1e-4 with cosine decay), and weight decay (1e-4).
    2. Evaluate final model on test split; confirm overall accuracy ≥ 82%.
    3. Save and lock final checkpoint as `ml/models/sortify_mvp_v1.pth`.
    4. Copy weights to `backend/app/models/sortify_mvp_v1.pth` for backend integration.
    5. Create checksum (MD5 or SHA-256) to ensure weight integrity.
  * **Verification:** Verify backend boots cleanly using the frozen `sortify_mvp_v1.pth` weights.
  * **Deliverable & Branch:** `feat/ml/aarav/checkpoint-freeze`.

* **Kathleen**
  * **Task:** Campus test dataset collection & real-world photo evaluation.
  * **Goal & Context:** Test the model on actual trash photographed across UC Berkeley campus waste bins.
  * **Action Steps:**
    1. Walk through UC Berkeley campus (MLK Student Union, Moffitt Library, Memorial Glade).
    2. Photograph 25–30 real waste items using smartphone camera under varied lighting and angles.
    3. Organize photos into `data/campus_test/{paper,plastic,glass,compost,landfill}`.
    4. Run `evaluate.py` against `data/campus_test/` using the frozen MVP model.
    5. Document real-world accuracy and compare against laboratory test split accuracy.
  * **Verification:** Log campus test accuracy and identify which physical items are most reliably recognized.
  * **Deliverable & Branch:** `docs/ml/kathleen/campus-evaluation-report`.

* **Max**
  * **Task:** Domain gap evaluation report & demo item identification.
  * **Goal & Context:** Bridge the gap between training distribution and physical camera conditions.
  * **Action Steps:**
    1. Analyze Kathleen's campus test results; identify specific visual factors causing confidence drops (shadows, background clutter, item crumpling).
    2. Curate a list of 5 "golden demo items" (e.g. clean Starbucks cold cup, compostable napkin, aluminum soda can) that consistently yield > 90% confidence.
    3. Document recommended physical scanning guidelines (e.g. hold camera 8–12 inches away, plain background) in `docs/ml/demo_scanning_guide.md`.
  * **Verification:** Test golden demo items with Caden and Mong on physical phones to confirm rock-solid live recognition.
  * **Deliverable & Branch:** `docs/ml/max/demo-items-guide`.

* **Doil**
  * **Task:** ML presentation visualizer script & metrics summary.
  * **Goal & Context:** Generate high-impact visual charts and metrics slides for the mid-semester presentation.
  * **Action Steps:**
    1. Create `ml/scripts/generate_presentation_charts.py`.
    2. Generate high-resolution figures (300 DPI):
       - Final confusion matrix with percentage annotations.
       - Per-class accuracy bar chart comparing Baseline vs Fine-tuned ResNet-18.
       - Training vs validation loss curve over 15 epochs.
       - Visual 3×3 grid of successful classifications on campus items with confidence percentages.
    3. Export figures to `docs/presentation_assets/` for easy inclusion in Google Slides.
  * **Verification:** Review exported PNG figures; ensure fonts and labels are crisp and readable on a large projector screen.
  * **Deliverable & Branch:** `feat/ml/doil/presentation-charts`.

---
# Week 6 — 🎤 Mid-Semester Presentation (Recorded Video Demo)

> **Theme:** Presentation Day featuring a high-quality recorded app demo video. Showcase the working MVP, technical architecture, and team retrospective.
>
> > [!IMPORTANT]
> > **All-Hands Slide Collaboration:** The entire team collaborates together on the presentation slide deck in Google Slides. Individual member tasks focus strictly on code, demo recording, and technical validation.

## High-Level Goals
- [ ] High-resolution app demo video recorded, edited, and embedded into slide deck
- [ ] Slide deck complete with architecture, ML metrics, and user journey
- [ ] 30-minute team retrospective held and documented in `docs/retrospective-midsem.md`

---

---

### Subteam Member Presentation Assignments

* **Aarav (AI/ML)**
  * **Task:** Mid-Sem Model Benchmark & Metrics Summary.
  * **Goal & Context:** Document formal machine learning model performance for technical review.
  * **Action Steps:**
    1. Compile final training metrics table: ResNet-18 baseline vs Fine-tuned ResNet-18.
    2. Document metrics: Top-1 Accuracy (83.4%), Per-Class F1-Scores, Mean Inference Latency (48ms on CPU).
    3. Author `ml/models/MIDSEM_METRICS.md` with complete architecture diagram and training parameters.
  * **Verification:** Review document with ML team and verify figures match presentation slide data.
  * **Deliverable & Branch:** `ml/models/MIDSEM_METRICS.md`.

* **Kathleen (AI/ML)**
  * **Task:** Physical Demo Items Benchmark & Preparation.
  * **Goal & Context:** Ensure the items chosen for the video demo yield flawless classification results.
  * **Action Steps:**
    1. Benchmark 10 candidate physical waste items against the frozen MVP model.
    2. Select the top 3 items with highest, most stable prediction confidence (> 92%):
       - Item 1: Clean plastic water bottle (`plastic`)
       - Item 2: Starbucks paper coffee cup (`paper/compost`)
       - Item 3: Aluminum soda can (`metal/recycling`)
    3. Hand off physical items and test notes to Caden for the recording session.
  * **Verification:** Confirm all 3 items classify correctly on 5 consecutive trial scans.
  * **Deliverable & Branch:** `docs/ml/kathleen/demo-items-benchmark.md`.

* **Max (AI/ML)**
  * **Task:** Catalog of Known Limitations & Failure Modes.
  * **Goal & Context:** Formulate thoughtful responses for presentation Q&A regarding model limitations.
  * **Action Steps:**
    1. Document known failure modes identified during testing (e.g. crumpled black plastic, translucent glass, items with food residue).
    2. Write technical mitigation strategies for Phase 2 (e.g. confidence thresholding, test-time augmentation, user feedback loops).
    3. Save catalog in `docs/ml/known-limitations.md`.
  * **Verification:** Review failure modes with presenters to prepare for audience technical questions.
  * **Deliverable & Branch:** `docs/ml/known-limitations.md`.

* **Doil (AI/ML)**
  * **Task:** Presentation Rehearsal Timing & Speaker Coordination.
  * **Goal & Context:** Keep presentation strictly within the allotted time limit and ensure seamless speaker handoffs.
  * **Action Steps:**
    1. Coordinate a 45-minute dry-run rehearsal with all 10 members.
    2. Time each presentation section: Introduction (2 min), UI & Video Demo (3 min), Architecture & Backend (2 min), ML Pipeline (3 min), Future Roadmap (2 min).
    3. Create a speaker cue sheet with designated slide owners and verbal handoff cues.
  * **Verification:** Conduct full run-through with timer; ensure presentation finishes with at least 2 minutes remaining for Q&A.
  * **Deliverable & Branch:** `docs/presentation_cue_sheet.md`.

---


---
# Week 7 — Authentication & User Accounts

> **Theme:** Implement Firebase user authentication, manage secure sessions on mobile, and protect backend endpoints with JWT middleware.

---

### 🤖 AI / ML Subteam
* **Aarav**
  * **Task:** Dynamic PyTorch model quantization experiment.
  * **Goal & Context:** Reduce model memory footprint and speed up CPU inference using INT8 weights.
  * **Action Steps:**
    1. Implement dynamic quantization script `ml/scripts/quantize.py`.
    2. Apply `torch.quantization.quantize_dynamic(model, {nn.Linear}, dtype=torch.qint8)`.
    3. Compare model file size: unquantized (~45MB) vs quantized (~12MB).
    4. Benchmark inference speed on 50 sample images; measure speedup percentage.
    5. Evaluate accuracy delta to ensure accuracy loss is < 1%.
  * **Verification:** Save quantized model to `ml/models/sortify_quantized.pth` and log benchmark metrics in PR.
  * **Deliverable & Branch:** `feat/ml/aarav/model-quantization`.

* **Kathleen**
  * **Task:** Targeted dataset expansion for weak classes.
  * **Goal & Context:** Boost accuracy on difficult waste items identified during Week 4 error analysis.
  * **Action Steps:**
    1. Collect 120 additional images focused on historically confused items:
       - Soiled paper/cardboard vs clean paper.
       - Clear plastic cups vs glass containers.
       - Crushed aluminum cans.
    2. Apply standard preprocessing and add to `data/raw_expanded/`.
    3. Re-run `split_data.py` to produce augmented dataset version `data/processed_v2/`.
  * **Verification:** Verify class balance remains consistent across dataset version 2.
  * **Deliverable & Branch:** `feat/ml/kathleen/dataset-expansion`.

* **Max**
  * **Task:** Retrain model on expanded dataset v2.
  * **Goal & Context:** Train new model weights leveraging the expanded dataset to improve edge case handling.
  * **Action Steps:**
    1. Run `train.py` on `data/processed_v2/` for 15 epochs.
    2. Monitor validation loss curves and compare convergence against v1 model.
    3. Save best checkpoint to `ml/models/sortify_v2.pth`.
    4. Run `evaluate.py` to calculate updated confusion matrix and per-class metrics.
  * **Verification:** Verify accuracy on previously weak classes (e.g. soiled paper) improves by at least 8%.
  * **Deliverable & Branch:** `feat/ml/max/retraining-v2`.

* **Doil**
  * **Task:** Comprehensive model evaluation report v2.
  * **Goal & Context:** Document performance gains achieved by dataset expansion and model retraining.
  * **Action Steps:**
    1. Compare v1 vs v2 model metrics side-by-side in a comparative table.
    2. Plot side-by-side confusion matrices (v1 on left, v2 on right) highlighting reduced false-positive rates.
    3. Author `docs/ml/model_v2_evaluation_report.md`.
  * **Verification:** Review report in subteam sync and confirm v2 checkpoint is ready for deployment.
  * **Deliverable & Branch:** `docs/ml/doil/model-v2-evaluation`.

---
# Week 8 — Engagement Tracker, Streaks & Gamification

> **Theme:** Drive daily student habits through streak tracking, eco-points, and scan history.

---

### 🤖 AI / ML Subteam
* **Aarav**
  * **Task:** Test-Time Augmentation (TTA) experimentation.
  * **Goal & Context:** Evaluate if averaging predictions across multiple augmented views improves accuracy on tricky images.
  * **Action Steps:**
    1. Implement `ml/scripts/tta_eval.py` applying 4 test-time transforms per test image:
       - Original image
       - Horizontal flip
       - Slight rotation (+10 degrees)
       - Center crop at 90% scale
    2. Average the 4 softmax probability vectors to obtain ensemble prediction.
    3. Benchmark accuracy and latency: compare single forward pass vs TTA forward pass.
    4. Document findings in `docs/ml/tta_experiments.md`.
  * **Verification:** Measure accuracy improvement vs inference latency increase; determine if TTA is viable for production.
  * **Deliverable & Branch:** `docs/ml/aarav/tta-experiments`.

* **Kathleen**
  * **Task:** Model version logging & loading helper script.
  * **Goal & Context:** Establish clean model checkpoint tracking and seamless switching between model versions.
  * **Action Steps:**
    1. Create `ml/models/MODEL_LOG.md` recording all trained checkpoints:
       - Version name, date trained, dataset used, epochs, validation accuracy, file size, and primary author.
    2. Create a clean Python loader helper in `ml/scripts/load_model.py`:
       - `load_model(version_name: str = "latest") -> nn.Module`: automatically resolves path and loads weights into `eval()` mode.
  * **Verification:** Run a test script calling `load_model("sortify_v2")` and verify model loads cleanly.
  * **Deliverable & Branch:** `ml/models/MODEL_LOG.md` & `ml/scripts/load_model.py`.

* **Max**
  * **Task:** PyTorch to ONNX export pipeline & validation.
  * **Goal & Context:** Export model to vendor-neutral ONNX format for accelerated inference runtimes.
  * **Action Steps:**
    1. Create `ml/scripts/export_onnx.py`.
    2. Export model graph using `torch.onnx.export()`:
       - Dummy input shape: `(1, 3, 224, 224)`.
       - Dynamic batch axis: `{"input": {0: "batch_size"}, "output": {0: "batch_size"}}`.
    3. Verify exported `.onnx` model using `onnx.checker.check_model()`.
    4. Benchmark output parity: pass 20 test images through both PyTorch and ONNX Runtime; assert predictions match within `1e-4` tolerance.
  * **Verification:** Save `ml/models/sortify.onnx` and verify ONNX Runtime inference outputs match PyTorch.
  * **Deliverable & Branch:** `feat/ml/max/onnx-export`.

* **Doil**
  * **Task:** Prototype ONNX to TensorFlow Lite (`.tflite`) conversion.
  * **Goal & Context:** Investigate potential for future on-device mobile neural execution.
  * **Action Steps:**
    1. Test conversion of `sortify.onnx` into `.tflite` format using `onnx2tf` or Google AI Edge Torch.
    2. Measure converted `.tflite` model size and test execution on sample tensor.
    3. Document feasibility, prerequisites, and limitations for React Native mobile embedding in `docs/ml/tflite_conversion_notes.md`.
  * **Verification:** Document conversion steps and commit `.tflite` benchmark notes to repository.
  * **Deliverable & Branch:** `docs/ml/doil/tflite-conversion`.

---
# Week 9 — System Integration Testing & Robustness

> **Theme:** Stress-test every component, eliminate cross-subteam bugs, and calibrate model confidence thresholds.

---

### 🤖 AI / ML Subteam
* **Aarav**
  * **Task:** Adversarial & out-of-distribution input stress testing.
  * **Goal & Context:** Understand model behavior on non-trash objects and extreme photo conditions.
  * **Action Steps:**
    1. Collect 30 challenging out-of-distribution images:
       - Non-trash items (selfies, pets, laptops, furniture).
       - Extreme lighting (pitch dark, heavy glare, overexposed flash).
       - Severe motion blur and multiple mixed items in one frame.
    2. Run inference across the adversarial set; record predicted classes and confidence scores.
    3. Document failure patterns in `docs/ml/adversarial_stress_test.md`.
  * **Verification:** Commit stress-test findings and identify threshold recommendations to reject out-of-distribution photos.
  * **Deliverable & Branch:** `docs/ml/aarav/adversarial-stress-test`.

* **Kathleen**
  * **Task:** Empirical confidence threshold calibration.
  * **Goal & Context:** Determine the optimal confidence threshold to balance false positives vs false rejections.
  * **Action Steps:**
    1. Create `ml/scripts/calibrate_threshold.py`.
    2. Test 3 confidence thresholds (0.40, 0.50, 0.60) across validation and campus test datasets.
    3. Calculate trade-off:
       - Precision vs Rejection Rate (how many correct items are mistakenly flagged as "Uncertain").
    4. Select optimal threshold (e.g. 0.50) where items with < 50% confidence return status `"uncertain": true` with recommendation: "Unable to identify clearly. Check local landfill/sorting guide."
    5. Hand off chosen threshold to backend team for integration into `POST /api/classify`.
  * **Verification:** Test threshold on 20 test images; confirm ambiguous items receive helpful uncertain notice while clear items pass.
  * **Deliverable & Branch:** `feat/ml/kathleen/confidence-thresholding`.

* **Max**
  * **Task:** Comparative model evaluation & checkpoint recommendation.
  * **Goal & Context:** Objectively compare all trained model checkpoints to select the single best production candidate.
  * **Action Steps:**
    1. Create `ml/scripts/compare_models.py`.
    2. Evaluate 3 candidate checkpoints on the identical test split:
       - Baseline ResNet-18 (Week 3)
       - Fine-tuned ResNet-18 v1 (Week 4)
       - Expanded Dataset ResNet-18 v2 (Week 7)
    3. Output a clean comparison table: Overall Accuracy, Per-Class F1-Scores, Inference Time, and Model Size.
    4. Write formal recommendation recommending the winning `.pth` file for final production.
  * **Verification:** Commit evaluation script and markdown comparison table to repository.
  * **Deliverable & Branch:** `docs/ml/max/model-comparison-report`.

* **Doil**
  * **Task:** Author official Model Card documentation.
  * **Goal & Context:** Provide standard industry documentation for the computer vision model per Hugging Face / Google standards.
  * **Action Steps:**
    1. Author `ml/MODEL_CARD.md` following standard format:
       - **Model Details:** Architecture (ResNet-18), framework (PyTorch 2.X), license.
       - **Intended Use:** Mobile waste item sorting for undergraduate campus recycling.
       - **Training Data:** Composition of TrashNet + campus samples (splits and augmentation details).
       - **Quantitative Analysis:** Final accuracy, per-class confusion matrix, precision/recall breakdown.
       - **Limitations & Biases:** Performance degradations on transparent glass, crumpled plastics, low light.
  * **Verification:** Review Model Card with ML subteam and ensure all metrics match official test results.
  * **Deliverable & Branch:** `ml/MODEL_CARD.md`.

---
# Week 10 — Production Hardening & UX Polish

> **Theme:** Make Sortify feel like a consumer-grade app: haptic feedback, dark mode, Dockerization, and clear setup guides.

---

### 🤖 AI / ML Subteam
* **Aarav**
  * **Task:** Verify Dockerized model inference performance.
  * **Goal & Context:** Ensure the PyTorch model performs reliably inside the Docker container under CPU memory constraints.
  * **Action Steps:**
    1. Pull Carlos's Docker container build locally.
    2. Run container with strict CPU and RAM resource limits (`--memory=1g --cpus=2`).
    3. Execute 50 sequential and concurrent classification requests against the container.
    4. Measure inference latency and ensure container memory does not continuously climb.
  * **Verification:** Confirm container executes requests under 100ms on CPU without crashing or triggering OOM killer.
  * **Deliverable & Branch:** `docs/ml/aarav/docker-inference-validation`.

* **Kathleen**
  * **Task:** Build interactive model demo Jupyter notebook.
  * **Goal & Context:** Create an accessible interactive playground for non-technical team members and evaluators.
  * **Action Steps:**
    1. Create `ml/notebooks/demo.ipynb` using `ipywidgets`.
    2. Implement file upload button allowing anyone to upload a photo from their computer.
    3. Run photo through the trained model; display the uploaded image alongside an interactive horizontal bar chart of class probabilities.
    4. Highlight top predicted category in the waste bin's color.
  * **Verification:** Run notebook in JupyterLab; upload 3 sample images and verify interactive charts render smoothly.
  * **Deliverable & Branch:** `ml/notebooks/demo.ipynb`.

* **Max**
  * **Task:** On-device mobile inference research & benchmarks.
  * **Goal & Context:** Document the architectural path for running Sortify without an internet connection in future releases.
  * **Action Steps:**
    1. Research mobile deployment options: TensorFlow Lite for React Native vs ONNX Runtime Mobile vs PyTorch Mobile (ExecuTorch).
    2. Benchmark model execution speed and app bundle size implications.
    3. Author `ml/docs/MOBILE_INFERENCE.md` detailing technical requirements and architectural recommendations for v2.
  * **Verification:** Commit technical research document to repository.
  * **Deliverable & Branch:** `ml/docs/MOBILE_INFERENCE.md`.

* **Doil**
  * **Task:** Author verified step-by-step model retraining guide in `ml/README.md`.
  * **Goal & Context:** Provide clear documentation so any contributor can retrain the model from scratch.
  * **Action Steps:**
    1. Author comprehensive `ml/README.md` containing:
       - Environment setup instructions (virtualenv, PyTorch install).
       - Dataset layout structure diagram (`data/processed/...`).
       - Exact CLI commands to run data splitting, preprocessing, training, and evaluation.
       - Troubleshooting section for common CUDA/MPS/out-of-memory errors.
    2. Verify the guide by opening a completely clean terminal and executing every step sequentially.
  * **Verification:** Confirm script finishes training and produces a working `.pth` model without manual code edits.
  * **Deliverable & Branch:** `ml/README.md`.

---
# Week 11 — Stretch Goals & Deployment

> **Theme:** Deploy backend to cloud, generate standalone mobile builds, and explore advanced stretch features in isolated branches.

---

### 🤖 AI / ML Subteam
* **Aarav**
  * **Task:** Prototype multi-object waste detection with YOLOv8.
  * **Goal & Context:** Explore YOLO object detection as an architectural stretch goal for future development.
  * **Action Steps:**
    1. In branch `feat/ml/aarav/yolov8-multiobject`:
       - Install Ultralytics: `pip install ultralytics`.
       - Load pretrained YOLOv8n model and test inference on multi-item waste images.
       - Extract bounding boxes, class labels, and confidence scores.
    2. Document feasibility, frame rate, and export formats in `docs/ml/yolov8_feasibility.md`.
  * **Verification:** Run script on sample multi-item photo; verify detected bounding boxes draw cleanly over items.
  * **Deliverable & Branch:** `feat/ml/aarav/yolov8-multiobject`.

* **Kathleen**
  * **Task:** Contamination classification heuristic prototype.
  * **Goal & Context:** Research secondary computer vision classifier to distinguish clean vs food-soiled recyclables.
  * **Action Steps:**
    1. Curate a small test set of 40 clean vs soiled recyclable items.
    2. Test color histogram and texture variance heuristics to detect grease stains and residue.
    3. Document heuristic decision tree accuracy in `docs/ml/contamination_detection_notes.md`.
  * **Verification:** Commit research findings and decision tree accuracy report to repository.
  * **Deliverable & Branch:** `docs/ml/kathleen/contamination-research`.

* **Max**
  * **Task:** Final performance metrics & comparative presentation visuals.
  * **Goal & Context:** Generate definitive comparative charts illustrating the model's evolution across the semester.
  * **Action Steps:**
    1. Generate publication-quality figures for the final presentation:
       - Side-by-side ROC curves and confusion matrices.
       - Accuracy progression chart: Week 1 Baseline (74%) → Week 4 MVP (83%) → Week 7 v2 (88%).
       - Latency vs Model Size bubble chart comparing architectures.
    2. Save all figures at 300 DPI in `docs/final_presentation_assets/`.
  * **Verification:** Review charts with ML lead to ensure labels and data match final verified metrics.
  * **Deliverable & Branch:** `docs/final_presentation_assets/`.

* **Doil**
  * **Task:** Author Future Work & Edge Hardware Roadmap.
  * **Goal & Context:** Formulate the long-term technical vision for Sortify beyond the 12-week semester.
  * **Action Steps:**
    1. Author `docs/ml/future-work-roadmap.md`:
       - Smart Waste Bins: Raspberry Pi / Google Coral edge inference with motorized sorting flaps.
       - Campus Bin Mapping: Geolocation map showing nearest compost/recycling bins across UC Berkeley.
       - Municipal Expansion: Automated scraping of municipal waste codes across California.
  * **Verification:** Review roadmap with team leads and incorporate into final presentation slides.
  * **Deliverable & Branch:** `docs/ml/future-work-roadmap.md`.

---
# Week 12 — 🎤 Final Presentation & Portfolio Release

> **Theme:** Present Sortify to the audience with a recorded full-featured demo video, clean up repository, and celebrate! 🎉
>
> > [!IMPORTANT]
> > **All-Hands Slide Collaboration:** The entire team collaborates together on the final presentation slide deck in Google Slides. Individual assignments below focus strictly on demo video production, final code polish, and repository release readiness.

## High-Level Goals
- [ ] Final comprehensive demo video produced, edited, and embedded in slides
- [ ] Presentation delivered cleanly across all subteams
- [ ] Repository is portfolio-ready, fully documented, and feature branches merged to `main`

---

---

### Subteam Member Presentation Assignments

* **Aarav (AI/ML)**
  * **Task:** Model Optimization & Quantization Final Report.
  * **Goal & Context:** Document machine learning optimization techniques applied throughout the semester.
  * **Action Steps:**
    1. Benchmark final quantized INT8 model vs unquantized FP32 model on CPU inference speed and RAM usage.
    2. Author `ml/docs/OPTIMIZATION.md` covering: dynamic quantization, layer freezing, and inference acceleration.
    3. Archive final production model weights in `ml/models/release_v1/`.
  * **Verification:** Commit optimization report and ensure release weights load cleanly.
  * **Deliverable & Branch:** `ml/docs/OPTIMIZATION.md`.

* **Kathleen (AI/ML)**
  * **Task:** Campus Real-World Testing Final Report.
  * **Goal & Context:** Summarize empirical performance across UC Berkeley campus waste bins.
  * **Action Steps:**
    1. Compile full test results from campus waste photo evaluations across the semester into `data/campus_test/CAMPUS_BENCHMARKS.md`.
    2. Document overall real-world accuracy (86.2%), per-category accuracy, and most challenging waste items.
    3. Include high-resolution photo collage of tested campus items.
  * **Verification:** Review report with ML lead and present empirical findings in final presentation.
  * **Deliverable & Branch:** `data/campus_test/CAMPUS_BENCHMARKS.md`.

* **Max (AI/ML)**
  * **Task:** Semester Model Evolution Technical Summary.
  * **Goal & Context:** Detail the mathematical and experimental journey from initial baseline to final production model.
  * **Action Steps:**
    1. Author `ml/docs/MODEL_EVOLUTION.md` detailing:
       - Baseline ResNet-18 (74.2% accuracy)
       - Fine-tuned ResNet-18 (83.4% accuracy)
       - Expanded Dataset ResNet-18 v2 (88.1% accuracy)
       - MobileNetV2 exploration and trade-offs
    2. Include loss curve progressions and parameter configurations.
  * **Verification:** Commit technical evolution document to repository.
  * **Deliverable & Branch:** `ml/docs/MODEL_EVOLUTION.md`.

* **Doil (AI/ML)**
  * **Task:** Project Wrap-Up Summary & Individual Contribution Log.
  * **Goal & Context:** Celebrate the team's achievements and formally document individual contributions.
  * **Action Steps:**
    1. Author `docs/CONTRIBUTIONS.md` celebrating individual contributions across all 10 members (Frontend, Backend, ML).
    2. Update root `README.md` with final project badges, architecture overview, demo video link, and team roster.
    3. Organize final team celebratory dinner / wrap-up gathering! 🍕🎉
  * **Verification:** Review `README.md` and `CONTRIBUTIONS.md` with the entire team during final retrospective.
  * **Deliverable & Branch:** `docs/CONTRIBUTIONS.md` & root `README.md`.

---


---

## 📊 Individual 12-Week Trajectory Matrix

| Member | Subteam | Weeks 1–3 (Onboarding & Foundation) | Weeks 4–6 (Core MVP Build & Demo Video) | Weeks 7–9 (Auth, Gamification & Hardening) | Weeks 10–12 (Polish, Deploy & Final Demo) |
|---|---|---|---|---|---|
| **Aarav** | AI / ML | W1 Transfer learning exercise, dataset aggregation, training pipeline script | Model fine-tuning, final MVP checkpoint selection, mid-sem metrics summary | Dynamic quantization, TTA experimentation, adversarial robustness testing | Docker inference validation, YOLOv8 multi-object prototype, quantization benchmark report |
| **Kathleen** | AI / ML | W1 Transfer learning exercise, train/val/test split script, dataloaders & augmentations | Model export packaging with classes.json, campus photo benchmark, demo item testing | Targeted dataset expansion, model log & loader helper, empirical threshold testing | Interactive demo notebook, contamination heuristics, campus benchmark report |
| **Max** | AI / ML | W1 Transfer learning exercise, preprocessing pipeline, baseline ResNet-18 training | MobileNetV2 benchmark, domain gap analysis, failure modes catalog | Retraining expanded data, ONNX export pipeline, model comparison evaluation | Mobile inference research, final metrics comparative charts, model evolution summary |
| **Doil** | AI / ML | W1 Transfer learning exercise, EDA notebook, confusion matrix eval script | Error analysis report, metrics visualizer script, rehearsal timing | Model evaluation report, ONNX to TFLite prototype, final Model Card | Retraining guide verification, future work roadmap, contributions doc & wrap-up |

---

## 🛠️ Best Practices & Coordination Rules

1. **Branch Hygiene:**
   * Always branch off fresh `main`: `git checkout main && git pull origin main && git checkout -b feat/<subteam>/<your-name>/<feature-name>`.
   * PRs must be focused and under 300 lines of code wherever possible.
   * Assign team leads and peer subteam members for reviews.
2. **No Direct Commits to Main:**
   * All changes must pass Ruff linting / formatting and automated CI checks before merging.
