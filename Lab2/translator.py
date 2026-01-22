import re


def convert_expr(expr):
    """Преобразование C++ выражений в Python."""
    expr = expr.replace("&&", " and ")
    expr = expr.replace("||", " or ")
    expr = expr.replace("!", " not ")
    expr = expr.replace("true", "True")
    expr = expr.replace("false", "False")
    return expr


class Function:
    def __init__(self, name, args, text):
        self.name = name
        self.args = args
        self.text = text

    def translate(self):
        """Транслирует функцию C++ в Python."""
        res = []

        # Парсинг аргументов
        args = ''
        if self.args.strip() and self.args.strip() != 'void':
            parts = [a.strip() for a in self.args.split(',')]
            names = [p.split()[-1] for p in parts]
            args = ", ".join(names)

        # Заголовок функции
        if self.name == "main":
            res.append("if __name__ == '__main__':")
        else:
            res.append(f"def {self.name}({args}):")

        indent = 1

        for raw in self.text.split("\n"):
            line = raw.strip()

            if line == '':
                continue

            tab = "    " * indent

            # Управление вложенностью - закрывающая скобка
            if line == "}":
                indent -= 1
                continue

            # Управление вложенностью - открывающая скобка
            if line == "{":
                continue

            # return с выражением
            m = re.match(r"return\s+(.*);", line)
            if m:
                expr = convert_expr(m.group(1))
                res.append(f"{tab}return {expr}")
                continue

            # return без выражения
            if line == "return;":
                res.append(f"{tab}return")
                continue

            # Объявление переменной
            m = re.match(r"(int|float|double|bool|string|void)\s+(\w+)\s*=\s*(.*);", line)
            if m:
                var_name = m.group(2)
                expr = convert_expr(m.group(3))
                res.append(f"{tab}{var_name} = {expr}")
                continue

            # Объявление без инициализации
            m = re.match(r"(int|float|double|bool|string)\s+(\w+);", line)
            if m:
                var_name = m.group(2)
                res.append(f"{tab}{var_name} = None")
                continue

            # Присваивание
            m = re.match(r"(\w+)\s*=\s*(.*);", line)
            if m:
                expr = convert_expr(m.group(2))
                res.append(f"{tab}{m.group(1)} = {expr}")
                continue

            # if
            m = re.match(r"if\s*\((.*?)\)\s*\{?", line)
            if m:
                expr = convert_expr(m.group(1))
                res.append(f"{tab}if {expr}:")
                indent += 1
                continue

            # else if
            m = re.match(r"else\s+if\s*\((.*?)\)\s*\{?", line)
            if m:
                expr = convert_expr(m.group(1))
                res.append(f"{tab}elif {expr}:")
                indent += 1
                continue

            # else
            if line.startswith("else"):
                res.append(f"{tab}else:")
                indent += 1
                continue

            # for обработка только такого вида: for (int i = 0; i < n; i++))
            m = re.match(r"for\s*\(\s*(int|float)?\s*(\w+)\s*=\s*(\d+)\s*;\s*(\w+)\s*<\s*(\w+)\s*;\s*\w+\+\+\s*\)",
                         line)
            if m:
                var = m.group(2)
                start = m.group(3)
                end = m.group(5)
                res.append(f"{tab}for {var} in range({start}, {end}):")
                indent += 1
                continue

            # while
            m = re.match(r"while\s*\((.*?)\)\s*\{?", line)
            if m:
                expr = convert_expr(m.group(1))
                res.append(f"{tab}while {expr}:")
                indent += 1
                continue

            # cout
            m = re.match(r"std::cout\s*<<(.+);", line)
            if m:
                output = m.group(1)
                # Разбиваем по <<
                parts = re.split(r'\s*<<\s*', output)
                # Убираем std::endl
                parts = [p for p in parts if p != 'std::endl']
                if parts:
                    result = ", ".join(parts)
                    res.append(f"{tab}print({result})")
                continue

            # Вызовы функций
            m = re.match(r"(\w+)\s*\((.*?)\);", line)
            if m:
                func_name = m.group(1)
                func_args = m.group(2)
                res.append(f"{tab}{func_name}({func_args})")
                continue

        return "\n".join(res)


def find_functions(code):
    """Находит все функции"""
    # Убираем все #include
    code = re.sub(r'#include.*?\n', '', code)

    functions = []
    lines = code.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Ищем объявление функции
        m = re.match(r'([\w\s:*&<>]+?)\s+(\w+)\s*\(([^)]*)\)', line)
        if m and i + 1 < len(lines) and lines[i + 1].strip() == '{':
            func_name = m.group(2)
            func_args = m.group(3)

            # Находим конец функции
            i += 2  # Пропускаем строку с {
            depth = 1
            body_start = i

            while i < len(lines) and depth > 0:
                if lines[i].strip() == '{':
                    depth += 1
                elif lines[i].strip() == '}':
                    depth -= 1
                i += 1

            body_end = i - 1
            body = '\n'.join(lines[body_start:body_end])

            functions.append({
                "name": func_name,
                "args": func_args,
                "body": body
            })
            continue

        i += 1

    return functions


class Program:
    def __init__(self, file_name):
        self.file_name = file_name
        self.cpp_code = self.read_file(file_name)
        self.functions = []

    def read_file(self, file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Ошибка: файл {file_name} не найден")
            return ""

    def parse(self):
        """Парсит C++ код и извлекает функции."""
        for info in find_functions(self.cpp_code):
            func = Function(info["name"], info["args"], info["body"])
            self.functions.append(func)

    def translate(self, output_file):
        """Транслирует программу в Python."""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for func in self.functions:
                    f.write(func.translate())
                    f.write("\n\n")

            print(f"Трансляция завершена: {output_file}")
        except IOError as e:
            print(f"Ошибка при трансляции: {e}")


if __name__ == "__main__":
    prog = Program("prog.cpp")
    prog.parse()
    prog.translate("prog.py")