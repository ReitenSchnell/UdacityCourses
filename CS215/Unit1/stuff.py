def naive(a, b):
    x = a
    y = b
    z = 0
    while x > 0:
        z = z + y
        x = x - 1
    return z

def click(n):
    print 'click'
    for j in range(n):
        for i in range(j):
            print j,i
def count(n):
    # Your code here to count the units of time
    # it takes to execute clique
    return 2 + n + sum(range(n))

print count(4)