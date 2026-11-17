"""Check a Sortify deployment and write a timestamped HTTP acceptance report."""

import argparse
import hashlib
import ipaddress
import json
import math
import time
from datetime import UTC, datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.parse import urlsplit
from uuid import uuid4

import httpx

from backend.app.schemas import (
    ClassifyResponse,
    GuestScanRecord,
    HistoryPage,
    SavedGuestScan,
)
from backend.app.schemas.stats import UserStatsResponse

IMAGE_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}
WARM_P95_TARGET_MS = 1500
UPTIME_INTERVAL_SECONDS = 300


def validate_url(value: str) -> str:
    parts = urlsplit(value)
    host = parts.hostname
    if not host or parts.username is not None or parts.query or parts.fragment:
        raise ValueError(
            "Provide a base URL without credentials, a query, or a fragment"
        )
    local = host == "localhost"
    try:
        local = local or ipaddress.ip_address(host).is_loopback
    except ValueError:
        pass
    if parts.scheme != "https" and not (parts.scheme == "http" and local):
        raise ValueError(
            "Use HTTPS for remote targets or HTTP for explicit localhost runs"
        )
    return str(httpx.URL(value.rstrip("/")))


def now() -> str:
    return datetime.now(UTC).isoformat()


def measure(
    client, method, path, expected_status, validate, **kwargs
) -> tuple[dict, object]:
    sample = {"started_at": now(), "method": method, "path": path, "status": None}
    start = time.perf_counter()
    value = None
    try:
        response = client.request(method, path, **kwargs)
        sample["status"] = response.status_code
        if response.status_code != expected_status:
            raise ValueError(
                f"Expected HTTP {expected_status}, received {response.status_code}"
            )
        value = validate(response.json())
    except httpx.TimeoutException:
        sample["error"] = "HTTP request timed out"
    except httpx.RequestError as error:
        sample["error"] = f"HTTP transport failure ({type(error).__name__})"
    except (ValueError, TypeError) as error:
        sample["error"] = str(error).splitlines()[0]
    sample["elapsed_ms"] = round((time.perf_counter() - start) * 1000, 3)
    sample["ok"] = "error" not in sample
    return sample, value


def validate_health(body):
    if not isinstance(body, dict) or body.get("status") != "ok":
        raise ValueError("Expected a health response with status ok")


def validate_classification(body, location):
    result = ClassifyResponse.model_validate(body, strict=True)
    if not result.item_name.strip() or not str(body.get("disposal_tip", "")).strip():
        raise ValueError("Classification is missing item name or disposal guidance")
    if body.get("location") != location.lower():
        raise ValueError(
            "Classification location does not match the requested municipality"
        )
    if "(scaffold)" in result.item_name.casefold():
        raise ValueError("Classification returned the current scaffold fallback")
    return result


def summarize_warm(samples: list[dict]) -> dict:
    durations = sorted(sample["elapsed_ms"] for sample in samples if sample["ok"])
    return {
        "sample_size": len(samples),
        "success_count": len(durations),
        "failure_count": len(samples) - len(durations),
        "percentile_method": "nearest rank of successful samples (ceil(p * n))",
        **{
            f"p{percentile}_ms": durations[
                math.ceil(percentile * len(durations) / 100) - 1
            ]
            if durations
            else None
            for percentile in (50, 95, 99)
        },
    }


def smoke_history(client, prediction: ClassifyResponse) -> dict:
    guest_id, scan_id = uuid4(), uuid4()
    expected = GuestScanRecord(
        user_id=guest_id,
        scan_id=scan_id,
        item_name=prediction.item_name,
        category=prediction.category,
        confidence=prediction.confidence,
        location=prediction.location,
        bin=prediction.bin,
        bin_color=prediction.bin_color,
    )

    def validate_saved(body):
        saved = SavedGuestScan.model_validate(body)
        if saved.scan_id != scan_id or saved.scan != expected:
            raise ValueError("Saved response does not match the synthetic scan")

    def validate_page(body):
        page = HistoryPage.model_validate(body)
        if page.scans != [expected] or page.next_cursor is not None:
            raise ValueError("Synthetic guest should contain exactly one matching scan")

    def validate_stats(body):
        stats = UserStatsResponse.model_validate(body, strict=True)
        if (
            stats.user_id != str(guest_id)
            or stats.total_scans != 1
            or stats.eco_points != 10
            or stats.category_counts != {expected.category: 1}
        ):
            raise ValueError(
                "Retrying the same ID should leave the synthetic guest with one scan"
            )

    samples = []
    for _ in range(2):
        saved, _ = measure(
            client,
            "POST",
            "/api/history",
            201,
            validate_saved,
            json=expected.model_dump(mode="json"),
        )
        samples.append(saved)
    history, _ = measure(
        client,
        "GET",
        "/api/history",
        200,
        validate_page,
        params={"user_id": str(guest_id)},
    )
    stats, _ = measure(client, "GET", f"/api/stats/{guest_id}", 200, validate_stats)
    samples.extend((history, stats))
    return {
        "user_id": str(guest_id),
        "scan_id": str(scan_id),
        "samples": samples,
        "retention": "Synthetic record may remain in staging storage after this check.",
        "ok": all(sample["ok"] for sample in samples),
    }


