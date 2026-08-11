#!/usr/bin/python3
import re
from bs4 import BeautifulSoup
import constants


# 마스토돈 멘션에서 온 HTML 원문을 깔끔한 텍스트로 바꿔줌
def filter_text(raw_text):
    soup = BeautifulSoup(raw_text, 'html.parser')
    parsed_text = soup.get_text(strip=True)
    return re.sub(constants.CLEANER, '', parsed_text)
