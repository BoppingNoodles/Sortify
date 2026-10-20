"""Convenience re-export for ml/scripts/evaluate.py.

Allows running or importing evaluate from both:
    python ml/evaluate.py ...
and
    python ml/scripts/evaluate.py ...
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ml.scripts.evaluate import (  # noqa: F401
    DEFAULT_CLASSES,
    DEFAULT_MODEL_PATH,
    DEFAULT_OUTPUT_PLOT,
    DEFAULT_TEST_DIR,
    RemappedDataset,
    build_model,
    create_test_loader,
    evaluate_model_performance,
    get_device,
    load_checkpoint,
    main,
    parse_args,
    plot_confusion_matrix,
    run_evaluation,
)

if __name__ == "__main__":
    main()
