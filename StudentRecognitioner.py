import os
import face_recognition as fr
import pyautogui
import time
import numpy as np
import cv2

class StudentRecognitioner:

    def __init__(self, known_pictures_location):

        known_pictures = self._get_known_pictures(known_pictures_location)
        self.known_encodings =  self._get_known_encodings()


    def _get_known_pictures(self, path):

        known = []
        self.path = path
        
        for dirs, folders, files in os.walk(path):
            for file in files:
                if file.endswith(".jpg") or file.endswith(".png"):
                    known.append(f"{dirs}/{file}")

        for i in range(len(known)):
            known[i] = known[i].replace("\\","/")
        
        if known: 
            return known
        else:
            raise ImportError("No pictures found!")


    def _get_known_encodings(self, known_pictures):

        relations = {}

        for pic in known_pictures:
            known_image = fr.load_image_file(pic)
            face_encodings = fr.face_encodings(known_image)
            print(face_encodings)
            known_encoding = fr.face_encodings(known_image)[0]
            relations.update({pic.replace(".jpg","").replace(".png","") : known_encoding})

        if relations: 
            return relations
        else:
            raise ValueError("No faces found in pictures!")

    
    def find_by_picture(self, picture, ShowResult=True):

        unknown_image = fr.load_image_file(picture)
        face_locations = fr.face_locations(unknown_image)
        face_encodings = fr.face_encodings(unknown_image, face_locations)
        face_names = []

        for face_encoding in face_encodings:
            
            name = "Unknown"
            matches = fr.compare_faces(list(self.known_encodings.values()), face_encoding)

            face_distances = fr.face_distance(list(self.known_encodings.values()), face_encoding)
            print(self.known_encodings)
            print(face_distances)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                
                name = list(self.known_encodings.keys())[best_match_index].replace(self.path+"/", "")
                # name = relations(best_match_index)

            face_names.append(name)

        if ShowResult:
            img = cv2.imread(picture)

            desired_width  = 600
            # desired_high = int(desired_width * (3/4))

            max_top, max_right, max_bottom, max_left = None, None, None, None

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Draw a box around the face
                cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(img, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(img, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                
                if not max_top or top < max_top:
                    max_top = top
                if not max_right or right > max_right:
                    max_right = right
                if not max_bottom or bottom > max_bottom:
                    max_bottom = bottom
                if not max_left or left < max_left:
                    max_left = left
            
            if face_names:
                if max_top <= 200:
                    max_top = 210
                if max_left <= 200:
                    max_left = 210
                # print(f"{max_top}, {max_right}, {max_bottom}, { max_left}")
                img = img[(max_top-200):(max_bottom+200), (max_left-200):(max_right+200)]

                # img = cv2.resize(img, (0, 0), fx=desired_width/(max_right-max_left), fy=desired_width/(max_right-max_left))
                picture = True
                cv2.imwrite("interface/temp.png", img)
            
            # cv2.imshow('Face Recognition', img)
            # cv2.waitKey(0) # waits until a key is pressed
            # cv2.destroyAllWindows()

        if picture:
            return face_names, picture
        else: 
            return face_names, None




    def _take_screenshot(self, delay, save=False):
        time.sleep(delay)
        myScreenshot = pyautogui.screenshot()
        if save:
            myScreenshot.save('screenshot.png')
        return myScreenshot
        

    def find_by_screenshot(self, screnshot_delay = 2, ShowResult=True):
        if ShowResult:
            screenshot = self._take_screenshot(screnshot_delay,save=True)
        else:
            screenshot = self._take_screenshot(screnshot_delay)
        unknown_image = np.array(screenshot)
        face_locations = fr.face_locations(unknown_image)
        face_encodings = fr.face_encodings(unknown_image, face_locations)
        face_names = []
        picture = False

        for face_encoding in face_encodings:
            
            name = "Unknown"
            matches = fr.compare_faces(list(self.known_encodings.values()), face_encoding)

            face_distances = fr.face_distance(list(self.known_encodings.values()), face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                
                name = list(self.known_encodings.keys())[best_match_index].replace(self.path+"/", "")
                # name = relations(best_match_index)

            face_names.append(name)

        if ShowResult:

            img = cv2.imread("screenshot.png")

            desired_width  = 600
            # desired_high = int(desired_width * (3/4))

            max_top, max_right, max_bottom, max_left = None, None, None, None

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Draw a box around the face
                cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(img, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(img, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                
                if not max_top or top < max_top:
                    max_top = top
                if not max_right or right > max_right:
                    max_right = right
                if not max_bottom or bottom > max_bottom:
                    max_bottom = bottom
                if not max_left or left < max_left:
                    max_left = left
            
            if face_names:
                if max_top <= 200:
                    max_top = 210
                if max_left <= 200:
                    max_left = 210
                # print(f"{max_top}, {max_right}, {max_bottom}, { max_left}")
                img = img[(max_top-200):(max_bottom+200), (max_left-200):(max_right+200)]

                # img = cv2.resize(img, (0, 0), fx=desired_width/(max_right-max_left), fy=desired_width/(max_right-max_left))
                cv2.imwrite("interface/temp.png", img)
                picture = True
            # cv2.imshow('Face Recognition', img)
            # cv2.waitKey(0) # waits until a key is pressed
            # cv2.destroyAllWindows()

        if os.path.exists("screenshot.png"):
            os.remove("screenshot.png")
        if picture:
            return face_names, picture
        else: 
            return face_names, None

        def set_path(path):
            self.__init__(path)

def main():
    path = "known_pictures"
    sr = StudentRecognitioner(path)
    print(sr.find_by_picture("test_pictures/Ronnie_Radke_June_2015_outtake.jpg"))

if __name__ == "__main__":
    main()
