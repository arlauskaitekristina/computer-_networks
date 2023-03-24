import socket
import threading

# Данные для подключения
HOST = '127.0.0.1'
PORT = 55555

# Запуск сервера
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Создаем два списка для хранения подключенных клиентов и их никнеймов позже
clients = []
nicknames = []

# Трансляция чата
def broadcast(message):
    for client in clients:
        client.send(message)

# Обработка сообщений
def manage(client):
    while True:
        try:
            # Прием сообщений
            message = client.recv(1024)
            broadcast(message)
        except:
            # Еесли возникает ошибка с подключением к этому клиенту, мы удаляем его и его никнейм, закрываем подключение и транслируем, 
            # что этот клиент вышел из чата
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} exit!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

# Прием новых подключений 
def receive():
    while True:
        # Прием подключения(адреса)
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Запрос и сохранение никнейма
        client.send('Nickname: '.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Вывод сообщения о подключении
        print("Nickname: {}".format(nickname))
        broadcast("{}".format(nickname).encode('ascii'))
        client.send('\nConnected to server'.encode('ascii'))


        # Запуск обработки подключений
        thread = threading.Thread(target=manage, args=(client,))
        thread.start()

print("listening...")
receive()