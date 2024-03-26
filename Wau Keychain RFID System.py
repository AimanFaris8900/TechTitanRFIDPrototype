import serial
import time
import threading
from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.font as font
from PIL import ImageTk, Image
import firebase_admin
from firebase_admin import credentials, initialize_app, storage, firestore

# Use a service account.
cred = credentials.Certificate('C:/Users/CM Aiman/Documents/VS Code projects\python projects/wau-keychain-tech-titan-firebase-adminsdk-ogj9q-be61de1c4f.json')

initialize_app(cred, {
    'storageBucket': 'wau-keychain-tech-titan.appspot.com',
})
bucket_name = "wau-keychain-tech-titan.appspot.com"

db = firestore.client()

arduino = serial.Serial(port='COM5', baudrate=9600, timeout=.1)
user_id = "F4000"

def write_data(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    #data = arduino.readline()
    #return data

def read_data():
    global user_id
    while True:
        data = arduino.readline().strip().decode('utf-8')
        trimdata = data[0:2]
        if trimdata == "ID":
            print(data[11:16])
            user_id = str(data[11:16])
            get_data()

def send_data():
    doc_ref = db.collection("Student").document("F4001")
    doc_ref.set({"Name": "Jang", 
                 "Form": 4, 
                 "Class": "Bestari",
                 "Credit": 500.00
                 })
    
def get_data():
    users_ref = db.collection("Student").document(user_id)
    docs = users_ref.get()

    if docs.exists:
        print(f"Document data: {docs.to_dict()}")
        docs = docs.to_dict()

        get_image()
        center_widget(docs)
    else:
        print("No such document!")

def update_image():
    imgfile = Image.open("C:/Users/CM Aiman/Documents/VS Code projects/python projects/RFID Images/"+user_id+".png")
    imgphoto = imgfile.resize((300,350))
    img = ImageTk.PhotoImage(imgphoto)
    image_container =canvasimage.create_image(0,0, anchor="nw",image=img)
    canvasimage.itemconfig(image_container,image=img)

def center_widget(studentdict):

    #Student Information Label
    
    label2.place(relx=0.48, rely=0.1, anchor=CENTER)
    
    separatorbot.place(relx=0, rely=0.995, relwidth=1, relheight=1)

    #Image Label Retriever
    
    #img2 = Image.open('C:/Users/CM Aiman/Documents/VS Code projects/python projects/RFID Images/'+user_id+'.png')
    #resize_image = img2.resize((300,350))
    #photo = ImageTk.PhotoImage(resize_image)
    #imagelabel.configure(image=photo)
    #imagelabel.place(relx=0.15, rely=0.5, anchor=CENTER)
    
    #imgconvert = ImageTk.PhotoImage(imgfile)
    #canvasimage.itemconfig(image_container,image=imgconvert)

    imgfile = Image.open("C:/Users/CM Aiman/Documents/VS Code projects/python projects/RFID Images/"+user_id+".png")
    imgphoto = imgfile.resize((300,350))
    img = ImageTk.PhotoImage(imgphoto)
    image_container =canvasimage.create_image(0,0, anchor="nw",image=img)
    canvasimage.itemconfig(image_container,image=img)

    #Student info list label
    
    nameLabel.place(relx=0.3, rely=0.3, anchor=W)
    
    formLabel.place(relx=0.3, rely=0.45, anchor=W)
    
    classLabel.place(relx=0.3, rely=0.6, anchor=W)

    creditLabel.place(relx=0.3, rely=0.75, anchor=W)

    namevar.set("Name: "+studentdict["Name"])
    formvar.set("Form: "+str(studentdict["Form"]))
    classvar.set("Class: "+studentdict["Class"])
    creditvar.set("Credit: "+str(studentdict["Credit"]))
    
    #set_widget(studentdict,namevar,formvar,classvar,creditvar)

def set_widget(studentdict,namevar,formvar,classvar,creditvar):

    namevar.set("Name: "+studentdict["Name"])
    formvar.set("Form: "+str(studentdict["Form"]))
    classvar.set("Class: "+studentdict["Class"])
    creditvar.set("Credit: "+str(studentdict["Credit"]))
    gui.update_idletasks()

def get_image():
    source_blob_name = user_id+".png"

    local_destination = 'C:/Users/CM Aiman/Documents/VS Code projects/python projects/RFID Images/'+source_blob_name

    bucket = storage.bucket()
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(local_destination)


if __name__ == "__main__":

    gui = Tk()
    buttonfont = font.Font(family='Arial', size=20)
    namevar = tk.StringVar()
    formvar = tk.StringVar()
    classvar = tk.StringVar()
    creditvar = tk.StringVar()

    frametop = Frame(gui)
    frametop.pack(fill="x")
    frametop.configure(background="gray45")
    framecenter = Frame(gui)
    framecenter.configure(background="gray45")
    framecenter.pack(fill=BOTH, expand= True)
    framebot = Frame(gui)
    framebot.configure(background="gray45")
    framebot.pack(side="bottom")

    #Window Title
    gui.configure(background="gray45")
    gui.state("zoomed")
    gui.title("Wau Keychain RFID System")

    #Top Page Title
    label = Label(frametop, text="Wau Keychain Data Display",background="gray45", font= ("Consolas",35), foreground="white")
    label.pack(side= BOTTOM)

    #Top Line Separator
    separatortop = ttk.Separator(frametop, orient="horizontal")
    separatortop.place(relx=0, rely=0.95, relwidth=1, relheight=1)

    # Center widgets
    label2 = Label(framecenter, text="Student Information",background="gray45", font= ("Consolas",40,"bold"), foreground="white")
    separatorbot = ttk.Separator(framecenter, orient="horizontal")

    #image = Image.open("C:/Users/CM Aiman/Documents/VS Code projects/python projects/RFID Images/F4000.png")
    #resize_image = image.resize((300,350))
    #photo = ImageTk.PhotoImage(resize_image)
    #imagelabel = Label(framecenter, image=photo)
    #imagelabel.place(relx=0.15, rely=0.5, anchor=CENTER)

    canvasimage = Canvas(framecenter, width=300, height=350)
    canvasimage.place(relx=0.15, rely=0.5, anchor=CENTER)

    imgphoto = Image.open("C:/Users/CM Aiman/Documents/VS Code projects/python projects/RFID Images/"+user_id+".png")
    imgphoto = imgphoto.resize((300,350))
    img = ImageTk.PhotoImage(imgphoto)
    
    print("USER ID: "+user_id)

    nameLabel = Label(framecenter, textvariable=namevar, bg="gray45", fg = "White", font= ("Helvetica", 30))
    nameLabel.configure(justify=LEFT)
    formLabel = Label(framecenter, textvariable=formvar, bg="gray45", fg = "White", font= ("Helvetica", 30))
    classLabel = Label(framecenter, textvariable=classvar, bg="gray45", fg = "White", font= ("Helvetica", 30))
    creditLabel = Label(framecenter, textvariable=creditvar, bg="gray45", fg = "White", font= ("Helvetica", 30))
    
    #Bottom Buttons
    buttonscan = Button(framebot, command=lambda: write_data("1"),text="Scan", bg="white", fg="black", font=buttonfont, height=1, width=10)
    buttonscan.pack(side= LEFT, padx=10, pady=10)
    buttoncancel = Button(framebot, command=lambda: center_widget(framecenter), text="Cancel", bg="white", fg="black", font=buttonfont, height=1, width=10)
    buttoncancel.pack(side= LEFT, padx=10, pady= 10)

    threading.Thread(target=read_data, daemon=True).start()
    gui.mainloop()