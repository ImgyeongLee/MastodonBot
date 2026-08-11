#!/usr/bin/python3
# 키워드로 이루어지는 조사 기능
import constants
from sheets import search


# API Request   구글 스프레드시트 API 2회
def investigate(keyword):
    finder = search.find(keyword, in_column=constants.SEARCH_KEYWORD, case_sensitive=True)
    if not finder:
        return "존재하지 않는 조사 키워드입니다."

    description = search.cell(finder.row, constants.SEARCH_DESCRIPTION).value
    return f"[{keyword}] {description}"
