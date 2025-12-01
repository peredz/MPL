import re


def function_ranges(code):
    func_start_pattern = re.compile(
        r'(\w[\w\s:*&<>]*)\s+(\w+)\s*\(([^)]*)\)\s*(\{)' )

    functions = []

    for m in func_start_pattern.finditer(code):
        start_brace = m.end() - 1  # позиция {
        pos = start_brace

        depth = 0
        end = -1

        while pos < len(code):
            if code[pos] == '{':
                depth += 1
            elif code[pos] == '}':
                depth -= 1
                if depth == 0:
                    end = pos
                    break
            pos += 1

        functions.append({
            "name": m.group(2),
            "args": m.group(3),
            "body_start": m.start(4) + 1,
            "body_end": end
        })

    return functions


def read_file(file_name):
    with open(file_name, 'r') as f:
        text = f.read()
    return text


class Program:

    def __init__(self, file_name):
        self.prog_cpp_text = read_file(file_name)
        self.functions_info = list()
        self.functions = list()

    def build(self):
        self.functions_info = function_ranges(self.prog_cpp_text)
        for function_info in self.functions_info:
            function_text = self.prog_cpp_text[
                function_info['body_start']:
                function_info['body_end']]

            self.functions.append(Function(
                function_info['name'],
                function_info['args'],
                function_text))

    def translate(self, output_file):
        with open(output_file, mode='w') as f:
            for function in self.functions:
                f.write(function.translate_text())


class Function:

    def __init__(self, function_name, function_args, function_text):
        self.name = function_name
        self.args = function_args
        self.text = function_text
        self.translated_text = ''

    def translate_text(self):
        args = ''
        if self.args: args = ', '.join([arg.split(' ')[1] for arg in self.args.split(',')])
        if self.name == 'main':
            self.translated_text += "if __name__ == '__main__':\n"
        else:
            self.translated_text += f"def {self.name} ({args}):"
        indent = 1
        for line in self.text.split('\n'):
            m = re.match(r"\s*({|})", line)
            if m:
                if m.group(1) == '{':
                    indent += 1
                elif m.group(1) == '}':
                    indent -= 1
            tabulation = "    " * indent
            # variable declaration
            m = re.match(r"(int|float|double)\s+(\w+)\s*=\s*(.*);", line)
            if m:
                self.translated_text += f"{tabulation}{m.group(2)} = {m.group(3)}"

            # assignment
            m = re.match(r"(\w+)\s*=\s*(.*);", line)
            if m:
                self.translated_text += f"{tabulation}{m.group(1)} = {m.group(2)}"

            # std::cout
            m = re.match(r"std::cout\s*<<\s*(.*?)\s*;", line)
            if m:
                text = m.group(1)
                text = text.replace('<<', ',')
                text = text.replace('std::endl', '\n')
                self.translated_text += f"{tabulation}print({m.group(1)}, end='')"

            # if (...)
            m = re.match(r"if\s*\((.*?)\)\s*\{", line)
            if m:
                self.translated_text += f"{tabulation}if {m.group(1)}:"

            # for (int i = 0; i < n; i++)
            m = re.match(r"for\s*\(\s*int\s+(\w+)\s*=\s*(\d+);\s*(\w+)\s*<(.*?);\s*\w+\+\+\s*\)\s*\{", line)
            if m:
                var = m.group(1)
                start = m.group(2)
                end = m.group(4)
                self.translated_text += f"{tabulation}for {var} in range({start}, {end}):"

            self.translated_text += '\n'
        return self.translated_text

if __name__ == '__main__':
    prog = Program('prog.cpp')
    prog.build()
    prog.translate('prog.py')