class Token(object):
    def __init__(self, type, value):
        self.type = type;
        self.value = value;

    def __str__(self):
        return "{type}  {value}".format(type=self.type, value=self.value)

    __repr__ = __str__
