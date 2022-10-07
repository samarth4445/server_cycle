from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import position
from functions.functions import otpGenerator

blp = Blueprint("location", __name__, description="Position of cycles.")

@blp.route("/location")
class Location(MethodView):
    def get(self):
        return {"positions": position}
    
    def post(self):
        request_data = request.get_json()
        cycleid = request_data["cycleid"]
        for i in position:
            if i["cycleid"] == cycleid:
                i["longitude"] = request_data["longitude"]
                i["latitude"] = request_data["latitude"]
                return {"message": "Information updated."}

        position.append({"longitude": request_data["longitude"], "latitude": request_data["latitude"], "cycleid": request_data["cycleid"]})
        return {"message": "Information sent."}, 201
