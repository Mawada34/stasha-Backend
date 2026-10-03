from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required
import os
import cloudinary
import cloudinary.uploader

upload_bp=Blueprint("upload",__name__)

cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET")

)
@upload_bp.route("/",methods=["POST"])
@jwt_required()
def upload_image():
    if "file" not in request.files:
        return jsonify({"error":"No File Provided"}),400

    file = request.files["file"]

    if file.filename=="":
        return jsonify({"error":"No file Provided"}),400

    try:
        result=cloudinary.uploader.upload(file, folder="stasha_interior")
        return jsonify ({"image_url":result["secure_url"]}),201
    except Exception as e:
        return jsonify({"error":str(e)}) ,500