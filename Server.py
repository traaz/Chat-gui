from socket import *
from threading import *
from time import sleep

clients = []
names = []

def clientThread(client):
    initname = client.recv(1024).decode('utf-8')
    bayrak = True

    while True:
        try:

            if bayrak:
                names.append(initname)
                print(initname, 'baglandi')
                bayrak = False

            message = client.recv(1024).decode('utf-8')

            if message == "fotograf geliyo":
                filepath = client.recv(1024).decode('utf-8')
                filepath = filepath.split("/")[-1]
                file = open(filepath, "wb")
                image_chunk = client.recv(40960000)
                file.write(image_chunk)
                file.close()
                """
                server.send("kanka fotograf geliyo".encode("utf-8"))
                server.send(filepath.encode("utf-8"))
                file = open(filepath, "rb")
                data = file.read(40960000)
                print("send data öncesi")
                server.send(data)
                print("send data sonrası")
                """
                message = ""
                for c in clients:
                    if c != client:
                        c.send("fotograf geliyo".encode("utf-8"))
                        index = clients.index(client)
                        name = names[index]
                        c.send(filepath.encode("utf-8"))
                        file = open(filepath, "rb")
                        data = file.read(40960000)
                        c.send(data)

            for c in clients:
                if c != client:
                    index = clients.index(client)
                    name = names[index]
                    c.send((name + ':' + message).encode('utf-8'))

        except:
            index = clients.index(client)
            clients.remove(client)
            name = names[index]
            names.remove(name)
            print(name + 'cikti')
            break


server = socket(AF_INET, SOCK_STREAM)
ip = 'localhost'
port = 8081

server.bind((ip, port))
server.listen()
print('Server dinlemede')

while True:
    client, address = server.accept()
    clients.append(client)
    print('Baglanti yapildi', address[0] + ':' + str(address[1]))
    thread = Thread(target=clientThread, args=(client,))
    thread.start()
    
