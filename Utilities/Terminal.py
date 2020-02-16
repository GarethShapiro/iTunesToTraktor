class Terminal:

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @classmethod
    def header(self, string, ownline = False):
        Terminal(f"{Terminal.HEADER}{string}{Terminal.ENDC}", ownline)

    @classmethod
    def info(self, string, ownline = False):
        Terminal(f"{Terminal.OKGREEN}{string}{Terminal.ENDC}", ownline)

    @classmethod
    def ok(self, string, ownline = False):
        Terminal(f"{Terminal.OKBLUE}{string}{Terminal.ENDC}", ownline)

    @classmethod
    def warning(self, string, ownline = False):
        Terminal(f"{Terminal.WARNING}{string}{Terminal.ENDC}", ownline)

    @classmethod
    def fail(self, string, ownline = False):
        Terminal(f"{Terminal.FAIL}{string}{Terminal.ENDC}", ownline)
        
    @classmethod
    def bold(self, string, ownline = False):
        Terminal(f"{Terminal.BOLD}{string}{Terminal.ENDC}", ownline)

    @classmethod
    def underline(self, string, ownline = False):
        Terminal(f"{Terminal.UNDERLINE}{string}{Terminal.ENDC}", ownline)

    def __init__(self, string, ownline):

        delimeter = "\n" if ownline == True else ""
        print(delimeter + string + delimeter)
