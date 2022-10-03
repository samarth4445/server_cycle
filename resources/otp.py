from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import otp, endTrip
from functions.functions import otpGenerator

blp = Blueprint("otp", __name__, description="OTP generation.")

@blp.route("/otp_gen")
class OtpGenerator(MethodView):
    def post(self):
        request_data = request.get_json()
        otp[request_data["cycleid"]] = otpGenerator()
        endTrip[request_data["cycleid"]] = 0
        return {"otp": otp[request_data["cycleid"]]}, 201

@blp.route("/otp_get/<int:cycleid>")
class OtpGet(MethodView):
    def get(self, cycleid):
        if cycleid not in otp or otp[cycleid] is None:
            return {"otp": None}, 404
        return {"otp": otp[cycleid]}

@blp.route("/endtrip/<int:cycleid>")
class EndTrip(MethodView):
    def get(self, cycleid):
        otp[cycleid] = None
        endTrip[cycleid] = 1
        return {"message": "Trip ended."}

@blp.route("/information/<int:cycleid>")
class Infomation(MethodView):
    def get(self, cycleid):
        return endTrip[cycleid]

