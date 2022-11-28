import math

def get_int_reputation(reputation: float):
    if reputation == 0:
        return 0
    else:
        return int(math.log10((abs((reputation))-9)*9)+25)