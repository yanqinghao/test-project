def test(i, **kwds):
    return ("a" if i==0 else "b")

print(test(1, a=1))