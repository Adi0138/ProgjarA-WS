import random

random.seed(123456)
for ii in range(10000):
    nn = random.randint(1, 1000)
    if nn % 2 == 0:
        print("ADD", nn)
    else:
        #print("ADD -%d" % (nn,))
        print("DEC", nn)
