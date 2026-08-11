#!/usr/bin/python3
# 상점 구매 기능
import constants
from sheets import character, store


def _is_affordable(price, money):
    return money >= price


# API Request   구글 스프레드시트 API 6회
def buy_something(account, item):
    store_finder = store.find(item, in_column=constants.STORE_ITEM, case_sensitive=True)
    if not store_finder:
        return '존재하지 않는 아이템이에요!'

    character_finder = character.find(account, in_column=constants.CHARACTER_ACCOUNT, case_sensitive=True)
    if not character_finder:
        return '존재하지 않는 유저입니다.'

    price = int(store.cell(store_finder.row, constants.STORE_PRICE).value)
    money = int(character.cell(character_finder.row, constants.CHARACTER_MONEY).value)

    if not _is_affordable(price, money):
        return '재화가 부족합니다.'

    budget = money - price
    character.update_cell(character_finder.row, constants.CHARACTER_MONEY, budget)
    user_name = character.cell(character_finder.row, constants.CHARACTER_NAME).value
    return f'{user_name}님, 성공적으로 {item}을 구매했어요! (잔액: {budget})'
