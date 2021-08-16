class A:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def a(self):
        return getattr(self, "_a", None)

    @a.setter
    def a(self, value):
        self._a = value

test = A()
print(test.a)
test.a = 2
print(test.a)
