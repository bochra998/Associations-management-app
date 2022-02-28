import random


def GeneratePassword():
    strins = 'abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?'
    len = 16
    pwd = "".join(random.sample(strins, len))
    return pwd
