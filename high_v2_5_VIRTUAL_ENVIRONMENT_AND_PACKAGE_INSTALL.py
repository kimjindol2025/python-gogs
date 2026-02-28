#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""
================================================================================
파이썬 고등학교 1학년 - v2.5: 가상 환경과 외부 패키지 설치
    — 나만의 독립된 실험실 만들기
================================================================================

【 본 파일의 구조 】
이 파일은 실행 가능한 Python 스크립트가 아닙니다.
대신 여러분이 터미널(Terminal)에서 직접 실행해야 할 명령어들과,
그에 따른 결과를 **교육용으로 문서화**한 가이드입니다.

각 섹션마다:
명령어 (터미널에 입력할 코드)
결과 (실행 후 나타나는 화면)
설명 (왜 이렇게 하는지?)

================================================================================
【 파트 1: 문제 상황 — 패키지의 충돌 】
================================================================================

상황: 여러 프로젝트를 동시에 진행하고 있습니다.

프로젝트 A: Django 4.0을 사용합니다
프로젝트 B: Django 3.5를 사용합니다

문제점:
  파이썬은 시스템 전역(Global)에 Django를 한 버전만 설치할 수 있습니다.
  → 프로젝트 A를 실행하면 Django 4.0 설치
  → 프로젝트 B를 실행하려니 Django 3.5를 원한다고 에러 발생!

안 좋은 상황:
  내 컴퓨터 (전역 Python 환경)
    └─ Django 4.0 ← 프로젝트 A를 위해 설치
       └─ requests 2.28
       └─ numpy 1.23
       └─ 프로젝트 B는 Django 3.5를 필요로 해서 실패!


================================================================================
【 파트 2: 해결책 — 가상 환경(Virtual Environment) 】
================================================================================

**가상 환경이란?**
각 프로젝트마다 '독립된 Python 세계'를 만드는 것입니다.

좋은 상황:
  내 컴퓨터
    ├─ 프로젝트 A (가상 환경)
    │   └─ Django 4.0
    │   └─ requests 2.28
    │
    └─ 프로젝트 B (가상 환경)
        └─ Django 3.5
        └─ numpy 1.20

각 프로젝트가 자신만의 패키지 세트를 가집니다!

【 비유 】
  • 전역 환경: 학교 도서관 (모두가 공유)
  • 가상 환경: 각 반의 작은 도서관 (1학년 1반만의 책)
     → 1학년 1반은 교과서 A를 사용
     → 1학년 2반은 교과서 B를 사용
     → 충돌 없음!


================================================================================
【 파트 3: 가상 환경 생성하기 】
================================================================================

**1단계: 터미널에서 프로젝트 폴더로 이동**

명령어:
  cd /path/to/my_project
  (또는 현재 폴더가 프로젝트 폴더면 그대로)

예시:
  cd ~/projects/gogs_project


**2단계: 가상 환경 생성**

명령어:
  python -m venv venv

설명:
  python -m venv    → Python의 venv 모듈을 실행
  venv              → 생성할 가상 환경 폴더의 이름

결과:
  venv/ 폴더이 생성됩니다 (약 10-50MB)

  내용:
  venv/
    ├─ bin/         (Mac/Linux: Python 실행파일, pip 등)
    ├─ lib/         (패키지들이 설치되는 폴더)
    ├─ include/     (C 헤더파일)
    └─ pyvenv.cfg   (설정 파일)

【 주의 】
  venv 폴더는 Git에 올리지 마세요! (.gitignore에 추가)
  왜? 매우 크고, 각 컴퓨터에서 재생성할 수 있기 때문입니다.


================================================================================
【 파트 4: 가상 환경 활성화하기 】
================================================================================

**Mac/Linux에서 활성화:**

명령어:
  source venv/bin/activate

실행 결과:
  (venv) $ ← 이렇게 (venv)가 앞에 붙습니다!

의미: 이제부터 이 터미널은 가상 환경 안에서 작동합니다.


**Windows에서 활성화:**

명령어:
  venv\Scripts\activate

실행 결과:
  (venv) C:\Users\gogs>


**확인하기:**

가상 환경 활성화 후 Python을 실행하면:

명령어:
  python
  >>> import sys
  >>> print(sys.prefix)

