import socket
import threading

def read_sok():
     while True:
         data = sor.recv(1024)  # Считывает данные сокета-сервера
         print(data.decode('utf-8'))  # Декодирует и печатает данные из сокета (переводит тип данных из byts в str)

server = '192.168.1.84', 49510 # адрес сервера
alias = input('введите nick: ') # Записывает имя, которое ввел клиент
sor = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  # Создает сокет клиента (IPv4, UDP)
sor.bind(('', 0))  # Связывает сокет клиента со всеми доступными интерфейсами IPv4
sor.sendto((alias + ' Connect to server').encode('utf-8'), server) # Отправляет данные в сокет. 
                                                                   # Сокет назначения указан во 2-ом параметре
potok = threading.Thread(target = read_sok) # Создает поток 
potok.start() # Стартует поток
while True:
     mensahe = input() # Записывает данные, которые ввел клиент
     sor.sendto(('[' + alias  + '] ' + mensahe).encode('utf-8'), server) # Передает данные серверу о подключении