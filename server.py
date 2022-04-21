# THE MAIN POINT WHERE CLIENTS CONNECT
 
 
import socket
# to handle client connections
import threading
from time import time, ctime
t = time()

# GENERAL LOCAL HOST IP ADDRESS
HOST = '127.0.0.1' 
PORT = 9090



server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()


clients = []
nicknames = []


# BORADCAST F(X) THAT SENDS MSSG TO ALL CONNECTED CLIENTS
def broadcast(message):
    for client in clients:
        client.send(message)
  
# HANDLE F(X) TO HANDLE INDIVUDAL CONNECTIONS
def handle(client):
    while True:
        try:
            message= client.recv(1024)
            print(f'[{nicknames[clients.index(client)]}]:{message}')
            broadcast(message)
            
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break
        

# RECIEVE F(X) TO ACCEPT NEW CONNECTIONS / LISTEN
# main function running in mainthread
def receive():
    while True:
        print ('[CURRENT TIME]',ctime(t))

        client, adderess = server.accept()
        print(f"[CONNECTED WITH {str(adderess)}]")
        
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)
    
        nicknames.append(nickname)
        clients.append(client)
        
        print(f"[CLIENT JOINED IS {nickname}]")

        client.send("""You are connected to server!        
""".encode('utf-8'))
        broadcast(f"""{nickname.decode('utf-8')} joined the chat
""".encode('utf-8'))

        
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        





# CALLS HANDLE F(X) WHICH CALLS BROADCAST F(X)
print('[SERVER RUNNING... ]')
receive()
print('[SERVER DOWN...]')




