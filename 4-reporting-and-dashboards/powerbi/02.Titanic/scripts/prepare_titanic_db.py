"""
Build a SQLite database from the Titanic CSV used in Project 2.1.

Usage
-----
python prepare_titanic_db.py [--csv PATH] [--db PATH]
"""

from __future__ import annotations

import argparse
import os
import sqlite3

import pandas as pd


HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV = os.path.normpath(os.path.join(HERE, "..", "Data", "Titanic.csv"))
DEFAULT_DB = os.path.normpath(os.path.join(HERE, "..", "Data", "titanic.db"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build titanic.db from Titanic.csv.")
    parser.add_argument("--csv", default=DEFAULT_CSV, help="Path to the Titanic CSV.")
    parser.add_argument("--db", default=DEFAULT_DB, help="Path to the output SQLite DB.")
    return parser.parse_args()


def normalize_number(value: object) -> float | None:
    if value is None or pd.isna(value):
        return None

    text = str(value).strip()
    if not text:
        return None

    text = text.replace(" ", "")

    if "," in text:
        text = text.replace(".", "")
        text = text.replace(",", ".")
    elif text.count(".") > 1:
        head, tail = text.rsplit(".", 1)
        text = head.replace(".", "") + "." + tail

    try:
        return float(text)
    except ValueError:
        return None


def load_titanic_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, sep=";", encoding="utf-8-sig", dtype=str)
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(".", "_", regex=False)
        .str.replace(r"[^a-z0-9_]+", "_", regex=True)
        .str.strip("_")
    )

    for column in df.columns:
        df[column] = df[column].map(lambda x: x.strip() if isinstance(x, str) else x)

    numeric_columns = ["pclass", "survived", "age", "sibsp", "parch", "fare", "body"]
    for column in numeric_columns:
        df[column] = df[column].map(normalize_number)

    integer_columns = ["pclass", "survived", "sibsp", "parch", "body"]
    for column in integer_columns:
        df[column] = df[column].astype("Int64")

    df.insert(0, "passenger_id", range(1, len(df) + 1))
    return df


def write_db(df: pd.DataFrame, db_path: str) -> None:
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("DROP TABLE IF EXISTS passengers")
        df.to_sql("passengers", conn, index=False)
        conn.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_passengers_id "
            "ON passengers(passenger_id)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_passengers_class_survived "
            "ON passengers(pclass, survived)"
        )
        conn.commit()
    finally:
        conn.close()


def main() -> None:
    args = parse_args()
    df = load_titanic_csv(args.csv)
    write_db(df, args.db)
    print(f"Created {args.db} with {len(df)} passengers.")


if __name__ == "__main__":
    main()
