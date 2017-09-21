import socket
import os
import pickle
from sys import argv
from collections import Counter
from operator import itemgetter
from threading import Thread


class Server:

    def __init__(self, filename, port):
        # получаем словарь вида: {слово: частота повторений}...
        words_counts = get_words_count(filename)
        # ...и преобразуем его в отсортированный по алфавиту,
        # затем по чаcтоте встречаемости списку и храним в объекте
        self.sorted_words = sorting_words_by_count(words_counts)

        # создаем сокет с IPv4 и TCP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # строка ниже для избежания ошибки "Address already in use"
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # создаем сокет с IPv4 и TCP
        self.sock.bind(('0.0.0.0', port))
        # говорим сокету начинать слушать
        self.sock.listen(1)
        print(f'Running server on 0.0.0.0:{port}')

    def handler(self, conn, addr):
        """
        Метод ждет от клиента данные (запрос) и после манипуляций
        отправляет данные обратно клиенту (ответ)
        """
        while True:
            # принимаем данные от клиента
            data = conn.recv(4096).decode()

            # если клиент отключился, закрываем подключение
            if not data:
                print(f'{str(addr[0])}:{str(addr[1])} disconnected')
                conn.close()
                break

            print(f'({str(addr[0])}:{str(addr[1])}) Recived: {data}')

            # проверяем форму запроса (должна быть вида: get <prefix>)
            if data.split()[0] == 'get' and data.split()[1]:
                token = data.split()[1]

                # получаем список слов, начинающийся с токена
                words_with_token = get_words_starting_with_token(
                    self.sorted_words, token
                )

                # используем pickle для сериализации списка...
                pickled_list = pickle.dumps(words_with_token)
                # ...и отправляем клиенту
                conn.send(pickled_list)
            # в случае несоответствия форме запроса
            # сериализуем и отправляем сообщение об ошибке
            else:
                err_msg = pickle.dumps('Wrong request. Use "get <prefix>"')
                conn.send(err_msg)

    def run(self):
        """Метод для запуска сервера"""
        while True:
            # принимаем клиента и получаем данные о нем
            conn, addr = self.sock.accept()
            # выделяем для нового клиента собственный процесс
            conn_thread = Thread(target=self.handler, args=(conn, addr))
            # закрываем программу не смотря на рабочие процессы
            conn_thread.daemon = True
            # запуск треда
            conn_thread.start()
            print(f'{str(addr[0])}:{str(addr[1])} connected')


def get_words_count(filename):
    """Получение файла и возврат слов и их количества повторений"""
    # узнаем директорию, откуда выполняется скрипт
    script_dir = os.path.dirname(__file__)

    # открываем файл для чтения
    with open(os.path.join(script_dir, filename), 'r') as file:
        # считаем слова и возвращаем список кортежей
        # (слово, количество повторений)
        words_counts = Counter(file.read().split())
        return list(words_counts.items())


def sorting_words_by_count(words_counts):
    """Получение отсортированных слов по частоте встречаемости (и алфавиту)"""
    # сортируем сперва слова в алфовитном порядке...
    sorted_by_words = sorted(words_counts, key=itemgetter(0))
    # ...затем сортируем слова в порядке частоты встречаемости
    sorted_by_counts = sorted(sorted_by_words,
                              key=itemgetter(1),
                              reverse=True)

    # получаем список слов, упорядоченных в порядке частоты встречаемости
    return [lst[0] for lst in sorted_by_counts]


def get_words_starting_with_token(words, token):
    """
    Обеспечивает вывод слов,
    которые содержат соответствующие токены начала
    """
    result_words = []
    for word in words:
        # если токен есть в начале слова...
        if word.startswith(token):
            result_words.append(word)

    return result_words


def get_filename():
    """
    Получаем имя файла, если аргумент присутствует.
    В противном случае возвращаем тестовый test.txt.
    Файл должен находиться в той же папке, что и этот скрипт
    """
    try:
        return argv[1]
    except IndexError:
        return 'test.txt'


def get_port_number():
    """
    Получаем номер порта, если аргумент присутствует.
    В противном случае возвращаем номер 8000
    """
    try:
        return int(argv[2])
    except IndexError:
        return 8000


def main():
    filename = get_filename()
    port = get_port_number()
    server = Server(filename, port)

    try:
        server.run()
    except KeyboardInterrupt:
        print('Shutting down...')


if __name__ == '__main__':
    main()
