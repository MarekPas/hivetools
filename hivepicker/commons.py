import math

def get_int_reputation(rep: float):

    if rep == 0:
        return 25
    score = max([math.log10(abs(rep)) - 9, 0])
    if rep < 0:
        score *= -1
    score = (score * 9.0) + 25.0
    return int(score)