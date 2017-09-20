from operator import itemgetter


def main():
    with open('test.txt', 'r') as file:
        number_of_words = int(file.readline())  # N
        words_counts = []
        tokens = []

        # читаем N-строк и записываем
        # (слово, количество повторений) в список
        for _ in range(number_of_words):
            word, count = file.readline().split(" ")
            words_counts.append((word, int(count)))

        number_of_tokens = int(file.readline())  # M

        # читаем M-строк и записываем все токены
        for _ in range(number_of_tokens):
            tokens.append(file.readline().rstrip('\n'))

        # сортируем сперва слова в алфовитном порядке...
        sorted_by_words = sorted(words_counts, key=itemgetter(0))
        # затем сортируем слова в порядке частоты встречаемости
        sorted_by_counts = sorted(sorted_by_words,
                                  key=itemgetter(1),
                                  reverse=True)

        # получаем список слов, упорядоченных в порядке частоты встречаемости
        sorted_words = [lst[0] for lst in sorted_by_counts]

        for token in tokens:
            for word in sorted_words:
                if word.startswith(token):
                    print(word)
            print()


if __name__ == '__main__':
    main()
