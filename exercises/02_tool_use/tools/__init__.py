"""
Mock tool implementations for workshop exercises.

These simulate external APIs and services so exercises can run without
real integrations. Each function has a clear signature, type hints, and
returns structured data.
"""

import random
from datetime import datetime, timezone


def get_weather(city: str, unit: str = "celsius") -> dict:
    """Get current weather for a city (mock data)."""
    weather_data = {
        "berlin": {"temp_c": 18, "condition": "Partly cloudy", "humidity": 65},
        "tokyo": {"temp_c": 28, "condition": "Sunny", "humidity": 45},
        "new york": {"temp_c": 22, "condition": "Clear", "humidity": 55},
        "london": {"temp_c": 15, "condition": "Rainy", "humidity": 80},
        "sydney": {"temp_c": 24, "condition": "Sunny", "humidity": 50},
        "paris": {"temp_c": 20, "condition": "Overcast", "humidity": 70},
    }

    city_lower = city.lower()
    if city_lower not in weather_data:
        return {"error": f"Weather data not available for '{city}'"}

    data = weather_data[city_lower]
    temp = data["temp_c"]

    if unit.lower() == "fahrenheit":
        temp = round(temp * 9 / 5 + 32)
        unit_label = "°F"
    else:
        unit_label = "°C"

    return {
        "city": city,
        "temperature": temp,
        "unit": unit_label,
        "condition": data["condition"],
        "humidity": data["humidity"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def convert_temperature(value: float, from_unit: str, to_unit: str) -> dict:
    """Convert temperature between Celsius and Fahrenheit."""
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    if from_unit == "celsius" and to_unit == "fahrenheit":
        result = round(value * 9 / 5 + 32, 1)
    elif from_unit == "fahrenheit" and to_unit == "celsius":
        result = round((value - 32) * 5 / 9, 1)
    else:
        return {"error": f"Cannot convert from '{from_unit}' to '{to_unit}'"}

    return {
        "original": value,
        "from_unit": from_unit,
        "converted": result,
        "to_unit": to_unit,
    }


def search_database(query: str, category: str = "all") -> dict:
    """Search a mock product database."""
    products = [
        {"id": "P001", "name": "Wireless Headphones", "category": "electronics", "price": 79.99, "rating": 4.5},
        {"id": "P002", "name": "Running Shoes", "category": "sports", "price": 129.99, "rating": 4.2},
        {"id": "P003", "name": "Coffee Maker", "category": "kitchen", "price": 49.99, "rating": 4.7},
        {"id": "P004", "name": "Laptop Stand", "category": "electronics", "price": 34.99, "rating": 4.3},
        {"id": "P005", "name": "Yoga Mat", "category": "sports", "price": 24.99, "rating": 4.6},
        {"id": "P006", "name": "Blender", "category": "kitchen", "price": 89.99, "rating": 4.1},
    ]

    query_lower = query.lower()
    results = [
        p
        for p in products
        if query_lower in p["name"].lower()
        and (category == "all" or p["category"] == category.lower())
    ]

    return {
        "query": query,
        "category": category,
        "results": results,
        "total": len(results),
    }


def calculate(expression: str) -> dict:
    """
    Evaluate a simple math expression.

    Only supports basic arithmetic for safety — no arbitrary code execution.
    """
    allowed_chars = set("0123456789+-*/().% ")
    if not all(c in allowed_chars for c in expression):
        return {"error": "Expression contains invalid characters. Only basic arithmetic is supported."}

    try:
        result = eval(expression, {"__builtins__": {}})  # noqa: S307 — restricted builtins
        return {"expression": expression, "result": result}
    except (SyntaxError, ZeroDivisionError, TypeError) as e:
        return {"error": f"Cannot evaluate '{expression}': {e}"}


def get_stock_price(ticker: str) -> dict:
    """Get mock stock price data for a ticker symbol."""
    stocks = {
        "AAPL": {"name": "Apple Inc.", "price": 187.44, "change": 1.23},
        "GOOGL": {"name": "Alphabet Inc.", "price": 141.80, "change": -0.45},
        "MSFT": {"name": "Microsoft Corp.", "price": 378.91, "change": 2.15},
        "AMZN": {"name": "Amazon.com Inc.", "price": 178.25, "change": 0.88},
        "TSLA": {"name": "Tesla Inc.", "price": 248.42, "change": -3.21},
        "NVDA": {"name": "NVIDIA Corp.", "price": 495.22, "change": 5.67},
    }

    ticker_upper = ticker.upper()
    if ticker_upper not in stocks:
        return {"error": f"Stock data not available for '{ticker}'"}

    data = stocks[ticker_upper]
    return {
        "ticker": ticker_upper,
        "name": data["name"],
        "price": data["price"],
        "change": data["change"],
        "change_percent": round(data["change"] / data["price"] * 100, 2),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def lookup_order(order_id: str) -> dict:
    """Look up a customer order by ID (mock data)."""
    orders = {
        "ORD-1001": {
            "order_id": "ORD-1001",
            "customer": "Alice Johnson",
            "items": [
                {"product": "Wireless Headphones", "qty": 1, "price": 79.99},
                {"product": "Laptop Stand", "qty": 1, "price": 34.99},
            ],
            "total": 114.98,
            "status": "delivered",
            "date": "2025-01-15",
        },
        "ORD-1002": {
            "order_id": "ORD-1002",
            "customer": "Bob Smith",
            "items": [
                {"product": "Running Shoes", "qty": 1, "price": 129.99},
            ],
            "total": 129.99,
            "status": "shipped",
            "date": "2025-02-20",
        },
        "ORD-1003": {
            "order_id": "ORD-1003",
            "customer": "Carol Davis",
            "items": [
                {"product": "Coffee Maker", "qty": 1, "price": 49.99},
                {"product": "Blender", "qty": 1, "price": 89.99},
            ],
            "total": 139.98,
            "status": "processing",
            "date": "2025-03-01",
        },
    }

    if order_id not in orders:
        return {"error": f"Order '{order_id}' not found"}

    return orders[order_id]


def search_faq(question: str) -> dict:
    """Search the FAQ knowledge base (mock data)."""
    faqs = [
        {
            "topic": "returns",
            "question": "What is your return policy?",
            "answer": "You can return any item within 30 days of purchase for a full refund. Items must be in original packaging.",
        },
        {
            "topic": "shipping",
            "question": "How long does shipping take?",
            "answer": "Standard shipping takes 5-7 business days. Express shipping (2-3 days) is available for $9.99.",
        },
        {
            "topic": "billing",
            "question": "How do I update my payment method?",
            "answer": "Go to Account Settings → Payment Methods → Add or edit your card details.",
        },
        {
            "topic": "account",
            "question": "How do I reset my password?",
            "answer": "Click 'Forgot Password' on the login page. We'll send a reset link to your registered email.",
        },
    ]

    question_lower = question.lower()
    matches = [
        faq
        for faq in faqs
        if any(
            word in question_lower
            for word in faq["topic"].split()
            + faq["question"].lower().split()
        )
    ]

    return {
        "query": question,
        "results": matches if matches else [{"answer": "No matching FAQ found. Please contact support."}],
        "total": len(matches),
    }


def process_refund(order_id: str, reason: str) -> dict:
    """Process a refund for an order (mock — always succeeds)."""
    return {
        "order_id": order_id,
        "refund_status": "approved",
        "reason": reason,
        "refund_amount": 114.98 if order_id == "ORD-1001" else 129.99,
        "estimated_days": random.randint(3, 7),
        "reference": f"REF-{random.randint(10000, 99999)}",
    }
