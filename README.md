# MastodonBot

A general mastodon bot python template cooperating with Google Spreadsheet.

구글 스프레드시트와 연동할 수 있는, 마스토돈 봇 파이썬 템플렛입니다.

## ABOUT

This bot is for the user who wants to facilitate the data management process for the OC(Original Character) community on the Mastodon platform. The guideline below is written in Korean, containing how to edit the source code and how to deploy this mastodon bot on the Google Cloud Platform via VM instance.

이 자동봇은 마스토돈 플랫폼의 자작 캐릭터 커뮤니티 운영에 있어서 데이터 관리를 용이하게 하기 위해 작성되었습니다. 아래 가이드라인은 한국어로 적혀 있으며 어떻게 소스 코드를 편집해야 하는지, 어떻게 해당 자동 봇을 GCP 가상머신 인스턴스를 통해 배포하는 지에 대해 서술되어 있습니다.

## 업데이트 (2026-08-11, MDT)

- 코드를 여러 파일로 분리하여 정리 (기능별 코드, 설정, 상수 분리)
- `.env` 파일에서 기능을 켜고 끄거나 명령어(키워드)를 바꿀 수 있도록 개선 (프로그래밍 지식 불필요)
- 설명 없는 단순 가챠([뽑기/n])가 다른 가챠 명령어에 가려서 실행되지 않던 오류 수정
- 출석 시 카운트가 1이 아니라 2씩 올라가던 오류 수정

## 업데이트 (2025-02-25, PST)

- 포스타입 가이드라인 작성 완료
- 가챠 타입 추가
- 기타 오류 수정

## Considering...

- 조사 기능에 관하여: 마스토돈 API의 제한은 5분당 300회 요청이라고 합니다. API 요청을 최소화하는 방법으로 구상을 해보겠습니다만, 현재로서는 해당 봇은 조사가 주로 되는 커뮤니티에는 적합하지 않을 수도 있습니다.
- 전투 기능에 관하여: 어떤 형식인지에 대한 관련 정보가 적습니다. 이와 관련되어 해당 글 최하단에 있는 이메일로 연락을 주시면 감사드리겠습니다.

## 자료

- [샘플 스프레드시트](https://docs.google.com/spreadsheets/d/1uQ5la1Z2OP1dTgUuUXyJjLEagznXyEWJ-GheA0u-Nc4/edit?usp=sharing)
- [구글 API 취득 방법](https://liwonfather.tistory.com/235)

## 제공되는 기능들

- 가챠 (확률 가챠, 그냥 노멀 가챠 포함)
- 상점
- 출석
- 참거짓
- 다이스
- 키워드 기반 조사

## 기능 사용법

- [가챠/n]: n은 가챠를 한 번에 몇 번 돌릴 지를 나타냅니다. (최대 10회, 희귀도 있음)
- [뽑기/n]: 위와 비슷하지만 희귀도 구분 없이 아이템만 n개 뽑습니다. (최대 10회)
- [가챠]: 위와는 다른 가챠 형식입니다. 아이템 설명과 함께 1개만 나옵니다.
- [구매/아이템이름]
- [출석]
- [T/F]
- [ndm] 혹은 [nDm]
- [조사/키워드]

커맨드 사이사이에 공백이 있거나 캐입 역극 도중에 넣어도 인식이 가능하게끔 만들었습니다.

위 명령어들은 기본값이며, `.env` 파일에서 원하는 단어로 바꿀 수 있습니다. 자세한 내용은 아래 "기능 켜기/끄기 및 명령어 바꾸기" 항목을 참고해주세요.

## 코드 구조

프로그래밍을 잘 모르셔도 괜찮습니다. **아래 파일들 중 `.env` 파일 하나만 편집하면 됩니다.** 나머지 파일은 코드를 관리/기여하는 분들을 위한 설명입니다.

- `.env`: 접속 정보, 기능 켜기/끄기, 명령어(키워드) 설정 (직접 만들고 채워야 하는 파일, `.env.sample` 참고)
- `constants.py`: 구글 스프레드시트의 탭 이름과 열 번호 등 코드 상의 상수
- `config.py`: `.env` 파일의 값을 읽어들이는 코드
- `sheets.py`: 구글 스프레드시트 연결
- `mastodon_client.py`: 마스토돈 봇 연결
- `utils.py`: 공통으로 쓰이는 텍스트 처리 함수
- `features/`: 기능별 코드 (가챠, 출석, 조사, 상점, 다이스, 참거짓)
- `listener.py`: 멘션을 받아 어떤 기능을 실행할지 결정하는 코드
- `bot_kr.py`: 봇을 실행하는 파일 (`python3 bot_kr.py` 로 실행)

## 기능 켜기/끄기 및 명령어 바꾸기

`.env.sample` 파일을 복사해 `.env` 파일을 만든 뒤, 그 안에서 아래와 같이 설정할 수 있습니다.

- **기능 켜기/끄기**: `ENABLE_ATTENDANCE`처럼 생긴 값들을 `true`/`false` 로 바꾸면 해당 기능이 켜지거나 꺼집니다. 예) `ENABLE_DICE=false` 로 하면 다이스 기능이 꺼집니다.
- **명령어(키워드) 바꾸기**: `KEYWORD_ATTENDANCE`처럼 생긴 값들을 원하는 단어로 바꾸면 사용자가 불러야 하는 명령어가 바뀝니다. 예) `KEYWORD_ATTENDANCE=출석확인` 으로 바꾸면 `[출석]` 대신 `[출석확인]` 이라고 멘션해야 출석 체크가 됩니다.

파일을 수정한 뒤 봇을 껐다가 다시 켜면 (`python3 bot_kr.py` 재실행) 바뀐 설정이 적용됩니다. 자세한 설명과 각 명령어의 사용법은 `.env.sample` 파일 안의 주석을 참고해주세요.

## 사용법

- [포스타입 가이드라인 참고](https://www.postype.com/@imgyeonglee/post/18833704)

## 안내사항

- 해당 코드의 수정이 거의 없다시피한 상업적 이용은 불가능합니다.
- 오픈소스입니다. 누구나 해당 Repository에 기여할 수 있습니다.

## 연락처

imgyeonglee@gmail.com

- 문의 및 질문.
- 오류 및 버그 제보.
- 새로운 기능 추가 요구 가능.
- 기타 피드백.
