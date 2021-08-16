import random
def test():
    while True:
        yield random.random()


def testH():
    for i in test():
        yield i
        print("jhhhhh")
        import time
        time.sleep(1)


def main():
    for i in testH():
        print(i)


main()