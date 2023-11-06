import socket
import threading

print("client start")

# подключение к серверу
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 4000))

# функция для чтения сообщений от сервера
def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode().strip("b'")
            print(message)
        except:
            # если возникла ошибка, то выходим из цикла
            print('An error occurred!')
            client_socket.close()
            break

# функция для отправки сообщений на сервер
def send():

    print("enter your nickname as a first message")

    while True:
        message = input()
        client_socket.sendall(message.encode())


#потоки для получения сообщений от сервера и отправки

receive_thread = threading.Thread(target=receive)
receive_thread.start()

send_thread = threading.Thread(target=send)
send_thread.start()