결과 (활성화된 경우):
  /path/to/my_project/venv

결과 (전역 Python인 경우):
  /usr/bin
  /Library/Frameworks/Python.framework/Versions/3.11


================================================================================
【 파트 5: 가상 환경 비활성화하기 】
================================================================================

언제: 다른 프로젝트로 이동할 때, 또는 작업을 마칠 때

명령어:
  deactivate

실행 결과:
  $ ← (venv)가 사라집니다!

의미: 다시 전역 Python 환경으로 돌아갑니다.


================================================================================
【 파트 6: pip — 패키지 설치 마법사 】
================================================================================

**pip란?**
Python Package Index에서 패키지를 가져와 설치하는 도구입니다.

비유: 앱 스토어(App Store)처럼 응용 프로그램(패키지)을 설치합니다.

【 pip 버전 확인 】

명령어:
  pip --version

결과:
  pip 24.0 from /path/to/my_project/venv/lib/python3.11/site-packages/pip

의미: 현재 가상 환경의 pip이 사용되고 있습니다.


【 pip 업그레이드 】

명령어 (Mac/Linux):
  pip install --upgrade pip

명령어 (Windows):
  python -m pip install --upgrade pip


================================================================================
【 파트 7: 가장 인기 있는 패키지 10가지 】
================================================================================

1. requests — 웹 API 호출
   명령어: pip install requests
   사용: 인터넷에서 데이터 가져오기

2. pandas — 데이터 분석 (엑셀의 미래)
   명령어: pip install pandas
   사용: CSV, Excel 파일 처리, 데이터 분석

3. numpy — 수학 계산 (매우 빠름)
   명령어: pip install numpy
   사용: 행렬 계산, 과학 연산

4. matplotlib — 그래프 그리기
   명령어: pip install matplotlib
   사용: 데이터를 그래프로 표현

5. flask — 웹서버 만들기
   명령어: pip install flask
   사용: 웹 어플리케이션 개발

6. django — 대규모 웹 프레임워크
   명령어: pip install django
   사용: 복잡한 웹 시스템 개발 (Instagram, Spotify)

7. beautifulsoup4 — 웹 크롤링
   명령어: pip install beautifulsoup4
   사용: 웹 페이지에서 데이터 추출

8. pillow — 이미지 처리
   명령어: pip install pillow
   사용: 사진 편집, 이미지 변환

9. pygame — 게임 개발
   명령어: pip install pygame
   사용: 2D 게임 만들기

10. pytest — 테스트 작성
    명령어: pip install pytest
    사용: 코드가 제대로 작동하는지 확인


================================================================================
【 파트 8: 패키지 설치하기 】
================================================================================

**설치 명령어:**

명령어:
  pip install requests

실행 결과:
  Collecting requests
  Downloading requests-2.31.0-py3-none-any.whl (62 kB)
  Installing collected packages: requests
  Successfully installed requests-2.31.0

의미: requests 패키지가 설치되었습니다!


**여러 패키지 한 번에 설치:**

명령어:
  pip install requests pandas matplotlib

결과:
  Successfully installed requests-2.31.0 pandas-2.0.3 matplotlib-3.7.1


**특정 버전 설치:**

명령어:
  pip install django==3.2

의미: Django 정확히 3.2 버전을 설치합니다


**최소 버전 지정:**

명령어:
  pip install django>=3.0

의미: Django 3.0 이상 어떤 버전이든 가능


================================================================================
【 파트 9: 설치된 패키지 확인 】
================================================================================

**설치된 모든 패키지 보기:**

명령어:
  pip list

결과:
  Package            Version
  -----------------  ---------
  pip                24.0
  requests           2.31.0
  pandas             2.0.3
  numpy              1.24.3
  matplotlib         3.7.1


**특정 패키지 정보 확인:**

명령어:
  pip show requests

결과:
  Name: requests
  Version: 2.31.0
  Summary: Python HTTP for Humans.
  Home-page: https://requests.readthedocs.io
  Author: Kenneth Reitz
  License: Apache 2.0
  Location: /path/to/venv/lib/python3.11/site-packages
  Requires: charset-normalizer, idna, urllib3, certifi
  Required-by:


================================================================================
【 파트 10: requirements.txt — 패키지 목록 저장 】
================================================================================

