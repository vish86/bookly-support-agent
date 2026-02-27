from __future__ import annotations

from typing import TypedDict


class PolicyAnswer(TypedDict):
    topic: str
    summary: str
    details: str


POLICIES: dict[str, PolicyAnswer] = {
    "shipping": {
        "topic": "shipping",
        "summary": "Bookly typically ships orders within 1–2 business days.",
        "details": (
            "Standard shipping within the US usually arrives within 3–5 business days "
            "after dispatch. International shipping can take 7–14 business days depending "
            "on the destination and customs processing. Tracking information is provided "
            "for most orders as soon as the carrier collects the package."
        ),
    },
    "returns": {
        "topic": "returns",
        "summary": "Most physical books can be returned within 30 days of delivery.",
        "details": (
            "Items must be in resaleable condition, with minimal wear and no significant "
            "damage. Defective or incorrectly shipped items are eligible for a full refund. "
            "Digital products (such as e-books) are generally non-refundable once downloaded."
        ),
    },
    "refunds": {
        "topic": "refunds",
        "summary": "Approved refunds are typically processed within 5–10 business days.",
        "details": (
            "Refunds are issued to the original payment method. Processing times may vary "
            "by bank or card issuer. You will receive an email confirmation once a refund "
            "has been initiated on Bookly's side."
        ),
    },
    "password_reset": {
        "topic": "password_reset",
        "summary": "You can reset your password using the 'Forgot password' link on the sign-in page.",
        "details": (
            "Enter the email address associated with your Bookly account. If we recognize "
            "the email, we will send a secure link that allows you to choose a new password. "
            "For security reasons, the link expires after a limited time."
        ),
    },
}


def get_policy_answer(topic: str) -> PolicyAnswer | None:
    """
    Return the best matching policy answer for a given topic keyword.
    """
    key = topic.strip().lower()
    if key in POLICIES:
        return POLICIES[key]

    # Simple fallback: try partial matches.
    for name, policy in POLICIES.items():
        if key in name or name in key:
            return policy

    return None

