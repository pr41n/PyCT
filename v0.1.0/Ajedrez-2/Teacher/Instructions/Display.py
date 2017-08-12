import turtle

def print_new_line():
        turtle.forward(10)


def print_new_col( integer):
    if integer % 2 == 0:
        print "||||    " * 4
        print "||||    " * 4
    else:
        print "    ||||" * 4
        print "    ||||" * 4

if __name__ == '__main__':
    for i in range(1, 9):
        print_new_line()
        print_new_col(i)
    print_new_line()