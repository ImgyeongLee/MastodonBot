#!/usr/bin/python3
# 가챠 기능 (확률 가챠 / 설명 없는 단순 가챠 / 설명 있는 단일 가챠)
import random

import constants
from sheets import gatcha_items, gatcha_items2


# 대략 5% 확률로 초레어, 15% 확률로 레어, 그 외 일반 (확률이 정확하지는 않음)
def _pick_quality():
    random_number = random.randint(1, 100)
    if random_number <= 5:
        return "SUPER_RARE"
    elif random_number <= 20:
        return "RARE"
    return "NORMAL"


# 가챠 (확률 있음)
# API Request   구글 스프레드시트 API 3회
def gatcha_with_prob(n, max_pulls):
    if n > max_pulls:
        return f"한 번에 최대 {max_pulls}번만 연속으로 뽑을 수 있어요!"

    super_rare_items = gatcha_items.col_values(constants.GATCHA_SUPER_RARE)
    rare_items = gatcha_items.col_values(constants.GATCHA_RARE)
    normal_items = gatcha_items.col_values(constants.GATCHA_NORMAL)

    inventory = []
    for _ in range(n):
        quality = _pick_quality()
        if quality == "SUPER_RARE":
            col_data = super_rare_items
        elif quality == "RARE":
            col_data = rare_items
        else:
            col_data = normal_items

        item_list = list(map(str, col_data[1:]))
        pick_num = random.randint(0, len(item_list) - 1)
        inventory.append(item_list[pick_num])

    return ", ".join(inventory) + "를 획득했어요!"


# 가챠 (확률 없음), 아이템 설명 없음
# API Request   구글 스프레드시트 API 1회
def gatcha_without_description(n, max_pulls):
    if n > max_pulls:
        return f"한 번에 최대 {max_pulls}번만 연속으로 뽑을 수 있어요!"

    item_names = gatcha_items2.col_values(constants.GATCHA_ITEM_NAME)
    item_list = list(map(str, item_names[1:]))

    inventory = []
    for _ in range(n):
        pick_num = random.randint(0, len(item_list) - 1)
        inventory.append(item_list[pick_num])

    return ", ".join(inventory) + "를 획득했어요!"


# 가챠 (확률 없음), 아이템 설명 있음, 1회만 뽑음
# API Request   구글 스프레드시트 API 2회
def gatcha_with_description():
    item_names = gatcha_items2.col_values(constants.GATCHA_ITEM_NAME)
    item_descs = gatcha_items2.col_values(constants.GATCHA_ITEM_DESC)

    item_list = list(map(str, item_names[1:]))
    item_desc_list = list(map(str, item_descs[1:]))

    pick_num = random.randint(0, len(item_list) - 1)
    return f"{item_list[pick_num]} 을(를) 뽑았다!" + "\n" + f"설명: {item_desc_list[pick_num]}"
