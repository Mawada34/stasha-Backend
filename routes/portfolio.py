from flask import Blueprint, request, jsonify
from db import connection
from flask_jwt_extended import jwt_required
import psycopg2.extras

portfolio_bp = Blueprint("portfolio", __name__)

# GET all portfolio items — public, no auth needed
@portfolio_bp.route("/", methods=["GET"])
def get_portfolio():
    conn = connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM portfolio_items ORDER BY display_order ASC, created_at DESC")
    items = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(items)

# ADD — protected
@portfolio_bp.route("/", methods=["POST"])
@jwt_required()
def add_portfolio_item():
    data = request.get_json()
    title = data.get("title")
    category = data.get("category")
    year = data.get("year")
    image_url = data.get("image_url")

    if not all([title, category, year, image_url]):
        return jsonify({"error": "Missing required fields"}), 400

    conn = connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        INSERT INTO portfolio_items (title, category, year, image_url)
        VALUES (%s, %s, %s, %s)
        RETURNING *;
    """, (title, category, year, image_url))
    new_item = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_item), 201

# EDIT — protected
@portfolio_bp.route("/<int:item_id>", methods=["PUT"])
@jwt_required()
def update_portfolio_item(item_id):
    data = request.get_json()
    conn = connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        UPDATE portfolio_items
        SET title = %s, category = %s, year = %s, image_url = %s
        WHERE id = %s
        RETURNING *;
    """, (data.get("title"), data.get("category"), data.get("year"), data.get("image_url"), item_id))
    updated_item = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not updated_item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(updated_item)

# DELETE — protected
@portfolio_bp.route("/<int:item_id>", methods=["DELETE"])
@jwt_required()
def delete_portfolio_item(item_id):
    conn = connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM portfolio_items WHERE id = %s RETURNING id;", (item_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not deleted:
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"message": "Deleted successfully"})

