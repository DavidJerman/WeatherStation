from picamera import PiCamera
from time import sleep
from PIL import Image
from datetime import datetime
import os


camera = PiCamera()
c = 0
while True:
    c += 1
    year, month, day, hour, minute = datetime.now().strftime("%Y"), datetime.now().strftime("%m"),\
                                     datetime.now().strftime("%d"), datetime.now().strftime("%H"),\
                                     datetime.now().strftime("%M")
    for file in os.listdir("static"):
        if file != "other":
            os.remove("./static/" + file)
    name = "_" + year + "_" + month + "_" + day + "_" + hour + "_" + minute

    camera.start_preview()
    camera.capture(f"./static/view{name}.jpg")
    camera.stop_preview()
    picture = Image.open(f"./static/view{name}.jpg")
    picture.save(f"./static/view_compressed{name}.jpg", optimize=True, quality=40)
    os.remove(f'./static/view{name}.jpg')
    print("Image taken: " + str(c))
    sleep(61)
