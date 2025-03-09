class PrintUtils:
    def __init__(self):
        pass

    @staticmethod
    def error(msg: str):
        print(f"\033[91m Error:\t\t \033[0m{msg}")

    @staticmethod
    def info(msg: str):
        print(f"\033[94m INFO:\t\t \033[0m{msg}")

    @staticmethod
    def success(msg: str):
        print(f"\033[92m Success:\t\t \033[0m{msg}")

    @staticmethod
    def warning(msg: str):
        print(f"\033[93m Warning:\t\t \033[0m{msg}")

    @staticmethod
    def progress(i: int, total: int):
        PrintUtils.info(f"[{i}/{total}]")

    @staticmethod
    def percent(i: int, total: int):
        PrintUtils.info(f"[{(i/total)*100:.2f}%]")
