from flask import Blueprint, request, jsonify
from db import connection
import psycopg2.extras
from flask_jwt_extended import jwt_required
services_bp = Blueprint("services", __name__)

# GET all services
@services_bp.route("/", methods=["GET"])
def get_services():
    conn = connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM services ORDER BY display_order ASC, id ASC")
    items = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(items)

# ADD a new service
@services_bp.route("/", methods=["POST"])
@jwt_required()
def add_service():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")

    if not all([name, description]):
        return jsonify({"error": "Missing required fields (name, description)"}), 400

    conn = connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        INSERT INTO services (name, description)
        VALUES (%s, %s)
        RETURNING *;
    """, (name, description))
    new_item = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_item), 201

# EDIT an existing service
@services_bp.route("/<int:item_id>", methods=["PUT"])
@jwt_required()
def update_service(item_id):
    data = request.get_json()
    conn = connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        UPDATE services
        SET name = %s, description = %s
        WHERE id = %s
        RETURNING *;
    """, (data.get("name"), data.get("description"), item_id))
    updated_item = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not updated_item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(updated_item)

# DELETE a service
@services_bp.route("/<int:item_id>", methods=["DELETE"])
@jwt_required()
def delete_service(item_id):
    conn = connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM services WHERE id = %s RETURNING id;", (item_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not deleted:
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"message": "Deleted successfully"})