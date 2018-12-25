from socket import *
from config import *
import pickle


def get_result(sock, do_write=False):
    while True:
        try:
            received_info = pickle.loads(sock.recv(1024))
            if do_write:
                with open('results.txt', 'a') as file:
                    file.writelines(
                        ['>Speed: ' + received_info['trig'],
                         '\n>Time: ' + received_info['time'],
                         '\n\n']
                    )

            print('>Speed: ' + received_info['trig'] + '\n' +
                  '>Time: ' + received_info['time'] + '\n' +
                  '\n\n')
        except Exception as error:
            print('>>Package delivery error: ' + str(error))


if __name__ == '__main__':
    client_socket = socket(AF_INET, SOCK_STREAM)  # creating socket
    print('>>Creating client socket')

    try:
        print('>>Connection to {}:{}'.format(ip_address, port))
        client_socket.connect((ip_address, port))
    except Exception as error:
        print('>>Connection error: ' + str(error))

    get_result(client_socket, do_write=True)
