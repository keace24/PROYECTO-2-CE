import socket
from _thread import *
import sys
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = ''
port = 5555

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

currentId = "0"
pos = ["0:50,50", "1:100,100"]
def threaded_client(conn):
    global currentId, pos
    env = currentId
    env_ = pickle.dumps(env)
    conn.send(env_)
    currentId = "1"
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            reply = pickle.loads(data)
            if not data:
                conn.send(pickle.dumps("Goodbye"))
                break
            else:
                print("Recieved: " + reply)
                arr = reply.split(":")
                id = int(arr[0])
                pos[id] = reply
                
                if id == 0: nid = 1
                if id == 1: nid = 0

                reply = pos[nid][:]
                print("Sending: " + reply)
            reply_ = pickle.dumps(reply)
            conn.sendall(reply_)
        except:
            break

    print("Connection Closed")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))