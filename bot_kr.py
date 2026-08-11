#!/usr/bin/python3
# 봇 실행 파일
# 실제 설정은 .env 파일 (기능 켜기/끄기, 키워드) 과 constants.py (구글 시트 구조) 에서 이루어집니다.
from listener import BotListener
from mastodon_client import mastodon


def main():
    mastodon.stream_user(BotListener(mastodon))


if __name__ == '__main__':
    main()
