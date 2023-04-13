from tkinter import *
from tkinter import filedialog
from gui_app import APP_GUI
from PIL import Image, ImageTk

class Photo(Frame):
    def __init__(self,parent,path_to_img):
        super().__init__(parent)
        self.config(bg="#00CCFF")
        self.canvas = Canvas(self)
        self.canvas.config(bg ="#FFCC99")
        self.img = PhotoImage(file=path_to_img)
        # px = parent.winfo_screenwidth()//2
        # py = parent.winfo_screenheight()//2
        # self.img.configure(width=px,height=py)
        self.canvas.create_image(0, 0, anchor="nw", image=self.img)  
        self.canvas.place(relx=0, rely=0, relheight=1, relwidth=1)

class BlinkingTitle(Frame):
    def __init__(self, parent, title, f):
        Frame.__init__(self, parent)
        self.config(bg= parent['bg'])
        self.label = Label(self, text=title,font= f)
        self.label.config(bg = parent['bg'])
        self.label.pack(pady=20)
        self.blink()

    def blink(self):
        self.label.configure(fg='red')
        self.after(500, self.unblink)

    def unblink(self):
        self.label.configure(fg='blue')
        self.after(500, self.blink)
class MyMenu(Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.config(bg='#FFCC99')

        self.title = BlinkingTitle(self, "||\_(-_-)_/||",('Small Fonts',55))
        self.title.place(relx = 0, rely= 0.1, relheight=0.4, relwidth=1)
        self.title.config(bg ="#FFCC99")

        self.file_path=""

        self.Button1 = Button(self)
        self.Button1.place(relx=0.18, rely=0.3, relheight=0.12, relwidth=0.64)
        self.Button1.config(bg ="#FFCC99")
        self.Button1.config(text='''Camera''')
        self.Button1.config(font=('Small Fonts',25))
        self.Button1.config(fg="#FFFFFF")
        self.Button1.config(activebackground="#FFCC99")
        self.Button1.config(activeforeground="#99FFFF")
        self.Button1.config(relief='flat',borderwidth=0,highlightthickness= 0)
        self.Button1.config(command=self.call_start)
        self.Button1.bind('<Enter>',self.on_enter)
        self.Button1.bind('<Leave>',self.on_leave)

        self.Button4 = Button(self)
        self.Button4.place(relx=0.18, rely=0.45, relheight=0.12, relwidth=0.64)
        self.Button4.config(bg ="#FFCC99")
        self.Button4.config(text='''File''')
        self.Button4.config(font=('Small Fonts',25))
        self.Button4.config(fg="#FFFFFF")
        self.Button4.config(activebackground="#FFCC99")
        self.Button4.config(activeforeground="#99FFFF")
        self.Button4.config(relief='flat',borderwidth=0,highlightthickness= 0)
        self.Button4.config(command=self.open_file)
        self.Button4.bind('<Enter>',self.on_enter)
        self.Button4.bind('<Leave>',self.on_leave)

        self.Button2 = Button(self)
        self.Button2.place(relx=0.18, rely=0.6, relheight=0.12, relwidth=0.64)
        self.Button2.config(bg ="#FFCC99")
        self.Button2.config(text='''How2use''')
        self.Button2.config(font=('Small Fonts',25))
        self.Button2.config(fg="#FFFFFF")
        self.Button2.config(activebackground="#FFCC99")
        self.Button2.config(activeforeground="#99FFFF")
        self.Button2.config(relief='flat',borderwidth=0,highlightthickness= 0)
        self.Button2.bind('<Enter>',self.on_enter)
        self.Button2.bind('<Leave>',self.on_leave)


        self.Button3 = Button(self) 
        self.Button3.place(relx=0.18, rely=0.75, relheight=0.12, relwidth=0.64)
        self.Button3.config(bg ="#FFCC99")
        self.Button3.config(text='''Quit''')
        self.Button3.config(font=('Small Fonts',25))
        self.Button3.config(fg="#FFFFFF")
        self.Button3.config(activebackground="#FFCC99")
        self.Button3.config(activeforeground="#99FFFF")
        self.Button3.config(command=quit)
        self.Button3.config(relief='flat',borderwidth=0,highlightthickness= 0)
        self.Button3.bind('<Enter>',self.on_enter)
        self.Button3.bind('<Leave>',self.on_leave)

        
    def on_enter(self,event):
        event.widget.config(fg='black')
        
    def on_leave(self,event):
        event.widget.config(fg='white')

    def call_start(self):
        self.file_path =" "
        appGui = APP_GUI(self.master,self.file_path)
        appGui.place(relx=0, rely= 0, relheight= 1, relwidth=1)

    def open_file(self):
        self.file_path = filedialog.askopenfilename()
        appGui = APP_GUI(self.master,self.file_path)
        appGui.place(relx=0, rely= 0, relheight= 1, relwidth=1)
        
        

class Root(Tk):
    def __init__(self):
        super().__init__()

        self.title('Title')
        self.geometry('1920x1080')
        # đặt hình dáng con trỏ chuột
        self.config(cursor="mouse")


        img = PhotoImage(file="img/icon_ai.png")
        self.iconphoto(False,img)

        self.frame_photo = Photo(self,"img/mem2.png")
        self.frame_photo.place(relx=0, rely= 0, relheight= 1, relwidth=0.5)

        self.myMenu = MyMenu(self)
        self.myMenu.place(relx=0.5, rely= 0, relheight= 1, relwidth=0.5)


if __name__ == '__main__':
    app = Root()
    app.mainloop()
    