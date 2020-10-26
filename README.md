# Simple-Face-Recognition-Program
KNU MIT Group 1

This program can find faces on photos and compare them to known.


INSTALL

run `pip3 install -r requirements.txt` in project root directory.

USE

To run with interface execute `python3 Start_interface.py`.
You can also use FaceRecogniser.py as a library in your code.

CREATING KNOWN FOLDER

Just put all photos with names in some folder, default is ./known_pictures (photos from subfolders are also read) and set path to this folder in Folder line.

Or if you are using FaceRecogniser.py as a library, create FaceRecogniser object specifying folder path.
