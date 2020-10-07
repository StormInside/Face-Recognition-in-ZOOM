import eel
import os
from StudentRecognitioner import StudentRecognitioner

sr = None

@eel.expose
def set_known_folder(folder):
    if folder:
        try:
            global sr
            sr = StudentRecognitioner(folder)
            if sr:
                return "Success initializing"
        except Exception as ex:
            return f"Error initializing -- {ex}"

    else:
        return "Error initializing -- No folder"

@eel.expose
def find_by_picture(picture_location):
    if picture_location:
        try:
            if os.path.exists("interface/temp.png"):
                os.remove("interface/temp.png")
            global sr
            if sr:
                res, picture = sr.find_by_picture(picture_location)
                return [res, picture]
            else:
                return "Error finding -- Initialize known photos first"
        except Exception as ex:
            return f"Error finding -- {ex}"

    else:
        return "Error finding -- No picture"

@eel.expose
def find_by_screenshot(delay):

    try:
        if os.path.exists("interface/temp.png"):
            os.remove("interface/temp.png")

        global sr
        if sr:
            if delay or delay == 0:
                res, picture = sr.find_by_screenshot(int(delay))
            else:
                res, picture = sr.find_by_screenshot()
            return [res, picture]
        else:
            return "Error finding -- Initialize known photos first"
    except Exception as ex:
        return f"Error finding -- {ex}"



eel.init("interface")
eel.start("main.html", size=(640, 768))
# test_pictures/Ronnie_Radke_June_2015_outtake.jpg