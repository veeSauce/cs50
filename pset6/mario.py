import cs50

def someFunc():

    while True:
        heightOfPyramid = cs50.get_int("Height: ")
        if heightOfPyramid != 0 and heightOfPyramid > 0:
            break
        if heightOfPyramid < 0:
            someFunc()

    y = 1
    x = heightOfPyramid

    for h in range(heightOfPyramid):
        print(" " * (x-1) + ("#" * y),  end = "")
        #print("  " + ("#" * y), end = "")
        print()
        y += 1
        x = x -1


someFunc()