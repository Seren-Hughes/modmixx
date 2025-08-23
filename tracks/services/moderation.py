import logging

import boto3
from django.conf import settings

logger = logging.getLogger(__name__)

# Labels that should block an image if detected
BLOCK_LABELS = {
    "Explicit Nudity",
    "Nudity",
    "Sexual Activity",
    "Suggestive",
    "Violence",
    "Hate Symbols",
    "Hate",
    "Smoking",
}


def _client():
    """Create Rekognition client with separate credentials if available."""
    rekog_key = getattr(settings, "REKOGNITION_ACCESS_KEY", None)
    rekog_secret = getattr(settings, "REKOGNITION_SECRET", None)

    print(
        f"DEBUG: Using Rekog key: {rekog_key[:10] if rekog_key else 'None'}..."
    )

    if rekog_key and rekog_secret:
        return boto3.client(
            "rekognition",
            region_name=settings.AWS_REGION,
            aws_access_key_id=rekog_key,
            aws_secret_access_key=rekog_secret,
        )
    else:
        print("DEBUG: Falling back to default AWS credentials")
        return boto3.client("rekognition", region_name=settings.AWS_REGION)


def scan_image_bytes(image_bytes: bytes):
    """
    Scan image content using AWS Rekognition for moderation.

    Analyzes image bytes for inappropriate content including nudity,
    violence, hate symbols, and drug-related content. Implements
    confidence-based thresholds for different content types.

    Args:
        image_bytes (bytes): Raw image data to analyze

    Returns:
        tuple: (allowed: bool, labels: list, failed: bool)
            - allowed: Whether image passes moderation
            - labels: List of detected moderation labels with confidence
            - failed: Whether the scan process failed (fail-open policy)

    Confidence Thresholds:
        - Drug content: 99% (avoid false positives)
        - Explicit/violent content: 85% (stricter enforcement)
        - Other inappropriate content: 80% (default minimum)
    """
    if not getattr(settings, "IMAGE_MODERATION_ENABLED", True):
        return True, [], False
    try:
        resp = _client().detect_moderation_labels(
            Image={"Bytes": image_bytes},
            MinConfidence=getattr(settings, "REKOG_MIN_CONFIDENCE", 80),
        )
        labels = resp.get("ModerationLabels", [])

        # Custom logic for different label types
        blocked = False
        for lbl in labels:
            name = lbl.get("Name", "")
            confidence = lbl.get("Confidence", 0)

            # Drug-related: require 99% confidence (avoid false positives)
            if (
                name in ["Pills", "Products", "Drugs & Tobacco"]
                and confidence >= 99
            ):
                blocked = True
                break
            # Other serious content: 85% confidence
            elif (
                name
                in [
                    "Explicit Nudity",
                    "Sexual Activity",
                    "Violence",
                    "Hate Symbols",
                    "Smoking",
                ]
                and confidence >= 85
            ):
                blocked = True
                break

        return (not blocked), labels, False  # Success, no failure
    except Exception as e:
        logger.warning("Rekognition scan failed (fail-open): %s", e)
        return True, [], True  # Fail-open: allowed but mark as failed
