from translator import Program


if __name__ == "__main__":
    """
    Транслируем из С++ в Python
    Поддерживает обработку функций, объявления переменных,
    присваивание, цикл for, условные конструкции, вывод в консоль.
    """

    prog = Program("prog.cpp")
    prog.parse()
    prog.translate("prog.py")