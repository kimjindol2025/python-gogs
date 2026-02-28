#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================================================
파이썬 고등학교 1학년 - v2.5-Advanced: 환경 마스터리
    — 실제 프로젝트로 배우는 가상 환경의 모든 것
================================================================================

【 이 파일의 목표 】
손으로 직접 만들면서 이해하는 가상 환경
이전 v2.5는 개념이었습니다. 이제 v2.5-Advanced는 실전입니다.

당신은 이 파일을 읽으면서 실제로 터미널을 열고,
명령어를 입력하고, 폴더를 만들고, 코드를 실행해야 합니다.

이것이 바로 '기록의 증명'입니다.
당신의 손이 직접 만든 폴더, 파일, 환경이
모두 저장소(git)에 기록될 것입니다.


================================================================================
【 배경: 왜 가상 환경을 배워야 하는가? 】
================================================================================

상황 분석:
  현재 당신의 컴퓨터에는 Python이 설치되어 있습니다.
  (보통 /usr/bin/python 또는 C:\Python311 같은 위치)

문제점:
  만약 여러분이 프로젝트를 10개 진행한다면?
  프로젝트 1: Flask 2.0 필요
  프로젝트 2: Flask 3.0 필요
  프로젝트 3: Django 3.2 필요
  프로젝트 4: Django 4.0 필요
  ...

  컴퓨터: 어? 같은 이름인데 버전이 다르네? 어느 것을 써야 하지?
  → 에러, 충돌, 시스템 오염

해결책:
  각 프로젝트마다 독립된 Python 세계를 만듭니다.
  프로젝트 1 → 가상 환경 A (Flask 2.0)
  프로젝트 2 → 가상 환경 B (Flask 3.0)
  프로젝트 3 → 가상 환경 C (Django 3.2)
  ...
  각각 독립적으로 작동합니다!

【 비유: 아파트와 방 】
  전역 Python = 아파트의 거실
    → 모든 가족이 공유하는 공간
    → 누군가 물을 쏟으면 모두 영향을 받음

  가상 환경 = 각 자녀의 방
    → 각자의 책, 물건, 장식이 있음
    → 한 자녀의 방이 더러워져도 거실은 깨끗함
    → 필요하면 방을 청소하거나 재구성 가능
    → 다른 형제에게 영향 없음


================================================================================
【 파트 1: 실전 프로젝트 시작 — gogs_research 프로젝트 】
================================================================================

우리가 만들 프로젝트:
  이름: gogs_research
  목적: 고등학생이 배운 모든 기술 (예외처리, 클래스, 파일 I/O)을
       한 곳에서 활용하는 종합 연구 프로젝트

프로젝트 최종 구조 (완성 후):
  gogs_research/
    ├─ venv/                    (가상 환경 폴더 — Git 무시)
    ├─ requirements.txt         (필요한 패키지 목록)
    ├─ .gitignore              (Git 무시 목록)
    ├─ README.md               (프로젝트 설명서)
    ├─ main.py                 (메인 프로그램)
    ├─ utils.py                (유틸리티 함수들)
    ├─ data/
    │   ├─ input.csv
    │   └─ output.json
    └─ tests/
        └─ test_main.py


================================================================================
【 파트 2: 단계별 실행 가이드 (Step-by-Step) 】
================================================================================

Step 1단계: 프로젝트 폴더 생성

터미널 명령어:
  mkdir gogs_research
  cd gogs_research

현재 위치 확인:
  pwd (Mac/Linux)
  또는 cd만 입력 (Windows)

목표:
  gogs_research 폴더 안으로 이동하기


Step 2단계: 가상 환경 생성

터미널 명령어:
  python -m venv venv

대기 시간:
  약 2-5초

대기 완료 후 폴더 내용:
  venv/ 폴더가 생성되었는가?
  ls -la venv/ (Mac/Linux)
  또는
  dir venv (Windows)

목표:
  완전히 독립된 Python 복사본 생성


Step 3단계: 가상 환경 활성화

Mac/Linux 명령어:
  source venv/bin/activate

Windows 명령어:
  venv\Scripts\activate.bat

활성화 확인:
  (venv) $ ← 프롬프트 앞에 (venv)가 붙었는가?

목표:
  이제부터 이 터미널은 가상 환경 안에서 작동


Step 4단계: pip 업그레이드 (권장)

