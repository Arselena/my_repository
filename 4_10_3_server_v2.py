import socket
from threading import Thread
import sys

class Server(socket.socket):  # Класс Server, который наследуется от класса socket.socket
    def __init__(self): # В конструкторе определяем основные параметры сервера
        super(Server, self).__init__(socket.AF_INET, socket.SOCK_STREAM)  # Вызываем метод __init__ класса socket.socket, т.е. создаем сокет
        self.bind(('localhost', 12345))  # Привязываем сокет к адресу и порту
        self.listen(3)  # Переводим сервер в готовность принимать данные
        print('Start Server')
        self.client = []
        self.flag = True # Переменная для завершения работы сервера  

    def start_socket(self):
            potok_server = Thread(target = self.stop_server, name='Target Server')  # Создаем поток для сервера, который ждет ввода exit
            potok_server.daemon = True # Будум завершать поток сразу после завершения программы   
            potok_server.start()
            try:
                while self.flag:
                    sock_user, addres_user = self.accept() # Ждем подключения новых клиентов (работает в основном потоке mine()
                    print (addres_user[0], addres_user[1])
                    sock_user.send(('Для выхода exit\n').encode('utf-8')) # Отправляем сообщение для клиентов
                    if sock_user not in self.client: # Если клиент новый, то добавляем в список клиентов
                        self.client.append(sock_user)
                    
                    potok = Thread(target=self.listen_sock, args=(sock_user,), daemon=True)  # Создаем потоки-слушатели для каждого клиента 
                    potok.start()
            except (ConnectionAbortedError, OSError) as e:
                pass
                              
    def send_data(self, data, socket_user=None):  # Отправляем данные клиентам (всем, кроме отправителя)
        for clients in self.client:
            if clients is not socket_user:
                clients.send(data)

    def listen_sock(self, sock_user):  # Слушаем клиентов
        try:
            while self.flag:  # Пока сервер работает читаем и передаем данные
                data_user = sock_user.recv(1024)
                data_user_decod = data_user.decode('utf-8')
                print(data_user_decod)
                
                if data_user_decod[-5:] == ']exit':
                    sock_user.close() # Закрываем сокет клиента
                    self.client.remove(sock_user) # Удаляем сокет из списка
                    break # Выходим из цикла while
                else:
                    self.send_data(data_user, sock_user)
        except (ConnectionResetError, ConnectionAbortedError) as e:  # Ловим ошибку когда клиент вышел из чата не по exit
            sock_user.close() # Закрываем сокет клиента
            self.client.remove(sock_user) # Удаляем сокет из списка
    
    def stop_server(self):
        while self.flag:
            d = input('для выхода введите exit: ')
            if d == 'exit':
                self.flag = False # Завершаем работу циклов в start_socket, listen_sock, stop_server
        self.close()
        sys.exit()
   
My_server = Server()  # Создаем объект сервера
My_server.start_socket()