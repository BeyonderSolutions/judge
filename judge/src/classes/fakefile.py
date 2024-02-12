import io


class FakeFile(io.StringIO):
    def __init__(self):
        super().__init__()
        self.buffer = self

    def write(self, s):
        if isinstance(s, bytes):
            # Decode bytes to a string and write
            s = s.decode('utf-8')
        super().write(s)

    def getvalue(self):
        return super().getvalue()
