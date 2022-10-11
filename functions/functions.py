import random
import asyncio
from db import validation

def otpGenerator():
    return random.randint(1000, 9999)

async def validate(cycleid):
    while True:
        if validation[cycleid] == 1:
            return 1
        elif validation[cycleid] == -1:
            return 0
