#!/usr/bin/python3
# 다이스(nDm) 기능
import random


def roll_dice(n, sides):
    return str(sum(random.randint(0, sides) for _ in range(n)))
