class A(object):
    def __init__(self, **kwds):
        for k, v in kwds.items():
            setattr(self, k, v)
    def run(self,a):
        print("a" if getattr(self, "name", None) else "v")
        return self.func(a)


func = lambda x: x+1

a = A(func=func)
print(a.run(2))
