import socket
import pickle
from aes import *
from userDatabase import users
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES

#19p1673@eng.asu.edu.eg
#19p6892@eng.asu.edu.eg
class senderNetwork:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.11"
        self.port = 9090
        self.addr = (self.server, self.port)
        self.port = self.connect()

    def connect(self):
        try:
            print('connect')
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass


    def send(self, data):
         try:
             Msg = data.split('|', 6)
             self.client.send(pickle.dumps(str(data)))
             msgReply = pickle.loads(self.client.recv(2048))
             msgR1 = pickle.loads(self.client.recv(2048))
             arr1 = msgReply
             with open('encryptedlMsg.txt', 'wb') as outfile:
                 outfile.write(arr1)
             decrypt_file(users[Msg[1]]['master_key'], 'encryptedlMsg.txt', 'decryptedMsg.txt')
             with open('decryptedMsg.txt', 'rb') as infile:
                 senderKeyToBeSendToSender = infile.read()
             msgOrgBodyFile = open('msgOrgSubject.txt', 'w')
             msgOrgBodyFile.write(Msg[3])
             msgOrgBodyFile.close()
             msgOrgBodyFile = open('msgOrgBody.txt', 'w')
             msgOrgBodyFile.write(Msg[4])
             msgOrgBodyFile.close()
             encrypt_file(senderKeyToBeSendToSender, 'msgOrgSubject.txt', 'msgEncryptedSubject.txt')
             encrypt_file(senderKeyToBeSendToSender, 'msgOrgBody.txt', 'msgEncryptedBody.txt')
             with open('msgEncryptedSubject.txt', 'rt') as infile:
                 subject = infile.read()
             with open('msgEncryptedBody.txt', 'rt') as infile:
                 body = infile.read()
             return subject, body, msgR1,

         except socket.error as e:
             print("error")
             print(e)