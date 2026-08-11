#!/usr/bin/python3
# 이 파일은 프로그래밍적인 값(구글 시트의 탭 이름, 열 번호 등)을 모아둔 곳입니다.
# 명령어(키워드)나 기능 켜기/끄기는 이 파일이 아니라 .env 파일에서 설정합니다.
import re

# 구글 스프레드시트의 워크시트(탭) 이름
# 스프레드시트 템플렛에서 탭 이름을 바꿨다면 여기도 맞춰서 바꿔주세요.
WORKSHEET_SEARCH = "조사"
WORKSHEET_ATTENDANCE = "출석"
WORKSHEET_GATCHA = "가챠"
WORKSHEET_GATCHA2 = "가챠2"
WORKSHEET_STORE = "상점"
WORKSHEET_CHARACTER = "캐릭터"

# 출석 워크시트 열(column) 번호
ATTENDANCE_ACCOUNT = 1
ATTENDANCE_NAME = 2
ATTENDANCE_DATE = 3
ATTENDANCE_COUNT = 4

# 조사 워크시트 열 번호
SEARCH_KEYWORD = 1
SEARCH_DESCRIPTION = 2

# 가챠(확률이 존재) 워크시트 열 번호
GATCHA_NORMAL = 1
GATCHA_RARE = 2
GATCHA_SUPER_RARE = 3

# 가챠(확률이 존재하지 않음) 워크시트 열 번호
GATCHA_ITEM_NAME = 1
GATCHA_ITEM_DESC = 2

# 상점 워크시트 열 번호
STORE_ITEM = 1
STORE_PRICE = 2

# 캐릭터 워크시트 열 번호
CHARACTER_ACCOUNT = 1
CHARACTER_NAME = 2
CHARACTER_MONEY = 3

# 봇이 답글을 달 때 공개 범위 (public, unlisted, private, direct)
REPLY_VISIBILITY = "unlisted"

# 사용자 입력에서 [ ] / 문자를 제외한 특수문자를 제거하는 정규표현식
CLEANER = re.compile(r'[^\w\s\[\]/]')
