import os

import face_recognition as fr

path = "known_pictures"

def get_known_pictures(path):

    known = []
    
    for dirs, folders, files in os.walk(path):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".png"):
                known.append(f"{dirs}/{file}")

    for i in range(len(known)):
        known[i] = known[i].replace("\\","/")

    return known

def get_known_encodings(known_pictures):

    relations = {}

    for pic in known_pictures:
        known_image = fr.load_image_file(pic)
        known_encoding = fr.face_encodings(known_image)[0]
        relations.update({pic.replace(".jpg","").replace(".png","") : known_encoding})

    return relations

def find_face(img, relations):
    unknown_image = fr.load_image_file(img)
    unknown_encoding = fr.face_encodings(unknown_image)[0]

    for name, encoding in relations.items():
        if fr.compare_faces([encoding], unknown_encoding)[0]:
            print("Coincidence found in:", name)


find_face("Ronnie_Radke_June_2015_outtake.jpg", get_known_encodings(get_known_pictures(path)))


    