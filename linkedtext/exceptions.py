
class FileNotFound(Exception):
    def __init__(self, message: str = None):
        if message is None:
            self.message = 'File not Found!'
        else:
            self.message = message
        super().__init__(self.message)
