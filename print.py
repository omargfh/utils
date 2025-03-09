from typing import Optional

class PrintUtils:
    def __init__(self):
        pass

    @staticmethod
    def error(*args, **kwargs):
        msg = " ".join(args)
        print(f"\033[91m Error:\t\t \033[0m{msg}", **kwargs)

    @staticmethod
    def info(*args, **kwargs):
        msg = " ".join(args)
        print(f"\033[94m INFO:\t\t \033[0m{msg}", **kwargs)

    @staticmethod
    def success(*args, **kwargs):
        msg = " ".join(args)
        print(f"\033[92m Success:\t\t \033[0m{msg}", **kwargs)

    @staticmethod
    def warning(*args, **kwargs):
        msg = " ".join(args)
        print(f"\033[93m Warning:\t\t \033[0m{msg}", **kwargs)


class FormattedText:
    @staticmethod
    def progress(i: int, total: int):
        return f"[{i}/{total}]"

    @staticmethod
    def percent(i: int, total: int):
        return f"[{(i/total)*100:.2f}%]"
