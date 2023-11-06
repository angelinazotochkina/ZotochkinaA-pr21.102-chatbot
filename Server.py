import socket
import threading


# Хранит данные о пользователе
class Client:
    def __init__(self, name_, socket):
        self.name = str(name_)
        self.client_socket = socket


# Отправляет новое сообщение всем, кроме указанного клиента
def notify_all(clients, client, message):
    for c in clients:
        if c != client:
            try:
                c.client_socket.send((client.name + ": " + str(message)).encode())
            except:
                try:
                    clients.remove(c)
                except ValueError:
                    pass
                print("Couldn't notify client")
                notify_all(clients, client, c.name + " exit chat")


# принимает сообщения у каждого клиента
def handle_client(client, clients):
    x = True
    iii = 0

    # получаем имя пользователя
    while x:
        try:
            request = client.client_socket.recv(1024)
            client.name = str(request.decode())
            x = False
        except:
            x = True
            iii = iii + 1

            if iii > 10:
                return

    notify_all(clients, client, client.name + " joined chat")

    # принимаем сообщения
    while True:
        try:
            request = client.client_socket.recv(1024)
        except:
            break

        if not request:
            break

        notify_all(clients, client, request.decode())

    # отсюда клиент больше не сможет отправлять сообщения
    notify_all(clients, client, (client.name + " exit chat").encode())

    client.client_socket.close()
    if client in clients:
        clients.remove(client)


def main():
    # подключаемся, готовим сокеты для клиентов
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 4000))
    server_socket.listen(5)
    clients = []

    # принимаем новых клиентов
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established!")

        newClient = Client("", client_socket)
        clients.append(newClient)

        # работаем с каждым новым клиентом в отдельном потоке
        client_thread = threading.Thread(target=handle_client, args=(newClient, clients))
        client_thread.start()


print("Server start")
main()