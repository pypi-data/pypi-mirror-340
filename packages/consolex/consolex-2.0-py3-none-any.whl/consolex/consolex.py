class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class console:
    @staticmethod
    def log(*texts, sep=' ', end='\n'):
        for i in range(len(texts)):
            print(texts[i], end=sep if i != len(texts) - 1 else '')
        print(end, end='')

    @staticmethod
    def warn(*texts, sep=' ', end='\n'):
        print(bcolors.WARNING+"⚠️  | ", end='')
        console.log(*texts, sep=sep, end=end)
        print(bcolors.ENDC,end='')

    @staticmethod
    def error(*texts, sep=' ', end='\n'):
        print(bcolors.FAIL+"❌ | ", end='')
        console.log(*texts, sep=sep, end=end)
        print(bcolors.ENDC,end='')

    @staticmethod
    def success(*texts, sep=' ', end='\n'):
        print(bcolors.OKGREEN+"✅ | ", end='')
        console.log(*texts, sep=sep, end=end)
        print(bcolors.ENDC,end='')
    
    @staticmethod
    def primary(*texts, sep=' ', end='\n'):
        print(bcolors.OKBLUE+"", end='')
        console.log(*texts, sep=sep, end=end)
        print(bcolors.ENDC,end='')