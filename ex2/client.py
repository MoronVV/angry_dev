#!/usr/bin/env python
import socket
import pickle
from sys import argv
from threading import Thread

# импортим из server.py, так как функция та же
from server import get_port_number


class Client:

    def __init__(self, ip, port):
        # создаем сокет с IPv4 и TCP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # создаем сокет с IPv4 и TCP
        self.sock.connect((ip, port))

        # создаем процесс для отправки сообщений
        input_thread = Thread(target=self.sendMsg)
        # закрываем программу не смотря на рабочие процессы
        input_thread.daemon = True
        # запуск треда
        input_thread.start()

        # ждем ответа от сервера
        while True:
            # получаем данные от сервера
            data = self.sock.recv(4096)

            # клиент отключился
            if not data:
                print("Connection with server was lost")
                break

            # избавляемся от сериализации
            unpickled = pickle.loads(data)

            # если ответ - список, тогда выводим клиенту слова
            if isinstance(unpickled, list):
                for word in unpickled:
                    print(word)
            # в ином случае - это сообщение об ошибке, выводим
            else:
                print(unpickled)
            print()

    def sendMsg(self):
        """Метод занимается отправкой запросов на сервер"""
        while True:
            self.sock.send(input().encode('utf-8'))


def get_ip_address():
    """
    Получаем ip-адрес, если аргумент присутствует.
    В противном случае возвращаем localhost
    """
    try:
        return argv[1]
    except IndexError:
        return '127.0.0.1'


def main():
    ip = get_ip_address()
    port = get_port_number()
    try:
        Client(ip, port)
    except KeyboardInterrupt:
        print("Connection is closed")


if __name__ == '__main__':
    main()
