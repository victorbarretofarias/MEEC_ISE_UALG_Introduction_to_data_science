"""
Simple Flask API for the Titanic database used in Project 2.1.

Usage
-----
python api.py [--db PATH] [--host HOST] [--port PORT]
"""

from __future__ import annotations

import argparse
import os
import sqlite3
from contextlib import contextmanager

import pandas as pd
from flask import Flask, jsonify, request


HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB = os.path.normpath(os.path.join(HERE, "..", "Data", "titanic.db"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a Flask API over titanic.db.")
    parser.add_argument("--db", default=DEFAULT_DB, help="Path to the SQLite DB.")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind.")
    parser.add_argument("--port", default=5000, type=int, help="Port to bind.")
    return parser.parse_args()


@contextmanager
def get_conn(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def create_app(db_path: str) -> Flask:
    app = Flask(__name__)

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.route("/passengers")
    def passengers():
        limit = request.args.get("limit", default=200, type=int)
        survived = request.args.get("survived", default=None, type=int)
        pclass = request.args.get("pclass", default=None, type=int)

        if limit < 1 or limit > 5000:
            return jsonify({"error": "limit must be between 1 and 5000"}), 400

        sql = "SELECT * FROM passengers WHERE 1=1"
        params: list[int] = []

        if survived in (0, 1):
            sql += " AND survived = ?"
            params.append(survived)

        if pclass in (1, 2, 3):
            sql += " AND pclass = ?"
            params.append(pclass)

        sql += " ORDER BY passenger_id LIMIT ?"
        params.append(limit)

        with get_conn(db_path) as conn:
            df = pd.read_sql(sql, conn, params=params)

        return jsonify(df.to_dict(orient="records"))

    @app.route("/summary/survival-by-class")
    def survival_by_class():
        sql = """
            SELECT
                pclass,
                COUNT(*) AS passengers,
                SUM(COALESCE(survived, 0)) AS survivors,
                ROUND(100.0 * AVG(COALESCE(survived, 0)), 2) AS survival_rate_pct
            FROM passengers
            GROUP BY pclass
            ORDER BY pclass
        """
        with get_conn(db_path) as conn:
            df = pd.read_sql(sql, conn)
        return jsonify(df.to_dict(orient="records"))

    return app


if __name__ == "__main__":
    args = parse_args()
    if not os.path.exists(args.db):
        raise FileNotFoundError(
            f"Database not found: {args.db}\n"
            "Run 'python prepare_titanic_db.py' first."
        )
    app = create_app(args.db)
    app.run(host=args.host, port=args.port, debug=False)
