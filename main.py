
from random import random
import random
from fastapi import FastAPI, File, Header, Response
from PIL import Image
import io
import PIL.ImageOps
from pydantic import BaseModel
from base64 import b64encode
from datetime import datetime
from fastapi.responses import StreamingResponse

app = FastAPI()

class Item(BaseModel):
    text: str

@app.get("/")
def home():
    return "home"

@app.post("/picture/invert")
async def getImage(file: bytes = File()):
    getimage = Image.open(io.BytesIO(file))
    inverted_image = PIL.ImageOps.invert(getimage)
    printImage = io.BytesIO()
    inverted_image.save(printImage, "JPEG")
    printImage.seek(0)
    return StreamingResponse(printImage, media_type="image/jpeg")


@app.get("/prime/{number}")
def MillerRabinPrimalityTest(number):
    try:
        # Convert it into integer
        val = int(number)
    except ValueError:
        return "Podaj liczbe"

    '''
    because the algorithm input is ODD number than if we get
    even and it is the number 2 we return TRUE ( spcial case )
    if we get the number 1 we return false and any other even
    number we will return false.
    '''
    number = int(number)
    if number == 2:
        return True
    elif number == 1 or number % 2 == 0:
        return False

    ''' first we want to express n as : 2^s * r ( were r is odd ) '''

    ''' the odd part of the number '''
    oddPartOfNumber = number - 1

    ''' The number of time that the number is divided by two '''
    timesTwoDividNumber = 0

    ''' while r is even divid by 2 to find the odd part '''
    while oddPartOfNumber % 2 == 0:
        oddPartOfNumber = oddPartOfNumber / 2
        timesTwoDividNumber = timesTwoDividNumber + 1

    '''
    since there are number that are cases of "strong liar" we 
    need to check more then one number
    '''
    for time in range(3):

        ''' choose "Good" random number '''
        while True:
            ''' Draw a RANDOM number in range of number ( Z_number )  '''
            randomNumber = random.randint(2, number) - 1
            if randomNumber != 0 and randomNumber != 1:
                break

        ''' randomNumberWithPower = randomNumber^oddPartOfNumber mod number '''
        randomNumberWithPower = pow(int(randomNumber), int(oddPartOfNumber), int(number))

        ''' if random number is not 1 and not -1 ( in mod n ) '''
        if (randomNumberWithPower != 1) and (randomNumberWithPower != number - 1):
            # number of iteration
            iterationNumber = 1

            ''' while we can squre the number and the squered number is not -1 mod number'''
            while (iterationNumber <= timesTwoDividNumber - 1) and (randomNumberWithPower != number - 1):
                ''' squre the number '''
                randomNumberWithPower = pow(randomNumberWithPower, 2, number)

                # inc the number of iteration
                iterationNumber = iterationNumber + 1
            '''     
            if x != -1 mod number then it because we did not found strong witnesses
            hence 1 have more then two roots in mod n ==>
            n is composite ==> return false for primality
            '''
            if (randomNumberWithPower != (number - 1)):
                return False

    ''' well the number pass the tests ==> it is probably prime ==> return true for primality '''
    return True

@app.get("/time")
# Authorization token: we need to base 64 encode it
# and then decode it to acsii as python 3 stores it as a byte string
def basic_auth(username, password):
    token_valid = 'YWRtaW46YWRtaW4xMjM='  # admin admin123
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")

    if (token_valid == token):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print()
        return Response(content="<h2>Current Time =" + current_time +"</h2>", media_type="text/html")
    else:
        return Response(content="<h2>nie udane logowanie</h2>", media_type="text/html")
