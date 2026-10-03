from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from db import connection
import psycopg2.extras

testimonials_bp = Blueprint("testimonials", __name__)

# GET all testimonials
@testimonials_bp.route("/", methods=["GET"])
def get_testimonials():
    conn = connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM testimonials ORDER BY display_order ASC, created_at DESC")
    items = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(items)

# ADD a new testimonial
@testimonials_bp.route("/", methods=["POST"])
@jwt_required()
def add_testimonial():
    data = request.get_json()
    client_name = data.get("client_name")
    role_location = data.get("role_location")
    project_type = data.get("project_type")
    quote = data.get("quote")
    image_url = data.get("image_url")

    if not all([client_name, quote, image_url]):
        return jsonify({"error": "Missing required fields (client_name, quote, image_url)"}), 400

    conn = connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        INSERT INTO testimonials (client_name, role_location, project_type, quote, image_url)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *;
    """, (client_name, role_location, project_type, quote, image_url))
    new_item = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_item), 201

# EDIT an existing testimonial
@testimonials_bp.route("/<int:item_id>", methods=["PUT"])
@jwt_required()
def update_testimonial(item_id):
    data = request.get_json()
    conn = connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        UPDATE testimonials
        SET client_name = %s, role_location = %s, project_type = %s, quote = %s, image_url = %s
        WHERE id = %s
        RETURNING *;
    """, (
        data.get("client_name"), data.get("role_location"),
        data.get("project_type"), data.get("quote"),
        data.get("image_url"), item_id
    ))
    updated_item = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not updated_item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(updated_item)

# DELETE a testimonial
@testimonials_bp.route("/<int:item_id>", methods=["DELETE"])
@jwt_required()
def delete_testimonial(item_id):
    conn = connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM testimonials WHERE id = %s RETURNING id;", (item_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not deleted:
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"message": "Deleted successfully"})