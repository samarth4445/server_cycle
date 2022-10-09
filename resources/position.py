import geopy.distance
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

        centre = (18.492583, 74.0255360)
        current_pos = (float(request_data["longitude"]), float(request_data["latitude"]))

        position_magnitude = geopy.distance.geodesic(centre, current_pos).km
        cycleid = request_data["cycleid"]

        if position_magnitude > 2.200408063912031:
            for i in position:
                if i["cycleid"] == cycleid:
                    i["longitude"] = request_data["longitude"]
                    i["latitude"] = request_data["latitude"]
                    i["fine"] = True
                    return {"message": "You are outside the university, you will be fined."}

        for i in position:
            if i["cycleid"] == cycleid:
                i["longitude"] = request_data["longitude"]
                i["latitude"] = request_data["latitude"]
                return {"message": "Information updated."}

        position.append({"longitude": request_data["longitude"], "latitude": request_data["latitude"], "cycleid": request_data["cycleid"], "fine": False})
        return {"message": "Information sent."}, 201
