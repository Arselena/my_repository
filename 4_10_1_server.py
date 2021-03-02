import socket

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # Метод socket создает UDP/IP сокет(точку соединения).  
                    # AF_INET - семейство интернет протоколов IPv4
                    # SOCK_DGRAM - датаграммный сокет, использует протокол передачи данных UDP
sock.bind(('192.168.1.84', 49510)) # Связывает сокет с конкретным адресом
                    # bind принимает один аргумент - кортеж из хоста и порта
client = [] # Создает список клиентов
print('Start Server')
while True: 
     data , addres = sock.recvfrom(1024)  # Читает данных из сокета (не более 1024 байт). 
                                          # Возвращает полученные данные и адрес сокета-отправителя
     print(addres[0], addres[1])
     if addres not in client:  # Если клиент новый добавляет его в список
             client.append(addres)
     for clients in client:  # Рассылает данные от клиента всем участникам чата, кроме отправителя
             if clients == addres: 
                 continue
             sock.sendto(data,clients)  