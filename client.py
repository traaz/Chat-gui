import os.path
from socket import *
from threading import *
from tkinter import *
from tkinter import filedialog as fd, simpledialog
from tkinter import messagebox
from PIL import ImageTk, Image
import requests

client = socket(AF_INET, SOCK_STREAM)
ip= 'localhost'
port = 8081


client.connect((ip, port))

def exit():

    pencere.destroy()


while True:

    nick_name =simpledialog.askstring("İsim", "İsim Giriniz: ")

    if (len(nick_name) > 0):
        pencere = Tk()
        pencere.title('Chat')


        def enter(event):
            sendMessage()


        global my_image
        messages =Text(pencere, width=50)
        messages.grid(row=0, column=0, padx=10, pady=10)
        yourMessage = Entry(pencere, width=50)
        yourMessage.insert(0, '')
        yourMessage.bind('<Return>', enter)
        yourMessage.grid(row=1,column=0,padx=10,pady=10)
        yourMessage.focus()
        yourMessage.select_range(0, END)


        def connect():
            client_name = nick_name
            # messages.insert(END, '\n'+ 'Baglandi ' + client_name)
            client.send(client_name.encode('utf8'))

        connect()
        def sendMessage():
            clientMessage = yourMessage.get()
            messages.insert(END, '\n'+ 'Sen: ' + clientMessage)
            client.send(clientMessage.encode('utf-8'))
            yourMessage.delete(0, END)
            messages.yview(END)

        def openFile():
            global my_image
            client.send("fotograf geliyo".encode("utf-8"))
            filepath = fd.askopenfilename()
            client.send(filepath.encode("utf-8"))
            file = open(filepath,"rb")
            data = file.read(40960000)
            client.send(data)
            file.close()
            print(filepath)
            my_image = ImageTk.PhotoImage(Image.open(filepath))
            position = messages.index(INSERT)
            messages.image_create(END, image=my_image)

        bmessageGonder = Button(pencere, text= 'Gonder',command=sendMessage)
        bmessageGonder.grid(row=2,column=0,padx=5,pady=5)

        dosyaSec = Button(pencere, text = 'Dosya Sec', command=openFile)
        dosyaSec.grid(row=3,column=0,padx=5,pady=5)

        def recvMessage():
            while True:
                serverMessage = client.recv(1024).decode('utf-8')
                if serverMessage == "fotograf geliyo":
                    print("üst")
                 ##   filepath = client.recv(1024).decode('utf-8')
                 ##   print("alt")
                    file = open("./images/foto.png", "wb")
                    image_chunk = client.recv(40960000)
                    file.write(image_chunk)
                    file.close()

                    my_image = ImageTk.PhotoImage(Image.open("./images/foto.png"))
                    position = messages.index(INSERT)
                    messages.image_create(END, image=my_image)

                else:
                    messages.insert(END, '\n' + serverMessage)

        recvThread = Thread(target=recvMessage)
        recvThread.daemon= True
        recvThread.start()

        pencere.mainloop()
        if (exit()):
            pencere.protocol('WM_DELETE_WINDOW', exit)
            break

    elif (len(nick_name) == 0):

            messagebox.showerror("İsim", "Lutfen Isim Giriniz..")
