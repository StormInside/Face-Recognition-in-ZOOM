import os
import face_recognition as fr
import pyautogui
import time
import numpy as np
import cv2


def _get_known_pictures(path):
    known = []

    for dirs, folders, files in os.walk(path):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".png"):
                known.append(f"{dirs}/{file}")

    for i in range(len(known)):
        known[i] = known[i].replace("\\", "/")

    if known:
        return known
    else:
        raise ImportError("No pictures found!")


def _get_known_encodings(known_pictures_locations):
    relations = {}

    for pic in known_pictures_locations:
        known_image = fr.load_image_file(pic)
        face_encodings = fr.face_encodings(known_image)
        if face_encodings:
            known_encoding = fr.face_encodings(known_image)[0]
            relations.update({pic: known_encoding})
        else:
            print("Faces not found in ", pic)

    if relations:
        return relations
    else:
        raise ValueError("No faces found in pictures!")


def _take_screenshot(delay, save=False):
    time.sleep(delay)
    my_screenshot = pyautogui.screenshot()
    if save:
        my_screenshot.save('screenshot.png')
    return my_screenshot


def show_result(face_locations, face_names, source_pic="screenshot.png", draw_found_pics_path=None):
    img = cv2.imread(source_pic)

    max_top, max_right, max_bottom, max_left = None, None, None, None

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Draw a box around the face
        cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(img, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        name_tmp = name.replace(".jpg", "").replace(".png", "")
        cv2.putText(img, name_tmp, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        if draw_found_pics_path and len(face_names) == 1:
            found_pic_path = draw_found_pics_path + "/" + name
            found_img_fr = fr.load_image_file(found_pic_path)
            f_top, f_right, f_bottom, f_left = fr.face_locations(found_img_fr)[0]
            found_img = cv2.imread(found_pic_path)

            found_img = found_img[(f_top - 50):(f_bottom + 50), (f_left - 50):(f_right + 50)]
            # height, width = found_img.shape
            cv2.rectangle(found_img, (0, 0), (found_img.shape[1], found_img.shape[0]), (0, 255, 0), 2)
            top_offset_for_center =int(((bottom-top) - found_img.shape[0]) // 2)
            img[top + top_offset_for_center: top + top_offset_for_center + found_img.shape[0],
            right + 50:right + 50 + found_img.shape[1]] = found_img

            top = min(top, top + top_offset_for_center)
            # left unchanged
            bottom = max(bottom, top + top_offset_for_center + found_img.shape[0])
            right = max(right, right + 50 + found_img.shape[1])

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
        img = img[(max_top - 200):(max_bottom + 200), (max_left - 200):(max_right + 200)]

    # img = cv2.resize(img, (0, 0), fx=desired_width/(max_right-max_left), fy=desired_width/(max_right-max_left))
    if __name__ == "__main__":
        cv2.imshow('Face Recognition', img)
        cv2.waitKey(0)  # waits until a key is pressed
        cv2.destroyAllWindows()
    else:
        cv2.imwrite("interface/temp.png", img)


class StudentRecognitioner:

    def __init__(self, known_pictures_dir_location):

        known_pictures_locations = _get_known_pictures(known_pictures_dir_location)
        self.path = known_pictures_dir_location
        self.known_encodings = _get_known_encodings(known_pictures_locations)

    def set_path(self, path):
        self.__init__(path)

    def _best_match(self, face_encodings):
        face_names = []
        for face_encoding in face_encodings:

            name = "Unknown"
            matches = fr.compare_faces(list(self.known_encodings.values()), face_encoding)

            face_distances = fr.face_distance(list(self.known_encodings.values()), face_encoding)
            # print(self.known_encodings)
            # print(face_distances)
            best_match_index = int(np.argmin(face_distances))

            if matches[best_match_index]:
                name = list(self.known_encodings.keys())[best_match_index]
                # name = relations(best_match_index)
                name = name.replace(self.path + "/", "")

            face_names.append(name)

        return face_names

    def _top_n_match(self, face_encodings, top=None):
        if top == None:
            top = 10
        face_names_distance_pairs = []
        for face_encoding in face_encodings:

            name = "Unknown"
            matches = fr.compare_faces(list(self.known_encodings.values()), face_encoding)

            face_distances = fr.face_distance(list(self.known_encodings.values()), face_encoding)
            # print(self.known_encodings)
            # print(face_distances)
            best_match_index = int(np.argmin(face_distances))

            known_encodings_address = list(self.known_encodings.keys())
            best_match_index_list = face_distances.tolist()
            address_distances_pairs = list(zip(best_match_index_list, known_encodings_address))
            cut_address_distances_pairs = sorted(address_distances_pairs, key=lambda pair: pair[0])[:top]

            if matches[best_match_index]:
                name = list(self.known_encodings.keys())[best_match_index]
                # name = relations(best_match_index)
                name = name.replace(self.path + "/", "")

            face_names_distance_pairs.append((name, cut_address_distances_pairs))

        return face_names_distance_pairs

    def find_by_picture(self, picture, top=None, ShowResult=True):

        unknown_image = fr.load_image_file(picture)
        face_locations = fr.face_locations(unknown_image)
        face_encodings = fr.face_encodings(unknown_image, face_locations)

        if top:
            face_names_distance_pairs = self._top_n_match(face_encodings, top)
            print(face_names_distance_pairs)
            face_names = [pair[0] for pair in face_names_distance_pairs]
        else:
            face_names = self._best_match(face_encodings)

        if ShowResult:
            show_result(face_locations, face_names, source_pic=picture, draw_found_pics_path=self.path)

        for i in range(len(face_names)):
            face_names[i] = face_names[i].replace(".jpg", "").replace(".png", "")

        if picture:
            return face_names, picture
        else:
            return face_names, None

    def find_by_screenshot(self, screnshot_delay=2, top=None, ShowResult=True):
        if ShowResult:
            screenshot = _take_screenshot(screnshot_delay, save=True)
        else:
            screenshot = _take_screenshot(screnshot_delay)
        unknown_image = np.array(screenshot)
        face_locations = fr.face_locations(unknown_image)
        face_encodings = fr.face_encodings(unknown_image, face_locations)
        face_names = []
        picture = False

        face_names = self._best_match(face_encodings)

        if ShowResult:
            show_result(face_locations, face_names)

        if os.path.exists("screenshot.png"):
            os.remove("screenshot.png")

        for i in range(len(face_names)):
            face_names[i] = face_names[i].replace(".jpg", "").replace(".png", "")

        if picture:
            return face_names, picture
        else:
            return face_names, None


def main():
    path = "known_pictures"
    sr = StudentRecognitioner(path)
    print(sr.find_by_picture("test_pictures/44_A_1.jpg", top=5))


if __name__ == "__main__":
    main()
