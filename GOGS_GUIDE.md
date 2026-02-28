# 🗂️ **Gogs 저장소 & 푸시 가이드**

> Gogs 원격 저장소 관리 및 푸시 방법 완벽 가이드

---

## **Gogs 저장소 정보**

### 저장소 URL

```
HTTPS: https://gogs.dclub.kr/kim/gogs_python.git
SSH: git@gogs.dclub.kr:kim/gogs_python.git

소유자: kim
저장소명: gogs_python
상태: ✅ 활성
```

### API 토큰

```
토큰: 826b3705d8a0602cf89a02327dcee25e991dd630
저장 위치: /data/data/com.termux/files/home/test-freelang-v4/.env
상태: ✅ 활성
```

---

## **방법 1️⃣: 토큰 기반 HTTPS 푸시 (권장)**

### Step 1: 토큰 설정

```bash
# 방법 A: URL에 직접 포함
git remote set-url origin https://kim:826b3705d8a0602cf89a02327dcee25e991dd630@gogs.dclub.kr/kim/gogs_python.git

# 방법 B: Git 자격증명 저장
git config credential.helper store

# 이후 첫 푸시시 토큰을 입력하면 자동 저장
```

### Step 2: 푸시 실행

```bash
# 현재 브랜치 푸시
git push origin master

# 특정 브랜치 푸시
git push origin feature-branch

# 모든 브랜치 푸시
git push origin --all

# 태그 포함 푸시
git push origin --tags
```

### Step 3: 확인

```bash
# 리모트 확인
git remote -v

# 푸시 이력 확인
git log --oneline | head -5
```

---

## **방법 2️⃣: 액세스 토큰 환경변수 사용**

### Step 1: 환경변수 설정

```bash
# .bashrc 또는 .zshrc에 추가
export GOGS_TOKEN="826b3705d8a0602cf89a02327dcee25e991dd630"
export GOGS_URL="https://gogs.dclub.kr"
export GOGS_REPO="kim/gogs_python.git"

# 즉시 적용
source ~/.bashrc
```

### Step 2: 스크립트로 푸시

```bash
#!/bin/bash
# push.sh

GOGS_TOKEN="826b3705d8a0602cf89a02327dcee25e991dd630"
GOGS_URL="https://gogs.dclub.kr"
GOGS_REPO="kim/gogs_python.git"

# 리모트 URL 설정
git remote set-url origin "https://kim:${GOGS_TOKEN}@gogs.dclub.kr/${GOGS_REPO}"

# 푸시
git push origin master

echo "✅ 푸시 완료!"
```

### Step 3: 실행

```bash
chmod +x push.sh
./push.sh
```

---

## **방법 3️⃣: 자동화된 커밋 & 푸시**

### 완전 자동화 스크립트

```bash
#!/bin/bash
# auto_commit_push.sh

set -e  # 오류시 중단

# 변수
GOGS_TOKEN="826b3705d8a0602cf89a02327dcee25e991dd630"
COMMIT_MESSAGE="${1:-Auto commit and push}"
BRANCH="${2:-master}"

echo "📝 상태 확인..."
git status

echo "📦 스테이징..."
git add -A

echo "✍️ 커밋 (메시지: $COMMIT_MESSAGE)..."
git commit -m "$COMMIT_MESSAGE"

echo "🚀 푸시 (브랜치: $BRANCH)..."
git remote set-url origin "https://kim:${GOGS_TOKEN}@gogs.dclub.kr/kim/gogs_python.git"
git push origin $BRANCH

echo "✅ 완료!"
echo "📊 최근 커밋:"
git log --oneline | head -3
```

### 사용법

```bash
# 기본 메시지로 커밋 & 푸시
./auto_commit_push.sh

# 커스텀 메시지
./auto_commit_push.sh "v9.4: 양자 인터넷 구현"

# 특정 브랜치
./auto_commit_push.sh "Update docs" "develop"
```

---

## **방법 4️⃣: SSH 키 기반 푸시**

### Step 1: SSH 키 생성 (처음 한 번)

```bash
# SSH 키 생성
ssh-keygen -t rsa -b 4096 -f ~/.ssh/gogs_key -N ""

# 퍼미션 설정
chmod 600 ~/.ssh/gogs_key
chmod 644 ~/.ssh/gogs_key.pub
```

### Step 2: Gogs에 공개키 등록

```bash
# 공개키 내용 복사
cat ~/.ssh/gogs_key.pub

# Gogs 웹사이트에서:
# 1. 로그인
# 2. Settings → SSH Keys
# 3. 공개키 붙여넣기
```

### Step 3: SSH 설정

```bash
# ~/.ssh/config 편집
vim ~/.ssh/config

# 다음 내용 추가:
Host gogs.dclub.kr
    HostName gogs.dclub.kr
    User git
    IdentityFile ~/.ssh/gogs_key
    StrictHostKeyChecking no
```

### Step 4: 리모트 URL 변경

```bash
# SSH URL로 변경
git remote set-url origin git@gogs.dclub.kr:kim/gogs_python.git

# 확인
git remote -v
```

### Step 5: 푸시

