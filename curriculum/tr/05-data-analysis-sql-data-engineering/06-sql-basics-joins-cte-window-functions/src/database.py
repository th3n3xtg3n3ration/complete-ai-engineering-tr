"""SQLite setup and safe execution helpers for the SQL lesson."""

from __future__ import annotations

from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from pathlib import Path
import sqlite3
from typing import Any

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    region TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    list_price REAL NOT NULL CHECK (list_price >= 0)
);

CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    order_at TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('paid', 'cancelled', 'refunded')),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS order_items (
    order_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price REAL NOT NULL CHECK (unit_price >= 0),
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
"""

CUSTOMERS = (
    ("c1", "Ada", "north", "2025-01-10"),
    ("c2", "Bora", "south", "2025-02-12"),
    ("c3", "Ceren", "north", "2025-03-18"),
    ("c4", "Deniz", "west", "2025-04-20"),
)

PRODUCTS = (
    ("p1", "Laptop", "electronics", 1000.0),
    ("p2", "Mouse", "electronics", 25.0),
    ("p3", "Desk", "furniture", 300.0),
    ("p4", "Chair", "furniture", 150.0),
)

ORDERS = (
    ("o1", "c1", "2026-01-05", "paid"),
    ("o2", "c1", "2026-02-10", "paid"),
    ("o3", "c2", "2026-01-15", "cancelled"),
    ("o4", "c2", "2026-03-01", "paid"),
    ("o5", "c3", "2026-02-20", "paid"),
)

ORDER_ITEMS = (
    ("o1", "p1", 1, 1000.0),
    ("o1", "p2", 2, 20.0),
    ("o2", "p2", 3, 22.0),
    ("o3", "p3", 1, 300.0),
    ("o4", "p3", 1, 280.0),
    ("o4", "p4", 2, 140.0),
    ("o5", "p4", 4, 150.0),
)


def connect(path: str | Path = ":memory:") -> sqlite3.Connection:
    """Create a SQLite connection with integrity checks enabled."""

    connection = sqlite3.connect(str(path))
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_schema(connection: sqlite3.Connection) -> None:
    """Create the lesson schema."""

    connection.executescript(SCHEMA_SQL)
    connection.commit()


def seed_demo_data(connection: sqlite3.Connection) -> None:
    """Insert deterministic lesson data into an empty schema."""

    connection.executemany("INSERT INTO customers VALUES (?, ?, ?, ?)", CUSTOMERS)
    connection.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", PRODUCTS)
    connection.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", ORDERS)
    connection.executemany("INSERT INTO order_items VALUES (?, ?, ?, ?)", ORDER_ITEMS)
    connection.commit()


def build_demo_database(path: str | Path = ":memory:") -> sqlite3.Connection:
    """Create, populate, and return the deterministic demo database."""

    connection = connect(path)
    create_schema(connection)
    seed_demo_data(connection)
    return connection


def fetch_all(
    connection: sqlite3.Connection,
    sql: str,
    parameters: Sequence[Any] | Mapping[str, Any] = (),
) -> list[dict[str, Any]]:
    """Execute a parameterized query and return dictionaries."""

    cursor = connection.execute(sql, parameters)
    return [dict(row) for row in cursor.fetchall()]


@contextmanager
def transaction(connection: sqlite3.Connection) -> Iterator[sqlite3.Connection]:
    """Commit on success and roll back when the block raises."""

    try:
        connection.execute("BEGIN")
        yield connection
    except Exception:
        connection.rollback()
        raise
    else:
        connection.commit()


def table_exists(connection: sqlite3.Connection, table_name: str) -> bool:
    """Return whether a user table exists."""

    row = connection.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?",
        (table_name,),
    ).fetchone()
    return row is not None


def row_count(connection: sqlite3.Connection, table_name: str) -> int:
    """Count rows for a trusted lesson table name."""

    allowed = {"customers", "products", "orders", "order_items"}
    if table_name not in allowed:
        raise ValueError(f"unsupported table: {table_name}")
    return int(connection.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0])


if __name__ == "__main__":
    database = build_demo_database()
    for table in ("customers", "products", "orders", "order_items"):
        print(table, row_count(database, table))
