#!/usr/bin/python3
# 마스토돈 멘션(알림)을 받아서 어떤 기능을 실행할지 결정하는 파일
import re

from mastodon.streaming import StreamListener

import config
import constants
from features import attendance as attendance_feature
from features import dice, gatcha, investigate, shop, truefalse
from utils import filter_text


# [키워드] 안의 내용을 "명령어"와 "/ 뒤의 값" 으로 나눠줌
# 슬래시(/)가 없으면 값은 None
def _split_command(text):
    if '/' in text:
        head, _, tail = text.partition('/')
        return head.strip(), tail.strip()
    return text.strip(), None


def _match_dice(raw, keyword):
    pattern = re.compile(rf"^(\d+)\s*{re.escape(keyword)}\s*(\d+)$", re.IGNORECASE)
    return pattern.match(raw)


class BotListener(StreamListener):
    def __init__(self, mastodon):
        self.mastodon = mastodon

    def on_notification(self, notification):
        if notification['type'] != 'mention':
            return

        user_text = filter_text(notification['status']['content'])

        if '[' not in user_text or ']' not in user_text:
            self._reply(notification, "명령어는 대괄호 [ ] 안에 적어주세요. 예) [출석]")
            return

        cmd_start = user_text.find('[') + 1
        cmd_end = user_text.find(']')
        raw = user_text[cmd_start:cmd_end].strip()

        self._dispatch(notification, raw)

    def _dispatch(self, notification, raw):
        commands = config.COMMANDS
        command_word, param = _split_command(raw)

        # 조사   [조사/키워드]
        if commands['investigate']['enabled'] and param is not None and command_word == commands['investigate']['keyword']:
            self._reply(notification, investigate.investigate(param))

        # 가챠 (확률)   [가챠/n]
        elif (commands['gatcha_prob']['enabled'] and param is not None and param.isdigit()
                and command_word == commands['gatcha_prob']['keyword']):
            self._reply(notification, gatcha.gatcha_with_prob(int(param), config.GATCHA_MAX_PULLS))

        # 가챠 (단순, 설명 없음)   [뽑기/n]
        elif (commands['gatcha_simple']['enabled'] and param is not None and param.isdigit()
                and command_word == commands['gatcha_simple']['keyword']):
            self._reply(notification, gatcha.gatcha_without_description(int(param), config.GATCHA_MAX_PULLS))

        # 가챠 (단순, 설명 있음, 1회)   [가챠]
        elif commands['gatcha_desc']['enabled'] and raw == commands['gatcha_desc']['keyword']:
            self._reply(notification, gatcha.gatcha_with_description())

        # 상점 구매   [구매/아이템이름]
        elif commands['shop']['enabled'] and param is not None and command_word == commands['shop']['keyword']:
            user_account = notification['status']['account']['username']
            self._reply(notification, shop.buy_something(user_account, param))

        # 출석   [출석]
        elif commands['attendance']['enabled'] and raw == commands['attendance']['keyword']:
            self._handle_attendance(notification)

        # 참/거짓   [T/F]
        elif commands['truefalse']['enabled'] and raw == commands['truefalse']['keyword']:
            self._reply(notification, truefalse.true_or_false())

        # 다이스   [ndm] 혹은 [nDm]
        elif commands['dice']['enabled'] and (dice_match := _match_dice(raw, commands['dice']['keyword'])):
            n, sides = int(dice_match.group(1)), int(dice_match.group(2))
            self._reply(notification, dice.roll_dice(n, sides))

        else:
            self._reply(notification, "명령어 형식이 올바르지 않은 것 같아요.")

    def _handle_attendance(self, notification):
        user_account = notification['status']['account']['username']
        user_name = attendance_feature.check_attendance(user_account)

        if user_name == 'NONE':
            self._reply(notification, "존재하지 않는 분이에요!")
        elif user_name == 'OVERWRITE':
            self._reply(notification, "오늘 이미 출석하셨어요!")
        else:
            self._reply(notification, f"{user_name}님, 출석 확인 되었습니다!")

    def _reply(self, notification, message):
        self.mastodon.status_reply(notification['status'], message, visibility=constants.REPLY_VISIBILITY)

    def handle_heartbeat(self):
        return super().handle_heartbeat()