```bash
git push origin master
# 토큰 입력 없이 자동으로 인증됨
```

---

## **Step-by-Step 푸시 체크리스트**

### 📋 푸시 전 확인사항

```bash
# 1️⃣ 변경사항 확인
git status

# 2️⃣ 변경내용 검토
git diff

# 3️⃣ 충돌 확인
git fetch origin
git log --oneline origin/master..HEAD

# 4️⃣ 리모트 확인
git remote -v
```

### 📦 커밋 및 푸시

```bash
# 1️⃣ 스테이징
git add -A
# 또는 선택적
git add FILE1 FILE2

# 2️⃣ 상태 확인
git status --short

# 3️⃣ 커밋
git commit -m "메시지"

# 4️⃣ 푸시
git push origin master

# 5️⃣ 확인
git log --oneline | head -1
```

---

## **커밋 메시지 규칙**

### 형식

```
<타입>: <제목>

<본문>

<푸터>
```

### 타입

```
feat: 새 기능
fix: 버그 수정
docs: 문서 작성/수정
refactor: 코드 리팩토링
perf: 성능 개선
test: 테스트 추가
chore: 빌드, 의존성 등
```

### 예시

```bash
# 기능 추가
git commit -m "feat: v9.3 행성급 합의 시스템 구현"

# 버그 수정
git commit -m "fix: MapReduce 청크 처리 오류 수정"

# 문서화
git commit -m "docs: ARCHITECTURE.md 추가"

# 상세 메시지
git commit -m "refactor: DataLakeOrchestrator 코드 정리

- 불필요한 변수 제거
- 메서드 추출로 가독성 개선
- 성능 20% 향상

Fixes #123"
```

---

## **브랜치 관리**

### 브랜치 생성 및 전환

```bash
# 브랜치 생성
git branch feature/v9-4-quantum

# 전환
git checkout feature/v9-4-quantum
# 또는
git checkout -b feature/v9-4-quantum  # 생성 & 전환

# 브랜치 목록
git branch -a
```

### 브랜치 푸시

```bash
# 로컬 브랜치 푸시
git push origin feature/v9-4-quantum

# 원격 브랜치 추적
git push --set-upstream origin feature/v9-4-quantum
# 이후 git push만 사용 가능

# 브랜치 삭제
git branch -d feature/v9-4-quantum
git push origin --delete feature/v9-4-quantum
```

---

## **풀 요청 (Pull Request)**

### Gogs에서 PR 생성

```bash
# 1️⃣ 브랜치 푸시
git push origin feature/v9-4-quantum

# 2️⃣ Gogs 웹사이트 접속
# https://gogs.dclub.kr/kim/gogs_python

# 3️⃣ "New Pull Request" 클릭
# - Base: master
# - Compare: feature/v9-4-quantum

# 4️⃣ PR 설명 작성 & 생성
```

### CLI로 PR 생성 (gh 도구 사용)

```bash
# gh 도구 설치 (선택사항)
# Gogs는 완전 지원하지 않을 수 있음

# 대신 수동으로 웹사이트에서 생성
```

---

## **태그 관리**

### 태그 생성

```bash
# 가벼운 태그
git tag v8.2

# 주석 태그 (권장)
git tag -a v8.2 -m "v8.2: 데이터 레이크 & 분산 병렬 처리"

# 태그 목록
git tag -l

# 특정 태그 상세
git show v8.2
```

### 태그 푸시

```bash
# 단일 태그 푸시
git push origin v8.2

# 모든 태그 푸시
git push origin --tags

# 태그 삭제
git tag -d v8.2
git push origin --delete v8.2
```

---

## **충돌 해결**

### 충돌 상황 처리

```bash
# 1️⃣ 상태 확인
git status

# 2️⃣ 충돌 파일 확인
git diff

# 3️⃣ 충돌 파일 수정
vim conflicted_file.py

# 마크업 제거:
# <<<<<<< HEAD
#   현재 코드
# =======
#   원격 코드
# >>>>>>> branch-name

# 4️⃣ 스테이징
git add conflicted_file.py

# 5️⃣ 커밋
git commit -m "Merge conflict resolved"

# 6️⃣ 푸시
git push origin master
```

### 병합 취소

```bash
# 병합 이전 상태로 돌아가기
git merge --abort

# 또는 이미 커밋된 경우
git reset --hard HEAD~1
```

---

## **문제 해결**

### 🔴 문제 1: "Authentication failed"

**증상**:
```
fatal: Authentication failed for 'https://gogs.dclub.kr/kim/gogs_python.git'
```

**해결**:
```bash
# 방법 1: 토큰 다시 설정
git remote set-url origin "https://kim:826b3705d8a0602cf89a02327dcee25e991dd630@gogs.dclub.kr/kim/gogs_python.git"

# 방법 2: 자격증명 초기화
git config --global credential.helper store
git push  # 토큰 입력

# 방법 3: SSH 키 사용으로 변경
git remote set-url origin git@gogs.dclub.kr:kim/gogs_python.git
```

---

### 🔴 문제 2: "Your branch is ahead"

**증상**:
```
Your branch is ahead of 'origin/master' by 2 commits.
```

