from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    data_dict = {item["id"]: item for item in data}
    picture = data_dict.get(id)  # Use dictionary lookup
    if picture:
        return jsonify(picture), 200
    return jsonify({"message": "Picture not found"}), 404  # Return 404 for missing records


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    data_dict = {item["id"]: item for item in data}
    picture = request.get_json()
    picture_id = picture["id"]
    if picture_id in data_dict:  # Check if ID already exists
        return jsonify({"Message": f"picture with id {picture_id} already present"}), 302
    
    data.append(picture)
    return jsonify(picture), 201  # 201 Created
######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    data_dict = {item["id"]: item for item in data}
    picture_update = request.get_json()
    if id not in data_dict:
        return jsonify({"message": "picture not found"}), 404

    data_dict[id].update(picture_update)
    
    for index, item in enumerate(data):
        if item["id"] == id:
            data[index] = data_dict[id]
            break

    return jsonify(data_dict[id]), 200  # OK
    

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for index, picture in enumerate(data):
        if picture["id"] == id:
            del data[index]  # Delete the picture from the list
            return "", 204  # Return 204 No Content

    # If the picture was not found, return a 404 error
    return jsonify({"message": "picture not found"}), 404
