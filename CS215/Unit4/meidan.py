def minimize_absolute(L):
    ind = len(L)/2
    while len(L):
        ind, L = arrange_array(ind, L)
    return ind

def arrange_array(ind, A):
    val = A[ind]
    bigger =  [A[i] for i in range(len(A)) if A[i] > val and i != ind]
    smaller = [A[i] for i in range(len(A)) if A[i] <= val and i != ind]
    print smaller, val, bigger
    after_sort_position = len(smaller)
    if after_sort_position == ind:
            return A[ind], []
    if after_sort_position > ind:
        return ind, smaller
    else:
        return ind - len(smaller) - 1, bigger


l = [6,5,4,5]
result = minimize_absolute(l)
print result
print sorted(l)

