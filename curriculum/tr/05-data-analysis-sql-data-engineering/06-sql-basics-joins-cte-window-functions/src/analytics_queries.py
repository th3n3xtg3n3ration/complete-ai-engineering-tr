"""Reusable analytical SQL queries using JOIN, CTE, and window functions."""

from __future__ import annotations

import sqlite3
from typing import Any

from database import fetch_all

PAID_ORDER_TOTALS_CTE = """
WITH paid_order_totals AS (
    SELECT
        o.order_id,
        o.customer_id,
        o.order_at,
        SUM(oi.quantity * oi.unit_price) AS order_revenue
    FROM orders AS o
    JOIN order_items AS oi ON oi.order_id = o.order_id
    WHERE o.status = 'paid'
    GROUP BY o.order_id, o.customer_id, o.order_at
)
"""


def paid_orders(
    connection: sqlite3.Connection,
    *,
    minimum_revenue: float = 0.0,
) -> list[dict[str, Any]]:
    """Return paid orders above a parameterized revenue threshold."""

    sql = PAID_ORDER_TOTALS_CTE + """
SELECT order_id, customer_id, order_at, ROUND(order_revenue, 2) AS order_revenue
FROM paid_order_totals
WHERE order_revenue >= :minimum_revenue
ORDER BY order_at, order_id;
"""
    return fetch_all(connection, sql, {"minimum_revenue": minimum_revenue})


def customer_revenue_summary(connection: sqlite3.Connection) -> list[dict[str, Any]]:
    """Use a LEFT JOIN so customers without paid orders remain visible."""

    sql = PAID_ORDER_TOTALS_CTE + """
SELECT
    c.customer_id,
    c.customer_name,
    c.region,
    COUNT(p.order_id) AS paid_order_count,
    ROUND(COALESCE(SUM(p.order_revenue), 0), 2) AS total_revenue,
    ROUND(COALESCE(AVG(p.order_revenue), 0), 2) AS average_order_value
FROM customers AS c
LEFT JOIN paid_order_totals AS p ON p.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name, c.region
ORDER BY total_revenue DESC, c.customer_id;
"""
    return fetch_all(connection, sql)


def order_line_details(connection: sqlite3.Connection) -> list[dict[str, Any]]:
    """Return one row per order line with customer and product attributes."""

    sql = """
SELECT
    o.order_id,
    o.order_at,
    o.status,
    c.customer_id,
    c.customer_name,
    p.product_id,
    p.product_name,
    p.category,
    oi.quantity,
    oi.unit_price,
    ROUND(oi.quantity * oi.unit_price, 2) AS line_revenue
FROM orders AS o
JOIN customers AS c ON c.customer_id = o.customer_id
JOIN order_items AS oi ON oi.order_id = o.order_id
JOIN products AS p ON p.product_id = oi.product_id
ORDER BY o.order_at, o.order_id, p.product_id;
"""
    return fetch_all(connection, sql)


def monthly_paid_revenue(connection: sqlite3.Connection) -> list[dict[str, Any]]:
    """Aggregate paid revenue by calendar month through a CTE."""

    sql = PAID_ORDER_TOTALS_CTE + """
SELECT
    SUBSTR(order_at, 1, 7) AS revenue_month,
    COUNT(*) AS paid_order_count,
    ROUND(SUM(order_revenue), 2) AS total_revenue
FROM paid_order_totals
GROUP BY SUBSTR(order_at, 1, 7)
ORDER BY revenue_month;
"""
    return fetch_all(connection, sql)


def customer_revenue_rank(connection: sqlite3.Connection) -> list[dict[str, Any]]:
    """Rank customers with DENSE_RANK after building a customer-level CTE."""

    sql = PAID_ORDER_TOTALS_CTE + """,
customer_totals AS (
    SELECT
        c.customer_id,
        c.customer_name,
        COALESCE(SUM(p.order_revenue), 0) AS total_revenue
    FROM customers AS c
    LEFT JOIN paid_order_totals AS p ON p.customer_id = c.customer_id
    GROUP BY c.customer_id, c.customer_name
)
SELECT
    customer_id,
    customer_name,
    ROUND(total_revenue, 2) AS total_revenue,
    DENSE_RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank
FROM customer_totals
ORDER BY revenue_rank, customer_id;
"""
    return fetch_all(connection, sql)


def running_customer_revenue(connection: sqlite3.Connection) -> list[dict[str, Any]]:
    """Compute cumulative paid revenue per customer."""

    sql = PAID_ORDER_TOTALS_CTE + """
SELECT
    customer_id,
    order_id,
    order_at,
    ROUND(order_revenue, 2) AS order_revenue,
    ROUND(
        SUM(order_revenue) OVER (
            PARTITION BY customer_id
            ORDER BY order_at, order_id
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ),
        2
    ) AS running_revenue
FROM paid_order_totals
ORDER BY customer_id, order_at, order_id;
"""
    return fetch_all(connection, sql)


def order_gap_days(connection: sqlite3.Connection) -> list[dict[str, Any]]:
    """Use LAG to calculate days since the previous paid order."""

    sql = PAID_ORDER_TOTALS_CTE + """,
with_previous AS (
    SELECT
        customer_id,
        order_id,
        order_at,
        LAG(order_at) OVER (
            PARTITION BY customer_id
            ORDER BY order_at, order_id
        ) AS previous_order_at
    FROM paid_order_totals
)
SELECT
    customer_id,
    order_id,
    order_at,
    previous_order_at,
    CASE
        WHEN previous_order_at IS NULL THEN NULL
        ELSE CAST(JULIANDAY(order_at) - JULIANDAY(previous_order_at) AS INTEGER)
    END AS days_since_previous
FROM with_previous
ORDER BY customer_id, order_at, order_id;
"""
    return fetch_all(connection, sql)


def customers_without_orders(connection: sqlite3.Connection) -> list[dict[str, Any]]:
    """Use NOT EXISTS as an anti-join."""

    sql = """
SELECT c.customer_id, c.customer_name
FROM customers AS c
WHERE NOT EXISTS (
    SELECT 1
    FROM orders AS o
    WHERE o.customer_id = c.customer_id
)
ORDER BY c.customer_id;
"""
    return fetch_all(connection, sql)


def top_product_per_category(connection: sqlite3.Connection) -> list[dict[str, Any]]:
    """Use ROW_NUMBER to select the highest-revenue product per category."""

    sql = """
WITH product_revenue AS (
    SELECT
        p.category,
        p.product_id,
        p.product_name,
        SUM(oi.quantity * oi.unit_price) AS total_revenue
    FROM products AS p
    JOIN order_items AS oi ON oi.product_id = p.product_id
    JOIN orders AS o ON o.order_id = oi.order_id
    WHERE o.status = 'paid'
    GROUP BY p.category, p.product_id, p.product_name
),
ranked AS (
    SELECT
        category,
        product_id,
        product_name,
        total_revenue,
        ROW_NUMBER() OVER (
            PARTITION BY category
            ORDER BY total_revenue DESC, product_id
        ) AS position
    FROM product_revenue
)
SELECT
    category,
    product_id,
    product_name,
    ROUND(total_revenue, 2) AS total_revenue
FROM ranked
WHERE position = 1
ORDER BY category;
"""
    return fetch_all(connection, sql)


if __name__ == "__main__":
    from database import build_demo_database

    database = build_demo_database()
    print(customer_revenue_summary(database))
    print(monthly_paid_revenue(database))
    print(customer_revenue_rank(database))