**해결**:
```bash
# 로컬 커밋을 푸시
git push origin master

# 또는 로컬 변경 취소
git reset --hard origin/master
```

---

### 🔴 문제 3: "rejected (non-fast-forward)"

**증상**:
```
! [rejected]        master -> master (non-fast-forward)
error: failed to push some refs to ...
```

**해결**:
```bash
# 1️⃣ 원격 변경사항 가져오기
git pull origin master

# 2️⃣ 충돌 해결 (있으면)
# (위의 충돌 해결 섹션 참고)

# 3️⃣ 다시 푸시
git push origin master

# 강제 푸시 (위험! 공동 저장소에서는 사용 금지)
# git push --force-with-lease origin master
```

---

### 🔴 문제 4: "Permission denied (publickey)"

**증상**:
```
Permission denied (publickey).
fatal: Could not read from remote repository.
```

**해결**:
```bash
# SSH 키 확인
ssh -T git@gogs.dclub.kr

# HTTPS로 변경
git remote set-url origin https://kim:826b3705d8a0602cf89a02327dcee25e991dd630@gogs.dclub.kr/kim/gogs_python.git

# 다시 푸시
git push origin master
```

---

## **고급 기능**

### Rebase (선형 히스토리)

```bash
# 최신 master를 현재 브랜치에 반영
git rebase origin/master

# 대화형 리베이스 (커밋 정리)
git rebase -i HEAD~3  # 최근 3개 커밋
```

### Stash (변경사항 임시 저장)

```bash
# 변경사항 임시 저장
git stash

# 브랜치 전환
git checkout master

# 다시 복원
git checkout feature-branch
git stash pop
```

### Cherry-pick (선택적 커밋 적용)

```bash
# 특정 커밋 적용
git cherry-pick <commit-hash>

# 범위 지정
git cherry-pick <start>..<end>
```

---

## **모범 사례**

### ✅ DO (권장)

```bash
# ✅ 자주 푸시 (하루 1-2회)
git push origin master

# ✅ 명확한 커밋 메시지
git commit -m "feat: 명확한 기능 설명"

# ✅ 작은 단위 커밋
# 한 파일에 한 기능

# ✅ 푸시 전 테스트
python test_*.py

# ✅ 태그로 버전 표시
git tag -a v1.0 -m "Release v1.0"
```

### ❌ DON'T (금지)

```bash
# ❌ 무분별한 강제 푸시
git push --force

# ❌ 불명확한 메시지
git commit -m "fix bug"

# ❌ 테스트 없이 푸시
git push

# ❌ 장시간 로컬 보관
# 주기적으로 푸시

# ❌ 커밋 히스토리 수정
git reset --hard origin/master  # 공동 저장소에서 금지
```

---

## **워크플로우 예시**

### 일반적인 개발 흐름

```bash
# 1️⃣ 최신 내용 동기화
git pull origin master

# 2️⃣ 새 브랜치 생성
git checkout -b feature/v9-4

# 3️⃣ 코드 작성
vim university_v9_4_QUANTUM_INTERNET.py

# 4️⃣ 테스트
python test_v9_4_quantum_internet.py

# 5️⃣ 커밋
git add university_v9_4_QUANTUM_INTERNET.py
git commit -m "feat: v9.4 양자 인터넷 구현"

# 6️⃣ 푸시
git push origin feature/v9-4

# 7️⃣ Gogs에서 PR 생성 & 리뷰
# https://gogs.dclub.kr/kim/gogs_python/pulls

# 8️⃣ Merge
git checkout master
git pull origin master
git merge feature/v9-4

# 9️⃣ 태그
git tag -a v9.4 -m "v9.4: 양자 인터넷"

# 🔟 푸시 (모든 것)
git push origin master --tags
```

---

## **빠른 참조 (Cheat Sheet)**

```bash
# 기본
git clone https://gogs.dclub.kr/kim/gogs_python.git
git status
git add .
git commit -m "메시지"
git push origin master

# 브랜치
git branch -a
git checkout -b feature-name
git push origin feature-name

# 태그
git tag -a v1.0 -m "Release"
git push origin --tags

# 기타
git log --oneline
git diff
git stash
git reset --hard HEAD~1
```

---

## **유용한 커맨드**

```bash
# 마지막 3개 커밋 이력
git log --oneline -3

# 특정 파일 커밋 이력
git log --oneline university_v8_2_DISTRIBUTED_DATA_LAKE.py

# 푸시 전 변경사항 미리보기
git diff origin/master

# 로컬과 원격 비교
git log --oneline ..origin/master

# 실수로 삭제한 커밋 복구
git reflog
git reset --hard <commit>
```

---

## 📞 **지원 및 문의**

```
Gogs URL: https://gogs.dclub.kr/kim/gogs_python
토큰 문제: .env 파일 확인
푸시 실패: git status 및 git remote -v 확인
권한 문제: SSH 키 또는 토큰 재설정
```

---

**문서 버전**: 1.0
**마지막 업데이트**: 2026년 02월 25일
**상태**: ✅ 모든 푸시 방법 완벽 가이드
