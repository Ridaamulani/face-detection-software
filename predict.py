import face_recognition
import cv2
import os
from django.conf import settings
from .models import *

# Load the images
def load_image(user):
    base_dir = str(settings.BASE_DIR)
    list_of_image = []
    list_of_id = []
    userprofile = Register.objects.filter()
    for i in userprofile:
        list_of_image.append(base_dir+i.image.url)
        list_of_id.append(i.id)
    print(list_of_image)
    list_of_image_person = []
    for i in list_of_image:
        image_of_person = face_recognition.load_image_file(i)
        list_of_image_person.append(image_of_person)
        #'C:\\Users\\bhuwa\\OneDrive\\Desktop\\AttendanceWithFaceRecognition\\DjCropRecommendation\\DjAttendanceFaceRecognition/media/mahesh-2.jpeg')
    # image_of_person2 = face_recognition.load_image_file(list_of_image[1])
        # "C:\\Users\\bhuwa\\OneDrive\\Desktop\\AttendanceWithFaceRecognition\\DjCropRecommendation\\DjAttendanceFaceRecognition/media/Narayan.jpeg")
    # image_of_person3 = face_recognition.load_image_file(
    #     "C:\\Users\\bhuwa\\OneDrive\\Desktop\\AttendanceWithFaceRecognition\\DjCropRecommendation\\DjAttendanceFaceRecognition/media/bhuwan.jpeg")
    # encoding_faces([image_of_person1, image_of_person2, image_of_person3])
    # list_of_image = [image_of_person1, image_of_person2]
    # image_of_person1 = face_recognition.load_image_file(media_path+"mahesh-2.jpeg")
    # image_of_person2 = face_recognition.load_image_file(media_path+"Narayan.jpeg")
    # image_of_person3 = face_recognition.load_image_file(media_path+"bhuwan.jpeg")
    return encoding_faces(user, list_of_image_person, list_of_id)

# Encoding the faces
def encoding_faces(user, list_of_image, list_of_id):
    list_of_face_encoding = []
    for i in list_of_image:
        face_encode = face_recognition.face_encodings(i)[0]
        list_of_face_encoding.append(face_encode)
    return recognize_faces(user, list_of_face_encoding, list_of_id)

def check_exist_file(user):
    # specify the file path
    media_path = str(settings.BASE_DIR) + "/media/" + user.username
    if not os.path.exists(media_path):
        # Create the directory if it doesn't exist
        os.makedirs(media_path)
        print(f"Directory {media_path} created successfully")
    else:
        print(f"Directory {media_path} already exists")
    file_path = media_path + "/image.jpeg"
    print(file_path, "file_path")
    # check if the file exists
    if os.path.exists(file_path):
        # delete the file
        os.remove(file_path)
        print("File deleted successfully.")
        return file_path
    else:
        print("File not found.")
        return file_path

def open_camera_and_take_picture(user):
    # open the camera
    cap = cv2.VideoCapture(0)

    # check if camera is opened successfully
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    # read a frame from the camera
    ret, frame = cap.read()

    # check if frame is captured successfully
    if not ret:
        print("Cannot read a frame from camera")
        exit()

    # save the frame as an image file
    file_path = check_exist_file(user)
    print(file_path, "file_path")
    cv2.imwrite(file_path, frame)

    # release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()
    return file_path

# Recognize the faces
def recognize_faces(user, list_of_face_encoding, list_of_id):
    file_path = open_camera_and_take_picture(user)
    unknown_image = face_recognition.load_image_file(file_path)
    try:
        unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
        results = face_recognition.compare_faces(list_of_face_encoding, unknown_face_encoding)
        userprofile = Register.objects.get(user=user)
        index = list_of_id.index(userprofile.id)
        if results[index]:
            print("Matched Successfully")
            return True
        else:
            print("Unknown person is in the image!")
            return False
    except:
        return False

