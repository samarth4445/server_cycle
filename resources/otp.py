from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import otp, endTrip, validation, position
from functions.functions import otpGenerator, validate
import threading
import asyncio

# docker build -t gocycle-server .
# docker run -dp 5005:5000 -w /app -v "$(pwd):/app" gocycle-server

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
        validation[cycleid] = 0

        for i in position:
            if cycleid == i["cycleid"]:
                i["fine"] = False
    
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
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(validate(cycleid))
        return {"validation": result}
