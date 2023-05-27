import os
import secrets
import socket
from _thread import *
import random
import pickle
from aes import encrypt_file, decrypt_file
from userDatabase import users
server = "192.168.1.11"
port = 9090

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")



def generate_key():
    return os.urandom(16)

def threaded_client(conn):
    while True:
        try:
            conn.send(pickle.dumps('1'))
            data = pickle.loads(conn.recv(2048))
            print('Data Received')
            if not data:
                print("Disconnected")
                break
            else:
                info = data.split('|', 6)
                if info[0] == '1':
                    if info[1] in users and info[2] in users:
                        senderNewKey = open("senderOrgKey.txt", "wb")
                        oxe = generate_key()
                        senderNewKey.write(oxe)
                        senderNewKey.close()
                        encrypt_file(users[info[1]]['master_key'], 'senderOrgKey.txt', 'senderEncryptedKey.txt')
                        encrypt_file(users[info[2]]['master_key'], 'senderOrgKey.txt', 'receiverEncryptedKey.txt')
                        with open('senderEncryptedKey.txt', 'rb') as infile:
                                senderKeyToBeSendToSender = infile.read()
                        with open('receiverEncryptedKey.txt', 'rb') as infile:
                                receiverKeYToBeSendToreceiver = infile.read()
                        reply = senderKeyToBeSendToSender
                        reply1 = receiverKeYToBeSendToreceiver
                else:
                    print('not an encryption request')
                conn.send(pickle.dumps(reply))
                conn.send(pickle.dumps(reply1))
        except:
            break
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn,))