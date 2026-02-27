from __future__ import annotations

from datetime import date, timedelta
from typing import TypedDict


class User(TypedDict):
    id: str
    name: str
    email: str
    city: str
    country: str


class OrderItem(TypedDict):
    sku: str
    title: str
    quantity: int
    unit_price: float


class Order(TypedDict):
    id: str
    user_id: str
    status: str
    total: float
    currency: str
    items: list[OrderItem]
    ordered_at: date
    shipped_at: date | None
    delivered_at: date | None
    carrier: str | None
    tracking_number: str | None
    destination_city: str
    destination_country: str


TODAY = date.today()


USERS: list[User] = [
    {
        "id": "u_001",
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "city": "New York",
        "country": "US",
    },
    {
        "id": "u_002",
        "name": "Brian Lee",
        "email": "brian@example.com",
        "city": "San Francisco",
        "country": "US",
    },
    {
        "id": "u_003",
        "name": "Carla Martinez",
        "email": "carla@example.com",
        "city": "Toronto",
        "country": "CA",
    },
]


ORDERS: list[Order] = [
    {
        "id": "B-1001",
        "user_id": "u_001",
        "status": "delivered",
        "total": 42.50,
        "currency": "USD",
        "items": [
            {
                "sku": "BK-9780143127741",
                "title": "The Martian",
                "quantity": 1,
                "unit_price": 15.00,
            },
            {
                "sku": "BK-9780307887443",
                "title": "Ready Player One",
                "quantity": 1,
                "unit_price": 27.50,
            },
        ],
        "ordered_at": TODAY - timedelta(days=14),
        "shipped_at": TODAY - timedelta(days=12),
        "delivered_at": TODAY - timedelta(days=9),
        "carrier": "UPS",
        "tracking_number": "1Z999AA10123456784",
        "destination_city": "New York",
        "destination_country": "US",
    },
    {
        "id": "B-1002",
        "user_id": "u_001",
        "status": "shipped",
        "total": 19.99,
        "currency": "USD",
        "items": [
            {
                "sku": "BK-9780062316110",
                "title": "The Alchemist",
                "quantity": 1,
                "unit_price": 19.99,
            },
        ],
        "ordered_at": TODAY - timedelta(days=5),
        "shipped_at": TODAY - timedelta(days=3),
        "delivered_at": None,
        "carrier": "FedEx",
        "tracking_number": "61299999999999999999",
        "destination_city": "New York",
        "destination_country": "US",
    },
    {
        "id": "B-1003",
        "user_id": "u_002",
        "status": "processing",
        "total": 59.00,
        "currency": "USD",
        "items": [
            {
                "sku": "BK-9780385472579",
                "title": "Zen and the Art of Motorcycle Maintenance",
                "quantity": 1,
                "unit_price": 18.00,
            },
            {
                "sku": "BK-9780553293357",
                "title": "Dune",
                "quantity": 1,
                "unit_price": 41.00,
            },
        ],
        "ordered_at": TODAY - timedelta(days=1),
        "shipped_at": None,
        "delivered_at": None,
        "carrier": None,
        "tracking_number": None,
        "destination_city": "San Francisco",
        "destination_country": "US",
    },
    {
        "id": "B-1004",
        "user_id": "u_003",
        "status": "delayed",
        "total": 24.99,
        "currency": "CAD",
        "items": [
            {
                "sku": "BK-9780307277671",
                "title": "The Road",
                "quantity": 1,
                "unit_price": 24.99,
            },
        ],
        "ordered_at": TODAY - timedelta(days=10),
        "shipped_at": TODAY - timedelta(days=7),
        "delivered_at": None,
        "carrier": "Canada Post",
        "tracking_number": "CP123456789CA",
        "destination_city": "Toronto",
        "destination_country": "CA",
    },
]


REFUND_WINDOW_DAYS = 30

