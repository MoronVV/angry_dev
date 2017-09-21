#!/usr/bin/env python
from operator import itemgetter


def get_words_and_counts():
    """
    Получение слов и число раз, которое встречается это слово в текстах
    (от пользователя)
    """
    number_of_words = int(input())  # N
    words_counts = []  # (w_i, n_i)

    # читаем N-строк и записываем
    # (слово, количество повторений) в список
    for _ in range(number_of_words):
        word, count = input().split(" ")
        words_counts.append((word, int(count)))

    return words_counts


def get_tokens():
    """Получение начала слов (от пользователя)"""
    number_of_tokens = int(input())  # M
    tokens = []  # u_i

    # читаем M-строк и записываем все токены
    for _ in range(number_of_tokens):
        tokens.append(input().rstrip('\n'))

    return tokens


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


def output(words, tokens):
    """
    Обеспечивает вывод слов,
    которые содержат соответствующие токены начала
    """
    print("#" * 20)
    for token in tokens:
        for word in words:
            # если токен есть в начале слова...
            if word.startswith(token):
                print(word)
        print()


def main():
    # получаем слова и числа (частота, с которой они встречаются в тексте)
    number_of_words = get_words_and_counts()

    # получаем начала слов (токены)
    tokens = get_tokens()

    # сортируем список предоставленных слов по частоте встречаемости
    sorted_words = sorting_words_by_count(number_of_words)

    # выводим слова, подходящие под условие, на экран
    output(sorted_words, tokens)


if __name__ == '__main__':
    main()
