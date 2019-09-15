spawnrule=[
    10,
    34,
    66,
    130,
    258,
    20,
    36,
    68,
    132,
    260,
    24,
    72,
    136,
    264,
    48,
    144,
    272,
    96,
    160,
    320]


def transition(result):
    if result%2 == 1 and bin(result)[2:].count("1") in range(2,4):
        return 1
    elif result in spawnrule:
        return 1
    else:
        return 0