from firebase_admin import initialize_app, db
from firebase_functions import https_fn
import flask
from flask import request
from google.cloud import firestore
import datetime
import os

initialize_app()
app = flask.Flask(__name__)
# db = firestore.Client()

# # Create a client to interact with Firestore
db = firestore.Client()


@app.get("/getImage/<image_id>")
def get_image_details(image_id):
    #get the image url and displayname
    doc_ref = db.collection("mcd-app-ui-skin").document("image"+image_id)
    return flask.jsonify(url=doc_ref.get(field_paths={"url"}).get("url"), displayName=doc_ref.get(field_paths={"displayName"}).get("displayName"))


@app.post("/setImage")
def set_field_office():
    if not request.args:
        return flask.jsonify({"result": str(request.args)})
   
    request_json = request.json
    if "image_id" not in request_json:
        return flask.jsonify({"result": "Missing parameter `image_id`"})
    image_id = request.args["image_id"]

    if "image_url" not in request_json:
        return flask.jsonify({"result": "Missing parameter `image_url`"})
    image_url = request.args["image_url"]

    if "image_display_name" not in request_json:
        return flask.jsonify({"result": "Missing parameter `image_display_name`"})
    image_display_name = request.args["image_display_name"]
    
    doc_ref = db.collection("mcd-app-ui-skin").document("image"+image_id)
    doc_ref.set({"url": image_url, "displayName": image_display_name})
    return flask.jsonify({"result": "SUCCESS"})


@https_fn.on_request()
def main(req: https_fn.Request) -> https_fn.Response:
    with app.request_context(req.environ):
        return app.full_dispatch_request()
