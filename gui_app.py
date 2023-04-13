from tkinter import *
import cv2
from PIL import Image, ImageTk
import numpy as np
from deepface import DeepFace
import os

class APP_GUI(Frame):
    def __init__(self,parent,file_path):
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

        self.btnBack = Button(self.Frame1)
        self.btnBack.place(relx=0, rely=0.9, relheight=0.1, relwidth=0.1)
        self.btnBack.config(bg ="#FFCC99")
        self.btnBack.config(text='''Back''')
        self.btnBack.config(font=('Small Fonts',25))
        self.btnBack.config(fg="#FFFFFF")
        self.btnBack.config(activebackground="#FFCC99")
        self.btnBack.config(activeforeground="#99FFFF")
        self.btnBack.config(relief='flat',borderwidth=0,highlightthickness= 0)
        self.btnBack.config(command=lambda: self.call_back())

        self.btnEx = Button(self.Frame1)
        self.btnEx.place(relx=0.3, rely=0.9, relheight=0.1, relwidth=0.1)
        self.btnEx.config(bg ="#FFCC99")
        self.btnEx.config(text='''Extract''')
        self.btnEx.config(font=('Small Fonts',25))
        self.btnEx.config(fg="#FFFFFF")
        self.btnEx.config(activebackground="#FFCC99")
        self.btnEx.config(activeforeground="#99FFFF")
        self.btnEx.config(relief='flat',borderwidth=0,highlightthickness= 0)
        self.btnEx.config(command=lambda: self.face_recog())



        if(file_path ==" "):
            self.face_recog_from_camera()
        else:
            self.face_recog_from_img(file_path)

            self.btnEx.config(command=lambda: self.face_recog())

    def face_recog_from_camera(self):
        ret, frame = self.cap.read()
        
        ret, frame = self.cap.read()
        if ret:
           self.face_recog(frame)
    
        # lặp lại quá trình cập nhật khung hình
        self.label.after(10, self.face_recog_from_camera)
            
    def face_recog_from_img(self,img_path):
        frame = cv2.imread(img_path)
        self.face_recog(frame)

        
    
    def detect_faces(self,frame):
        # chuyển đổi khung hình thành ảnh xám để tăng tốc độ xử lý
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # sử dụng CascadeClassifier để nhận diện khuôn mặt
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        # vẽ hình chữ nhật xung quanh khuôn mặt và trả về hình ảnh mới
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        return frame
    
    def face_recog(self,frame):
            self.frame = self.detect_faces(frame)
            
            result = DeepFace.analyze(self.frame,actions=['emotion'],enforce_detection=True)
            result2 = DeepFace.analyze(self.frame, actions=['gender'],enforce_detection=True)

            # In kết quả
            print(result2[0]['dominant_gender'])
            print(result2[0]['gender'])
            font = cv2.FONT_HERSHEY_SIMPLEX
            # cv2.putText(self.frame,
            Rtext =    result2[0]['dominant_gender']+" "+result[0]['dominant_emotion']
            #     (100,100),
            #     font, 3,
            #     (0, 0, 255),
            #     2,
            #     cv2.LINE_4)
            print(result[0])
            #self.emj_url = f"F:/B20DCAT161/emojis/{result[0]['dominant_emotion']}.png"
            path = os.getcwd().replace("\\","/") +"/emojis/"
            self.emj_url = (path+result[0]['dominant_emotion']+".png")

            self.lbResult = Label(self,text = Rtext)
            self.lbResult.place(relx=0.55, rely= 0.5, relheight= 0.5, relwidth= 0.4)

            from app import Photo
            self.emj_result = Photo(self,self.emj_url)
            self.emj_result.place(relx=0.55, rely= 0.1, relheight= 0.6, relwidth=0.4)
            

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            photo = ImageTk.PhotoImage(image)
            self.label.config(image=photo)
            self.label.image = photo
    
    def call_back(self):
        self.cap.release()
        self.destroy()

