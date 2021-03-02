import socket
from threading import Thread

class Client(socket.socket): # Инициализируем отсновные параметры клиента
    def __init__(self):
        super(Client, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(('localhost', 12345))
        self.alias = input('Введите имя: ')
        self.send((self.alias + ' Connect to server').encode('utf-8'))

    def read_sok(self):  # Читаем данные с сервера
        try:
            while True:
                data = self.recv(1024)
                print(data.decode('utf-8'))
        except (ConnectionResetError, ConnectionAbortedError) as e:
            print('Сервер не работает или вы вышли из чата')

            
    def start_client(self):
        potok = Thread(target=self.read_sok, daemon=True) # Читаем данные с сервера в отдельном потоке
        potok.start()
        
        while True:  # Ждем ввода данных и отправляем на сервер
            mensahe = input()
            if mensahe == 'exit':
                break
            else:
                self.send(('[' + self.alias  + ']' + mensahe).encode('utf-8'))
        
        self.close()

My_Client = Client()  # Создаем объект клиента
My_Client.start_client()