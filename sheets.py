#!/usr/bin/python3
# 구글 스프레드시트 연결 및 워크시트(탭) 참조를 모아둔 파일
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import config
import constants

_SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
]

_credentials = ServiceAccountCredentials.from_json_keyfile_name(config.GOOGLE_CREDENTIAL_JSON, _SCOPE)
_gc = gspread.authorize(_credentials)
_sh = _gc.open_by_url(config.GOOGLE_SHEET_URL)

search = _sh.worksheet(constants.WORKSHEET_SEARCH)
attendance = _sh.worksheet(constants.WORKSHEET_ATTENDANCE)
gatcha_items = _sh.worksheet(constants.WORKSHEET_GATCHA)
gatcha_items2 = _sh.worksheet(constants.WORKSHEET_GATCHA2)
store = _sh.worksheet(constants.WORKSHEET_STORE)
character = _sh.worksheet(constants.WORKSHEET_CHARACTER)
