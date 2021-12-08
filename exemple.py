def place(k):
    x = 0
    y = 0

    if k % 4 == 0:
        x += 1
        print(" modulo 4 reste 0 " + " x=" + str(x) + " y=" + str(y) + " k=" + str(k))
    elif k % 4 == 1:
        y += 1
        print(" modulo 4 reste 1 " + " x=" + str(x) + " y=" + str(y) + " k=" + str(k))
    elif k % 4 == 2:
        x -= 1
        print(" modulo 4 reste 2 " + " x=" + str(x) + " y=" + str(y) + " k=" + str(k))
    elif k % 4 == 3:
        y -= 1
        print(" modulo 4 reste 3 " + " x=" + str(x) + " y=" + str(y) + " k=" + str(k))
    else:
        x = 0
        y = 0
        print(x, y) 
def ex():
    k=0
    for k in range(0, 5):
        place(k)
        k += 1
        print(k)

def func(_static={'counter': 0}):
    _static['counter'] += 1
    print(_static['counter'])

func()


def cardinal(k ,i):

    x = 0
    y = 0


    if k % 4 == 0:
        x += i
    if k % 4 == 1:
        y += i
    if k % 4 == 2:
        x -= i
    if k % 4 == 3:
        y -= i

    print(i)
    place(x, y)

     # cardinal(k, i)
        # k += 1
        # if k % 4 == 0:
        #     i += 1
        # print(k)