from tkinter import *
import cv2
from PIL import Image, ImageTk
import numpy as np
from deepface import DeepFace


class APP_GUI(Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.cap = cv2.VideoCapture(0)
        # khởi tạo mô hình CascadeClassifier để nhận diện khuôn mặt
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


        self.Frame1 = Frame(self)
        self.Frame1.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.Frame1.config(relief=GROOVE)
        self.Frame1.config(borderwidth="2")
        self.Frame1.config(background="#d9d9d9")

        self.label = Label(self.Frame1)
        self.label.place(relx=0, rely=0, relheight=1 , relwidth= 0.5)

        self.bntBack = Button(self.Frame1)
        self.bntBack.place(relx=0, rely=0.9, relheight=0.1, relwidth=0.1)
        self.bntBack.config(bg ="#FFCC99")
        self.bntBack.config(text='''Back''')
        self.bntBack.config(font=('Small Fonts',25))
        self.bntBack.config(fg="#FFFFFF")
        self.bntBack.config(activebackground="#FFCC99")
        self.bntBack.config(activeforeground="#99FFFF")
        self.bntBack.config(relief='flat',borderwidth=0,highlightthickness= 0)
        self.bntBack.config(command=lambda: self.call_back())

        self.face_recog()

    def face_recog(self):
        ret, frame = self.cap.read()
        if ret:
            frame = self.detect_faces(frame)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            photo = ImageTk.PhotoImage(image)
            result = DeepFace.analyze(frame,actions=['emotion'],enforce_detection=False)
            result2 = DeepFace.analyze(frame, actions=['gender'],enforce_detection=False)

            # In kết quả
            print(result2[0]['dominant_gender'])
            print(result2[0]['gender'])
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame,
                result2[0]['dominant_gender']+" "+result[0]['dominant_emotion'],
                (50,50),
                font, 3,
                (0, 0, 255),
                2,
                cv2.LINE_4)
            print(result[0])
            self.emj_url = f"F:/B20DCAT161/emojis/{result[0]['dominant_emotion']}.png"

            from app import Photo
            self.emj_result = Photo(self,self.emj_url)
            self.emj_result.place(relx=0.6, rely= 0.1, relheight= 0.5, relwidth=0.4)
            

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            photo = ImageTk.PhotoImage(image)
            self.label.config(image=photo)
            self.label.image = photo

            
    
        # lặp lại quá trình cập nhật khung hình
        self.label.after(10, self.face_recog)
            
    def detect_faces(self,frame):
        # chuyển đổi khung hình thành ảnh xám để tăng tốc độ xử lý
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # sử dụng CascadeClassifier để nhận diện khuôn mặt
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        # vẽ hình chữ nhật xung quanh khuôn mặt và trả về hình ảnh mới
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        return frame
    
    def get_faces(self,frame):
        confidence_threshold=0.5
        # convert the frame into a blob to be ready for NN input
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104, 177.0, 123.0))
        FACE_PROTO = 'D:/project_Py/res10_300x300_ssd_iter_140000_fp16.caffemodel'
        FACE_MODEL = 'D:/project_Py/deploy.protottxt.txt'
# GENDER_MODEL = 'D:/project_Py/deploy_gender.prototxt'
# GENDER_PROTO = 'D:/project_Py\gender_net.caffemodel'
# MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
# GENDER_LIST = ['Male', 'Female']
        face_net = cv2.dnn.readNetFromCaffe(FACE_MODEL, FACE_PROTO)
        # set the image as input to the NN
        face_net.setInput(blob)
        # perform inference and get predictions
        output = np.squeeze(face_net.forward())
        # initialize the result list
        faces = []
        # Loop over the faces detected
        for i in range(output.shape[0]):
            confidence = output[i, 2]
        if confidence > confidence_threshold:
            box = output[i, 3:7] * \
                np.array([frame.shape[1], frame.shape[0],
                         frame.shape[1], frame.shape[0]])
            # convert to integers
            start_x, start_y, end_x, end_y = box.astype(np.int64)
            # widen the box a little
            start_x, start_y, end_x, end_y = start_x - \
                10, start_y - 10, end_x + 10, end_y + 10
            start_x = 0 if start_x < 0 else start_x
            start_y = 0 if start_y < 0 else start_y
            end_x = 0 if end_x < 0 else end_x
            end_y = 0 if end_y < 0 else end_y
            # append to our list
            faces.append((start_x, start_y, end_x, end_y))
        return faces

    def call_back(self):
        self.cap.release()
        self.destroy()

