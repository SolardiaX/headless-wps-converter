class ConvertException(Exception):
    def __init__(self, text, hr):
        self.text = text
        self.hr = hr

    def __str__(self):
        return "Convert failed: Details - {} ErrCode - {}".format(self.text, hex(self.hr & 0xFFFFFFFF))
