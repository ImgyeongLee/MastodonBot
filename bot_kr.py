#!/usr/bin/python3
from mastodon import Mastodon
from mastodon.streaming import StreamListener
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
from datetime import datetime
import re
import random
import gspread


# 봇 세팅
# api_base_url의 경우, 마스토돈 서버마다 다르게 설정해주어야 함.
# 본인은 일단 기본적으로 플래닛 서버를 쓰기에 플래닛으로 설정함.
mastodon = Mastodon(
        client_id="클라이언트 키를 복사 붙여넣기 하세요.",
        client_secret="클라이언트 비밀 키를 복사 붙여넣기 하세요.",
        access_token="액세스 토큰을 복사 붙여넣기 하세요",
        api_base_url="https://planet.moe"
        )

# 구글 스프레드시트 세팅
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

# 비공개 키 (Credential key) 파일 이름 (.json)
json = "비공개키파일이름.json"

credentials = ServiceAccountCredentials.from_json_keyfile_name(json, scope)

# 구글 스프레드시트에 연결
gc = gspread.authorize(credentials)

# 스프레드시트 열기 (스프레드시트 URL)
sh = gc.open_by_url("당신의 구글스프레드시트URL")

# 워크시트 선택
search = sh.worksheet("조사")
attendance = sh.worksheet("출석")
gatcha_items = sh.worksheet("가챠")
store = sh.worksheet("상점")
character = sh.worksheet("캐릭터")

# 워크시트 열 (column) 정리
# 출석
ATTENDANCE_ACCOUNT = 1
ATTENDANCE_NAME = 2
ATTENDANCE_DATE = 3
ATTENDANCE_COUNT = 4

# 조사
SEARCH_KEYWORD = 1
SEARCH_DESCRIPTION = 2

# 가챠
GATCHA_NORMAL = 1
GATCHA_RARE = 2
GATCHA_SUPER_RARE = 3

# 상점
STORE_ITEM = 1
STORE_PRICE = 2

# 캐릭터
CHARACTER_ACCOUNT = 1
CHARACTER_NAME = 2
CHARACTER_MONEY = 3

# [/]빼고 전부 제거하는 정규 표현식
CLEANER = re.compile('[^\w\s\[\]/]')


# 깔끔한 텍스트를 얻는 함수
# @param    rawText:string
# @return   string
def filterText(rawText):
    soup = BeautifulSoup(rawText, 'html.parser')
    parsed_text = soup.get_text(strip=True)
    filtered_text = re.sub(CLEANER, '', parsed_text)
    return filtered_text


# 다이스, nDm을 굴림
# @param    n:number
# @param    m:number
# @return   int
def dice(n, m):
    random_number = sum(random.randint(0, m) for _ in range(n))
    return random_number


# 참 거짓
# @return string
def trueOrFalse():
    result = random.randint(0, 1)

    if result == 0:
        return "False"
    else:
        return "True"


# 가챠
# @param    n:number - 가챠 횟수
# @return   list
def gatcha(n):
    if n > 10:
        return "한 번에 최대 10번만 연속으로 뽑을 수 있어요!"

    inventory = []
    for _ in range(n):
        quality = gatcha_helper()

        if quality == "SUPER_RARE":
            col_data = gatcha_items.col_values(GATCHA_SUPER_RARE)
        elif quality == "RARE":
            col_data = gatcha_items.col_values(GATCHA_RARE)
        else:
            col_data = gatcha_items.col_values(GATCHA_NORMAL)

        items = col_data[1:]
        item_list = list(map(str, items))
        max_len = len(item_list)

        pick_num = random.randint(0, max_len - 1)
        inventory.append(item_list[pick_num])

    result = ", ".join(inventory) + "를 획득했어요!"
    return result


# 가챠 헬퍼 함수. 가챠의 등급을 결정해준다. (일반 - 레어 - 초레어)
# 대략 5% 확률로 초레어, 15% 확률로 레어, 그 외 일반 (물론, 확률이 정확하지 않음)
# @return   string
def gatcha_helper():
    random_number = random.randint(0, 100)

    if random_number <= 5:
        return "SUPER_RARE"
    elif random_number <= 20:
        return "RARE"
    else:
        return "NORMAL"


# 출석을 확인하는 함수
# @param    account:string
# @return   string
def checkAttendance(account):
    # 계정을 스프레드시트에서 찾음
    finder = attendance.find(account, in_column=ATTENDANCE_ACCOUNT, case_sensitive=True)
    account_row = finder.row

    # 만약 계정이 시트에 있을 경우, 출석을 체크하고 캐릭터의 이름을 반환함
    if account_row:
        current_datetime = datetime.now().strftime('%Y-%m-%d')
        count = int(attendance.cell(account_row, ATTENDANCE_COUNT).value)
        attendance.update_cell(account_row, ATTENDANCE_COUNT, count + 1)
        attendance.update_cell(account_row, ATTENDANCE_DATE, current_datetime)
        character_name = attendance.cell(account_row, ATTENDANCE_NAME).value
        return character_name
    # 계정이 시트에 존재하지 않을 경우, X를 반환
    else:
        return "X"


