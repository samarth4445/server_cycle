from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import otp, endTrip, validation
from functions.functions import otpGenerator

blp = Blueprint("otp", __name__, description="OTP generation.")

@blp.route("/otp_gen")
class OtpGenerator(MethodView):
    def post(self):
        request_data = request.get_json()
        if otp[request_data["cycleid"]] == None:
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
        return {"endTrip": endTrip[cycleid]}, 200

    def post(self, cycleid):
        request_data = request.get_json()
        if endTrip[cycleid] != 1:
            correctOTPEntered = request_data["correctOTPEntered"]
            validation[cycleid] = correctOTPEntered
            return {"message": "Information sent."}, 201
        return {"message": "Cycle not in use."}, 400

@blp.route("/validation/<int:cycleid>")
class ValidateOTP(MethodView):
    def get(self, cycleid):
        return {"validation": validation[cycleid]}
