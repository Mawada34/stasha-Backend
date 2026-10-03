from flask import Blueprint, request, jsonify
from db import connection
from flask_jwt_extended import jwt_required
import psycopg2.extras

content_bp = Blueprint("content", __name__)

# ---------- HERO ----------
@content_bp.route("/hero", methods=["GET"])
def get_hero():
    conn = connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM hero_content WHERE id = 1;")
    item = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(item or {})

@content_bp.route("/hero", methods=["PUT"])
def update_hero():
    data = request.get_json()
    conn = connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        INSERT INTO hero_content (id, headline, subheadline, video_url, years_count, projects_count, satisfaction_pct)
        VALUES (1, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            headline = EXCLUDED.headline,
            subheadline = EXCLUDED.subheadline,
            video_url = EXCLUDED.video_url,
            years_count = EXCLUDED.years_count,
            projects_count = EXCLUDED.projects_count,
            satisfaction_pct = EXCLUDED.satisfaction_pct
        RETURNING *;
    """, (
        data.get("headline"), data.get("subheadline"), data.get("video_url"),
        data.get("years_count"), data.get("projects_count"), data.get("satisfaction_pct")
    ))
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(updated)

# ---------- ABOUT ----------
@content_bp.route("/about", methods=["GET"])
def get_about():
    conn = connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM about_content WHERE id = 1;")
    item = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(item or {})

@content_bp.route("/about", methods=["PUT"])
@jwt_required()
def update_about():
    data = request.get_json()
    conn = connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        INSERT INTO about_content (id, image_url, paragraph_1, paragraph_2, badge_number)
        VALUES (1, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            image_url = EXCLUDED.image_url,
            paragraph_1 = EXCLUDED.paragraph_1,
            paragraph_2 = EXCLUDED.paragraph_2,
            badge_number = EXCLUDED.badge_number
        RETURNING *;
    """, (
        data.get("image_url"), data.get("paragraph_1"),
        data.get("paragraph_2"), data.get("badge_number")
    ))
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(updated)

# ---------- SITE SETTINGS ----------
@content_bp.route("/settings", methods=["GET"])
def get_settings():
    conn = connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM site_settings WHERE id = 1;")
    item = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(item or {})

@content_bp.route("/settings", methods=["PUT"])
@jwt_required()
def update_settings():
    data = request.get_json()
    conn = connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        INSERT INTO site_settings (id, booking_url, footer_tagline, instagram_url, pinterest_url, linkedin_url)
        VALUES (1, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            booking_url = EXCLUDED.booking_url,
            footer_tagline = EXCLUDED.footer_tagline,
            instagram_url = EXCLUDED.instagram_url,
            pinterest_url = EXCLUDED.pinterest_url,
            linkedin_url = EXCLUDED.linkedin_url
        RETURNING *;
    """, (
        data.get("booking_url"), data.get("footer_tagline"),
        data.get("instagram_url"), data.get("pinterest_url"), data.get("linkedin_url")
    ))
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(updated)