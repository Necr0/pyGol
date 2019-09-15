def quaterneray(n):
    if n == 0:
        return '0'
    nums = []
    while n:
        n, r = divmod(n, 4)
        nums.append(str(r))
    return ''.join(reversed(nums))

def transition(result):
    if result%4 == 1 and quaterneray(result).count('2')==2:
            return 2
    elif result%4 == 2:
        return 3
    elif result%4 == 3:
        return 1
    else:
        return result%4