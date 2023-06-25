import math
import hashlib

def get_int_reputation(rep: float):
    if rep == 0:
        return 25
    score = max([math.log10(abs(rep)) - 9, 0])
    if rep < 0:
        score *= -1
    score = (score * 9.0) + 25.0
    return int(score)


def salt_password(password, salt):
    salted_password = password + salt.strip().lower()
    hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
    return hashed_password
