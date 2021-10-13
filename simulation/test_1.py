def func(test, data):
    return eval(test)

data = {"test": 1}
print(func("data['test']+1", data))