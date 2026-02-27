from __future__ import annotations

from datetime import date
from typing import Any, TypedDict

from .data import ORDERS, REFUND_WINDOW_DAYS, USERS


class OrderLookupResult(TypedDict):
    found: bool
    reason: str
    order: dict[str, Any] | None


class RefundEligibilityResult(TypedDict):
    eligible: bool
    reason: str
    refundable_amount: float
    currency: str


def _normalize(s: str) -> str:
    return s.strip().lower()


def lookup_order(order_id: str, email_or_last_name: str) -> OrderLookupResult:
    """
    Look up an order by id and email or last name.
    """
    order_id_norm = _normalize(order_id)
    email_name_norm = _normalize(email_or_last_name)

    matching_orders = [o for o in ORDERS if _normalize(o["id"]) == order_id_norm]
    if not matching_orders:
        return {
            "found": False,
            "reason": "No order found with the provided order id.",
            "order": None,
        }

    order = matching_orders[0]
    user = next((u for u in USERS if u["id"] == order["user_id"]), None)
    if user is None:
        return {
            "found": False,
            "reason": "Order is associated with an unknown customer record.",
            "order": None,
        }

    if email_name_norm not in {_normalize(user["email"]), _normalize(user["name"].split()[-1])}:
        return {
            "found": False,
            "reason": "Customer details do not match the order on file.",
            "order": None,
        }

    enriched = {
        "id": order["id"],
        "status": order["status"],
        "total": order["total"],
        "currency": order["currency"],
        "items": order["items"],
        "ordered_at": order["ordered_at"].isoformat(),
        "shipped_at": order["shipped_at"].isoformat() if order["shipped_at"] else None,
        "delivered_at": order["delivered_at"].isoformat()
        if order["delivered_at"]
        else None,
        "carrier": order["carrier"],
        "tracking_number": order["tracking_number"],
        "destination_city": order["destination_city"],
        "destination_country": order["destination_country"],
        "customer_name": user["name"],
        "customer_email": user["email"],
    }

    return {
        "found": True,
        "reason": "Order located successfully.",
        "order": enriched,
    }


def list_recent_orders(email: str, limit: int = 3) -> list[dict[str, Any]]:
    """
    Return recent orders for a given customer email, newest first.
    """
    email_norm = _normalize(email)
    user_ids = [u["id"] for u in USERS if _normalize(u["email"]) == email_norm]
    if not user_ids:
        return []

    user_orders = [o for o in ORDERS if o["user_id"] in user_ids]
    user_orders.sort(key=lambda o: o["ordered_at"], reverse=True)

    result: list[dict[str, Any]] = []
    for order in user_orders[:limit]:
        result.append(
            {
                "id": order["id"],
                "status": order["status"],
                "total": order["total"],
                "currency": order["currency"],
                "ordered_at": order["ordered_at"].isoformat(),
            }
        )
    return result


def evaluate_refund_eligibility(order_id: str, reason: str) -> RefundEligibilityResult:
    """
    Evaluate whether an order is eligible for a refund based on synthetic rules.
    """
    order_id_norm = _normalize(order_id)
    reason_norm = _normalize(reason)

    matching_orders = [o for o in ORDERS if _normalize(o["id"]) == order_id_norm]
    if not matching_orders:
        return {
            "eligible": False,
            "reason": "No order found with the provided order id.",
            "refundable_amount": 0.0,
            "currency": "USD",
        }

    order = matching_orders[0]
    currency = order["currency"]

    today = date.today()
    delivered_at = order["delivered_at"]

    if delivered_at is None:
        return {
            "eligible": False,
            "reason": "Order has not been delivered yet; refunds are not available.",
            "refundable_amount": 0.0,
            "currency": currency,
        }

    days_since_delivery = (today - delivered_at).days
    if days_since_delivery > REFUND_WINDOW_DAYS:
        return {
            "eligible": False,
            "reason": f"Order was delivered {days_since_delivery} days ago, "
            f"which is outside the {REFUND_WINDOW_DAYS}-day return window.",
            "refundable_amount": 0.0,
            "currency": currency,
        }

    damage_keywords = {"damaged", "defective", "wrong item", "misprint"}
    is_damaged = any(word in reason_norm for word in damage_keywords)

    refundable_amount = order["total"]
    explanation = "Order is within the return window."
    if is_damaged:
        explanation = (
            "Order is within the return window and the item is reported as defective."
        )

    return {
        "eligible": True,
        "reason": explanation,
        "refundable_amount": refundable_amount,
        "currency": currency,
    }

