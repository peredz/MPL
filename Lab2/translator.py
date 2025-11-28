# реализуем класс функций
# создание и присваивание у переменных
# вывод на экран
# циклы
# условия
#

# надо сделать выделение блоков {}
# выделение скобок

import re

class Program:
    def __init__(self, file_name):
        self.prog_cpp = self.read_file(file_name)
        self.functions = list()

    def read_file(self, file_name):
        with open(file_name, 'r') as f:
            text = f.read()
        return text

    def assemble(self):
        pass

class Func:

    def __init__(self, return_type, *args):
        self.return_type = return_type


if __name__ == '__main__':
    pass