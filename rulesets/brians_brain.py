def ternary(n):
    if n == 0:
        return '0'
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    return ''.join(reversed(nums))

def transition(result):
    if result%3 == 0 and ternary(result).count('1')==2:
        return 1
    elif result%3 == 1:
        return 2
    else:
        return 0