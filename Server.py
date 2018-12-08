import socket
import sys
import pickle
from random import randint
import time


bind_ip = socket.gethostname()
bind_port = 9090


def stream_start(ip, port, devices=1):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(devices)  # max connections
    print('>>Listening on {}:{}'.format(ip, port))
    client_sock, address = server.accept()
    print('>>Accepted connection {}:{}'.format(client_sock, address))
    return client_sock


def debugging(client_sock):
    start_time = time.time()
    package_id = 0
    for _ in range(101):
        message = {'speed': str(randint(0, 3000)),
                   'time': str(round(time.time() - start_time, 3)),
                   'package_check': str(package_id)
                   }

        print('>Speed: ' + message['speed'] + '\n' +
              '>Time: ' + message['time'] + '\n' +
              '>Id: ' + message['package_check'] + '\n' +
              '\n\n')
        if int(message['package_check']) != 87:
            client_sock.sendall(pickle.dumps(message))
        time.sleep(0.1)
        package_id += 1
    client_sock.close()


def main():
    client = stream_start(bind_ip, bind_port)
    debugging(client)


if __name__ == '__main__':
    main()
