def quaterneray(n):
    if n == 0:
        return '0'
    nums = []
    while n:
        n, r = divmod(n, 4)
        nums.append(str(r))
    return ''.join(reversed(nums))

def transition(result):
    quat = quaterneray(result).count('2')
    if result%4 == 1  and (quat==1 or quat==2):
            return 2
    elif result%4 == 2:
        return 3
    elif result%4 == 3:
        return 1
    else:
        return result%4