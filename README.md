# MastodonBot

A general mastodon bot python template cooperating with Google Spreadsheet.

구글 스프레드시트와 연동할 수 있는, 마스토돈 봇 파이썬 템플렛입니다.

## 자료

-  [샘플 스프레드시트](https://docs.google.com/spreadsheets/d/1uQ5la1Z2OP1dTgUuUXyJjLEagznXyEWJ-GheA0u-Nc4/edit?usp=sharing)
-  [구글 API 취득 방법](https://liwonfather.tistory.com/235)

## 제공되는 기능들

-  가챠
-  상점
-  출석
-  참거짓
-  다이스
-  키워드 기반 조사

## 기능 사용법

-  [가챠/n]: n은 가챠를 한 번에 몇 번 돌릴 지를 나타냅니다. (최대 10회)
-  [구매/아이템이름]
-  [출석]
-  [T/F]
-  [ndm] 혹은 [nDm]
-  [조사/키워드]

커맨드 사이사이에 공백이 있거나 캐입 역극 도중에 넣어도 인식이 가능하게끔 만들었습니다.

## 사용법

-  마스토돈에 봇 계정을 만듭니다.
-  마스토돈 봇 계정 -> 환경설정 -> 개발에서 내 응용프로그램을 클릭하면 보이는 정보들을 확인해둡니다.
-  bot_kr.py를 다운로드하거나 복붙하여 따로 .py 파일을 만듭니다.
-  제공되는 구글 스프레드시트 템플렛의 사본을 만듭니다.
-  API를 사용하기 위해 API 키를 취득합니다. (json 파일로 저장됨)
-  bot_kr.py의 코드에 필요한 정보들을 기입합니다. (마스토돈 봇 정보, json 파일 이름)
-  코드를 실행하면 봇이 작동합니다.
-  다만, 본인의 컴퓨터가 24/7 동안 작동되고 있어야 하며, 이외 배포하는 방법은 따로 알아보셔야 합니다.

## 안내사항

-  해당 코드의 수정이 거의 없다시피한 상업적 이용은 불가능합니다.
-  오픈소스입니다. 누구나 해당 Repository에 기여할 수 있습니다.
-  파이썬이 주 프로그래밍 언어가 아니라 다소 코드가 깔끔하지 않을 수 있습니다.

## 연락처

mingbab33@gmail.com

-  문의 및 질문.
-  오류 및 버그 제보.
-  새로운 기능 추가 요구 가능.
-  기타 피드백.

## Considering...

-  캐릭터 정보 관리
-  조사 기능 개선 (피드백 요함)
-  코드 리팩토링
