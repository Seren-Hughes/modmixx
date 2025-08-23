import requests
import os

PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_URL = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def get_toxicity_score(text):
    """
    Analyze text content using Google's Perspective API for toxicity detection.

    Args:
        text (str): The text content to analyze

    Returns:
        float: Toxicity score between 0.0 (not toxic) and 1.0 (very toxic)

    Raises:
        requests.RequestException: If API call fails
    """
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(
        f"{PERSPECTIVE_API_URL}?key={PERSPECTIVE_API_KEY}", json=data
    )
    response.raise_for_status()
    result = response.json()
    return result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
