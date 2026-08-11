#!/usr/bin/python3
# ===========================================================================
# 이 파일은 .env 파일에 적힌 설정값을 읽어들이는 역할만 합니다.
# 프로그래밍을 모르셔도 됩니다. 실제로 값을 바꾸는 곳은 .env 파일입니다.
# (.env.sample 을 복사해서 .env 로 이름을 바꾼 뒤, 그 안의 값을 수정해주세요.)
# ===========================================================================
import os

from dotenv import load_dotenv

load_dotenv()


def _get_bool(env_name, default):
    value = os.getenv(env_name)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "y", "on")


def _get_str(env_name, default):
    value = os.getenv(env_name)
    if value is None or value.strip() == "":
        return default
    return value.strip()


# 마스토돈 봇 접속 정보
MASTODON_CLIENT_ID = os.getenv("CLIENT_ID")
MASTODON_CLIENT_SECRET = os.getenv("CLIENT_SECRET")
MASTODON_ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
MASTODON_API_BASE_URL = os.getenv("API_BASE_URL")

# 구글 스프레드시트 접속 정보
GOOGLE_CREDENTIAL_JSON = os.getenv("CRENDENTIAL_JSON")
GOOGLE_SHEET_URL = os.getenv("GOOGLE_SHEET_URL")

# 가챠를 한 번에 최대 몇 번까지 연속으로 뽑을 수 있는지
GATCHA_MAX_PULLS = int(_get_str("GATCHA_MAX_PULLS", "10"))

# ===========================================================================
# 기능 켜기/끄기 & 명령어(키워드) 설정
# ===========================================================================
# enabled: True 면 기능이 켜짐, False 면 꺼짐 (해당 명령어에 봇이 반응하지 않음)
# keyword: 사용자가 멘션으로 [키워드] 형태로 부르는 단어
#
# gatcha_prob 와 gatcha_desc 는 기본값이 둘 다 "가챠" 인데, 이건 정상입니다.
# [가챠] (숫자 없이) 로 부르면 gatcha_desc가, [가챠/5] 처럼 숫자와 함께 부르면
# gatcha_prob 가 실행되므로 같은 단어를 써도 서로 구분됩니다.
COMMANDS = {
    "investigate": {
        "enabled": _get_bool("ENABLE_INVESTIGATE", True),
        "keyword": _get_str("KEYWORD_INVESTIGATE", "조사"),
    },
    "gatcha_prob": {
        "enabled": _get_bool("ENABLE_GATCHA_PROB", True),
        "keyword": _get_str("KEYWORD_GATCHA_PROB", "가챠"),
    },
    "gatcha_simple": {
        "enabled": _get_bool("ENABLE_GATCHA_SIMPLE", True),
        "keyword": _get_str("KEYWORD_GATCHA_SIMPLE", "뽑기"),
    },
    "gatcha_desc": {
        "enabled": _get_bool("ENABLE_GATCHA_DESC", True),
        "keyword": _get_str("KEYWORD_GATCHA_DESC", "가챠"),
    },
    "shop": {
        "enabled": _get_bool("ENABLE_SHOP", True),
        "keyword": _get_str("KEYWORD_SHOP", "구매"),
    },
    "attendance": {
        "enabled": _get_bool("ENABLE_ATTENDANCE", True),
        "keyword": _get_str("KEYWORD_ATTENDANCE", "출석"),
    },
    "dice": {
        "enabled": _get_bool("ENABLE_DICE", True),
        "keyword": _get_str("KEYWORD_DICE", "d"),
    },
    "truefalse": {
        "enabled": _get_bool("ENABLE_TRUEFALSE", True),
        "keyword": _get_str("KEYWORD_TRUEFALSE", "T/F"),
    },
}