def run_release(client, image, location, request_count, staging_history=False) -> dict:
    payload = image.read_bytes()
    files = {"file": (image.name, payload, IMAGE_TYPES[image.suffix.lower()])}
    health, _ = measure(client, "GET", "/health", 200, validate_health)
    report = {
        "health": health,
        "image": {"name": image.name, "sha256": hashlib.sha256(payload).hexdigest()},
        "location": location,
        "first_classification": None,
        "warm_requests": [],
        "warm_target_ms": WARM_P95_TARGET_MS,
        "requested_warm_count": request_count,
    }

    def classify():
        sample, prediction = measure(
            client,
            "POST",
            "/api/classify",
            200,
            lambda body: validate_classification(body, location),
            params={"location": location},
            files=files,
        )
        if prediction is not None:
            sample["prediction"] = prediction.model_dump(
                include={"category", "confidence", "alternatives"}
            )
        return sample, prediction

    if health["ok"]:
        first, prediction = classify()
        report["first_classification"] = first
        report["warm_requests"] = [classify()[0] for _ in range(request_count)]
        if staging_history and prediction is not None:
            report["staging_history"] = smoke_history(client, prediction)

    summary = summarize_warm(report["warm_requests"])
    report["warm_summary"] = summary
    report["warm_target_met"] = (
        summary["p95_ms"] is not None and summary["p95_ms"] < WARM_P95_TARGET_MS
    )
    report["ok"] = bool(
        health["ok"]
        and report["first_classification"]["ok"]
        and summary["success_count"] == request_count
        and report["warm_target_met"]
        and (not staging_history or report.get("staging_history", {}).get("ok", False))
    )
    return report


def write_report(output: Path, report: dict) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(dir=output.parent, delete=False) as temp:
        temporary = Path(temp.name)
    try:
        temporary.write_text(
            json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8"
        )
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)


def observe_health(client, report, output, minutes):
    start = time.monotonic()
    observation = {
        "requested_minutes": minutes,
        "interval_seconds": UPTIME_INTERVAL_SECONDS,
        "elapsed_seconds": 0,
        "complete": False,
        "failure_count": 0,
        "missed_intervals": 0,
        "samples": [],
    }
    report["uptime"] = observation
    for offset in range(0, minutes * 60 + 1, UPTIME_INTERVAL_SECONDS):
        time.sleep(max(0, start + offset - time.monotonic()))
        if time.monotonic() >= start + offset + UPTIME_INTERVAL_SECONDS:
            observation["missed_intervals"] += 1
            observation["elapsed_seconds"] = round(time.monotonic() - start, 3)
            report["ok"] = False
            write_report(output, report)
            continue
        health, _ = measure(client, "GET", "/health", 200, validate_health)
        observation["samples"].append(health)
        observation["elapsed_seconds"] = round(time.monotonic() - start, 3)
        observation["failure_count"] += int(not health["ok"])
        report["ok"] = report["ok"] and health["ok"]
        observation["complete"] = (
            offset == minutes * 60 and not observation["missed_intervals"]
        )
        write_report(output, report)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--image", type=Path, required=True)
    parser.add_argument("--location", required=True)
    parser.add_argument(
        "--requests", type=int, default=20, help="Warm measurements (at least 20)"
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--timeout", type=float, default=15, help="HTTP timeout in seconds"
    )
    parser.add_argument(
        "--environment", choices=("development", "staging", "production"), required=True
    )
    parser.add_argument(
        "--candidate-sha", help="Deployed application commit supplied by the owner"
    )
    parser.add_argument(
        "--model-sha256", help="Deployed checkpoint digest supplied by the owner"
    )
    parser.add_argument("--storage-mode", choices=("memory", "firestore"))
    parser.add_argument("--staging-history", action="store_true")
    parser.add_argument(
        "--observe-minutes",
        type=int,
        default=0,
        help="Health observation window (multiple of five minutes)",
    )
    args = parser.parse_args()
    try:
        base_url = validate_url(args.base_url)
    except (ValueError, httpx.InvalidURL) as error:
        parser.error(str(error))
    if args.requests < 20 or not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error("Provide at least 20 warm requests and a finite positive timeout")
    if (
        not args.location.strip()
        or args.image.suffix.lower() not in IMAGE_TYPES
        or not args.image.is_file()
    ):
        parser.error("Provide a municipality and an existing JPEG, PNG, or WebP image")
    if args.staging_history and args.environment != "staging":
        parser.error(
            "History writes require --environment staging and --staging-history"
        )
    if args.output.resolve() == args.image.resolve():
        parser.error("Choose an output path distinct from the sample image")
    if args.output.exists():
        parser.error("Choose a new report path to preserve previous observations")
    if args.observe_minutes < 0 or args.observe_minutes % 5:
        parser.error(
            "The observation window must be a nonnegative multiple of five minutes"
        )

    try:
        with httpx.Client(
            base_url=base_url, timeout=args.timeout, follow_redirects=False
        ) as client:
            report = {
                "started_at": now(),
                "base_url": base_url,
                "environment": args.environment,
                "deployment_owner_metadata": {
                    "candidate_sha": args.candidate_sha,
                    "model_sha256": args.model_sha256,
                    "storage_mode": args.storage_mode,
                },
                "http_timeout_seconds": args.timeout,
                **run_release(
                    client,
                    args.image,
                    args.location,
                    args.requests,
                    args.staging_history,
                ),
            }
            write_report(args.output, report)
            if args.observe_minutes:
                observe_health(client, report, args.output, args.observe_minutes)
    except (OSError, ValueError, httpx.InvalidURL) as error:
        parser.exit(1, f"Release check failed: {error}\n")
    print(
        f"HTTP checks {'passed' if report['ok'] else 'failed'}. Report: {args.output}"
    )
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