# 키워드로만 이루어지는 조사
# @param    keyword:string
# @return   string
def investigate(keyword):
    # 키워드가 있는지 확인
    finder = search.find(keyword, in_column=SEARCH_KEYWORD, case_sensitive=True)
    if finder:
        keyword_row = finder.row
    else:
        return "존재하지 않는 키워드입니다."

    result = f"[{keyword}]: " + search.cell(keyword_row, SEARCH_DESCRIPTION).value

    return result


# 상점구입
# @param    account:string
# @param    item:string
# @return   string
def buySomething(account, item):
    store_finder = store.find(item, in_column=STORE_ITEM, case_sensitive=True)
    if store_finder:
        item_row = store_finder.row
    else:
        return '존재하지 않는 아이템이에요!'

    character_finder = character.find(account, in_column=CHARACTER_ACCOUNT, case_sensitive=True)
    if character_finder:
        account_row = character_finder.row
    else:
        return '존재하지 않는 유저입니다.'

    if item_row:
        price = int(store.cell(item_row, STORE_PRICE).value)
        money = int(character.cell(account_row, CHARACTER_MONEY).value)
        if isAffordable(price, money):
            budget = money - price
            character.update_cell(account_row, CHARACTER_MONEY, budget)
            user_name = character.cell(account_row, CHARACTER_NAME).value
            return f'{user_name}님, 성공적으로 {item}을 구매했어요! (잔액: {budget})'
        else:
            return '이런, 재화가 부족하네요!'
    return '함수에 오류가 있는 것 같으니 제보 바랍니다.'


# 상점구입 헬퍼함수
# @param    price:number
# @param    money:number
# @return   boolean
def isAffordable(price, money):
    return money > price


# 이벤트 리스너
class Listener(StreamListener):
    def on_notification(self, notification):
        if notification['type'] == "mention":
            print("타입이 멘션입니다.")
            print("내용은 다음과 같습니다 == " + notification['status']['content'])

            user_text = filterText(notification['status']['content'])

            print("user_text는 다음과 같습니다 == " + user_text)

            # 형식이 올바르다면
            if '[' in user_text and ']' in user_text:

                cmdStart = user_text.find("[") + 1
                cmdEnd = user_text.find("]")

                user_text = user_text[cmdStart:cmdEnd]

                # 가챠
                # 키워드 형식: [조사/키워드]
                if "조사" in user_text and '/' in user_text:
                    keyword_start = user_text.find("/") + 1
                    keyword = user_text[keyword_start:]
                    result = investigate(keyword)
                    mastodon.status_post(f"@{notification['status']['account']['acct']} " + result, in_reply_to_id=notification['status']['id'], visibility='unlisted')

                # 가챠
                # 키워드 형식: [가챠/n]
                elif "가챠" in user_text and '/' in user_text:
                    round_start = user_text.find("/") + 1
                    round = int(user_text[round_start:])
                    result = gatcha(round)
                    mastodon.status_post(f"@{notification['status']['account']['acct']} " + result, in_reply_to_id=notification['status']['id'], visibility='unlisted')

                # 상점
                # 키워드 형식: [구매/아이템 이름]
                elif "구매" in user_text and '/' in user_text:
                    user_account = notification['status']['account']["username"]
                    item_start = user_text.find("/") + 1
                    item = user_text[item_start:]
                    result = buySomething(user_account, item)
                    mastodon.status_post(f"@{notification['status']['account']['acct']} " + result, in_reply_to_id=notification['status']['id'], visibility='unlisted')

                # 출석
                # 키워드 형식: [출석]
                elif "출석" in user_text:
                    user_account = notification['status']['account']["username"]
                    user_name = checkAttendance(user_account)
                    if user_name != 'X':
                        mastodon.status_post(f"@{notification['status']['account']['acct']} {user_name}님, 어서오세요. 오늘 출석하셨네요!", in_reply_to_id=notification['status']['id'], visibility='unlisted')
                    else:
                        mastodon.status_post(f"@{notification['status']['account']['acct']} 존재하지 않는 이름이에요!", in_reply_to_id=notification['status']['id'], visibility='unlisted')

                # 다이스
                # 키워드 형식: [ndm] 혹은 [nDm]
                elif "D" in user_text or "d" in user_text:

                    if "D" in user_text:
                        user_text = user_text.lower()

                    nMid = user_text.find("d")

                    n = int(user_text[:nMid].strip())
                    m = int(user_text[nMid + 1:].strip())

                    result = dice(n, m)
                    mastodon.status_post(f"@{notification['status']['account']['acct']} {result}", in_reply_to_id=notification['status']['id'], visibility='unlisted')

                # 참/거짓
                # 키워드 형식: [T/F]
                elif "T" in user_text and "F" in user_text and '/' in user_text:
                    result = trueOrFalse()
                    mastodon.status_post(f"@{notification['status']['account']['acct']} {result}", in_reply_to_id=notification['status']['id'], visibility='unlisted')

            else:
                mastodon.status_post(f"@{notification['status']['account']['acct']} 키워드 형식이 올바르지 않은 것 같아요.", in_reply_to_id=notification['status']['id'], visibility='unlisted')
                print("형식이 올바르지 아니함")

    def handle_heartbeat(self):
        return super().handle_heartbeat()


# 메인함수
def main():
    mastodon.stream_user(Listener())


# 실행
if __name__ == '__main__':
    main()