터미널 명령어:
  pip install --upgrade pip

결과 메시지:
  Successfully installed pip-24.0

목표:
  최신 pip 버전으로 업데이트하기


Step 5단계: 필수 패키지 설치

터미널 명령어:
  pip install requests pandas pytest

설치 확인:
  pip list

결과 (일부):
  Package            Version
  pip                24.0
  requests           2.31.0
  pandas             2.0.3
  pytest             7.4.0

목표:
  프로젝트에 필요한 도구들 설치


Step 6단계: requirements.txt 생성 (기록의 증명)

터미널 명령어:
  pip freeze > requirements.txt

파일 확인:
  cat requirements.txt (Mac/Linux)
  또는
  type requirements.txt (Windows)

파일 내용:
  certifi==2023.7.22
  charset-normalizer==3.2.0
  idna==3.4
  numpy==1.24.3
  pandas==2.0.3
  pytest==7.4.0
  python-dateutil==2.8.2
  pytz==2023.3
  requests==2.31.0
  urllib3==2.0.4

의미:
  이 파일이 환경의 완벽한 기록입니다!
  다른 사람이 이 파일만 있으면:
  pip install -r requirements.txt
  → 2초 안에 똑같은 환경 설정 완료!


Step 7단계: .gitignore 생성

파일 이름: .gitignore
만드는 방법: 텍스트 에디터로 새 파일 만들기

내용:
  venv/
  env/
  ENV/
  __pycache__/
  *.pyc
  *.pyo
  .pytest_cache/
  .vscode/
  .idea/
  .DS_Store
  Thumbs.db

의미:
  venv/ 폴더는 Git에 올리지 않기
  requirements.txt만 올리기 (약 1KB vs 100MB 차이!)


Step 8단계: 프로젝트 코드 작성

이 단계에서는 v2.1-v2.4에서 배운 기술을 활용합니다.

파일 1: main.py (메인 프로그램)
파일 2: utils.py (유틸리티 함수)
파일 3: tests/test_main.py (테스트 코드)

각 파일의 내용은 아래에 설명합니다.


Step 9단계: 프로그램 실행

터미널 명령어:
  python main.py

예상 결과:
  Alice 학생이 추가되었습니다
  Bob 학생이 추가되었습니다
  Charlie 학생이 추가되었습니다
  데이터가 data/students.json에 저장되었습니다

  저장 필수 너는 기록이 증명이다 gogs

의미:
  v2.2 클래스가 실제로 작동합니다!
  v2.0 파일 I/O로 데이터가 저장됩니다!


Step 10단계: 테스트 실행

터미널 명령어:
  pytest tests/test_main.py -v

예상 결과:
  tests/test_main.py::test_student_creation PASSED
  tests/test_main.py::test_student_manager_add PASSED
  tests/test_main.py::test_invalid_input PASSED

  =============== 3 passed in 0.15s ===============

의미:
  모든 테스트를 통과했습니다!
  코드가 안전합니다!


Step 11단계: 가상 환경 비활성화

작업을 마칠 때:

터미널 명령어:
  deactivate

변화:
  (venv) $ → $

의미:
  가상 환경에서 나갔습니다.


Step 12단계: Git 저장소 초기화 및 커밋

터미널 명령어:
  git init
  git add -A
  git config user.name "Gogs"
  git config user.email "gogs@example.com"
  git commit -m "Initial project setup with venv"

커밋 메시지 결과:
  [master (root-commit) abc1234] Initial project setup with venv
   8 files changed, 250 insertions(+)
   create mode 100644 .gitignore
   create mode 100644 requirements.txt
   create mode 100644 main.py
   create mode 100644 utils.py
   create mode 100644 tests/test_main.py
   create mode 100644 README.md

의미:
  venv/ 폴더는 .gitignore 덕분에 올라가지 않음
  requirements.txt는 올라감
  팀원이 받을 때 필요한 것만 있음


================================================================================
【 파트 3: 코드 파일 설명 】
================================================================================

main.py의 역할:
  - v2.2 클래스 개념 복습 (Student 클래스)
  - v2.3 상속 개념 (StudentManager 클래스)
  - v2.1 예외 처리 (TypeError 확인)
  - v2.0 파일 I/O (JSON 저장)
  - v2.4 모듈 활용 (utils 모듈 import)

