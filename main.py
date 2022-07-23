# Тут склейка, запуск бота

from typing import NamedTuple


class Parser(NamedTuple):
    first: str
    second: str


# Тут должна быть основная функция, которая по запросу из ТГ
# отдает топ-5 объявлений отсортированных по рангу объявлений
# который хранятся в БД
# Эта функция принимает данные из БД
# В ней вызывается модуль cards(объявления).get_top_cards(функция отдачи 5 объявлений)


def main_func(name: str) -> NamedTuple:
    names = name.split()
    return Parser(first=names[0], second=names[1])


if __name__ == "__main__":
    print(main_func)
