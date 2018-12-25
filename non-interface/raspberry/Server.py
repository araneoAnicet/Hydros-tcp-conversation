import socket
import sys
import pickle
from random import randint
import time
import Raspberry_take_values as rasp


rasp.initialize(rasp.TRIG_PIN)

bind_ip = '192.168.43.101'
bind_port = 9000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(1)  # max backlog of connections

print('Listening on {}:{}'.format(bind_ip, bind_port))
client_sock, address = server.accept()
print('Accepted connection {}:{}'.format(client_sock, address))
curr_time = time.time()
prog_begin_time = time.time()

while True:
    if rasp.pin_status(rasp.TRIG_PIN) == 1:
        if rasp.pin_status(rasp.TRIG_PIN) == 0:
            message = {'trig': str(rasp.take_val(curr_time)),
                       'time': str(time.time() - prog_begin_time)}
            #pickle.dumps(message)
            
            curr_time = time.time()
            print('>' + message['trig'] + '\n')
            client_sock.send(pickle.dumps(message))
            time.sleep(0.1)
client_sock.close()
