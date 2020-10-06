import eel
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
            global sr
            if sr:
                res = sr.find_by_picture(picture_location)
                return res
            else:
                return "Error finding -- Initialize known photos first"
        except Exception as ex:
            return f"Error finding -- {ex}"

    else:
        return "Error finding -- No picture"

@eel.expose
def find_by_screenshot(delay):
    try:
        global sr
        if sr:
            if delay:
                res = sr.find_by_screenshot(delay)
            else:
                res = sr.find_by_screenshot()
            return res
        else:
            return "Error finding -- Initialize known photos first"
    except Exception as ex:
        return f"Error finding -- {ex}"



eel.init("interface")
eel.start("main.html", size=(600, 768))
# test_pictures/Ronnie_Radke_June_2015_outtake.jpg