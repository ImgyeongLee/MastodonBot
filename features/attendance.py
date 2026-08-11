#!/usr/bin/python3
# 출석 기능
from datetime import datetime

import constants
from sheets import attendance


# 출석을 확인하는 함수
# @return   "NONE" (미등록 유저) / "OVERWRITE" (이미 출석함) / 캐릭터 이름 (정상 출석)
# API Request   구글 스프레드시트 API 5회
def check_attendance(account):
    finder = attendance.find(account, in_column=constants.ATTENDANCE_ACCOUNT, case_sensitive=True)
    if not finder:
        return "NONE"

    account_row = finder.row
    current_date = datetime.now().strftime('%Y-%m-%d')
    attendance_count = attendance.cell(account_row, constants.ATTENDANCE_COUNT).value
    previous_date = attendance.cell(account_row, constants.ATTENDANCE_DATE).value

    if attendance_count and previous_date:
        date1 = datetime.strptime(previous_date, "%Y-%m-%d").date()
        date2 = datetime.strptime(current_date, "%Y-%m-%d").date()

        if date1 == date2:
            return "OVERWRITE"

        count = int(attendance_count) + 1
    else:
        count = 1

    attendance.update_cell(account_row, constants.ATTENDANCE_COUNT, count)
    attendance.update_cell(account_row, constants.ATTENDANCE_DATE, current_date)
    return attendance.cell(account_row, constants.ATTENDANCE_NAME).value