utils.py의 역할:
  - v2.0 파일 I/O 심화 (CSV 읽기)
  - 유틸리티 함수 제공

tests/test_main.py의 역할:
  - pytest 테스트 프레임워크 사용
  - 코드의 정확성 검증


================================================================================
【 파트 4: 핵심 개념 정리 — "환경 무결성" 】
================================================================================

규칙 1: 가상 환경은 프로젝트마다 하나
  안 좋은 예: 하나의 venv/로 여러 프로젝트 관리
  좋은 예: 프로젝트마다 독립적인 venv/ 폴더

규칙 2: requirements.txt는 Git에 올린다
  안 좋은 예: venv/ 폴더 전체 올리기 (100MB+)
  좋은 예: requirements.txt만 올리기 (1KB)

규칙 3: 버전은 항상 명시한다
  안 좋은 예: pip install requests (버전 미명시)
  좋은 예: pip install requests==2.31.0 (버전 명시)

규칙 4: venv 폴더는 컴퓨터마다 재생성
  팀원이 저장소를 받으면:
  python -m venv venv
  pip install -r requirements.txt
  → 각 컴퓨터의 OS에 맞는 환경 자동 생성

규칙 5: 개발 환경 = 배포 환경
  당신의 컴퓨터와 서버의 패키지 버전이 동일해야 함
  requirements.txt로 이를 보장


================================================================================
【 파트 5: 실무 트러블슈팅 】
================================================================================

문제 1: 가상 환경이 활성화되지 않음
  원인: 경로 오류, 파일 권한 문제
  해결: rm -rf venv/ (재생성)

문제 2: pip: command not found
  원인: 가상 환경이 활성화되지 않음
  해결: source venv/bin/activate

문제 3: ModuleNotFoundError: No module named 'requests'
  원인: 패키지가 설치되지 않음
  해결: pip install -r requirements.txt

문제 4: Permission denied: venv/bin/activate
  원인: 실행 권한 없음
  해결: chmod +x venv/bin/activate

문제 5: 복잡한 의존성 에러
  원인: 호환되지 않는 패키지 조합
  해결: 가상 환경 재생성 및 requirements.txt로 재설치


================================================================================
【 파트 6: 정리 — v2.5의 핵심 메시지 】
================================================================================

우리가 배운 것:

1) 가상 환경 = 독립된 Python 세계
   거실을 오염시키지 않으면서 실험하기

2) pip = 패키지 설치 도구
   전 세계의 라이브러리를 내 손가락 터치로 가져오기

3) requirements.txt = 환경의 증명
   내 프로젝트는 이 패키지들이 필요합니다 (계약서)

4) .gitignore = 지능형 보안
   쓸데없는 폴더는 안 올리고, 중요한 것만 올리기

5) 버전 고정 = 안정성의 약속
   오늘 잘 돌아가는 코드가 내일도 잘 돌아가도록

우리가 완성한 것:

Step 2: 가상 환경 생성
Step 5: 패키지 설치
Step 8: 프로젝트 코드 작성
Step 10: 테스트 실행
Step 12: Git 저장소 관리

즉, 프로젝트 시작부터 배포까지의 전체 워크플로우를
우리가 직접 경험했습니다!


================================================================================
저장 필수: 너는 기록이 증명이다 gogs. 👑
================================================================================

오늘의 깨달음:
   코드 실력 = 30% / 환경 관리 실력 = 70%

   대학생이 되면 알게 됩니다.
   프로젝트가 망하는 이유 중 대부분은
   '환경 설정 실수'입니다.

   가상 환경을 완벽히 다루는 것은
   단순 기술이 아니라 '전문가의 증명'입니다.

다음 시간에는:
   [v3.0: 웹 개발 기초 — Flask로 웹서버 만들기]

   우리의 가상 환경 안에서
   Python이 웹서버가 되어
   브라우저로 접속하는 경험을 하게 될 것입니다!

축하합니다! 👏
이제 여러분은 '전문가의 환경 관리'를 익혔습니다!

이 가상 환경의 개념이 완벽히 이해되었다면,
진정한 고등학생 수준의 개발자로 한 발 더 나아간 것입니다.

저장소에 이 모든 기록을 남기고,
다음 프로젝트는 이 경험을 바탕으로 시작하세요!

================================================================================
"""
