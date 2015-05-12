import operator


def __tuple_apply(op, left, right):
    result = list(left)
    for i in range(len(right)):
        result[i] = op(result[i], right[i])
    return tuple(result)


def tuple_add(left, right):
    return __tuple_apply(operator.add, left, right)


def tuple_sub(left, right):
    return __tuple_apply(operator.sub, left, right)
