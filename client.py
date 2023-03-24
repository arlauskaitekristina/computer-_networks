# Необходимо написать программу-клиент, которая будет цепляться к вашему серверу в Интернете - 158.160.19.47 
# порт 55555, после того как соединение произошло, первое сообщение будет ником пользователя 
# (после подключения сервер отправляет 'NICK'), а далее, любое отправленное сообщение сервер будет транслировать 
# всем другим клиентам. Таким образом клиенты общаются между собой.

import socket, threading
from time import sleep

# Открываем сокет
sock = socket.socket()

# Коннектимся
addr = ("127.0.0.1", 55555) # ip-адрес яндекса и https-порт
sock.connect(addr)

# Подготовим HTTP-запрос
# вначале b - переводим в двоичный вид
def sock_send(data):
    sock.send(data)

def sock_recieve():
# Передаём размер буфера - по сколько байт будем перехватывать с нашей сетевой карты приходящих на неё данных и заносить в переменную
    while True:
        data_in = sock.recv(1024)
        print(data_in.decode('ascii'))

sock_send(b"marsel")

rec_thread = threading.Thread(target=sock_recieve)
rec_thread.start()

while True:
    data = input()
    if data == '0':
        sock.close()
    sock_send(f"marsel: {data}".encode('ascii'))