**목적:**
"이 프로젝트는 이 패키지들이 필요합니다"라는 걸 다른 사람에게 알려주기

【 requirements.txt 생성 】

명령어:
  pip freeze > requirements.txt

결과: requirements.txt 파일 생성됨

파일 내용:
  requests==2.31.0
  pandas==2.0.3
  numpy==1.24.3
  matplotlib==3.7.1
  flask==2.3.2

의미: 정확히 이 버전들을 사용했다는 기록입니다.


【 requirements.txt 사용하기 (다른 팀원) 】

상황: 팀원이 내 코드를 받았습니다.

팀원의 명령어:
  pip install -r requirements.txt

결과:
  Successfully installed requests-2.31.0 pandas-2.0.3 numpy-1.24.3...

의미: 나와 정확히 같은 환경이 설정됩니다!


【 requirements.txt 수동으로 만들기 】

파일: requirements.txt
내용:
  requests>=2.25.0
  pandas>=1.3.0
  numpy>=1.21.0
  flask>=2.0.0

의미: 이 버전 이상이면 괜찮다는 의미입니다 (더 유연함)


================================================================================
【 파트 11: 실제 프로젝트 구조 — 가상 환경 포함 】
================================================================================

프로젝트 폴더 구조:

my_python_project/
  ├─ venv/                          (가상 환경 폴더 — Git 무시)
  │   ├─ bin/
  │   ├─ lib/
  │   └─ include/
  │
  ├─ src/                           (소스 코드)
  │   ├─ main.py
  │   ├─ utils.py
  │   └─ config.py
  │
  ├─ data/                          (데이터 파일)
  │   ├─ input.csv
  │   └─ output.json
  │
  ├─ tests/                         (테스트 코드)
  │   ├─ test_main.py
  │   └─ test_utils.py
  │
  ├─ requirements.txt               (패키지 목록)
  ├─ .gitignore                     (Git 무시 목록)
  ├─ README.md                      (프로젝트 설명)
  └─ .git/                          (Git 저장소)


【 .gitignore 내용 】

파일: .gitignore
내용:
  # 가상 환경 무시
  venv/
  env/
  ENV/

  # Python 캐시
  __pycache__/
  *.pyc
  *.pyo

  # IDE 설정
  .vscode/
  .idea/

  # 운영 체제
  .DS_Store
  Thumbs.db


================================================================================
【 파트 12: 패키지 업데이트 및 제거 】
================================================================================

**패키지 업데이트:**

명령어:
  pip install --upgrade requests

또는 짧게:
  pip install -U requests

결과:
  Collecting requests
  Downloading requests-2.32.0-py3-none-any.whl
  Successfully installed requests-2.32.0


**모든 패키지 업데이트:**

명령어:
  pip install --upgrade pip setuptools wheel


**패키지 제거:**

명령어:
  pip uninstall requests

결과:
  Found existing installation: requests 2.31.0
  Uninstalling requests-2.31.0...
  Successfully uninstalled requests-2.31.0


**확인 없이 제거:**

명령어:
  pip uninstall requests -y


================================================================================
【 파트 13: 가상 환경 관리 팁 】
================================================================================

**여러 프로젝트 관리:**

폴더 구조:
  my_projects/
    ├─ project_a/
    │   ├─ venv/
    │   ├─ main.py
    │   └─ requirements.txt
    │
    └─ project_b/
        ├─ venv/
        ├─ main.py
        └─ requirements.txt


프로젝트 전환:
  # 프로젝트 A 작업
  cd ~/my_projects/project_a
  source venv/bin/activate
  python main.py
  deactivate

  # 프로젝트 B 작업으로 이동
  cd ~/my_projects/project_b
  source venv/bin/activate
  python main.py


**가상 환경 삭제:**

더 이상 필요 없으면:

명령어:
  rm -rf venv/        (Mac/Linux)
  rmdir /s venv       (Windows)

주의: 폴더 전체가 삭제되므로, 필요한 코드는 venv 외부에 있어야 합니다!


**가상 환경 백업:**

문제 발생 시 복구하려면:

명령어:
  pip freeze > requirements.txt
  rm -rf venv/
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt


================================================================================
【 파트 14: 자주 나는 에러와 해결 】
================================================================================

**에러 1: pip: command not found**

