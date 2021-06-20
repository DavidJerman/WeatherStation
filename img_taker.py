from picamera import PiCamera
from time import sleep
from PIL import Image
from datetime import datetime
import os


camera = PiCamera()
c = 0
while True:
    try:
        # Takes a new photo every 61 seconds and saves it for display
        c += 1
        filename = datetime.now().strftime("_%Y_%m_%d_%H_%M")
        for file in os.listdir("static/imgs"):
            os.remove("./static/imgs/" + file)

        camera.start_preview()
        camera.capture(f"./static/imgs/view{filename}.jpg")
        camera.stop_preview()
        picture = Image.open(f"./static/imgs/view{filename}.jpg")
        picture.save(f"./static/imgs/view_compressed{filename}.jpg", optimize=True, quality=90)
        os.remove(f'./static/imgs/view{filename}.jpg')
        print("Image taken: " + str(c))
        sleep(61)
    except:
        print("Image could not be taken, an error occurred.")
