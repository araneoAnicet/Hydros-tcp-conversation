import socket
import os.path
import pickle
import time
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class UserApp(App):

    def __init__(self):
        super(UserApp, self).__init__()
        self.connected = False
        self.written_ip = ''
        self.saved_data = []
        self.predkosc = ''
        self.srednia_predkosc = ''
        self.max_predkosc = ''
        self.przyspieszenie = ''
        self.max_przyspieszenie = ''

        self.connection_status_layout = Label(text='N/I')
        self.speed_widget = Label(text='Prędkość: ')
        self.speed_max_widget = Label(text='Max Prędkość: ')
        self.a_widget = Label(text='Przyspieszenie: ')
        self.a_max_widget = Label(text='Max Przyspieszenie: ')
        self.time_widget = Label(text='Czas: ')

    def lables_text_change(self):
        self.speed_widget.text = 'Prędkość: ' + received_info['speed']
        self.time_widget.text = 'Czas: ' + received_info['time']

    def stream_connect(self, ip, port):  # tcp client connection
        global client_socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((ip, port))
            print('>>Connected to {}:{}'.format(ip, port))
            return True
        except Exception as error:
            print('>>Error while connection:\n' + str(error))
            return False

    def info_get(self, do_write=False, save_data=False):  # tcp data receive
        global client_socket
        package_id = 0
        if os.path.isfile('results.txt'):
            os.remove('results.txt')
        while True:
            try:
                received_info = pickle.loads(client_socket.recv(1024))
                if save_data:
                    self.saved_data.append(received_info)
                if do_write:
                    with open('results.txt', 'a') as file:
                        file.writelines(
                            ['>Speed: ' + received_info['speed'],
                             '\n>Time: ' + received_info['time'],
                             '\n>Id: ' + received_info['package_check'],
                             '\n\n']
                        )

                self.lables_text_change()

                print('>Speed: ' + received_info['speed'] + '\n' +
                      '>Time: ' + received_info['time'] + '\n' +
                      '>Id: ' + received_info['package_check'] +
                      '\n\n')

                package_id += 1
            except Exception as error:
                return '>>Error while receiving data:\n' + str(error)

    def on_connect_press(self, instance):
        if self.connected == False:
            if self.stream_connect(self.written_ip, 9090):
                self.connected = True
                self.info_get(do_write=True, save_data=True)
                self.connected = False
                print(self.saved_data)

    def on_text(self, instance, value):
        self.written_ip = value
        print(self.written_ip)

    def build(self):
        main_layout = BoxLayout(spacing=2, orientation='horizontal')
        left_side_layout = BoxLayout(spacing=2, orientation='vertical')
        right_side_layout = BoxLayout(spacing=2, orientation='vertical')
        connect_layout = BoxLayout(spacing=2, orientation='vertical')
        program_output_layout = BoxLayout(spacing=2, orientation='vertical')

        program_output_layout.add_widget(self.connection_status_layout)

        ip_input = TextInput(multiline=False)
        ip_input.bind(text=self.on_text)

        connect_layout.add_widget(ip_input)
        connect_layout.add_widget(Button(text='connect', on_press=self.on_connect_press))

        right_side_layout.add_widget(connect_layout)
        right_side_layout.add_widget(program_output_layout)

        left_side_layout.add_widget(self.speed_widget)
        left_side_layout.add_widget(self.speed_max_widget)
        left_side_layout.add_widget(self.a_widget)
        left_side_layout.add_widget(self.a_max_widget)

        main_layout.add_widget(left_side_layout)
        main_layout.add_widget(right_side_layout)

        return main_layout


AppObject = UserApp()

if __name__ == '__main__':
    AppObject.run()