원인: pip이 설치되지 않음 또는 경로에 없음

해결:
  python -m pip install requests
  (python을 앞에 붙입니다)


**에러 2: ModuleNotFoundError: No module named 'requests'**

원인: requests 패키지를 설치하지 않았음 또는 전역 Python 사용 중

해결:
  1) 가상 환경 활성화 확인
     source venv/bin/activate

  2) pip install requests 실행

  3) 설치 확인
     pip list


**에러 3: ERROR: Could not find a version that satisfies**

원인: 존재하지 않는 패키지 이름 또는 버전

해결:
  pip search requests  (정확한 이름 찾기)
  또는
  https://pypi.org 에서 검색


**에러 4: Permission denied**

원인: 시스템 패키지 폴더에 접근 권한 없음 (전역 환경)

해결:
  반드시 가상 환경을 사용하세요!
  source venv/bin/activate


================================================================================
【 파트 15: 협업 워크플로우 】
================================================================================

**상황: 팀 프로젝트**

**1단계: 프로젝트 시작 (리더)**

처음 설정:
  git clone <repo>
  cd project
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  python main.py

**2단계: 패키지 추가 (리더)**

새로운 기능을 위해 패키지 필요:
  pip install flask

**3단계: requirements.txt 업데이트**

명령어:
  pip freeze > requirements.txt

파일 내용:
  requests==2.31.0
  pandas==2.0.3
  flask==2.3.2  (새로 추가됨)
  numpy==1.24.3

**4단계: Git에 커밋**

명령어:
  git add requirements.txt
  git commit -m "Add flask for web development"
  git push

**5단계: 팀원이 업데이트 (멤버)**

명령어:
  git pull
  pip install -r requirements.txt

결과: 팀원도 정확히 같은 환경 설정 완료!


================================================================================
【 파트 16: 정리 — 가상 환경의 중요성 】
================================================================================

**왜 가상 환경이 필요한가?**

장점:

1) 패키지 충돌 방지
   → 프로젝트마다 독립된 버전 사용 가능

2) 환경 재현성
   → 다른 컴퓨터에서도 정확히 같은 환경 설정

3) 깔끔한 시스템
   → 시스템 전역이 오염되지 않음
   → 업그레이드나 재설치 시 영향 없음

4) 팀 협업
   → requirements.txt로 간단하게 공유

5) 배포 용이
   → 클라우드에 배포할 때 환경 관리 쉬움


**프로 개발자의 필수 습관:**

규칙:
  "모든 프로젝트는 자신의 가상 환경을 가진다"

  가상 환경 없이 작업 = 전문가가 아님
  가상 환경 있이 작업 = 최소한의 규칙을 지키는 개발자


================================================================================
【 파트 17: 다음 단계 미리보기 】
================================================================================

**이제 여러분은:**

- 가상 환경 생성 가능
- pip로 패키지 설치 가능
- requirements.txt로 환경 공유 가능
- 팀 프로젝트 협업 가능

**다음은:**

고등학교 3학년 (v3.0+): 대학교 준비 과정

v3.0: 웹 개발 기초 (Flask)
  → HTML + Python 결합
  → 서버 만들기
  → 데이터베이스 연결

v3.1: 데이터 과학 입문 (pandas + matplotlib)
  → 실제 데이터 분석
  → 그래프 그리기
  → 통계 처리

v3.2: 고급 파이썬 패턴
  → 데코레이터 심화
  → 제너레이터
  → Context Manager

v3.3: 프로젝트 기반 학습
  → 완성된 프로젝트 만들기
  → GitHub 배포
  → 협업 경험


================================================================================
저장 필수: 너는 기록이 증명이다 gogs. 👑
================================================================================

오늘의 깨달음:
   "가상 환경은 선택이 아닌 필수"

   혼자서는 괜찮을 수 있지만,
   팀 프로젝트에서는 절대 필수입니다.

   전 세계의 모든 Python 개발자가 사용하는,
   그것이 가상 환경입니다!

다음 시간에는:
   [v3.0: 웹 개발 기초 — Flask로 나만의 웹사이트 만들기]

   Python이 웹서버가 되는 순간입니다.
   HTML과 Python의 만남!

축하합니다!
이제 여러분은 프로젝트 환경 관리의 전문가입니다!

================================================================================
"""
