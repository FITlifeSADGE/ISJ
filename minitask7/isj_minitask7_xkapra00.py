#minitask 7

def deprecated(function):
    def some_old_function(x,y):
        print('Call to deprecated function: ' + function.__name__)
        print(function(x,y))
    return some_old_function

@deprecated
def some_old_function(x, y):
    return x + y

some_old_function(1,2)


# should write:
# Call to deprecated function: some_old_function
# 3